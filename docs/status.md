# 현황

마지막 갱신: 2026-11-09

## 완료
- 프로젝트 초기 설정: uv, ruff, Makefile, 폴더 구조
- 스키마: Video (Author, VideoStats), Hashtag, Article, `normalize_tag` 유틸
- 작업 구조 문서: `CLAUDE.md`, `docs/architecture.md`, `docs/status.md`, `docs/decisions/` (0001~0004), `.gitignore` 정리 (커밋 전)

## 다음 할 일 (우선순위 순)
1. 문서 세트 커밋: CLAUDE.md, docs/, .gitignore. 빈 파일이 스테이징됐던 이력이 있어 `git add` 재확인 필요2. **데이터 소스 가능성 검증** (`scripts/`에서): 숏폼 해시태그·영상, 글로벌 기사를 합법적이고 안정적으로 가져올 수 있는가. 이 프로젝트의 가장 큰 위험 요소
3. `.claude/` 설정: `settings.json`(ruff 자동 실행 hook), `settings.local.json`(홈 폴더의 이력서용 `~/CLAUDE.md` 제외)
4. `Digest` 스키마 추가 (초안 먼저 승인)
5. 테스트 재도입: pytest 추가, 스키마·`normalize_tag` 테스트 작성 (2026-11-09 롤백으로 빠진 상태)
6. `Collector` / `Notifier` 인터페이스와 `pipeline.run()` 구현
   - Discord 연동 전에: `.env`를 읽지 못하게 deny 설정 완료 (웹훅 URL을 `.env`에 넣기 전)
7. 프로젝트명을 `trend-digest`로 변경 (0004): GitHub 저장소명, `pyproject.toml`의 name, CLAUDE.md 제목·괄호 설명, README. 저장소명 변경 후 `git remote set-url` 필요
8. README 수정 (구조 확정 후, 이름 변경과 함께)

## 미결정
- 데이터 소스 (2번에서 검증)
- Discord 전달 방식: 웹훅 vs 봇
- 주별 스냅샷 보관 위치 (`data/`를 repo에 커밋 / Actions 캐시 / 기타)
- 주 단위 요일·시각, 주 경계 시간대
- 프로젝트명 변경 시점
- 빈 태그 허용 여부: 현재 `Hashtag(name="#")`가 `name=""`로 통과함
- naive datetime 허용 여부
