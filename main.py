from urllib.parse import urlsplit
from dotenv import load_dotenv
import requests
import os


def shorten_link(token, link):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    body = {
        "url": link
    }

    response = requests.post(
        'https://clc.li/api/url/add',
        headers=headers,
        json=body
        )
    response.raise_for_status()
    short_url = response.json()
    full_short_link = short_url['shorturl']
    return full_short_link


def get_count_clicks(token, link):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(
        url=f'https://clc.li/api/urls?short={link}',
        headers=headers
        )

    response.raise_for_status()
    link_stats = response.json()
    return link_stats
    if 'data' in link_stats:
        return link_stats['data'].get('clicks', 0)

    if 'error' in link_stats:
        error = link_stats.get('message', 'Неизвестная ошибка')
        print(f"API вернул ошибку: {error}")
        return 0

    return 0


def is_shorten_link(link):
    return 'clc.li' in link


def main():
    load_dotenv()
    token = os.getenv('CLC_LI_TOKEN_TO_API')
    user_input = input("Введите ссылку: ").strip()

    if not token:
        print("ОШИБКА: Не найден токен в переменных окружения!")
        return

    if not user_input.startswith(('http://', 'https://')):
        user_input = f'https://{user_input}'
    
    if is_shorten_link(user_input):
        try:
            link_stats = get_count_clicks(token, user_input)
            
            if 'data' in link_stats:
                clicks_count = link_stats['data'].get('clicks', 0)
                print('Количество кликов ', clicks_count)
            elif 'error' in link_stats:
                error = link_stats.get('message', 'Неизвестная ошибка')
                print(f"API вернул ошибку: {error}")
            else:
                print("Не удалось получить статистику")
                
        except requests.exceptions.HTTPError:
            print("Ошибка соединения с API!")
        return

    try:
        response = requests.get(user_input, timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        print("Ошибка: Ссылка не работает или недоступна!")
        return

    try:
        full_short_link = shorten_link(token, user_input)
        print('Короткая ссылка ', full_short_link)
    except requests.exceptions.HTTPError:
        print("ОШИБКА: Проблема при обращении к API!")
        return


if __name__ == "__main__":
    main()
