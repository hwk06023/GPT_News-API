import math
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


def summarize_news_content(post_content: str, prompt: str, max_length: int) -> str:
    summarized_text = ""
    tmp_li = []
    while len(post_content) > max_length:
        num_parts = math.ceil(len(post_content) / max_length)
        part_length = len(post_content) // num_parts
        for j in range(num_parts):
            start_index = j * part_length
            end_index = start_index + part_length
            content_part = post_content[start_index:end_index]
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": content_part},
                ],
            )
            tmp_li.append(response.choices[0].message.content)
        post_content = " ".join(tmp_li)
        if len(post_content) <= max_length:
            summarized_text = post_content
            break
    else:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": post_content},
            ],
        )
        tmp_li.append(response.choices[0].message.content)
        summarized_text = " ".join(tmp_li)
    return summarized_text
