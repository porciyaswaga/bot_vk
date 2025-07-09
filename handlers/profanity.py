def contains_bad_words(text, blacklist_file='data/blacklist.txt'):
    try:
        with open(blacklist_file, encoding='utf-8') as f:
            bad_words = [line.strip() for line in f if line.strip()]
        for word in bad_words:
            if word.lower() in text.lower():
                return True
    except FileNotFoundError:
        pass
    return False
