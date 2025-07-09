import requests
from config import YANDEX_API_KEY, YANDEX_FOLDER_ID


def is_relevant_to_vk_education(question: str) -> bool:
    """
    Использует GPT, чтобы определить, относится ли вопрос к VK Education Projects.
    """
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Authorization": f"Api-Key {YANDEX_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "modelUri": f"gpt://{YANDEX_FOLDER_ID}/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.3,
            "maxTokens": 20
        },
        "messages": [
            {
                "role": "system",
                "text": (
                    "Ты фильтр. Твоя задача — определить, относится ли вопрос к теме VK Education Projects. "
                    "Отвечай только 'Да' или 'Нет'."
                )
            },
            {"role": "user", "text": question}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        reply = response.json()["result"]["alternatives"][0]["message"]["text"].lower()
        return "да" in reply
    except Exception as e:
        print("Ошибка при проверке релевантности GPT:", e)
        return False


def ask_yandex_gpt(user_question: str) -> str:
    """
    Отправляет вопрос в YandexGPT с разной системой сообщений в зависимости от тематики.
    """
    is_relevant = is_relevant_to_vk_education(user_question)

    if is_relevant:
        system_prompt = (
            "Ты помощник, который отвечает только на вопросы, связанные с VK Education Projects. "
            "Отвечай кратко и по делу. Если вопрос не относится к VK Education, скажи, что можешь помочь только по этой теме."
        )
    else:
        system_prompt = (
            "Ты универсальный помощник. Отвечай понятно, точно и по существу. "
            "Если вопрос слишком общий или неясен, попроси переформулировать."
        )

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Authorization": f"Api-Key {YANDEX_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "modelUri": f"gpt://{YANDEX_FOLDER_ID}/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.5,
            "maxTokens": 700
        },
        "messages": [
            {
                "role": "system",
                "text": system_prompt
            },
            {
                "role": "user",
                "text": user_question
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["result"]["alternatives"][0]["message"]["text"].strip()
    except Exception as e:
        print("Ошибка при обращении к GPT:", e)
        return "Извините, не удалось получить ответ от GPT."
