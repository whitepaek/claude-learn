# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 목적

Claude 및 Claude Code의 학습과 Best Practice 활용법을 배우기 위해 공식 문서, 검증된 플러그인, 쿡북 등을 모아둔 레퍼런스 워크스페이스이다.

## 세션 시작 시 행동

1. 아래 하위 프로젝트 목록을 순회하며, 디렉토리가 **존재하지 않으면** `git clone`으로 받고, **존재하면** `git pull`로 최신 상태를 유지한다.

| 디렉토리 | 원격 저장소 URL |
|----------|----------------|
| everything-claude-code | https://github.com/affaan-m/everything-claude-code.git |
| oh-my-claudecode | https://github.com/Yeachan-Heo/oh-my-claudecode.git |
| claude-cookbooks | https://github.com/anthropics/claude-cookbooks.git |
| claude-code-tips | https://github.com/ykdojo/claude-code-tips.git |
| spec-kit | https://github.com/github/spec-kit.git |
| claude-plugins-official | https://github.com/anthropics/claude-plugins-official.git |

2. 사용자의 질문에 하위 프로젝트 내 자료만으로 충분하지 않을 경우, 아래 레퍼런스 링크를 `WebFetch`로 참조하여 최신 정보와 팁을 제공한다.

## 레퍼런스 링크

### 공식 문서
- https://platform.claude.com/docs/en/home
- https://code.claude.com/docs

### 아티클 / 블로그
- https://adocomplete.com/advent-of-claude-2025/

### 커뮤니티 / SNS
- https://www.reddit.com/r/ClaudeAI/
- https://x.com/ykdojo
- https://x.com/adocomplete

## 하위 프로젝트

### everything-claude-code/
Anthropic 해커톤 우승자의 Claude Code 설정 모음집. 에이전트(13개), 스킬(31개), 커맨드(33개), 멀티 언어 규칙, 훅 설정 등 실전 운영 구성을 참고할 수 있다.

### oh-my-claudecode/
TypeScript 멀티 에이전트 오케스트레이션 플러그인. 33개 에이전트(Haiku/Sonnet/Opus 티어), 7가지 실행 모드(autopilot, ralph, ultrawork, ultrapilot, ecomode, swarm, pipeline), MCP 브리지, LSP/AST 통합 등의 구현을 참고할 수 있다.

### claude-cookbooks/
Anthropic 공식 쿡북. Claude API 활용 Jupyter 노트북과 Python 예제 모음. RAG, 분류, 요약, tool use, 멀티모달, Agent SDK 등 주제별 예제가 있다.

### claude-code-tips/
45개의 Claude Code 실전 팁. 상태바 커스터마이징, Git 워크플로우, 컨테이너 활용, 시스템 프롬프트 최적화, TDD, 병렬화 등을 다룬다.

### spec-kit/
GitHub 공식 Spec-Driven Development(SDD) 툴킷. 명세(Specification)를 먼저 작성하고 코드를 생성하는 방법론을 지원한다. `specify` CLI, 슬래시 커맨드(constitution, specify, clarify, plan, tasks, implement, analyze, checklist), 확장 시스템, 19개 이상의 AI 에이전트 통합(Claude Code, Copilot, Gemini 등)을 제공한다.

### claude-plugins-official/
Anthropic 공식 Claude Code 플러그인 디렉토리. 내부(Anthropic 개발) 플러그인과 외부(서드파티) 플러그인을 포함하며, LSP 통합(TypeScript, Go, Python, Rust, Swift 등), 코드 리뷰, PR 리뷰, 기능 개발, 플러그인 개발 도구 등 표준 플러그인 구조와 레퍼런스 구현을 참고할 수 있다.
