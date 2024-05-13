from newsapi import NewsApiClient

from .summarize import summarize_news_content
import os

api_key = os.environ.get("NEWS_API_KEY")
api = NewsApiClient(api_key=api_key)


def fetch_news(country: str, category: str) -> dict:

    summarized_news = ""
    summarize_text_system_prompt = f"You are a helpful assistant. If you have any important information (schedule, location ..), please keep the information, and summarize any other information. The output language is {country}."
    summarize_title_system_prompt = (
        f"Summarize this text in one sentence please. The output language is {country}."
    )

    idx = 1
    news_num = 5
    result = {}

    while idx <= news_num:
        text = api.get_top_headlines(category=category, country=country)
        cleaned_text = " ".join(text.split())
        print(cleaned_text)
        max_length = 5000
        summarized_title = summarize_news_content(
            cleaned_text, summarize_title_system_prompt, max_length
        )
        summarized_text = summarize_news_content(
            cleaned_text, summarize_text_system_prompt, max_length
        )

        summarized_news += f"{summarized_text}\n"
        idx += 1
        result[idx] = {
            "title": summarized_title,
            "summarized_news": summarized_news,
            "country": country,
            "genre": category,
        }

    return result
