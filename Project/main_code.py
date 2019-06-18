import urllib.request
import json
from russtress import Accent

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

all_poems = {}

for result in results:
    data = json.loads(result)
    for i in range(100):
        poem = data['response']['items'][i]['text']
        if len(poem.split('\n')) == 4:
            for string in poem.split('\n'):
                string = string[0].upper() + string[1:]
                all_poems[string.strip('.,:;-– ')] = []

for key, value in all_poems.items():
    words = key.split()
    clear_words = []
    for word in words:
        word = word.strip(',.-–—!?():“”"')
        if len(word) > 0:
            clear_words.append(word)
    clear = ' '.join(clear_words)
    value.append(clear.lower())

accent = Accent()

for value in all_poems.values():
    value.append(accent.put_stress(value[0]))

vowels = 'аеёиоуыэюя'
cons = 'бвгджзйклмнпрстфхцчшщьъ'

for value in all_poems.values():
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

with open('All_poems.txt', 'a', encoding='utf-8') as file:
    for key, value in all_poems.items():
        file.write('{}\t{}\t{}\t{}\t{}\n'.format(key, value[0], value[1],
                                                 ''.join(value[2]),
                                                 ''.join(value[3])))
