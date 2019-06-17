import urllib.request
import json
from russtress import Accent
import random


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

db = {}

for result in results:
    data = json.loads(result)
    for i in range(100):
        poem = data['response']['items'][i]['text']
        if len(poem.split('\n')) == 4:
            for string in poem.split('\n'):
                string = string[0].upper() + string[1:]
                db[string.strip('.,:;-– ')] = []

for key, value in db.items():
    words = key.split()
    clear_words = []
    for word in words:
        word = word.strip(',.-–—!?():“”"')
        if len(word) > 0:
            clear_words.append(word)
    clear = ' '.join(clear_words)
    value.append(clear.lower())

accent = Accent()
for value in db.values():
    value.append(accent.put_stress(value[0]))

vowels = 'аеёиоуыэюя'
cons = 'бвгджзйклмнпрстфхцчшщьъ'

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

sym = "0123456789.,?!…:;()[]-_|/\"'«»*{}<>@#$%^&№"


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
