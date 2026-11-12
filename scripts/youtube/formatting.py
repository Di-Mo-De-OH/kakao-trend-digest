from typing import Any


def fmt_duration(sec: int) -> str:
    """초를 'M:SS' 문자열로 바꾼다. 예: 200 -> '3:20'."""
    minutes, seconds = divmod(sec, 60)
    return f"{minutes}:{seconds:02d}"


def fmt_count(stats: dict[str, Any], field: str) -> str:
    """통계 값을 천 단위 쉼표 문자열로 바꾼다. 예: '43443466' -> '43,443,466'.

    숨김 처리된 지표는 응답에 필드가 없어서 '-'로 표시한다.
    """
    value = stats.get(field)
    return f"{int(value):,}" if value is not None else "-"
