import json
from twitch_scraper.scraper.scraper import TwitchVideoCommentsScraper


print("Starting scrapper...")
twitch_comment_scrapper = TwitchVideoCommentsScraper()

print("Scrapping video 1910960172...")

comments = twitch_comment_scrapper.get_video_comments("1910960172")

print("Writing result...")

with open("1910960172.json", "w") as outfile:
    outfile.write(json.dumps(comments))
