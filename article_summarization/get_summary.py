import os

import openai
from openai import OpenAI


def get_bullet_points(article_text):
    my_prompt = (f"""
            Based on the following text make a tight summary of the main issues 
            concerning this article in the form of bullet point.
            Please recommend four books which the user could use to delve in the topics a bit more.
            This is the article text:  
            {article_text}
    """)

    env_var_name = "OPENAI_API_KEY"
    openai.api_key = os.environ.get(env_var_name)

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a geopolitics expert."},
            {"role": "user", "content": my_prompt}
        ]
    )

    return response.choices[0].message.content.strip()
