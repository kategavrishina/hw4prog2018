
# coding: utf-8

# In[52]:


import urllib.request  

results = []
for i in range(0, 800, 100):
    count = 100
    token = 'c2bff29ec2bff29ec2bff29e68c2d6303acc2bfc2bff29e9e17800d29762b' \
            '8017da70c3'
    request = 'https://api.vk.com/method/wall.get?owner_id=-26179488&count' \
              '=%d&offset=%d&v=5.92&access_token=%s' % (count, i, token)
    req = urllib.request.Request(request) 
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    results.append(result)


# In[96]:


import json

db = {}

for result in results:
    data = json.loads(result)
    for i in range(count):
        poem = data['response']['items'][i]['text']
        if len(poem.split('\n')) == 4:
            for string in poem.split('\n'):
                string = string[0].upper() + string[1:]
                db[string.strip('.,:;-– ')] = []


# In[99]:


for key, value in db.items():
    words = key.split()
    clear_words = []
    for word in words:
        word = word.strip(',.-–—!?():“”"')
        if len(word) > 0:
            clear_words.append(word)
    clear = ' '.join(clear_words)
    value.append(clear.lower())


# In[100]:


from russtress import Accent


# In[101]:


accent = Accent()
for value in db.values():
    value.append(accent.put_stress(value[0]))


# In[103]:


vowels = 'аеёиоуыэюя'
cons = 'бвгджзйклмнпрстфхцчшщьъ'


# In[104]:


for value in db.values():
    vow_in_line = []
    cons_in_line = []
    last_word = value[1].split()[-1].lower()
    for let in last_word:
        if let in vowels or let == '\'':
            vow_in_line.append(let)
        elif let in cons:
            cons_in_line.append(let)
    value.append(vow_in_line)
    value.append(cons_in_line)


# In[106]:


import random


# In[162]:


sym = "0123456789.,?!…:;()[]-_|/\"'«»*{}<>@#$%^&№"

def rhymes(text):
    words = [] 
    variants = []
    for word in text.strip().split():
        word = word.strip(sym)
        if len(word) > 0:
            words.append(word)
    if len(words) > 0:
        vow_in_last = []
        cons_in_last = []
        phrase = accent.put_stress(' '.join(words))
        last = phrase.split()[-1]
        for let in last:
            if let in vowels or let == '\'':
                vow_in_last.append(let)
            elif let in cons:
                cons_in_last.append(let)
        for key, value in db.items():
            if value[1].split()[-1] == last:
                continue
            elif len(value[2]) == 1 and len(value[3]) > 1:
                if len(vow_in_last) == 0:
                    variants.append('0')
                elif len(vow_in_last) == 1:
                    if len(cons_in_last) == 0:
                        if vow_in_last[-1] == value[2][-1]:
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


# In[171]:


import flask
import telebot
import conf

telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}
bot = telebot.TeleBot(conf.TOKEN)


# In[172]:


WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Здравствуйте! Это бот, который"
                     " находит рифму к "
                    "Вашему сообщению из творчества Игоря Губермана.")

@bot.message_handler(func=lambda m: True)
def my_function(message):
    sent = message.text
    reply = rhymes(sent)
    bot.send_message(message.chat.id, reply)
    
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
        
app.run(host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
        ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
        debug=True)


# In[173]:


if __name__ == '__main__':
    bot.polling(none_stop=True, timeout=123)

