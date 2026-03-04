import requests
import os
import json
from dotenv import load_dotenv
from urllib.parse import urlsplit



def shorten_link(token, user_input):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    body = {
        "url": user_input
    }

    response = requests.post(
        'https://clc.li/api/url/add',
        headers=headers,
        json=body
        )
    response.raise_for_status()
    short_url = response.json()
    split_link = urlsplit(short_url['shorturl'])
    short_link = split_link.netloc+split_link.path

    return short_link

def main():
    load_dotenv()
    user_input = input("Введите ссылку для сокращения: ").strip()
    if not user_input.startswith(('http://', 'https://')):
        user_input = 'https://' + user_input
    try:
        response = requests.get(user_input, timeout=5)
        response.raise_for_status()
    except:
        print("Ошибка: Ссылка не работает или недоступна!")
        return

    token = os.getenv('API_CLC_LI')
    if not token:
        print("ОШИБКА: Не найден токен в переменных окружения!")
        return
    try:
        short_link = shorten_link(token, user_input)
    except requests.exceptions.HTTPError:
        print("ОШИБКА: Не правильно ввели ссылку!")
        return

    print('Короткая ссылка', short_link)
    # print(json.dumps(short_url, indent=4, ensure_ascii=False))
    # print(response)
    # print(response.text)

if __name__ == "__main__":
    main()
