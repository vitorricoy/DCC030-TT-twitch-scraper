Steps to run:

1. Install poetry
2. Install selenium driver
3. Install certificates to run scrapper (ca.crt file).
4. Run command
```sh
poetry install
poetry run src/twitch_scraper/main.py
```
5. Fill `USER_DATA_DIR` and `BINARY_LOCATION` variables in [`token.py`](src/twitch_scraper/integrity/token.py)