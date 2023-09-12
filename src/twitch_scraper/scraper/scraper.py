import json
from typing import Any
from twitch_scraper.scraper.headers import twitch_base_headers

import requests

from twitch_scraper.integrity.token import TokenManager


class TwitchVideoCommentsScraper:
    def __init__(self):
        self.url = "https://gql.twitch.tv/gql"
        self.token_manager = TokenManager()

    def _get_headers(self, video_id: str):
        return self.token_manager.get_token(
            f"https://www.twitch.tv/videos/{video_id}",
            "VideoCommentsByOffsetOrCursor",
        )

    def _refresh_headers(self, video_id: str):
        return self.token_manager.refresh_token(
            f"https://www.twitch.tv/videos/{video_id}",
            "VideoCommentsByOffsetOrCursor",
        )

    def _make_request(self, headers: dict[str, Any], data: dict[str, Any]):
        resp = requests.post(self.url, headers=headers, data=data)
        return resp.status_code, resp.text

    def _build_data(self, cursor: str | None, video_id: str):
        cursor_portion = (
            f"""
                "cursor":"{cursor}"
            """
            if cursor
            else ""
        )
        offset_portion = (
            """
            "contentOffsetSeconds": 0
        """
            if not cursor
            else ""
        )
        return json.dumps(
            json.loads(
                f"""
            [
                {{
                    "operationName": "VideoCommentsByOffsetOrCursor",
                    "variables": {{
                        "videoID":"{video_id}",
                        {cursor_portion}{offset_portion}
                    }},
                    "extensions": {{
                        "persistedQuery": {{
                            "version": 1,
                            "sha256Hash":"b70a3591ff0f4e0313d126c6a1502d79a1c02baebb288227c582044aa76adf6a"
                        }}
                    }}
                }}
            ]
        """
            ),
            separators=(",", ":"),
        )

    def get_video_comments(self, video_id: str):
        next_cursor = None

        comments_res = []

        cont = 0

        while True:
            cont += 1
            data = self._build_data(next_cursor, video_id)

            print(
                f"Requesting page {cont} ({len(comments_res)} comments collected until now)..."
            )

            status, body = self._make_request(
                {
                    **twitch_base_headers,
                    **self._get_headers(video_id),
                },
                data,
            )

            if status != 200:
                print(f"Collected page {cont} with status {status}")
                print(body)
                break

            if "failed integrity check" in body:
                self._refresh_headers(video_id)
                status, body = self._make_request(
                    {
                        **twitch_base_headers,
                        **self._get_headers(video_id),
                    },
                    data,
                )

            try:
                response = json.loads(body)
                comments = response[0]["data"]["video"]["comments"]

                comments_res.extend(
                    [
                        {
                            "id": comment["node"]["id"],
                            "commenter_login": comment["node"]["commenter"][
                                "login"
                            ]
                            if comment["node"]["commenter"]
                            else None,
                            "content_offset": comment["node"][
                                "contentOffsetSeconds"
                            ],
                            "created_at": comment["node"]["createdAt"],
                            "message": " ".join(
                                [
                                    fragment["text"]
                                    for fragment in comment["node"]["message"][
                                        "fragments"
                                    ]
                                ]
                            ),
                        }
                        for comment in comments["edges"]
                    ]
                )

                if not comments["pageInfo"]["hasNextPage"]:
                    break

                next_cursor = comments["edges"][0]["cursor"]
            except Exception as e:
                print(body)
                raise e

        return comments_res
