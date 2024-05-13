from concurrent.futures import ThreadPoolExecutor
from utils.news_api import fetch_news
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
    GENERAL = "general"
    ENTERTAINMENT = "entertainment"
    SPORTS = "sports"
    SCIENCE = "science"
    TECHNOLOGY = "technology"
    BUSINESS = "business"
    HEALTH = "health"


"""
Only "Source" can be used when specifying "Source".

When specifying "Country", the use of "Source" is not allowed.
When specifying "Category", the use of "Source" is not allowed.

Both "Country" and "Category" can be used at the same time.
"""


def lambda_handler(event, context):
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
            Category.ENTERTAINMENT.value,
        )
        results[Country.CN] = executor.submit(
            fetch_news,
            Country.CN.value,
            Category.ENTERTAINMENT.value,
        )
        results[Country.KR] = executor.submit(
            fetch_news,
            Country.KR.value,
            Category.ENTERTAINMENT.value,
        )
        results[Country.JP] = executor.submit(
            fetch_news,
            Country.JP.value,
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
