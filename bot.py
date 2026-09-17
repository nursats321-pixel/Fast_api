
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Токен бота не найден в .env")


API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_telegram_message(chat_id: int, text: str):
    url = f"{API_URL}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=5
        )

        return response.status_code == 200

    except requests.RequestException as e:
        print(f"Ошибка отправки: {e}")
        return False


def get_updates(offset=None):
    url = f"{API_URL}/getUpdates"

    params = {
        "timeout": 30
    }

    if offset is not None:
        params["offset"] = offset

    try:
        response = requests.get(
            url,
            params=params,
            timeout=35
        )

        return response.json()

    except requests.RequestException as e:
        print(f"Ошибка получения сообщений: {e}")
        return None


def main():
    print("Бот запущен и ожидает сообщения...")

    offset = None

    while True:
        data = get_updates(offset)

        if data is None:
            continue

        if not data.get("ok"):
            print("Ошибка Telegram:", data)
            continue

        for update in data["result"]:
            offset = update["update_id"] + 1

            message = update.get("message")

            if not message:
                continue

            chat_id = message["chat"]["id"]
            text = message.get("text", "")

            print(f"Получено: {text}")

            if text == "/start":
                send_telegram_message(
                    chat_id,
                    "Привет! 👋\nБот работает!"
                )
            else:
                send_telegram_message(
                    chat_id,
                    f"Ты написал: {text}"
                )


if __name__ == "__main__":
    main()