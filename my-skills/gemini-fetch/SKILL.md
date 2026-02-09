---
name: gemini-fetch
description: Fetch content from any URL using Gemini CLI when WebFetch is blocked (403, timeout, authentication required, etc.). Use when WebFetch fails or returns errors for any website.
---

# Gemini Fetch - WebFetch 차단 사이트 우회

WebFetch가 실패하는 사이트(403, 차단, 인증 필요 등)에서 Gemini CLI를 통해 콘텐츠를 가져온다.

고유한 세션 이름을 생성하고(예: `gemini_<random>`), 전체 과정에서 동일하게 사용한다.

## 1. 세션 시작

```bash
tmux new-session -d -s <session_name> -x 200 -y 50
tmux send-keys -t <session_name> 'gemini -m gemini-3-pro-preview' Enter
sleep 3  # Gemini CLI 로딩 대기
```

## 2. 질의 전송 및 출력 캡처

URL을 직접 전달하거나, URL과 함께 구체적인 지시를 보낸다.

**URL 콘텐츠 가져오기:**
```bash
tmux send-keys -t <session_name> 'Fetch and summarize the content from this URL: <target_url>' Enter
sleep 30  # 응답 대기 (복잡한 페이지는 최대 90초)
tmux capture-pane -t <session_name> -p -S -500
```

**특정 정보 추출:**
```bash
tmux send-keys -t <session_name> 'Go to <target_url> and extract: <specific_request>' Enter
sleep 30
tmux capture-pane -t <session_name> -p -S -500
```

**웹 검색:**
```bash
tmux send-keys -t <session_name> 'Search the web for: <search_query>' Enter
sleep 30
tmux capture-pane -t <session_name> -p -S -500
```

## 3. Enter 전송 여부 확인

캡처된 출력에서 질의 텍스트의 위치를 확인한다.

**Enter 미전송** - 질의가 박스 안에 있음:
```
╭─────────────────────────────────────╮
│ > Your actual query text here       │
╰─────────────────────────────────────╯
```

**Enter 전송됨** - 질의가 박스 밖에 있고, 처리 중 표시가 보임:
```
> Your actual query text here

⠋ Our hamsters are working... (processing)

╭────────────────────────────────────────────╮
│ >   Type your message or @path/to/file     │
╰────────────────────────────────────────────╯
```

빈 프롬프트 `Type your message or @path/to/file`은 항상 박스 안에 표시되며 이는 정상이다. 중요한 것은 **내가 보낸 질의 텍스트**가 박스 안인지 밖인지 여부다.

질의가 박스 안에 있으면 Enter를 다시 전송한다:
```bash
tmux send-keys -t <session_name> Enter
```

## 4. 응답이 불완전할 때

출력이 잘렸거나 응답 중간인 경우:
```bash
sleep 15  # 추가 대기
tmux capture-pane -t <session_name> -p -S -1000  # 더 넓은 범위 캡처
```

## 5. 후속 질의

같은 세션에서 추가 질문이 가능하다:
```bash
tmux send-keys -t <session_name> 'Follow-up question here' Enter
sleep 30
tmux capture-pane -t <session_name> -p -S -500
```

## 6. 세션 정리

작업 완료 후 반드시 세션을 종료한다:
```bash
tmux kill-session -t <session_name>
```

## 사용 시 참고사항

- **sleep 시간 조정**: 단순 질문 `10~15초`, URL 분석 `30초`, 복잡한 웹 검색 `60~90초`
- **캡처 범위**: `-S -500`은 최근 500줄. 긴 응답은 `-S -1000`으로 늘린다
- **세션 재사용**: 같은 주제의 후속 질문은 세션을 유지하고 추가 질의한다
- **모델 변경**: 빠른 응답이 필요하면 `gemini-3-flash-preview`, 깊은 분석은 `gemini-3-pro-preview`
