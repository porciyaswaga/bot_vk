import requests
import time
from config import ACCESS_TOKEN, GROUP_ID, API_VERSION

def send_message(user_id, message):
    requests.get("https://api.vk.com/method/messages.send", params={
        "access_token": ACCESS_TOKEN,
        "user_id": user_id,
        "message": message,
        "random_id": int(time.time() * 1000000),
        "v": API_VERSION
    })

def get_long_poll_server():
    response = requests.get("https://api.vk.com/method/groups.getLongPollServer", params={
        "access_token": ACCESS_TOKEN,
        "group_id": GROUP_ID,
        "v": API_VERSION
    }).json()

    if "error" in response:
        print("Ошибка VK API при получении Long Poll сервера:")
        print(response["error"])
        raise Exception("Не удалось получить Long Poll сервер")

    return response["response"]
