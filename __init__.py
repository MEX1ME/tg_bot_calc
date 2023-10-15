from flask import Flask, render_template, request, Response
import modul as m


memory = {}


app = Flask(__name__, template_folder="../public_html")


@app.route("/python-bot/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        msg = request.get_json()
        chat_id = None
        txt = None

        if "message" in msg and "text" in msg["message"]:
            chat_id, txt = m.tel_parse_message(msg)

        if txt is not None:
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

                if len(memory[chat_id]) == 1:
                    m.tel_send_calculator(chat_id, "Уже есть число в памяти. Что сделать с числом?")
                else:
                    if len(memory[chat_id]) == 0 or len(memory[chat_id]) == 2:
                        memory[chat_id].append(m.correct_num_for_memory(txt))
                    if len(memory[chat_id]) == 1:
                        m.tel_send_calculator(chat_id, "Что сделать с числом?")

                if len(memory[chat_id]) == 3:
                    if memory[chat_id][1] == "Разделить" and memory[chat_id][2] == 0:
                        del memory[chat_id]
                        m.tel_send_message(chat_id, "Очень смешно.. Память калькулятора очищена")
                    elif memory[chat_id][1] == "В степень" and ((memory[chat_id][2] % 1 == 0 and memory[chat_id][2]>=100) or (memory[chat_id][2] % 1 > 0 and memory[chat_id][2]>=10)):
                        del memory[chat_id]
                        m.tel_send_message(chat_id, "Давай сначала, слишком долго считать")
                    else:
                        result = f"Ответ: {m.calculate(memory[chat_id][0],memory[chat_id][1],memory[chat_id][2])}"
                        m.answer_calculate_and_hide_keyboard(chat_id, result)
                        del memory[chat_id]

            elif chat_id in memory:
                if txt in [
                    "Прибавить",
                    "Вычесть",
                    "Умножить",
                    "Разделить",
                    "В степень",
                    "Корень степени",
                ]:
                    if len(memory[chat_id]) == 1:
                        memory[chat_id].append(txt)
                    else:
                        memory[chat_id][1] = txt

                    if len(memory[chat_id]) == 2:
                        m.answer_on_calc(chat_id, txt)

            
                elif txt == "Стереть":
                    del memory[chat_id]
                    m.tel_send_message(chat_id, "Память калькулятора очищена")
                else:
                    del memory[chat_id]
                    m.tel_send_message(chat_id, "Начни сначала, память калькулятора очищена")

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



