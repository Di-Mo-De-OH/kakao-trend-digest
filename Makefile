.DEFAULT_GOAL := help
.PHONY: help install lint format check fix clean

help: ## 사용 가능한 명령어 목록
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

install: ## 의존성 설치 (dev 포함)
	uv sync

lint: ## ruff 린트 검사
	uv run ruff check .

format: ## ruff 코드 포맷팅
	uv run ruff format .

fix: ## ruff 자동 수정 가능한 린트 오류 수정 + 포맷팅
	uv run ruff check --fix .
	uv run ruff format .

check: ## CI용 검사 (린트 + 포맷 확인, 파일 수정 없음)
	uv run ruff check .
	uv run ruff format --check .

clean: ## 캐시 파일 삭제
	rm -rf .ruff_cache .pytest_cache .mypy_cache
	find . -type d -name __pycache__ -not -path "./.venv/*" -prune -exec rm -rf {} +
