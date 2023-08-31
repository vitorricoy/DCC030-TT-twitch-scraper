from time import sleep
from typing import Any
from seleniumwire.undetected_chromedriver.v2 import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args, **kwargs
            )
        return cls._instances[cls]


class TokenManager(metaclass=Singleton):
    _headers: dict[str, Any] = {}

    def _fetch_token_from_url_and_action(self, url: str, action: str):
        print("Scrapping token from twitch page in Chrome...")
        options = ChromeOptions()
        options.add_argument(
            "--user-data-dir=/home/vitorricoy/.config/google-chrome/Profile 3"
        )
        options.add_argument("--allow-running-insecure-content")
        # options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.binary_location = "/opt/google/chrome"
        options.add_argument(
            f"--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
        driver = Chrome(chrome_options=options)
        driver.get(url)
        # Wait for ad
        sleep(50)
        # Advance video
        cont = 0
        while cont < 10:
            for i in range(20):
                driver.find_element(
                    By.CSS_SELECTOR,
                    "html",
                ).send_keys(Keys.ARROW_RIGHT)
                sleep(1)
            sleep(30)
            requests = driver.requests.copy()
            requests.reverse()
            for request in requests:
                try:
                    if (
                        action in request.body.decode("utf-8")
                        and "Client-Integrity" in request.headers
                    ):
                        print(f"Got headers: {self._headers}")
                        driver.quit()
                        return {**request.headers}
                except:
                    pass
            cont += 1
        print("Tried a lot to get token but could not get it")
        raise Exception()
        driver.quit()
        return {}

    def get_token(self, url: str, action: str):
        if self._headers == {}:
            self._headers = self._fetch_token_from_url_and_action(url, action)
        return self._headers

    def refresh_token(self, url: str, action: str):
        self._headers = self._fetch_token_from_url_and_action(url, action)
        return self._headers
