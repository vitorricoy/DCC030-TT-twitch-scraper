import requests

headers = {
    "Client-Id": "kimne78kx3ncx6brgo4mv6wki5h1ko",
    "Client-Request-Id": "qnJu83nK35PtcF3BCxEqoZYZ2Wdlep0c",
    "Client-Version": "17740ddf-0c35-482d-ab21-e9b5c986a1a5",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "X-Device-Id": "jNTYYhwQ44uebzdHnCpC9F4DoLUHhR2N",
}

response = requests.post("https://gql.twitch.tv/integrity", headers=headers)

print(response.json())
