import requests
from app.config import API_URL

def send_message(test):
    payload = {"query : text"}
    r = requests.post(f"{API_URL}/query", json=payload)
    return r.json().get("answer", "Désolé, je n'ai pas pu traiter votre demande.")