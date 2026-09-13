import os

def load_cookies(auth_input):
    if os.path.isfile(auth_input):
        with open(auth_input, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return auth_input
