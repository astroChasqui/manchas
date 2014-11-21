from flask import Flask, render_template, request, session, redirect, url_for
import wikipedia
import datetime
from functions import *
from forms import DateForm
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sunspots'

text_sunspot = wikipedia.summary('Sunspot').split('\n')
text_cycle = wikipedia.summary('Solar cycle').split('\n')
text_rotation = wikipedia.page('Solar rotation').\
                  section('Using sunspots to measure rotation').split('\n')

img_today = get_img(datetime.date.today())

path = os.path.dirname(os.path.realpath(__file__))

@app.route("/")
def index():
    return render_template("index.html", text=text_sunspot)

@app.route("/today")
def today():
    return render_template("today.html", img=img_today)

@app.route("/cycle")
def cycle():
    return render_template("cycle.html", text=text_cycle)

@app.route("/rotation", methods=['GET', 'POST'])
def rotation():
    if not session.get('date'):
        date, weeks = datetime.date(2014, 10, 30), 1
    else:
        date = datetime.date.fromordinal(session.get('date'))
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
            date = session['date'] = None
        return redirect(url_for('rotation'))
    else:
        gifname = str(date) + "_" + str(weeks) + ".gif"
        giffile = os.path.join(path, "static", gifname)
        if not os.path.isfile(giffile):
            cmd = "convert -delay 50 "
            for d in range(-7*weeks, 1):
                img = get_img(date + datetime.timedelta(d))
                if img:
                    cmd += img + " "
            cmd += "-loop 0 "+giffile
            os.system(cmd)
        return render_template("rotation.html", text=text_rotation,
                               form=form, gifname=gifname)
