import requests
import os
import json
from dotenv import load_dotenv



def get_short_url(headers):
    url = 'https://clc.li/api/url/add'
    link_request = input("Введите ссылку для сокращения:")
    
    body = {
        "url": link_request
    }
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response


def main():
    load_dotenv()
    api_clc_li = os.getenv('API_CLC_LI')
    if not api_clc_li:
        print("ОШИБКА: Не найден токен в переменных окружения!")
        return
    
    headers = {
        'Authorization': f'Bearer {api_clc_li}',
        'Content-Type': 'application/json'
    }
    response = get_short_url(headers)
    short_url = response.json()
    
    print("\nВот ваша ссылка:", short_url['shorturl'])
    # print(json.dumps(short_url, indent=4, ensure_ascii=False))
    # print(response)
    # print(response.text)

if __name__ == "__main__":
    main()
