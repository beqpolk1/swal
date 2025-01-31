from flask import render_template

def add_entry(methods = ['GET']):
    return render_template("add_entry.html.j2")