# Statusline

## Layout (10 lines)

```
[sess]  ctx: 10%  $1.23  12m 34s
        ────────  ─────  ───────
[rate]  5h: 24% (1h 19m left)  7d: 41% (resets 2026-04-14 16:25)
        ─────────────────────  ─────────────────────────────────
[cost]  today: $38.02  week: $720.50  month: $720.50
        ─────────────  ─────────────  ──────────────
[info]  claude-opus-4-6  v2.1.90
        ───────────────  ───────
[repo]  ~/workspace/claude-learn  main ↙2↗1
        ────────────────────────  ────
```

## Lines

| Line | Title | Items | Source |
|------|-------|-------|--------|
| 1 | `[sess]` | context usage, session cost, duration | stdin JSON |
| 2 | `[rate]` | 5h usage + remaining, 7d usage + reset datetime (with year) | stdin JSON (Pro/Max) |
| 3 | `[cost]` | today cost, weekly cost, monthly cost | ccusage (`bun x`) |
| 4 | `[info]` | model ID, Claude Code version | stdin JSON |
| 5 | `[repo]` | working directory, branch (Cmd+click -> GitHub), pull/push counts | stdin JSON + git |

## Title Rules

- 4-char uniform: `sess`, `rate`, `cost`, `info`, `repo`
- Format: `[xxxx]` + 2 spaces (8 visible chars total)
- Color: Grey (242)
- Underline row: ANSI-wrapped 6 grey spaces + 2 normal spaces (trim prevention)

## Color Palette

Powerlevel10k Pure base + 256-color extensions.

### Pure Base

| Color | Code | Items |
|-------|------|-------|
| Green | 2 | 5h threshold normal (standard) |
| Yellow | 3 | 5h threshold warning / ccusage today |
| Red | 1 | 5h threshold danger |
| Blue | 4 | model ID |
| Magenta | 5 | session cost |
| Cyan | 6 | session duration |
| Grey | 242 | titles, null fallback |
| Grey LO | 245 | directory, branch, version |

### ctx Threshold (dark)

| Color | Code | Threshold |
|-------|------|-----------|
| Dark Green | 22 | < 50% |
| Dark Yellow | 136 | 50-79% |
| Dark Red | 88 | >= 80% |

### 7d Threshold (dim)

| Color | Code | Threshold |
|-------|------|-----------|
| Dim Green | 65 | < 50% |
| Dim Yellow | 179 | 50-79% |
| Dim Red | 131 | >= 80% |

### Pull/Push Indicators

| Color | Code | Item |
|-------|------|------|
| Blue | 4 | ↙ pull (behind remote) |
| Green | 2 | ↗ push (ahead of remote) |

### ccusage Cost Gradient

| Color | Code | Item |
|-------|------|------|
| Yellow | 3 | today |
| Gold | 179 | week |
| Salmon | 173 | month |

## 3-Tier Threshold (importance-based brightness)

| Threshold | ctx (dark, high) | 5h (standard, mid) | 7d (dim, low) |
|-----------|-----------------|--------------------|--------------| 
| null | Grey (242) | Grey (242) | Grey (242) |
| < 50% | Dark Green (22) | Green (2) | Dim Green (65) |
| 50-79% | Dark Yellow (136) | Yellow (3) | Dim Yellow (179) |
| >= 80% | Dark Red (88) | Red (1) | Dim Red (131) |

### Underline `[!]` Marker

밑줄 행에 `[!]`를 표시하여 임계값 초과를 시각적으로 강조한다.

| 항목 | 조건 | 밑줄 예시 |
|------|------|----------|
| ctx | >= 50% (주의 이상) | `[!] ────` |
| 5h | >= 80% (위험) | `[!] ─────────────────` |
| 7d | >= 80% (위험) | `[!] ─────────────────` |

조건 미달 시 기존 `────────` 밑줄 유지.

## Underline Rules

- `─` chars matching visible text length (ANSI codes excluded)
- Same color as the item above
- 2-space gap between items

## Caching

| Target | Cache File | TTL | Method |
|--------|-----------|-----|--------|
| Git | `/tmp/statusline-git-cache.json` | 5s | `git` CLI (local refs) |
| Git fetch | `/tmp/statusline-git-fetch.stamp` | 180s | `git fetch --quiet` (background, non-blocking) |
| ccusage | `/tmp/statusline-ccusage-cache.json` | 300s | `bun x ccusage` x3 parallel (`ThreadPoolExecutor`) |

### Git Auto Fetch

- 180초(3분) 주기로 `git fetch`를 백그라운드 실행 (VS Code 기본값 기준)
- `Popen` + `start_new_session=True`로 statusline 렌더링을 차단하지 않음
- `/tmp/statusline-git-fetch.lock`으로 동시 실행 방지 (원자적 lock)
- fetch 실패 시 silent 처리, 기존 로컬 상태 유지

## ccusage Cost Calculation

| Command | Range | `--since` |
|---------|-------|-----------|
| `bun x ccusage daily` | today | YYYYMMDD |
| `bun x ccusage weekly` | last 7 days | 7 days ago |
| `bun x ccusage monthly` | this month | YYYYMM01 |

Options: `-m auto` (default), `--offline` (local pricing), `--json` (JSON output)

## Conditional Field Handling

| Field | When absent |
|-------|------------|
| `context_window.used_percentage` (null) | `ctx: --` (Grey) |
| `rate_limits` (not in JSON) | `5h: --`, `7d: --` (Grey) |
| `cost.total_duration_ms` (0) | `--` |
| No upstream tracking branch | pull/push not shown |
| Not a git repo | directory only |

## Code Structure

```
statusline.py
├── Colors          (13-41)    color constants
├── Cache           (43-78)    read/write/stale check, fetch constants
├── Rendering       (81-120)   block, underline, title, threshold_color, render_line
├── Data sources    (123-237)  maybe_background_fetch, get_git_info, get_ccusage_data
├── Formatters      (240-275)  fmt_cost, fmt_duration, fmt_pct, fmt_time_remaining, fmt_resets_at
└── Main            (278-367)  extract fields -> render 5 lines -> output
```
