import json
import requests
from requests.structures import CaseInsensitiveDict

url = "https://gql.twitch.tv/gql"

headers = CaseInsensitiveDict()
headers["Accept"] = "*/*"
headers["Accept-Language"] = "pt-BR"
headers["Client-Id"] = "kimne78kx3ncx6brgo4mv6wki5h1ko"
headers[
    "Client-Integrity"
] = "v4.public.eyJjbGllbnRfaWQiOiJraW1uZTc4a3gzbmN4NmJyZ280bXY2d2tpNWgxa28iLCJjbGllbnRfaXAiOiIxNzkuMjIxLjE2OC4yMDYiLCJkZXZpY2VfaWQiOiJIZHoxSWZoUGtDYWhyOGRSb3cxdUY5bGUxbzFnbTVCdiIsImV4cCI6IjIwMjMtMDgtMzBUMTc6NTg6MzhaIiwiaWF0IjoiMjAyMy0wOC0zMFQwMTo1ODozOFoiLCJpc19iYWRfYm90IjoiZmFsc2UiLCJpc3MiOiJUd2l0Y2ggQ2xpZW50IEludGVncml0eSIsIm5iZiI6IjIwMjMtMDgtMzBUMDE6NTg6MzhaIiwidXNlcl9pZCI6IiJ9uYTpQd_dzfcxiAxgwGa8Wf0ifQ76zG9V2gqanuMZ38jSUK52p6fRoBI2pfF-xvv-bHDxFFMKwgBj9rLJx6WXDw"
headers["Client-Session-Id"] = "2b1189abfcc34d4e"
headers["Client-Version"] = "4cfa60e5-23fe-412a-8675-e944bca3981f"
headers["Connection"] = "keep-alive"
headers["Content-Type"] = "text/plain;charset=UTF-8"
headers["Origin"] = "https://www.twitch.tv"
headers["Referer"] = "https://www.twitch.tv/"
headers["Sec-Fetch-Dest"] = "empty"
headers["Sec-Fetch-Mode"] = "cors"
headers["Sec-Fetch-Site"] = "same-site"
headers[
    "User-Agent"
] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
headers["X-Device-Id"] = "Hdz1IfhPkCahr8dRow1uF9le1o1gm5Bv"
headers[
    "sec-ch-ua"
] = '''"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"'''
headers["sec-ch-ua-mobile"] = "?0"
headers["sec-ch-ua-platform"] = '''"Linux"'''

next_cursor = None

comments_res = []

while True:
    cursor_portion = (
        f"""
        "cursor":"{next_cursor}"
    """
        if next_cursor
        else ""
    )
    offset_portion = (
        """
        "contentOffsetSeconds": 0
    """
        if not next_cursor
        else ""
    )
    data = json.dumps(
        json.loads(
            f"""
        [
            {{
                "operationName": "VideoCommentsByOffsetOrCursor",
                "variables": {{
                    "videoID":"1911945600",
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

    resp = requests.post(url, headers=headers, data=data)

    print(resp.status_code)
    print(comments_res)

    if resp.status_code != 200:
        print(resp.json())
        break
    response = resp.json()
    comments = response[0]["data"]["video"]["comments"]

    comments_res.extend([comment["node"] for comment in comments["edges"]])

    if not comments["pageInfo"]["hasNextPage"]:
        break

    next_cursor = comments["edges"][0]["cursor"]

print(comments_res)
