import yfinance as yf
import csv
from world_model_test import Portfolio
from notopenai import NotOpenAI

CLIENT = NotOpenAI(api_key="e0e0c8e6-de84-4f8e-b407-9d408e470f0d")


chat_completion = CLIENT.chat.completions.create(
    messages=[{"role": "user", "content": "Say hello in json"}],
    model="gpt-3.5-turbo",
    response_format={"type": "json_object"}
)
print(chat_completion.choices[0].message.content)