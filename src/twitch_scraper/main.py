import json
from twitch_scraper.scraper.scraper import TwitchVideoCommentsScraper
from twitch_scraper.scraper.video_list import TwitchVideoList


print("Starting scrapper...")
twitch_comment_scrapper = TwitchVideoCommentsScraper()
video_list = TwitchVideoList()

streamer_login = input("Type the streamer login that should be crawled: ")

videos = video_list.get_video_list(streamer_login)

with open(f"out/{streamer_login}.json", "w") as outfile:
    outfile.write(json.dumps(videos))

for video in videos["videos"]:
    print(f"Scrapping video {video['id']}...")

    comments = twitch_comment_scrapper.get_video_comments(video["id"])

    print("Writing result...")

    with open(f"out/{streamer_login}/{video['id']}.json", "w") as outfile:
        outfile.write(json.dumps(comments))
