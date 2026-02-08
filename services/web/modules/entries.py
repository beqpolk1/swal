from flask import render_template, request
import util_lib

def entries(id : str = None):
    if (id is None):
        try:
            return render_template("entry_list.html.j2")
        except Exception as e:
            return (util_lib.GENERAL_TEMPLATE_EXCEPTION.format(exception = e))
    else:
        try:
            return render_template("entry_single.html.j2", id = id)
        except Exception as e:
            return (util_lib.GENERAL_TEMPLATE_EXCEPTION.format(exception = e))