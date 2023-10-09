import requests
import re
import config


TOKEN = config.API_TOKEN


def tel_parse_message(message):
    try:
        chat_id = message["message"]["chat"]["id"]
        txt = message["message"]["text"]
        return chat_id, txt
    except:
        return "NO text found-->>"


def tel_send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    r = requests.post(url, json=payload)
    return r


def answer_calculate_and_hide_keyboard(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": {"remove_keyboard": True}
    }
    response = requests.post(url, json=payload)
    return response.json()


def is_valid_number(num):
    pattern = r"^-?\d+([\.,]\d+)?$"
    return re.match(pattern, num) is not None


def correct_num_for_memory(num):
    if "," in num:
        num = num.replace(",", ".")
    num = float(num)
    return num


def answer_on_calc(chat_id, txt):
    if txt == "Прибавить":
        tel_send_message(chat_id, "Сколько прибавить?")
    if txt == "Вычесть":
        tel_send_message(chat_id, "Сколько вычесть?")
    if txt == "Умножить":
        tel_send_message(chat_id, "На сколько умножить?")
    if txt == "Разделить":
        tel_send_message(chat_id, "На сколько разделить?")
    if txt == "В степень":
        tel_send_message(chat_id, "В какую степень возвести?")
    if txt == "Корень степени":
        tel_send_message(chat_id, "Корень какой степени извлечь?")


def calculate(num1, sym, num2):
    if sym == "Прибавить":
        return (
            str(num1 + num2).rstrip("0").rstrip(".")
            if num1 + num2 % 1
            else str(int(num1 + num2))
        )
    if sym == "Вычесть":
        return (
            str(num1 - num2).rstrip("0").rstrip(".")
            if num1 - num2 % 1
            else str(int(num1 - num2))
        )
    if sym == "Умножить":
        return (
            str(num1 * num2).rstrip("0").rstrip(".")
            if num1 * num2 % 1
            else str(int(num1 * num2))
        )
    if sym == "Разделить":
        return (
            str(num1 / num2).rstrip("0").rstrip(".")
            if num1 / num2 % 1
            else str(int(num1 / num2))
        )
    if sym == "В степень":
        return (
            str(num1**num2).rstrip("0").rstrip(".")
            if num1**num2 % 1
            else str(int(num1**num2))
        )
    if sym == "Корень степени":
        return (
            str(num1 ** (1 / num2)).rstrip("0").rstrip(".")
            if num1 ** (1 / num2) % 1
            else str(int(num1 ** (1 / num2)))
        )


def tel_send_image(chat_id):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    payload = {
        "chat_id": chat_id,
        "photo": "https://qmex.ru/image/catalog/mexlogo.png",
        "caption": "Тех Мех корпорейшен продакшен.\nСайт автора qmex.ru, там все ответы.\nЖми /go для продолжения.",
    }
    r = requests.post(url, json=payload)
    return r

    
def tel_send_calculator(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": {
            "keyboard": [
                [
                    {"text": "Прибавить"},
                    {"text": "Вычесть"},
                ],
                [
                    {"text": "Умножить"},
                    {"text": "Разделить"},
                ],
                [
                    {"text": "В степень"},
                    {"text": "Корень степени"},
                ],
                [
                    {"text": "Стереть"},
                ],
            ],
            "one_time_keyboard": True,
            "resize_keyboard": True,
            "remove_keyboard": True
        },
    }
    r = requests.post(url, json=payload)
    return r

