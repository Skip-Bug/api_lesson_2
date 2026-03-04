import requests
import os
import json
from dotenv import load_dotenv



def get_my_account(headers):
    # url = 'https://clc.li/api/account'
    url = 'https://clc.li/api/account'
    response = requests.get(url, headers=headers)
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
    response = get_my_account(headers)
    account_data = response.json()
    print(json.dumps(account_data, indent=4, ensure_ascii=False))
    print(response)
    print(response.text)
if __name__ == "__main__":
    main()
