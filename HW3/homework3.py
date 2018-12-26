import urllib.request
import time
import re
import html
import os
import csv

def download_page(pageUrl):
    try:
        page = urllib.request.urlopen(pageUrl)
        text = page.read().decode('cp1251')
        text = html.unescape(text)
        return text
    except:
        print('Error at', pageUrl)

def meta(text):
    r = re.search('''<div class=\"articleName\">
            <h1>(.*?)</h1>''', text)
    if r:
        header = r.group(1)
    else:
        return None

    r = re.search('''<div class="articleAuthor">
            Автор: (.*?)        </div>''', text)
    if r:
        author = r.group(1).lower().title()
    else:
        author = None

    r = re.search('''<div class="articleNum">
            (.*?)        </div>''', text)
    if r:
        data = r.group(1)
        year = data.split()[4]
        month = data.split()[3]
        if data.split()[3] == 'января':
            month = '01'
        elif data.split()[3] == 'февраля':
            month = '02'
        elif data.split()[3] == 'марта':
            month = '03'
        elif data.split()[3] == 'апреля':
            month = '04'
        elif data.split()[3] == 'мая':
            month = '05'
        elif data.split()[3] == 'июня':
            month = '06'
        elif data.split()[3] == 'июля':
            month = '07'
        elif data.split()[3] == 'августа':
            month = '08'
        elif data.split()[3] == 'сентября':
            month = '09'
        elif data.split()[3] == 'октября':
            month = '10'
        elif data.split()[3] == 'ноября':
            month = '11'
        elif data.split()[3] == 'декабря':
            month = '12'
        created = str(data.split()[2]) + '.' + month + '.' + str(year)
    else:
        month = None
        year = None
        created = None

    return header, author, month, year, created

def plain(text, metadata):
    r = re.search('''<div class=\"articleText\">
            (.*?)</div>''', text)
    if r:
        text = r.group(1)
        text = re.sub('<br>', '\n', text)
        regTag = re.compile('</?[a-z]*?>',re.DOTALL)
        plaintext = regTag.sub("", text)
    else:
        plaintext = ''
    path = 'paper' + os.sep + 'plain' + os.sep + str(metadata[3]) + os.sep + \
           str(metadata[2])
    if not os.path.exists(path):
        os.makedirs(path)
    num = str(len(os.listdir(path)) + 1)
    with open('%s\\%s.txt' %(path, num), 'w', encoding = 'utf-8') as f:
        f.write(plaintext)
    return plaintext, num

def ms():
    tree = os.walk('paper')
    for root, dirs, files in tree:
        for file in files:
            inp = root + os.sep + file
            lst = inp.split('\\')
            if lst[1] != 'metadata.csv':
                out = lst[0] + os.sep + 'mystem-plain' + os.sep + lst[2] \
                      + os.sep + lst[3]
                if not os.path.exists(out):
                    os.makedirs(out)
                os.system('mystem.exe -cdil --eng-gr ' + inp + ' ' + out + \
                                                      os.sep + lst[4])
                out = lst[0] + os.sep + 'mystem-xml' + os.sep + lst[2] \
                      + os.sep + lst[3]
                if not os.path.exists(out):
                    os.makedirs(out)
                os.system('mystem.exe -cdil --eng-gr --format xml ' + inp +
                          ' ' + out + \
                          os.sep + file.split('.')[0] + '.xml')


def table(header, author, month, year, created, pageUrl, num):
    if header is not None:
        with open('paper\metadata.csv', 'a') as f:
            f.write('paper\plain\%s\%s\%s\t%s\t%s\t%s\tпублицистика\tNone\t'
                    'нейтральный\t'
                    'н-возраст\tн-уровень\tгородская\t%s\tПермский '
                    'обозреватель\t%s\tгазета\tРоссия\tПермь\tru\n' %(
                year, month, num, author, header, created, pageUrl, year))


commonUrl = 'http://www.permoboz.ru'

os.mkdir('paper')
with open('paper\metadata.csv', 'a') as f:
    f.write('path\tauthor\theader\tcreated\tsphere\ttopic\tstyle\t'
            'audience_age\taudience_level\taudience_size\tsource\tpublication'
            '\tpubl_year\tmedium\tcountry\tregion\tlanguage\n')

for i in range(498, 900):
    pageUrl = commonUrl + '/txt.php?n=%s' % i
    metadata = meta(download_page(pageUrl))
    if metadata != None:
        a = plain(download_page(pageUrl), metadata)
        num = a[1]
        table(metadata[0], metadata[1], metadata[2], metadata[3], metadata[
            4], pageUrl, num)
        time.sleep(2)
ms()

with open('paper\metadata.csv') as f:
    text = csv.reader(f, delimiter='\t')
    for meta in text:
        if meta[0] != 'path':
            with open ('%s.txt' %(meta[0]),'r+',encoding='utf-8') as f:
                all = f.readlines()
                f.seek(0)
                f.writelines(['@au %s\n@ti %s\n@da %s\n@topic %s\n@url %s\n\n' \
                    % (meta[1],meta[2],meta[3],None,meta[10])] + all)

