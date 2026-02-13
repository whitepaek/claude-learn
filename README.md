# claude-learn

Claude 및 Claude Code의 학습과 Best Practice 활용법을 배우기 위한 레퍼런스 워크스페이스.
공식 문서, 검증된 플러그인, 쿡북, 실전 팁 등을 한곳에 모아 참고할 수 있다.

## 하위 프로젝트 (Subprojects)

| 디렉토리 | 설명 | 저장소 |
|----------|------|--------|
| `everything-claude-code` | Anthropic 해커톤 우승자의 Claude Code 실전 설정 모음집. 에이전트, 스킬, 커맨드, 멀티 언어 규칙, 훅 설정 등을 참고할 수 있다. | [GitHub](https://github.com/affaan-m/everything-claude-code) |
| `oh-my-claudecode` | TypeScript 멀티 에이전트 오케스트레이션 플러그인. autopilot, ralph, ultrawork 등 7가지 실행 모드와 MCP 브리지, LSP/AST 통합 등의 구현을 참고할 수 있다. | [GitHub](https://github.com/Yeachan-Heo/oh-my-claudecode) |
| `claude-cookbooks` | Anthropic 공식 쿡북. Claude API 활용 Jupyter 노트북과 Python 예제 모음. RAG, 분류, 요약, tool use, 멀티모달, Agent SDK 등 주제별 예제가 있다. | [GitHub](https://github.com/anthropics/claude-cookbooks) |
| `claude-code-tips` | Claude Code 실전 팁 모음. 상태바 커스터마이징, Git 워크플로우, 컨테이너 활용, 시스템 프롬프트 최적화, TDD, 병렬화 등을 다룬다. | [GitHub](https://github.com/ykdojo/claude-code-tips) |
| `spec-kit` | GitHub 공식 Spec-Driven Development(SDD) 툴킷. 명세를 먼저 작성하고 코드를 생성하는 방법론과 CLI, 슬래시 커맨드, 확장 시스템, 19개 이상의 AI 에이전트 통합을 제공한다. | [GitHub](https://github.com/github/spec-kit) |

## 시작하기 (Getting Started)

### 1. 프로젝트 클론

```bash
git clone https://github.com/whitepaek/claude-learn.git
cd claude-learn
```

### 2. 하위 프로젝트 초기화

프로젝트 디렉토리에서 Claude Code를 실행하고, 하위 프로젝트 업데이트를 요청한다.

```
claude
> 하위 프로젝트를 최신 상태로 업데이트해줘
```

`CLAUDE.md`에 정의된 지침에 따라 각 하위 프로젝트를 clone하거나 pull한다.

> **참고**: `CLAUDE.md`는 자동 실행 스크립트가 아니라 Claude가 참고하는 **지침 파일**이다.
> 세션이 시작되었다고 지침이 자동 실행되지 않으며, 위와 같이 사용자가 명시적으로 요청해야 동작한다.

## CLAUDE.md

이 저장소에는 `CLAUDE.md` 파일이 포함되어 있다.
Claude Code가 세션을 시작할 때 자동으로 읽어들이는 프로젝트 지침 파일로,
하위 프로젝트 동기화 규칙과 레퍼런스 링크 등이 정의되어 있다.

## 레퍼런스 링크 (References)

**공식 문서**
- [Claude Platform Docs](https://platform.claude.com/docs/en/home)
- [Claude Code Docs](https://code.claude.com/docs)

**아티클 / 블로그**
- [Advent of Claude 2025](https://adocomplete.com/advent-of-claude-2025/)

**커뮤니티 / SNS**
- [r/ClaudeAI (Reddit)](https://www.reddit.com/r/ClaudeAI/)
- [@ykdojo (X)](https://x.com/ykdojo)
- [@adocomplete (X)](https://x.com/adocomplete)
