# 현황

마지막 갱신: 2026-11-12

## 완료
- 프로젝트 초기 설정: uv, ruff, Makefile, 폴더 구조
- 스키마: Video (Author, VideoStats), Hashtag, Article, `normalize_tag` 유틸
- 작업 구조 문서: `CLAUDE.md`, `docs/architecture.md`, `docs/status.md`, `docs/decisions/` (0001~0004), `.gitignore` 정리 (커밋 완료, b3dd383)
- `.claude/` 설정: `settings.json`(git 쓰기 명령·`gh pr create`·`.env` 읽기 deny, 위험한 git 명령 `reset`·`clean`·`restore`·`branch -D`·`stash drop`은 ask), `settings.local.json`(홈 폴더 `~/CLAUDE.md` 제외, gitignore 대상)

## 다음 할 일 (우선순위 순)
1. **데이터 소스 가능성 검증** (`scripts/`에서): 숏폼 해시태그·영상, 글로벌 기사를 합법적이고 안정적으로 가져올 수 있는가. 이 프로젝트의 가장 큰 위험 요소
   - 사전 조사(2026-11-12, 웹 검색 기준·공식 원문 미확인): 공식 경로로 확실한 건 YouTube뿐. TikTok(Research API는 연구 승인제·상업 이용 금지 설명, Creative Center는 공개 API 없음)과 Instagram(해시태그 검색은 비즈니스 계정·앱 심사·7일 30개 제한, 트렌딩 순위 엔드포인트 없음)은 어려워 보임
   - 진행: `scripts/youtube/` 패키지로 YouTube 검증 스크립트 작성·리팩터링 완료, 실행 확인됨 (지난 7일 업로드 영상 조회수순, region=KR). 실행: `uv run --env-file env/.env python -m scripts.youtube.main` (프로젝트 루트에서, 키는 `env/.env`의 `YOUTUBE_API_KEY`)
     - 구조: `utils.py`(상수) · `parse.py`(길이 파싱) · `formatting.py`(출력용 포맷) · `client.py`(`call()`) · `main.py`(흐름·출력). 수집기를 만들 때 `parse.py`를 `app/collectors/`로 옮긴다
   - 원본 응답 확인 (2026-11-12, 영상 3개 샘플 기준):
     - 해시태그 전용 필드 없음. `description`의 `#태그`를 파싱해야 한다. `snippet.tags`는 키워드 목록이고 없는 영상도 있다
     - 조회수·좋아요 등 숫자 지표는 문자열로 온다. 숨김 지표는 필드 자체가 없다
     - Shorts 판별 공식 필드 없음. 길이로 추정 (샘플 3개 모두 60초 이하)
     - `regionCode=KR`인데도 한국어가 아닌 영상(영어·일본어)이 섞여 나온다
   - 다음 확인할 것: `relevanceLanguage=ko` 추가 시 결과가 한국어 영상 위주로 바뀌는지, 25개 전체 결과에서 Shorts 혼입·좋아요·구독자 숨김 비율·검색 순서와 실제 조회수 순서 일치 여부, 해시태그 추출 방식, `Author.followers`를 `int | None`으로 바꿀지
2. `Digest` 스키마 추가 (초안 먼저 승인)
3. 테스트 재도입: pytest 추가, 스키마·`normalize_tag` 테스트 작성 (2026-11-09 롤백으로 빠진 상태)
4. `Collector` / `Notifier` 인터페이스와 `pipeline.run()` 구현
5. 프로젝트명을 `trend-digest`로 변경 (0004): GitHub 저장소명, `pyproject.toml`의 name, CLAUDE.md 제목·괄호 설명, README. 저장소명 변경 후 `git remote set-url` 필요
6. README 수정 (구조 확정 후, 이름 변경과 함께)

## 미결정
- 데이터 소스 (1번에서 검증): MVP를 YouTube 영상 + 영상에서 집계한 해시태그로 갈지, TikTok Creative Center 약관 확인·유료 제3자 데이터까지 볼지
- 영상 수집 지역: 지금은 `KR` 상수로 둠. 글로벌로 볼지. 한국어 영상만 볼지(`relevanceLanguage`)도 함께 결정
- Discord 전달 방식: 웹훅 vs 봇
- 주별 스냅샷 보관 위치 (`data/`를 repo에 커밋 / Actions 캐시 / 기타)
- 주 단위 요일·시각, 주 경계 시간대
- 프로젝트명 변경 시점
- 빈 태그 허용 여부: 현재 `Hashtag(name="#")`가 `name=""`로 통과함
- naive datetime 허용 여부
- ruff 자동 실행 hook 도입 여부: 이번 `settings.json`에는 넣지 않음. 지금은 `make check`로 수동 확인
- `settings.json` 자체를 Claude가 수정하지 못하게 `Edit` deny를 걸지 (걸면 설정 변경은 사용자가 직접 해야 함)
