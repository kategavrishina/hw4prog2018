import flask
import telebot
import os
from main_code import rhymes

app = flask.Flask(__name__)

TOKEN = os.environ["TOKEN"]
bot = telebot.TeleBot(TOKEN, threaded=False)


bot.remove_webhook()
bot.set_webhook(url="https://gariki-bot.herokuapp.com/bot")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Здравствуйте! Это бот, который находит"
                                      " рифму к Вашему сообщению из творчества"
                                      " Игоря Губермана.\n /about - Кто "
                                      "такой Игорь Губерман?\n /info - "
                                      "Почему рифма не находится?\n /stopit - "
                                      "Если хотите закончить общение с "
                                      "ботом")


@bot.message_handler(commands=['about'])
def smth_about(message):
    bot.send_message(message.chat.id, "И́горь Миро́нович Губерма́н (род. 7 "
                                      "июля 1936, Харьков) — русский прозаик,"
                                      " поэт, получивший широкую известность "
                                      "благодаря своим афористичным и "
                                      "сатирическим четверостишиям — «гарикам»"
                                      ".\n\n«Гарики» для бота были взяты из "
                                      "группы ВКонтакте ("
                                      "https://vk.com/igor_guberman). Стихи "
                                      "действительно заслуживают внимания. "
                                      "Обязательно почитайте на досуге!")


@bot.message_handler(commands=['info'])
def information(message):
    bot.send_message(message.chat.id, "Если рифма не находится, причин может "
                                      "быть несколько:\n1) Вы ввели "
                                      "некорректный запрос (бот принимает и "
                                      "понимает только слова на русском "
                                      "языке, написанные правильно)\n2) "
                                      "Текст довольно нестандартный, к нему "
                                      "сложно найти рифму\n3) Просто в "
                                      "творчестве поэта не нашлось "
                                      "подходящих строк, рифмы Губермана "
                                      "весьма необычны\n\nЕсли Вы хотите "
                                      "узнать, как это все работает, "
                                      "но рифмы для Ваших запросов никак не "
                                      "находятся, попробуйте слова "
                                      "\"весной\", \"она\", \"месть\", \"я\".")


@bot.message_handler(commands=['stopit'])
def interrupting(message):
    bot.send_message(message.chat.id, "Надеюсь, Вам понравилось. Всего "
                                      "хорошего!")


@bot.message_handler(func=lambda m: True)
def my_function(message):
    sent = message.text
    reply = rhymes(sent)
    bot.send_message(message.chat.id, reply)


@app.route("/", methods=['GET', 'HEAD'])
def index():
    return 'ok'


@app.route("/bot", methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
