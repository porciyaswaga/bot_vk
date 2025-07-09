import json
from rapidfuzz import fuzz
from config import FUZZY_THRESHOLD

def load_faq(filepath='data/faq.json'):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_faq_answer(user_input: str, faq_data: list) -> str | None:
    user_input = user_input.lower().strip()

    if len(user_input) < 4:
        return None

    for item in faq_data:
        for phrase in item["questions"]:
            if phrase in user_input:
                return item["answer"]

    best_score = 0
    best_answer = None

    for item in faq_data:
        for phrase in item["questions"]:
            score = fuzz.partial_ratio(user_input, phrase)
            if score > best_score:
                best_score = score
                best_answer = item["answer"]

    if best_score >= FUZZY_THRESHOLD:
        return best_answer

    return None
