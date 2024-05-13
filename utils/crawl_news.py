from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from .summarize import summarize_news_content
import time


def setup_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("user-agent=Mozilla/5.0 ~~ .")
    driver = webdriver.Chrome(service=Service(), options=options)
    return driver


def fetch_news(country: str, url, category: str) -> dict:
    driver = setup_driver()
    summarized_news = ""
    summarize_text_system_prompt = f"You are a helpful assistant. If you have any important information (schedule, location ..), please keep the information, and summarize any other information. The output language is {country}."
    summarize_title_system_prompt = (
        f"Summarize this text in one sentence please. The output language is {country}."
    )

    idx = 1
    try_count = 0
    max_try = 5
    news_num = 5
    result = {}

    while idx <= news_num:
        link_tag = None
        driver.get(url)
        time.sleep(7)
        print(f"Fetching {country} {idx}th link")
        crawling_success = False
        try:
            link_tag = driver.find_element(
                By.XPATH,
                f'//*[@id="i10-panel"]/c-wiz/c-wiz[{idx}]/c-wiz/div/article/a',
            )
            crawling_success = True
        except:
            link_tag = driver.find_element(
                By.XPATH,
                f'//*[@id="i10-panel"]/c-wiz/c-wiz[{idx}]/c-wiz/article/div[1]/div[2]/div/a',
            )
            crawling_success = True
        finally:
            if crawling_success == False:
                if try_count < max_try:
                    try_count += 1
                    continue
                else:
                    print(f"Failed to crawl {country} {idx}th link. (Doesn't exist)")
                    break
        if link_tag:
            link_url = link_tag.get_attribute("href")
            driver.get(link_url)
            time.sleep(10)
            text = driver.find_element(By.TAG_NAME, "body").text
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
                "url": url,
                "title": summarized_title,
                "summarized_news": summarized_news,
                "country": country,
                "category": category,
            }

    driver.quit()
    return result
