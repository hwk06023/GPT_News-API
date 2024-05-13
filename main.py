from concurrent.futures import ThreadPoolExecutor
from utils.crawl_news import fetch_news
from enum import Enum
import json
import requests
import os


class Country(Enum):
    US = "us"
    CN = "cn"
    KR = "kr"
    JP = "jp"


class Category(Enum):
    ENTERTAINMENT = "Entertainment"
    SPORTS = "Sports"
    SCIENCE_TECHNOLOGY = "Science/Technology"
    BUSINESS = "Business"
    HEALTH = "Health"


def lambda_handler(event, context):
    genre_url_dict = {
        Category.ENTERTAINMENT: "CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FtdHZHZ0pMVWlnQVAB?hl=",
        Category.SPORTS: "CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtdHZHZ0pMVWlnQVAB?hl=",
        Category.SCIENCE_TECHNOLOGY: "CAAqKAgKIiJDQkFTRXdvSkwyMHZNR1ptZHpWbUVnSnJieG9DUzFJb0FBUAE?hl=",
        Category.BUSINESS: "CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtdHZHZ0pMVWlnQVAB?hl=",
        Category.HEALTH: "CAAqIQgKIhtDQkFTRGdvSUwyMHZNR3QwTlRFU0FtdHZLQUFQAQ?hl=",
    }
    common_url = "https://news.google.com/topics/"
    urls = {
        Country.US: common_url
        + genre_url_dict[Category.ENTERTAINMENT]
        + "en-US&gl=US&ceid=US%3Aen",
        Country.CN: common_url
        + genre_url_dict[Category.ENTERTAINMENT]
        + "zh-CN&gl=CN&ceid=CN%3Azh-Hans",
        Country.KR: common_url
        + genre_url_dict[Category.ENTERTAINMENT]
        + "ko-KR&gl=KR&ceid=KR%3Ako",
        Country.JP: common_url
        + genre_url_dict[Category.ENTERTAINMENT]
        + "ja&gl=JP&ceid=JP%3Aja",
    }
    results = {
        Country.US: dict(),
        Country.CN: dict(),
        Country.KR: dict(),
        Country.JP: dict(),
    }

    with ThreadPoolExecutor(max_workers=4) as executor:
        results[Country.US] = executor.submit(
            fetch_news,
            Country.US.value,
            urls[Country.US],
            Category.ENTERTAINMENT.value,
        )
        results[Country.CN] = executor.submit(
            fetch_news,
            Country.CN.value,
            urls[Country.CN],
            Category.ENTERTAINMENT.value,
        )
        results[Country.KR] = executor.submit(
            fetch_news,
            Country.KR.value,
            urls[Country.KR],
            Category.ENTERTAINMENT.value,
        )
        results[Country.JP] = executor.submit(
            fetch_news,
            Country.JP.value,
            urls[Country.JP],
            Category.ENTERTAINMENT.value,
        )

    endpoint = os.getenv("TARGET_ENDPOINT_DEV")

    payload = {
        Country.US.value: results[Country.US].result(),
        Country.CN.value: results[Country.CN].result(),
        Country.KR.value: results[Country.KR].result(),
        Country.JP.value: results[Country.JP].result(),
    }
    payload_json = json.dumps(payload)

    print(payload_json)

    response = requests.post(endpoint, json=payload_json)

    response_json = response.json()

    return response_json


lambda_handler(None, None)
