from flask import Flask, render_template
import wikipedia
import datetime
from functions import *


app = Flask(__name__)

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

@app.route("/rotation")
def rotation():
    return render_template("rotation.html", text=text_rotation)
