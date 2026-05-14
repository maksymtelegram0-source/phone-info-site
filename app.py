from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# загружаем .env
load_dotenv()

# создаём Flask приложение
app = Flask(__name__)

# получаем API ключ
API_KEY = os.getenv("API_KEY")


@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    if request.method == "POST":

        number = request.form.get("number")

        # простая проверка номера
        if len(number) < 8:

            result = {
                "error": "Введите корректный номер"
            }

            return render_template(
                "index.html",
                result=result
            )

        try:

            # API URL
            url = f"https://api.apilayer.com/number_verification/validate?number={number}"

            # headers
            headers = {
                "apikey": API_KEY
            }

            # запрос к API
            response = requests.get(
                url,
                headers=headers
            )

            # если успешно
            if response.status_code == 200:

                result = response.json()

                # если номер невалидный
                if not result.get("valid"):

                    result = {
                        "error": "Номер не найден"
                    }

            else:

                result = {
                    "error": "Ошибка API"
                }

        except:

            result = {
                "error": "Ошибка соединения"
            }

    return render_template(
        "index.html",
        result=result
    )


# запуск сервера
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )