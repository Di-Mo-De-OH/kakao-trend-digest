# 0004. 프로젝트명을 trend-digest로 변경한다

상태: 확정 (변경 시점 미정) · 2026-11-09

## 배경
프로젝트명이 kakao-trend-digest라서 이름에 "kakao"가 들어 있다.
카카오톡 전달을 취소하고 Discord로 가면서(0001) 이름이 실제와 맞지 않게 됐다.

## 결정
프로젝트명을 `trend-digest`로 변경한다.
변경 시점은 아직 정하지 않았다 (status.md 참고).

## 변경 이유
카카오톡 전달을 취소했다. 운영자가 사용자 각각의 아이디를 알아야 하는 방식이
이 서비스에 부적합하기 때문이다. 카카오가 빠졌으므로 이름에서도 kakao를 뺀다.

## 결과
- 변경 대상: GitHub 저장소명, `pyproject.toml`의 name, CLAUDE.md의 제목과 괄호 설명, README.
- 저장소명을 바꾸면 원격 URL이 바뀌므로 로컬에서 `git remote set-url`이 필요하다.
- 변경 전까지는 CLAUDE.md의 "이름은 kakao지만 전달 채널은 Discord" 설명을 유지한다.
