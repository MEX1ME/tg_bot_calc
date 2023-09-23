from flask import Flask, render_template, request, Response
import modul as m


memory = {}


app = Flask(__name__, template_folder="../public_html")


@app.route("/python-bot/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        msg = request.get_json()
        chat_id = None
        callback_data = None
        txt = None

        if "callback_query" in msg:
            chat_id, callback_data = m.tel_parse_buttons(msg)
        elif "message" in msg and "text" in msg["message"]:
            chat_id, txt = m.tel_parse_message(msg)

        if callback_data is not None:
            if len(memory[chat_id]) == 1:
                memory[chat_id].append(callback_data)
            else:
                memory[chat_id][1] = callback_data
            if len(memory[chat_id]) == 2:
                m.answer_on_calc(chat_id, callback_data)

        elif txt is not None:
            if txt == "/start":
                m.tel_send_image(chat_id)
            elif txt == "/go":
                if chat_id in memory:
                    del memory[chat_id]
                m.tel_send_message(
                    chat_id,
                    "Этот бот умеет делать вид, что он калькулятор.\nДля начала отправь мне любое число",
                )

            elif m.is_valid_number(txt):
                if chat_id not in memory:
                    memory[chat_id] = []

                if len(memory[chat_id]) == 1 and callback_data not in [
                    "+",
                    "-",
                    "/",
                    "*",
                ]:
                    m.tel_send_message(chat_id, "Уже есть число в памяти, жми на кнопку")
                else:
                    if len(memory[chat_id]) == 0 or len(memory[chat_id]) == 2:
                        memory[chat_id].append(m.correct_num_for_memory(txt))
                    if len(memory[chat_id]) == 1:
                        m.tel_send_calc(chat_id)

                if len(memory[chat_id]) == 3:
                    result = f"Ответ: {m.calculate(memory[chat_id][0],memory[chat_id][1],memory[chat_id][2])}"
                    m.tel_send_message(chat_id, result)
                    del memory[chat_id]

            else:
                m.tel_send_message(chat_id, "Думаю ты так не думаешь")

        return Response("ok", status=200)
    else:
        return "<h1>Приветствую, странник. Переходи на qmex.ru. Только там Все ответы.</h1>"


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return render_template("home.html")


if __name__ == "__main__":
    app.run(threaded=True)
