from flask import Flask, render_template
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
    date = datetime.date.today()
    weeks = 2
    form = DateForm(year=date.year, month=date.month, day=date.day,
                    weeks=weeks)
    gifname = str(date) + "_" + str(weeks) + ".gif"
    if not os.path.isfile(os.path.join("static", gifname)):
        cmd = "convert -delay 50 "
        for d in range(-7*weeks, 1):
            img = get_img(date + datetime.timedelta(d))
            if img:
                cmd += img + " "
        cmd += "-loop 0 static/"+gifname
        os.system(cmd)

    return render_template("rotation.html", text=text_rotation, form=form,
                           gifname=gifname)
