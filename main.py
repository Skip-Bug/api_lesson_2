import requests
import os
import json
from dotenv import load_dotenv
from urllib.parse import urlsplit



def shorten_link(token, url):
    link_request = input("Введите ссылку для сокращения:")

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    body = {
        "url": link_request
    }
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    short_url = response.json()
    split_link = urlsplit(short_url['shorturl'])

    return (split_link.netloc+split_link.path)


def main():
    load_dotenv()
    url = 'https://clc.li/api/url/add'
    token = os.getenv('API_CLC_LI')
    if not token:
        print("ОШИБКА: Не найден токен в переменных окружения!")
        return
    
    print('Короткая ссылка', shorten_link(token, url))
    # print(json.dumps(short_url, indent=4, ensure_ascii=False))
    # print(response)
    # print(response.text)

if __name__ == "__main__":
    main()
