from .perform_search import perform_search 
from flask import render_template, request
import util_lib

def entries(id : str = None):
    if (id is None):
        result = perform_search(request.args)

        try:
            return render_template("entry_list.html.j2", data = result)
        except Exception as e:
            return (util_lib.GENERAL_TEMPLATE_EXCEPTION.format(exception = e))
    else:
        result = perform_search({"id": id})

        try:
            return render_template("entry_single.html.j2", data = result, id = id)
        except Exception as e:
            return (util_lib.GENERAL_TEMPLATE_EXCEPTION.format(exception = e))