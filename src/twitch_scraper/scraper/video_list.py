from typing import Any
import requests
import json


class TwitchVideoList:
    def __init__(self):
        self.url = "https://gql.twitch.tv/gql"

    def _get_headers(self):
        return {
            "Client-ID": "kimne78kx3ncx6brgo4mv6wki5h1ko",
            "Content-Type": "application/json",
        }

    def _make_request(self, data: dict[str, Any]):
        resp = requests.post(self.url, headers=self._get_headers(), data=data)
        return resp.status_code, resp.text

    def _build_data(self, streamer_login: str):
        return (
            '{"query":"query { \\n  user(login: \\"'
            + streamer_login
            + '\\") {\\n    login\\n    videos(sort: TIME, options: {minLengthSeconds: 1200}) {\\n      edges {\\n        node {\\n          id\\n          title\\n          viewCount\\n          createdAt\\n          lengthSeconds\\n          broadcastType\\n        }\\n      }\\n    }\\n  }\\n}","variables":{}}'
        )

    def get_video_list(self, streamer_login: str):
        data = self._build_data(streamer_login)

        print(f"Requesting videos of streamer {streamer_login}...")

        status, body = self._make_request(
            data,
        )

        if status != 200:
            print(f"Collected videos with status {status}")
            print(body)
            return []

        try:
            response = json.loads(body)
            return {
                "login": streamer_login,
                "videos": [
                    {
                        "id": video["node"]["id"],
                        "title": video["node"]["title"],
                        "views": video["node"]["viewCount"],
                        "created_at": video["node"]["createdAt"],
                        "length": video["node"]["lengthSeconds"],
                        "type": video["node"]["broadcastType"],
                    }
                    for video in response["data"]["user"]["videos"]["edges"]
                ],
            }
        except Exception as e:
            print(body)
            raise e
