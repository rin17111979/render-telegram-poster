from flask import Flask
import random
import requests
import os

app = Flask(__name__)


def load_posts():
    with open("posts.txt", "r", encoding="utf-8") as f:
        content = f.read().strip()
    return [p.strip() for p in content.split("\n\n") if p.strip()]


@app.route("/post")
def publish_post():
    try:
        posts = load_posts()
        post = random.choice(posts)
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        channel = os.getenv("TELEGRAM_CHANNEL")

        resp = requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data={"chat_id": channel, "text": post, "parse_mode": "HTML"},
        )
        return (
            "✅ Пост опубликован!"
            if resp.status_code == 200
            else f"❌ Телеграм ошибка: {resp.text}"
        )
    except Exception as e:
        return f"❌ Ошибка: {str(e)}"


@app.route("/")
def alive():
    return "✅ Сервис работает. Используй /post для публикации."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
