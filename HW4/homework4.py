import csv
import matplotlib.pyplot as plt
import json
import numpy as np
from flask import Flask
from flask import url_for, render_template, request, redirect
from matplotlib import style
style.use('ggplot')

app = Flask(__name__)


@app.route('/')
def form():
    if request.args:
        f = open('data.csv', 'a', encoding='utf-8')
        firstname = request.args['firstname']
        lastname = request.args['lastname']
        sex = request.args['sex']
        age = request.args['age']
        home = request.args['home']
        cakes = request.args['photo']
        # запись в файл csv
        print(firstname, lastname, sex, age, home, cakes, sep=',', file=f)
        return redirect(url_for('answer'))
    return render_template('index.html')


@app.route('/answer')
def answer():
    # страница навигации
    url = url_for('stats')
    url_1 = url_for('show_json')
    url_2 = url_for('search')
    return render_template('answer.html', url=url, url_1=url_1, url_2=url_2)


@app.route('/stats')
def stats():
    with open('data.csv', encoding='utf-8') as csvfile:
        f = list(csv.reader(csvfile))
    length = len(f)
    # переменные для общего графика
    cup = 0
    cake = 0
    muf = 0
    other = 0
    # переменнные для корреляции с полом
    cup_f = 0
    cup_m = 0
    cake_f = 0
    cake_m = 0
    muf_f = 0
    muf_m = 0
    other_f = 0
    other_m = 0
    # переменные для корреляции с местом
    cup_mos = 0
    cup_spb = 0
    cup_other = 0
    cake_mos = 0
    cake_spb = 0
    cake_other = 0
    muf_mos = 0
    muf_spb = 0
    muf_other = 0
    other_mos = 0
    other_spb = 0
    other_other = 0
    # переменные для корреляции с возрастом
    cup_18 = 0
    cup_25 = 0
    cup_40 = 0
    cup_100 = 0
    cake_18 = 0
    cake_25 = 0
    cake_40 = 0
    cake_100 = 0
    muf_18 = 0
    muf_25 = 0
    muf_40 = 0
    muf_100 = 0
    other_18 = 0
    other_25 = 0
    other_40 = 0
    other_100 = 0
    x = ['Капкейки', 'Кексы', 'Маффины', 'Другое']
    y = [cup, cake, muf, other]
    for row in f:
        ln = len(row)
        if row[ln - 1] == x[0]:
            y[0] += 1
            if row[2] == 'жен':
                cup_f += 1
            else:
                cup_m += 1
            if row[4] == 'Москва':
                cup_mos += 1
            elif row[4] == 'Санкт-Петербург':
                cup_spb += 1
            else:
                cup_other += 1
            if row[3] == '<18':
                cup_18 += 1
            elif row[3] == '18-25':
                cup_25 += 1
            elif row[3] == '25-40':
                cup_40 += 1
            else:
                cup_100 += 1
        elif row[ln - 1] == x[1]:
            y[1] += 1
            if row[2] == 'жен':
                cake_f += 1
            else:
                cake_m += 1
            if row[4] == 'Москва':
                cake_mos += 1
            elif row[4] == 'Санкт-Петербург':
                cake_spb += 1
            else:
                cake_other += 1
            if row[3] == '<18':
                cake_18 += 1
            elif row[3] == '18-25':
                cake_25 += 1
            elif row[3] == '25-40':
                cake_40 += 1
            else:
                cake_100 += 1
        elif row[ln - 1] == x[2]:
            y[2] += 1
            if row[2] == 'жен':
                muf_f += 1
            else:
                muf_m += 1
            if row[4] == 'Москва':
                muf_mos += 1
            elif row[4] == 'Санкт-Петербург':
                muf_spb += 1
            else:
                muf_other += 1
            if row[3] == '<18':
                muf_18 += 1
            elif row[3] == '18-25':
                muf_25 += 1
            elif row[3] == '25-40':
                muf_40 += 1
            else:
                muf_100 += 1
        else:
            y[3] += 1
            if row[2] == 'жен':
                other_f += 1
            else:
                other_m += 1
            if row[4] == 'Москва':
                other_mos += 1
            elif row[4] == 'Санкт-Петербург':
                other_spb += 1
            else:
                other_other += 1
            if row[3] == '<18':
                other_18 += 1
            elif row[3] == '18-25':
                other_25 += 1
            elif row[3] == '25-40':
                other_40 += 1
            else:
                other_100 += 1

    fig1, ax1 = plt.subplots()
    ax1.pie(y, labels=x, counterclock=False, autopct='%1.1f%%',
            colors=['#fea993', '#fbeeac', '#ffb07c', '#ffff84'], startangle=90)
    ax1.axis('equal')
    plt.title('Общее соотношение ответов:')
    plt.savefig('static/plot1.png', dpi=125)

    # график для пола
    n_groups = 4
    means_women = (cup_f, cake_f, muf_f, other_f)
    means_men = (cup_m, cake_m, muf_m, other_m)

    plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8

    plt.bar(index, means_women, bar_width, alpha=opacity, color='#fcc006',
            label='Женский')

    plt.bar(index + bar_width, means_men, bar_width, alpha=opacity,
            color='#7b002c', label='Мужской')

    plt.title('Корреляция с полом информантов')
    plt.xticks(index + bar_width / 2, ('Капкейки', 'Кексы', 'Маффины',
                                       'Другое'))
    plt.legend()
    plt.tight_layout()
    plt.savefig('static/plot2.png', dpi=100)

    # график для места
    n1_groups = 4
    means_moscow = (cup_mos, cake_mos, muf_mos, other_mos)
    means_spb = (cup_spb, cake_spb, muf_spb, other_spb)
    means_other = (cup_other, cake_other, muf_other, other_other)

    plt.subplots()
    index = np.arange(n1_groups)
    bar_width = 0.2
    opacity = 0.8

    plt.bar(index - bar_width/2, means_moscow, bar_width, alpha=opacity,
            color='#fcc006',
            label='Москва')

    plt.bar(index + bar_width/2, means_spb, bar_width, alpha=opacity,
            color='#7b002c', label='Санкт-Петербург')

    plt.bar(index + 3*bar_width/2, means_other, bar_width, alpha=opacity,
            color='#1e488f', label='Другое')

    plt.title('Корреляция с местом жительства информантов')
    plt.xticks(index + bar_width/2, ('Капкейки', 'Кексы', 'Маффины', 'Другое'))
    plt.legend()
    plt.tight_layout()
    plt.savefig('static/plot3.png', dpi=100)

    # график для возраста
    n2_groups = 4
    means_18 = (cup_18, cake_18, muf_18, other_18)
    means_25 = (cup_25, cake_25, muf_25, other_25)
    means_40 = (cup_40, cake_40, muf_40, other_40)
    means_100 = (cup_100, cake_100, muf_100, other_100)

    plt.subplots()
    index = np.arange(n2_groups)
    bar_width = 0.2
    opacity = 0.8

    plt.bar(index - bar_width, means_18, bar_width, alpha=opacity,
            color='#fcc006',
            label='< 18 лет')

    plt.bar(index, means_25, bar_width, alpha=opacity,
            color='#7b002c', label='18-25 лет')

    plt.bar(index + bar_width, means_40, bar_width, alpha=opacity,
            color='#1e488f', label='25-40 лет')

    plt.bar(index + 2*bar_width, means_100, bar_width, alpha=opacity,
            color='k', label='> 40 лет')

    plt.title('Корреляция с возрастом информантов')
    plt.xticks(index + bar_width / 2,
               ('Капкейки', 'Кексы', 'Маффины', 'Другое'))
    plt.legend()
    plt.tight_layout()
    plt.savefig('static/plot4.png', dpi=100)
    return render_template('stats.html', filereader=f, length=length,
                           url1='static/plot1.png', url2='static/plot2.png',
                           url3='static/plot3.png', url4='static/plot4.png')


@app.route('/json')
def show_json():
    lst = []
    with open('data.csv', encoding='utf-8') as csvfile:
        f = list(csv.reader(csvfile))
    for row in f:
        lst.append({'Имя': row[0], 'Фамилия': row[1], 'Пол': row[2],
                    'Возраст': row[3], 'Место жительства': row[4],
                    'Ответ': row[5]})
    json_string = json.dumps(lst, ensure_ascii=False, indent=4, separators=(
        ',', ': '))
    return render_template('showjson.html', json=json_string)


@app.route('/search')
def search():
    if request.args:
        res = []
        # проверка на пустой ввод (случай "question=")
        if request.args['question'] != '' or len(request.args) > 1:
            with open('data.csv', encoding='utf-8') as csvfile:
                f = list(csv.reader(csvfile))
            vls = []
            for value in request.args.values():
                # пустой текстовый запрос
                if value != '':
                    vls.append(value)
            for row in f:
                count = 0
                for vl in vls:
                    if vl.lower() in ' '.join(row).lower():
                        count += 1
                # проверка на то, что все параметры из списка есть в строке
                if count == len(vls):
                    res.append(row)
            # если таких строк не нашлось
            if len(res) == 0:
                return render_template('bad_request.html')
            else:
                return render_template('results.html', all=res)
    return render_template('search.html')


@app.route('/nothingfound')
def bad_request():
    return render_template('bad_request.html')


@app.route('/results')
def results():
    return render_template('results.html')


if __name__ == '__main__':
    app.run(debug=True)
