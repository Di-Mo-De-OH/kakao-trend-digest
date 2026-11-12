import re

_DURATION = re.compile(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?")


def duration_seconds(iso: str) -> int:
    """'PT1H2M3S' 같은 ISO 8601 길이를 초로 바꾼다. 해석할 수 없으면 0."""
    m = _DURATION.fullmatch(iso)
    if not m:
        return 0
    hours, minutes, seconds = (int(x or 0) for x in m.groups())
    return hours * 3600 + minutes * 60 + seconds
