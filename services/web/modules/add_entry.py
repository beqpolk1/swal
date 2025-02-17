from flask import render_template, request
from .entry import Entry
from .perform_add_entry import perform_add_entry

def add_entry(mode : str):
    if (request.method == "GET"): 
        return render_template("add_entry.html.j2", mode = mode)
    elif (request.method == "POST"):
        new_entry = Entry(request.form["artist"], 
                          request.form["album"], 
                          request.form["release_year"], 
                          request.form["genre"], 
                          request.form["interest_level"], 
                          request.form["is_starred"], 
                          request.form["is_obtained"], 
                          request.form["link"])
        
        return perform_add_entry(new_entry)