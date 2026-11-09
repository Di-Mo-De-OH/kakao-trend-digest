# kakao-trend-digest

매주 한 번, 지난 한 주 기준 숏폼 트렌드(해시태그·영상)와 글로벌 트렌드
기사·영상 링크를 Discord로 전달하는 파이프라인.
(이름은 kakao지만 전달 채널은 Discord로 결정됨)

## 세션 시작 시
- `docs/status.md`를 먼저 읽고 현재 단계, 다음 할 일, 미결정 사항을 파악한다.
- 구조에 영향을 주는 작업 전에는 `docs/architecture.md`를 확인한다.
- 확정된 결정은 `docs/decisions/`에 있다. 그와 다른 방향으로 가려면 먼저 물어본다.

## 명령어 (패키지 관리는 uv)
- `make check` — ruff 린트+포맷 검사, 문제 있으면 자동 수정 후 재검사
- `make install` — 의존성 설치 (`uv sync`)
- 그 외 명령어는 `make help`로 확인한다.
- 파이썬 도구는 항상 `uv run`으로 실행한다.

## 디렉터리
- `app/schemas/` — pydantic 데이터 모델 (Video, Hashtag, Article)
- `app/core/` — 공용 유틸
- `app/collectors/` — 외부 소스에서 데이터 수집
- `app/ranking/` — 점수화·정렬
- `app/ai/` — 요약 등 LLM 처리
- `app/notifier/` — Discord 전달
- `app/storage/` — 주별 스냅샷 저장 (rank_change 계산용)
- `tests/`, `scripts/`, `data/`, `.github/workflows/`

## 작업 방식 (가장 중요)
- 새 파일·모듈·의존성·설정을 추가하거나 구조를 바꿀 때는, 만들기 전에 초안을 먼저 보여주고 승인받는다. 기존 코드의 단순 수정은 바로 한다.
- git 스테이징(add·rm·mv), 커밋, 푸시, PR 생성은 어떤 경우에도 하지 않는다. 사용자가 직접 한다. (`.claude/settings.json`의 deny로도 막혀 있다. git status·diff·log 같은 읽기 명령은 가능하다.)
- reset --hard, clean, force push처럼 되돌릴 수 없는 git 작업은 실행 전에 위험성(무엇이 사라지는지)을 사용자에게 알리고 확인받는다.
- 테스트 코드는 Claude가 작성한다.
- 작업을 마치기 전에 `make check`를 통과시킨다.

## 코드 규칙
- Python 3.14, pydantic v2, ruff(E, F, I, B, UP).
- 파일명은 소문자 snake_case.
- 대화·주석·문서는 한국어, 식별자·명령어는 영어.
- 커밋 메시지는 `feat:` `fix:` `docs:` `chore:` 접두사 + 한국어 설명.

## 보안
- `.env`는 절대 읽거나 출력하지 않는다.
- 웹훅 URL·토큰·API 키는 코드, 로그, 커밋에 넣지 않는다.

## 세션 종료 시
- `docs/status.md`를 갱신한다 (한 일 / 다음 할 일 / 미결정).
- 새로 확정된 결정은 `docs/decisions/`에 한 파일로 기록한다.