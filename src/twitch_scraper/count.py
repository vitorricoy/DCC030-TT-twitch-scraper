from genericpath import isfile
import json
import os

dirs = os.listdir("out")

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

print(len(distinct_ids))
print(total)
