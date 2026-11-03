import unicodedata


def normalize_tag(value: str) -> str:
    v = unicodedata.normalize("NFC", value)  # 한글 자모 합치기
    return v.strip().lstrip("#").strip().lower()
