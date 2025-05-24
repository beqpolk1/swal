from flask import render_template, request
from .perform_add_entry import perform_add_entry
from classes import Job_Status

def add_entry(mode : str):
    if (request.method == "GET"): 
        try:
            return render_template("add_entry.html.j2", mode = mode)
        except Exception as e:
            return (f"Exception rendering template: {e}")
    
    elif (request.method == "POST"):
        add_result = perform_add_entry(request.form, request.files)
        try:
            return render_template("add_entry.html.j2", result = add_result)
        except Exception as e:
            return (f"Exception rendering template: {e}")
