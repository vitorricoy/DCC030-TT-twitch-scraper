from genericpath import isfile
import json
import os

from twitch_scraper.scraper.video_list import TwitchVideoList

dirs = os.listdir("out")

video_list = TwitchVideoList()

distinct_ids = set()
total = 0
for dir in dirs:
    if not isfile("out/" + dir):
        files = os.listdir("out/" + dir)
        for file in files:
            if isfile("out/" + dir + "/" + file):
                with open("out/" + dir + "/" + file, "r") as file:
                    data = file.read()
                    json_data = json.loads(data)
                    total += len(json_data)
                    for message in json_data:
                        distinct_ids.add(message["commenter_login"])
all_videos = []

for id in distinct_ids:
    user_videos = video_list.get_video_list(id)
    print(user_videos)
    videos = user_videos["videos"]
    all_videos.append([video["id"] for video in videos])


with open("second_level.json", "w") as outfile:
    outfile.write(json.dumps(all_videos))
