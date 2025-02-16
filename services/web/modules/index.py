from flask import render_template
import random

def index():
    myRand = random.randrange(1, 101)
    return render_template("index.html.j2", rand = myRand)