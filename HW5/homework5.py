import csv
import sqlite3
from flask import Flask
from flask import render_template, request
import os
import re

app = Flask(__name__)

con = sqlite3.connect("corpus.db", check_same_thread=False)


def create():
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS result(name, author, date, url, "
                "path, plain, mystem);")
    to_db = []
    with open(os.path.join('paper', 'metadata.csv')) as f:
        meta = csv.reader(f, delimiter='\t')
        for row in meta:
            if row[0] != 'path':
                to_db.append([row[2], row[1], row[3], row[10], row[0]])
    for i in range(len(to_db)):
        path = to_db[i][4]
        path_mystem = path.replace('plain', 'mystem-plain')
        with open('%s.txt' % path, 'r', encoding='utf-8') as f:
            text = f.readlines()
            to_db[i].append('\n'.join(text[6:]))
        with open('%s.txt' % path_mystem, 'r', encoding='utf-8') as g:
            mstm = g.read()
            to_db[i].append(mstm)
    cur.executemany(
        "INSERT INTO result (name, author, date, url, path, plain, mystem) "
        "VALUES (?, ?, ?, ?, ?, ?, ?);", to_db)
    con.commit()


create()


@app.route('/')
def search():
    if request.args:
        lst = []
        query = request.args['query']
        result = 1
        inp = "input"
        out = "output"
        if not os.path.exists(inp):
            os.makedirs(inp)
        with open(os.path.join(inp, 'temporary.txt'), 'w', encoding='utf-8') \
                as f:
            f.write(query)
        if not os.path.exists(out):
            os.makedirs(out)
        os.system('mystem.exe -cdil --eng-gr ' + inp + os.sep +
                  "temporary.txt" + ' ' + "output" + os.sep + "temporary.txt")
        with open(os.path.join(out, 'temporary.txt'), 'r', encoding='utf-8') \
                as g:
            real_query = g.read()
        os.remove(os.path.join(inp, 'temporary.txt'))
        os.remove(os.path.join(out, 'temporary.txt'))
        cur = con.cursor()
        cur.execute("SELECT * FROM result")
        found = cur.fetchall()
        word = re.search('{.*?=', real_query)
        for row in found:
            if re.search(word.group(), row[6]):
                mystem_forms = re.findall('{.*?=', row[6])
                index = mystem_forms.index(word.group())
                lst.append([row[3], ' '.join(row[5].split()[
                                                  (index-20):(index+20)])])
        nf = 0
        if len(lst) == 0:
                nf = 1
        return render_template('index.html', result=result, query=query,
                               lst=lst, nf=nf)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
    con.close()
