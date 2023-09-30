import requests
import re
import config


TOKEN = config.API_TOKEN


def tel_parse_message(message):  #
    try:
        chat_id = message["message"]["chat"]["id"]
        txt = message["message"]["text"]
        return chat_id, txt
    except:
        return "NO text found-->>"


def tel_parse_buttons(message):  #
    try:
        chat_id = message["callback_query"]["message"]["chat"]["id"]
        response_data = message["callback_query"]["data"]
        return chat_id, response_data
    except:
        return "NO text found-->>"


def tel_send_message(chat_id, text):  #
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    r = requests.post(url, json=payload)
    return r


def tel_send_calc(chat_id):  #
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": "Что сделать с числом?",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {"text": "Прибавить", "callback_data": "+"},
                    {"text": "Вычесть", "callback_data": "-"},
                ],
                [
                    {"text": "Умножить", "callback_data": "*"},
                    {"text": "Разделить", "callback_data": "/"},
                ],
                [
                    {"text": "В степень", "callback_data": "**"},
                    {"text": "Корень степени", "callback_data": "x ** (1/y)"},
                ],
            ]
        },
    }
    r = requests.post(url, json=payload)
    return r


def is_valid_number(num):  #
    pattern = r"^-?\d+([\.,]\d+)?$"
    return re.match(pattern, num) is not None


def correct_num_for_memory(num):  #
    if "," in num:
        num = num.replace(",", ".")
    num = float(num)
    return num


def answer_on_calc(chat_id, callback_data):  #
    if callback_data == "+":
        tel_send_message(chat_id, "Сколько прибавить?")
    if callback_data == "-":
        tel_send_message(chat_id, "Сколько вычесть?")
    if callback_data == "*":
        tel_send_message(chat_id, "На сколько умножить?")
    if callback_data == "/":
        tel_send_message(chat_id, "На сколько разделить?")
    if callback_data == "**":
        tel_send_message(chat_id, "В какую степень возвести?")
    if callback_data == "x ** (1/y)":
        tel_send_message(chat_id, "Корень какой степени извлечь?")


def calculate(num1, sym, num2):  #
    if sym == "+":
        return (
            str(num1 + num2).rstrip("0").rstrip(".")
            if num1 + num2 % 1
            else str(int(num1 + num2))
        )
    if sym == "-":
        return (
            str(num1 - num2).rstrip("0").rstrip(".")
            if num1 - num2 % 1
            else str(int(num1 - num2))
        )
    if sym == "*":
        return (
            str(num1 * num2).rstrip("0").rstrip(".")
            if num1 * num2 % 1
            else str(int(num1 * num2))
        )
    if sym == "/":
        return (
            str(num1 / num2).rstrip("0").rstrip(".")
            if num1 / num2 % 1
            else str(int(num1 / num2))
        )
    if sym == "**":
        return (
            str(num1**num2).rstrip("0").rstrip(".")
            if num1**num2 % 1
            else str(int(num1**num2))
        )
    if sym == "x ** (1/y)":
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


# ###
# def tel_parse_keyboard(message):
#     try:
#         callback_query = message['callback_query']
#         chat_id = callback_query['message']['chat']['id']
#         data = callback_query['data']
#         message_id = callback_query['message']['message_id']
#         return chat_id, callback_query, data, message_id
#     except:
#         return "NO text found-->>"
# ###


# ###
# def send_keyboard(chat_id, text, reply_markup=None):
#     url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
#     payload = {
#         "chat_id": chat_id,
#         "text": text,
#         "reply_markup": {
#             "keyboard": [
#                 [
#                     {"text": "Кнопка 1", "callback_data": "+"},
#                     {"text": "Кнопка 2", "callback_data": "button2"},
#                 ]
#             ],
#             "one_time_keyboard": True,
#             "resize_keyboard": True,
#         },
#     }
#     r = requests.post(url, json=payload)
#     return r
# ###