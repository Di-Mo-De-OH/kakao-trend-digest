import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from .utils import BASE_URL


def call(endpoint: str, **params: str) -> dict[str, Any]:
    """YouTube Data API 엔드포인트를 호출해 JSON 응답을 dict로 돌려준다.

    키는 환경변수 YOUTUBE_API_KEY에서 읽는다.
    키가 없거나 호출이 실패하면 메시지를 출력하고 종료한다.
    """
    key = os.environ.get("YOUTUBE_API_KEY")
    if not key:
        sys.exit(
            "YOUTUBE_API_KEY가 없습니다. env/.env에 넣고 "
            "--env-file env/.env로 실행하세요."
        )
    query = urllib.parse.urlencode({**params, "key": key})
    url = f"{BASE_URL}/{endpoint}?{query}"
    try:
        with urllib.request.urlopen(url, timeout=10) as res:
            return json.load(res)
    except urllib.error.HTTPError as e:
        # URL에 키가 들어 있으므로 URL은 출력하지 않는다.
        sys.exit(f"{endpoint} 실패: HTTP {e.code} {e.read().decode()[:300]}")
    except urllib.error.URLError as e:
        sys.exit(f"{endpoint} 연결 실패: {e.reason}")
