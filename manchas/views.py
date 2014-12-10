from flask import Flask, render_template, request, session, redirect,\
                  url_for, flash
import wikipedia
import datetime
from functions import *
from forms import DateForm
import os
import sqlite3
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sunspots'

text_sunspot = wikipedia.summary('Sunspot').split('\n')
text_cycle = wikipedia.summary('Solar cycle').split('\n')
text_rotation = wikipedia.page('Solar rotation').\
                  section('Using sunspots to measure rotation').split('\n')
text_issn = wikipedia.summary('Wolf number').split('\n')[0:2]

path = os.path.dirname(os.path.realpath(__file__))

@app.route("/")
def index():
    session.clear()
    return render_template("index.html", text=text_sunspot)

@app.route("/today")
def today():
    img_today = get_img(datetime.date.today())
    return render_template("today.html", img=img_today)

@app.route("/cycle", methods=['GET', 'POST'])
def cycle():
    if not session.get('date'):
        date, weeks = datetime.date(2014, 10, 30), 2
        session['date'] = date.toordinal()
    else:
        date = datetime.date.fromordinal(session.get('date'))
    form = DateForm(year=date.year, month=date.month, day=date.day)
    if request.method == 'POST':
        try:
            date = datetime.date(form.year.data,
                                 form.month.data,
                                 form.day.data)
            session['date'] = date.toordinal()
            session['weeks'] = form.weeks.data
        except:
            date = datetime.date.fromordinal(session.get('date'))
            flash('Invalid date. Using previous value.')
        return redirect(url_for('cycle'))
    else:
        conn = sqlite3.connect(os.path.join(path, 'static', 'ISSN_D_tot.db'))
        conn_cursor = conn.cursor()

        conn_cursor.execute('SELECT year, month, day, ssn '\
                            'FROM ISSN_D_tot WHERE year >= 2001')
        data = np.array(conn_cursor.fetchall()).T
        year, month, day, ssn = data[0], data[1], data[2], data[3]
        dates = [datetime.date(y,m,d) for y,m,d in zip(year, month, day)]
        conn_cursor.execute('SELECT ssn FROM ISSN_D_tot '\
                            'WHERE year == '+str(date.year)+\
                            ' AND month == '+str(date.month)+\
                            ' AND day == '+str(date.day))
        try:
            ssnx = conn_cursor.fetchone()[0]
        except:
            ssnx = None
        conn.close()

        ssn_img = str(date)+'.png'
        if not os.path.isfile(os.path.join(path, 'static', 'cycle', ssn_img)):
            plt.figure(figsize=(5,4))
            plt.ylim([0,260])
            plt.xlabel('Date')
            plt.title('International sunspot number')
            plt.scatter(dates, ssn, alpha=0.5, s=10)
            plt.scatter([date], [ssnx], s=200, c='green')
            plt.tight_layout()
            plt.savefig(os.path.join(path, 'static', 'cycle', ssn_img))
            plt.close()
        img = get_img(date)

        return render_template("cycle.html", text=text_cycle, img=img,
                               form=form, ssnx=ssnx, ssn_img=ssn_img,
                               text_issn=text_issn)

    return render_template("cycle.html", text=text_cycle)

@app.route("/rotation", methods=['GET', 'POST'])
def rotation():
    if not session.get('date'):
        date = datetime.date(2014, 10, 30)
    else:
        date = datetime.date.fromordinal(session.get('date'))
    if not session.get('weeks'):
        weeks = 2
    else:
        weeks = session.get('weeks')
    form = DateForm(year=date.year, month=date.month, day=date.day,
                    weeks=weeks)
    if request.method == 'POST':
        try:
            date = datetime.date(form.year.data,
                                 form.month.data,
                                 form.day.data)
            session['date'] = date.toordinal()
            session['weeks'] = form.weeks.data
        except:
            date = datetime.date.fromordinal(session.get('date'))
            flash('Invalid date. Using previous value.')
        return redirect(url_for('rotation'))
    else:
        gifname = str(date) + '_' + str(weeks) + '.gif'
        giffile = os.path.join(path, 'static', 'rotation', gifname)
        if not os.path.isfile(giffile):
            cmd = "convert -delay 50 "
            for d in range(-7*weeks, 1):
                img = get_img(date + datetime.timedelta(d))
                if img:
                    cmd += img + ' '
            cmd += '-loop 0 '+giffile
            os.system(cmd)
        return render_template('rotation.html', text=text_rotation,
                               form=form, gifname=gifname)
