import logging
import os
from pathlib import Path

import requests

from scripts.python.config import BASE_URL, CACHE_DIR, DEFAULT_CACHE

logger = logging.getLogger(__name__)

# Auto generated user agent from https://iplogger.org/useragents/
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_4) AppleWebKit/537.44 (KHTML, like Gecko) Chrome/51.0.1965.123 Safari/534"
}


def send_and_cache_request(url: str, should_cache=DEFAULT_CACHE):
    if should_cache:
        file_name = (url.replace(BASE_URL, "").replace("/", "_"))[1:] + ".html"

        Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)
        file_path = Path(CACHE_DIR, file_name)
        if os.path.exists(file_path):
            logger.info(f"Reading from cache {file_name}")
            with open(file_path, "r") as f:
                return f.read()
        else:
            response = send_request(url)
            with open(file_path, "w") as f:
                f.write(response.text)
                return response.text

    else:
        return send_request(url).text


def send_request(url: str):
    logger.info(f"Sending request to {url}")
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"Failed to get {url}")
    return response
