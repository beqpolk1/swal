from .perform_search import perform_search 
from flask import render_template, request
import util_lib

def entries(_id : str = None):
    if (_id is None):
        result = perform_search(request.args, False)

        try:
            return render_template("entry_list.html.j2", data = result, prev_search = request.query_string.decode("utf-8"))
        except Exception as e:
            return (util_lib.GENERAL_TEMPLATE_EXCEPTION.format(exception = e))
    else:
        result = perform_search({"_id": _id}, True)

        try:
            return render_template("entry_single.html.j2", data = result, id = _id, prev_search = request.args["prev"])
        except Exception as e:
            return (util_lib.GENERAL_TEMPLATE_EXCEPTION.format(exception = e))