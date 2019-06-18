import flask
import telebot
import os
import random
from russtress import Accent

accent = Accent()

app = flask.Flask(__name__)

TOKEN = os.environ["TOKEN"]
bot = telebot.TeleBot(TOKEN, threaded=False)


bot.remove_webhook()
bot.set_webhook(url="https://gariki-bot.herokuapp.com/bot")

sym = "0123456789.,?!…:;()[]-_|/\"'«»*{}<>@#$%^&№"
vowels = 'аеёиоуыэюя'
cons = 'бвгджзйклмнпрстфхцчшщьъ'

db = {}

with open('All_poems.txt', encoding='utf-8') as new_file:
    all_lines = new_file.readlines()

for row in all_lines:
    line = row.strip().split('\t')
    try:
        db[line[0]] = [line[1], line[2], list(line[3]), list(line[4])]
    except IndexError:
        db[line[0]] = [line[1], line[2], list(line[3]), []]


def rhymes(text):
    all_words = []
    variants = []
    for wrd in text.strip().split():
        wrd = wrd.strip(sym)
        if len(wrd) > 0:
            all_words.append(wrd)
    if len(all_words) > 0:
        vow_in_last = []
        cons_in_last = []
        phrase = accent.put_stress(' '.join(all_words))
        last = phrase.split()[-1]
        for letter in last:
            if letter in vowels or letter == '\'':
                vow_in_last.append(letter)
            elif letter in cons:
                cons_in_last.append(letter)
        for key, value in db.items():
            if value[1].split()[-1] == last:
                continue
            elif len(value[2]) == 1 and len(value[3]) > 1:
                if len(vow_in_last) == 0:
                    variants.append('0')
                elif len(vow_in_last) == 1:
                    if len(cons_in_last) == 0:
                        if vow_in_last[-1] == value[2][-1] and \
                                value[1].split()[-1][-1] in vowels:
                            variants.append(key)
                    elif len(cons_in_last) == 1:
                        if vow_in_last[-1] == value[2][-1] and \
                                cons_in_last[-1] == value[3][-1]:
                            variants.append(key)
                    elif len(cons_in_last) > 1:
                        if (vow_in_last[-1] == value[2][-1] and
                                cons_in_last[-1] == value[3][-1]
                                and cons_in_last[-2] == value[3][-2]):
                            variants.append(key)
                elif len(vow_in_last) > 1:
                    if len(cons_in_last) == 1:
                        if (vow_in_last[-2] == value[2][-1] and
                                cons_in_last[-1] == value[3][-1]
                                and vow_in_last[-1] == '\''):
                            variants.append(key)
                    elif len(cons_in_last) > 1:
                        if vow_in_last[-2] == value[2][-1] and \
                                vow_in_last[-1] == '\'':
                            if cons_in_last[-1] == value[3][-1] and \
                                    cons_in_last[-2] == value[3][-2]:
                                variants.append(key)
            elif len(value[2]) > 1 and len(value[3]) > 1:
                if len(vow_in_last) == 0:
                    variants.append('0')
                elif len(vow_in_last) == 1:
                    if len(cons_in_last) == 0:
                        if vow_in_last[-1] == value[2][-2] and\
                                value[2][-1] == '\'':
                            variants.append(key)
                    elif len(cons_in_last) == 1:
                        if (vow_in_last[-1] == value[2][-2] and
                                cons_in_last[-1] == value[3][-1]
                                and value[2][-1] == '\''):
                            variants.append(key)
                    elif len(cons_in_last) > 1:
                        if (vow_in_last[-1] == value[2][-1] and
                                cons_in_last[-1] == value[3][-1]
                            and cons_in_last[-2] == value[3][-2]
                                and value[2][-1] == '\''):
                            variants.append(key)
                elif len(vow_in_last) > 1:
                    if len(cons_in_last) == 1:
                        if (vow_in_last[-1] == value[2][-1] and
                                vow_in_last[-2] == value[2][-2]
                                and cons_in_last[-1] == value[3][-1]):
                            variants.append(key)
                    elif len(cons_in_last) > 1:
                        if (vow_in_last[-1] == value[2][-1]
                                and vow_in_last[-2] == value[2][-2]
                                and vow_in_last[-3] == value[2][-3]):
                            if cons_in_last[-1] == value[3][-1] \
                                    and cons_in_last[-2] == value[3][-2]:
                                variants.append(key)
            else:
                continue
    else:
        variants.append('0')
    if len(variants) == 0:
        reply = 'К сожалению, к Вашему тексту ' \
                'не нашлось рифмы. Попробуйте ещё раз.'
    elif variants[0] == '0':
        reply = 'К сожалению, к Вашему тексту невозможно подобрать рифму.'
    elif len(variants) == 1 and variants[0] != '0':
        reply = variants[0]
    else:
        reply = random.choice(variants)
    return reply


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
