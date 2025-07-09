import time
import requests
from utils.vk_api import send_message, get_long_poll_server
from handlers.faq_handler import load_faq, get_faq_answer
from handlers.profanity import contains_bad_words
from handlers.gpt_handler import ask_yandex_gpt

def run_bot():
    faq_data = load_faq()
    server_data = get_long_poll_server()
    ts = server_data["ts"]
    key = server_data["key"]
    server = server_data["server"]

    print("Бот запущен...")

    while True:
        try:
            response = requests.get(f"{server}", params={
                "act": "a_check",
                "key": key,
                "ts": ts,
                "wait": 25
            }, timeout=30).json()

            if "updates" not in response:
                print("Обновление long poll сервера...")
                server_data = get_long_poll_server()
                ts = server_data["ts"]
                key = server_data["key"]
                server = server_data["server"]
                continue

            ts = response["ts"]

            for update in response["updates"]:
                if update["type"] == "message_new":
                    msg = update["object"]["message"]
                    user_id = msg["from_id"]
                    text = msg["text"]

                    print(f"[{user_id}] > {text}")

                    if text.lower().strip() in ["привет", "начать", "старт", "здравствуйте", "здравствуй", "hello", "hi"]:
                        send_message(
                            user_id,
                            "Привет! Я могу помочь с вопросами о VK Education Projects или ответить на любые другие интересующую тебя вопросы."
                        )
                        continue

                    if contains_bad_words(text):
                        send_message(user_id, "Пожалуйста, не используйте нецензурную лексику.")
                        continue

                    answer = get_faq_answer(text, faq_data)
                    if answer:
                        send_message(user_id, answer)
                        continue

                    gpt_reply = ask_yandex_gpt(text)
                    if gpt_reply:
                        send_message(user_id, gpt_reply)
                    else:
                        send_message(user_id, "Извините, не удалось получить ответ. Попробуйте позже.")

        except Exception as e:
            print("Ошибка:", e)
            time.sleep(2)

if __name__ == "__main__":
    run_bot()
