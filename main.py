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
    split_link = urlsplit(short_url['shorturl'])
    short_link = split_link.netloc+split_link.path
    full_short_link = short_url['shorturl']

    return short_link, full_short_link


def get_count_clicks(token, link):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(
        url=f'https://clc.li/api/urls?short={link}',
        headers=headers,
        )
    
    response.raise_for_status()    

    links_data = response.json()
    clicks_count = links_data['data']['clicks']
  
    # print(json.dumps(links_data, indent=4, ensure_ascii=False))

    return clicks_count


def main():
    load_dotenv()
    token = os.getenv('API_CLC_LI')
    user_input = input("Введите ссылку: ").strip()
    if not token:
       print("ОШИБКА: Не найден токен в переменных окружения!")
       return   
    if 'clc.li' in user_input:
        try:
            clicks_count = get_count_clicks(token, user_input)
            print('Количество кликов ', clicks_count)  
        except requests.exceptions.HTTPError:
            print("ОШИБКА: Проблема при подсчете!")
        return
  
    if not user_input.startswith(('http://', 'https://')):
        user_input = 'https://' + user_input
    try:
        response = requests.get(user_input, timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        print("Ошибка: Ссылка не работает или недоступна!")
        return


    try:
        short_link, full_short_link = shorten_link(token, user_input)
        print('Короткая ссылка ', short_link)
    except requests.exceptions.HTTPError:
        print("ОШИБКА: Проблема при обращении к API!")
        return

    # print('Полная короткая ссылка ', full_short_link)


if __name__ == "__main__":
    main()
