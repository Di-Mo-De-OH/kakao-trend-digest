"""YouTube 지난 7일 인기 영상 수집 가능성 검증 (일회성 스크립트).

실행: uv run --env-file env/.env python -m scripts.youtube.main

- env/.env에 YOUTUBE_API_KEY가 있어야 한다. 키는 어디에도 출력하지 않는다.
- 호출은 3번이다 (검색 100 + 영상 1 + 채널 1 = 약 102 쿼터 유닛).
- 표준 라이브러리만 쓴다. app/ 모듈은 건드리지 않는다.
"""

import sys
from datetime import UTC, datetime, timedelta

from .client import call
from .formatting import fmt_count, fmt_duration
from .parse import duration_seconds
from .utils import DAYS, MAX_RESULTS, REGION_CODE, SHORT_LIMIT_SEC


def main() -> None:
    """검색 → 영상 상세 → 채널 통계 순으로 호출해 결과를 표로 출력한다.

    마지막에 검증 요약(Shorts 추정 수, 숨김 지표 수, 정렬 일치 여부)도 출력한다.
    """
    since = (datetime.now(UTC) - timedelta(days=DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    found = call(
        "search",
        part="id",
        type="video",
        order="viewCount",
        publishedAfter=since,
        regionCode=REGION_CODE,
        maxResults=str(MAX_RESULTS),
    )
    video_ids = [item["id"]["videoId"] for item in found.get("items", [])]
    if not video_ids:
        sys.exit("검색 결과가 없습니다.")

    videos = call(
        "videos",
        part="snippet,statistics,contentDetails",
        id=",".join(video_ids),
    )
    by_id = {v["id"]: v for v in videos.get("items", [])}

    channel_ids = sorted({v["snippet"]["channelId"] for v in by_id.values()})
    channels = call("channels", part="statistics", id=",".join(channel_ids))
    channel_stats = {c["id"]: c["statistics"] for c in channels.get("items", [])}

    print(
        f"지난 {DAYS}일 업로드 · 검색 조회수순 · region={REGION_CODE} · since {since}\n"
    )
    print(
        f"{'#':>2} {'조회수':>12} {'좋아요':>10} {'구독자':>12} {'길이':>7}  제목 / URL"
    )

    views: list[int] = []
    short_count = hidden_likes = hidden_subs = 0
    for rank, video_id in enumerate(video_ids, 1):
        video = by_id.get(video_id)
        if video is None:  # 검색 후 삭제되거나 비공개로 바뀐 영상
            continue
        stats = video["statistics"]
        sec = duration_seconds(video["contentDetails"]["duration"])
        ch_stats = channel_stats.get(video["snippet"]["channelId"], {})

        views.append(int(stats.get("viewCount", 0)))
        short_count += sec <= SHORT_LIMIT_SEC
        hidden_likes += "likeCount" not in stats
        if ch_stats.get("hiddenSubscriberCount"):
            subscribers = "숨김"
            hidden_subs += 1
        else:
            subscribers = fmt_count(ch_stats, "subscriberCount")

        print(
            f"{rank:>2} {fmt_count(stats, 'viewCount'):>12} "
            f"{fmt_count(stats, 'likeCount'):>10} {subscribers:>12} "
            f"{fmt_duration(sec):>7}  {video['snippet']['title'][:50]}"
        )
        print(f"{'':>48}https://www.youtube.com/watch?v={video_id}")

    in_order = views == sorted(views, reverse=True)
    print(
        f"\n영상 {len(views)}개 · {SHORT_LIMIT_SEC}초 이하 {short_count}개 · "
        f"좋아요 숨김 {hidden_likes}개 · 구독자 숨김 {hidden_subs}개"
    )
    print(f"검색 순서 = 실제 조회수 순서: {'예' if in_order else '아니오'}")
    print("쿼터 사용 추정: 102 유닛 (search 100 + videos 1 + channels 1)")


if __name__ == "__main__":
    main()
