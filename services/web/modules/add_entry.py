from flask import render_template

def add_entry(mode : str):
    return render_template("add_entry.html.j2", mode = mode)