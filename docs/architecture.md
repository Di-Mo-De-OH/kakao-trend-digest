# 아키텍처

## 목적
매주 한 번, 지난 한 주 기준 숏폼 트렌드(해시태그·영상)와 글로벌 트렌드 기사를
수집·정렬해 Discord로 링크를 전달한다.

범위 밖 (지금은 하지 않음):
- 실시간 알림, 구독자 관리, 웹 UI
- 기사·영상 원문 저장 (링크만 전달한다)
- AI 요약 (MVP 이후. `app/ai/`는 비워 두고 `Article.summary`는 `None`으로 남긴다)

## 데이터 흐름
```
collectors ──▶ ranking ──▶ Digest ──▶ notifier ──▶ Discord
    │                         ▲
    └────────▶ storage ◀──────┘
             (주별 스냅샷: rank_change, 중복 방지)
```
1. collectors: 소스별로 Hashtag / Video / Article을 수집한다.
2. storage: 지난 주 스냅샷을 읽어 rank_change·is_new 계산에 쓴다.
3. ranking: 점수화해 상위 N개를 고른다.
4. 결과를 Digest(한 주치 결과 묶음)로 만든다. Digest 스키마는 아직 없다.
5. notifier가 Discord 길이 제한에 맞게 나눠 보낸다.
6. 이번 주 스냅샷을 storage에 저장한다.

## 모듈 책임
| 모듈 | 책임 | 외부 I/O |
|---|---|---|
| schemas | 도메인 데이터 모델 (pydantic) | 없음 |
| core | 공용 유틸 | 없음 |
| collectors | 외부 소스 → 스키마 변환 | HTTP |
| ranking | 점수화·정렬 | 없음 (순수 함수) |
| notifier | Digest → Discord 전달 | HTTP |
| storage | 스냅샷 읽기·쓰기 | 파일 |
| ai | (MVP 제외) 요약 | LLM API |
| pipeline | 위 모듈을 엮는 조율자 (`app/pipeline.py`) | 없음 (모듈에 위임) |

## 의존 규칙
- schemas, core는 다른 app 모듈을 import하지 않는다. 나머지가 이 둘을 import한다.
- collectors / ranking / notifier / storage(/ ai)는 서로 import하지 않는다.
  이들을 연결하는 곳은 `pipeline.py` 하나뿐이다.
- 외부 I/O는 collectors, notifier, storage(/ ai)에만 둔다. ranking은 순수 함수로 유지한다.

## 실행 구조: app/pipeline.py
두 층으로 나눈다.

| 구성 | 하는 일 | 테스트 |
|---|---|---|
| `run(collectors, storage, notifier, week)` | 순서 제어, 실패 정책, 중복 방지 | 가짜 객체를 주입해 검증 |
| `main()` / `if __name__ == "__main__"` | 실제 객체 생성, `.env`에서 설정 읽기, `run()` 호출 | 하지 않음 (얇은 껍데기) |

- 실행: `uv run python -m app.pipeline` (로컬과 GitHub Actions 동일)
- `pipeline.py`가 하는 일: 구현체 조립, 호출 순서, 부분 실패 처리, 주 단위 중복 판단.
- `pipeline.py`가 하지 않는 일: HTTP 호출, 점수 계산, 메시지 포맷팅. 이건 각 모듈의 몫이다.
  파일이 50~80줄을 넘기면 로직이 새어 들어온 신호로 본다.
- `scripts/`는 일회성 도구용이다 (예: 데이터 소스 가능성 검증).

## 원칙
- 소스 하나가 실패해도 전체를 중단하지 않는다. 가능한 섹션만 보내고 실패는 로그에 남긴다.
- 멱등성: 같은 주(ISO week)를 다시 실행해도 결과가 같고 중복 전송하지 않는다.
  '보냈다'는 기록은 전송이 성공한 뒤에만 남긴다.
- datetime은 timezone-aware로 다룬다.
- 소스와 전달 수단은 교체 가능하도록 인터페이스(Collector, Notifier)로 둔다.

## 미결정
`docs/status.md`의 "미결정" 참고. 주요 항목:
- 데이터 소스
- 전달 방식 (Discord 웹훅 vs 봇)
- 스냅샷 보관 위치
- 주 단위 요일·시각, 주 경계 시간대
