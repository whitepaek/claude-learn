#!/usr/bin/env python3
"""Claude Code custom statusline - Powerlevel10k Pure palette with 3-tier threshold"""

import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Colors - Powerlevel10k Pure base + 256-color extensions
# ---------------------------------------------------------------------------
# Pure base
GREEN = 2        # ctx threshold normal (standard)
YELLOW = 3       # ctx threshold warning (standard) / ccusage today
RED = 1          # ctx threshold danger (standard)
BLUE = 4         # model ID
MAGENTA = 5      # session cost
CYAN = 6         # session duration
GREY = 242       # titles, fallback
GREY_LO = 245    # directory, branch, version

# 256-color: 5h threshold (dim)
DIM_GREEN = 65
DIM_YELLOW = 179
DIM_RED = 131

# 256-color: ctx threshold (dark)
DARK_GREEN = 22
DARK_YELLOW = 136
DARK_RED = 88

# 256-color: ccusage cost gradient
COST_TODAY = YELLOW  # 3
COST_WEEK = 179      # gold
COST_MONTH = 173     # salmon

RESET = "\033[0m"

# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------
GIT_CACHE = "/tmp/statusline-git-cache.json"
GIT_CACHE_TTL = 5

CCUSAGE_CACHE = "/tmp/statusline-ccusage-cache.json"
CCUSAGE_CACHE_TTL = 300

FETCH_LOCK = "/tmp/statusline-git-fetch.lock"
FETCH_STAMP = "/tmp/statusline-git-fetch.stamp"
FETCH_TTL = 180

_ANSI_RE = re.compile(r"\033\][^\a]*\a|\033\[[^m]*m")


def cache_is_stale(path, ttl):
    if not os.path.exists(path):
        return True
    return time.time() - os.path.getmtime(path) > ttl


def read_cache(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return None


def write_cache(path, data):
    try:
        with open(path, "w") as f:
            json.dump(data, f)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------
TITLE_PAD = f"\033[38;5;{GREY}m{'':>6}\033[0m  "

_THRESHOLD = {
    "standard": {50: GREEN, 80: RED, "mid": YELLOW, "low": GREEN},
    "dim":      {50: DIM_GREEN, 80: DIM_RED, "mid": DIM_YELLOW, "low": DIM_GREEN},
    "dark":     {50: DARK_GREEN, 80: DARK_RED, "mid": DARK_YELLOW, "low": DARK_GREEN},
}


def block(text, color):
    return f"\033[38;5;{color}m{text}{RESET}"


def underline(text, color, marker=False):
    visible_len = len(_ANSI_RE.sub("", text))
    if marker:
        return f"\033[38;5;{color}m[!] {'─' * max(visible_len - 4, 0)}{RESET}"
    return f"\033[38;5;{color}m{'─' * visible_len}{RESET}"


def title(name):
    return f"\033[38;5;{GREY}m[{name}]{RESET}  "


def threshold_color(pct, level="standard"):
    if pct is None:
        return GREY
    t = _THRESHOLD[level]
    if pct >= 80:
        return t[80]
    if pct >= 50:
        return t["mid"]
    return t["low"]


def render_line(texts, colors, markers=None):
    if markers is None:
        markers = [False] * len(texts)
    line = "  ".join(block(t, c) for t, c in zip(texts, colors))
    uline = "  ".join(underline(t, c, m) for t, c, m in zip(texts, colors, markers))
    return line, uline


# ---------------------------------------------------------------------------
# Data sources
# ---------------------------------------------------------------------------
def maybe_background_fetch(cwd):
    """Fire-and-forget git fetch if TTL has expired and no fetch is already running."""
    if os.path.exists(FETCH_STAMP):
        if time.time() - os.path.getmtime(FETCH_STAMP) < FETCH_TTL:
            return
    try:
        fd = os.open(FETCH_LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.close(fd)
    except FileExistsError:
        return
    try:
        subprocess.Popen(
            ["git", "fetch", "--quiet", "--no-progress"],
            cwd=cwd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        open(FETCH_STAMP, "w").close()
    except Exception:
        pass
    finally:
        try:
            os.unlink(FETCH_LOCK)
        except OSError:
            pass


def get_git_info(cwd):
    maybe_background_fetch(cwd)
    if not cache_is_stale(GIT_CACHE, GIT_CACHE_TTL):
        cached = read_cache(GIT_CACHE)
        if cached is not None:
            return cached

    info = {"branch": "", "remote": "", "behind": 0, "ahead": 0}
    try:
        subprocess.check_output(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=cwd, stderr=subprocess.DEVNULL, text=True,
        )
        info["branch"] = subprocess.check_output(
            ["git", "branch", "--show-current"],
            cwd=cwd, stderr=subprocess.DEVNULL, text=True,
        ).strip()
        if not info["branch"]:
            info["branch"] = subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"],
                cwd=cwd, stderr=subprocess.DEVNULL, text=True,
            ).strip()
        try:
            remote = subprocess.check_output(
                ["git", "remote", "get-url", "origin"],
                cwd=cwd, stderr=subprocess.DEVNULL, text=True,
            ).strip()
            remote = re.sub(r"^git@github\.com:", "https://github.com/", remote)
            remote = re.sub(r"\.git$", "", remote)
            info["remote"] = remote
        except Exception:
            pass
        try:
            behind = subprocess.check_output(
                ["git", "rev-list", "--count", "HEAD..@{u}"],
                cwd=cwd, stderr=subprocess.DEVNULL, text=True,
            ).strip()
            ahead = subprocess.check_output(
                ["git", "rev-list", "--count", "@{u}..HEAD"],
                cwd=cwd, stderr=subprocess.DEVNULL, text=True,
            ).strip()
            info["behind"] = int(behind)
            info["ahead"] = int(ahead)
        except Exception:
            pass
    except Exception:
        pass

    write_cache(GIT_CACHE, info)
    return info


def _run_ccusage(args):
    try:
        output = subprocess.check_output(
            ["bun", "x", "ccusage"] + args,
            stderr=subprocess.DEVNULL, text=True, timeout=15,
        )
        return json.loads(output).get("totals", {}).get("totalCost", 0)
    except Exception:
        return 0


def get_ccusage_data():
    if not cache_is_stale(CCUSAGE_CACHE, CCUSAGE_CACHE_TTL):
        cached = read_cache(CCUSAGE_CACHE)
        if cached is not None:
            return cached

    now = datetime.now()
    commands = {
        "today": ["daily", "--since", now.strftime("%Y%m%d"), "--json", "--offline"],
        "week":  ["weekly", "--since", (now - timedelta(days=7)).strftime("%Y%m%d"), "--json", "--offline"],
        "month": ["monthly", "--since", now.strftime("%Y%m01"), "--json", "--offline"],
    }

    costs = {"today": 0, "week": 0, "month": 0}
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(_run_ccusage, args): key for key, args in commands.items()}
        for future in as_completed(futures):
            costs[futures[future]] = future.result()

    write_cache(CCUSAGE_CACHE, costs)
    return costs


# ---------------------------------------------------------------------------
# Formatters
# ---------------------------------------------------------------------------
def fmt_cost(val):
    return "--" if val is None else f"${val:.2f}"


def fmt_duration(ms):
    if not ms:
        return "--"
    total = int(ms / 1000)
    h, remainder = divmod(total, 3600)
    m, s = divmod(remainder, 60)
    return f"{h}h {m}m" if h > 0 else f"{m}m {s}s"


def fmt_pct(val):
    return "--" if val is None else f"{val:.0f}%"


def fmt_time_remaining(resets_at):
    if not resets_at:
        return ""
    remaining = int(resets_at - time.time())
    if remaining <= 0:
        return "0m left"
    h, remainder = divmod(remaining, 3600)
    m = remainder // 60
    return f"{h}h {m}m left" if h > 0 else f"{m}m left"


def fmt_resets_at(resets_at):
    if not resets_at:
        return ""
    return f"resets {datetime.fromtimestamp(resets_at).strftime('%Y-%m-%d %H:%M')}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    data = json.load(sys.stdin)

    # --- Extract fields ---
    model_id = data.get("model", {}).get("id", "--")
    version = data.get("version", "--")
    used_pct = data.get("context_window", {}).get("used_percentage")
    cost_usd = data.get("cost", {}).get("total_cost_usd")
    duration_ms = data.get("cost", {}).get("total_duration_ms")
    cwd = data.get("workspace", {}).get("current_dir") or data.get("cwd", "")

    rate_limits = data.get("rate_limits", {})
    five_h = rate_limits.get("five_hour", {})
    seven_d = rate_limits.get("seven_day", {})

    home = os.path.expanduser("~")
    short_cwd = cwd.replace(home, "~", 1) if cwd.startswith(home) else cwd

    git = get_git_info(cwd)
    ccusage = get_ccusage_data()

    # --- [sess] context | session cost | duration ---
    ctx_marker = used_pct is not None and used_pct >= 50
    sess_line, sess_uline = render_line(
        [f"ctx: {fmt_pct(used_pct)}", fmt_cost(cost_usd), fmt_duration(duration_ms)],
        [threshold_color(used_pct, "dark"), MAGENTA, CYAN],
        markers=[ctx_marker, False, False],
    )

    # --- [rate] 5h | 7d ---
    five_h_text = f"5h: {fmt_pct(five_h.get('used_percentage'))}"
    remain = fmt_time_remaining(five_h.get("resets_at"))
    if remain:
        five_h_text += f" ({remain})"

    seven_d_text = f"7d: {fmt_pct(seven_d.get('used_percentage'))}"
    reset = fmt_resets_at(seven_d.get("resets_at"))
    if reset:
        seven_d_text += f" ({reset})"

    five_h_pct = five_h.get("used_percentage")
    seven_d_pct = seven_d.get("used_percentage")
    rate_line, rate_uline = render_line(
        [five_h_text, seven_d_text],
        [threshold_color(five_h_pct), threshold_color(seven_d_pct, "dim")],
        markers=[five_h_pct is not None and five_h_pct >= 80, seven_d_pct is not None and seven_d_pct >= 80],
    )

    # --- [cost] today | week | month ---
    cost_line, cost_uline = render_line(
        [f"today: {fmt_cost(ccusage['today'])}", f"week: {fmt_cost(ccusage['week'])}", f"month: {fmt_cost(ccusage['month'])}"],
        [COST_TODAY, COST_WEEK, COST_MONTH],
    )

    # --- [info] model | version ---
    info_line, info_uline = render_line(
        [model_id, f"v{version}"],
        [BLUE, GREY_LO],
    )

    # --- [repo] directory | branch (clickable) | pull/push ---
    repo_texts = [short_cwd]
    repo_colors = [GREY_LO]
    if git["branch"]:
        branch = f"\033]8;;{git['remote']}\a{git['branch']}\033]8;;\a" if git["remote"] else git["branch"]
        repo_texts.append(branch)
        repo_colors.append(GREY_LO)
    repo_line, repo_uline = render_line(repo_texts, repo_colors)

    if git["branch"]:
        behind, ahead = git.get("behind", 0), git.get("ahead", 0)
        sync_parts = []
        if behind > 0:
            sync_parts.append(block(f"↙{behind}", BLUE))
        if ahead > 0:
            sync_parts.append(block(f"↗{ahead}", GREEN))
        if sync_parts:
            repo_line += " " + "".join(sync_parts)

    # --- Output ---
    for label, line, uline in [
        ("sess", sess_line, sess_uline),
        ("rate", rate_line, rate_uline),
        ("cost", cost_line, cost_uline),
        ("info", info_line, info_uline),
        ("repo", repo_line, repo_uline),
    ]:
        print(title(label) + line)
        print(TITLE_PAD + uline)


if __name__ == "__main__":
    main()
