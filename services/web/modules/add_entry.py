from flask import render_template, request
from .perform_add_entry import perform_add_entry
import util_lib

def add_entry(mode : str):
    if (request.method == "GET"): 
        try:
            return render_template("add_entry.html.j2", mode = mode)
        except Exception as e:
            return (util_lib.GENERAL_TEMPLATE_EXCEPTION.format(exception = e))
    
    elif (request.method == "POST"):
        add_result = perform_add_entry(request.form, request.files)
        try:
            return render_template("add_entry.html.j2", result = add_result)
        except Exception as e:
            return (util_lib.GENERAL_TEMPLATE_EXCEPTION.format(exception = e))
