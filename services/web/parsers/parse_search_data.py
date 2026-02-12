import util_lib
from classes import Parse_Result
from flask import current_app

def parse_search_data(param_obj) -> Parse_Result:
    parse_result = Parse_Result()

    for func in [
        lambda: _parse_text_search(param_obj, parse_result),
        lambda: _parse_starred(param_obj, parse_result)
    ]:
        func()

    return parse_result

def _parse_text_search(params, parse_result : Parse_Result):
    try:
        text_search = util_lib.get_str_or_none_2(params, "q")

        if text_search is not None:
            if len(text_search) < current_app.config["MIN_Q_LENGTH"]:
                parse_result.add_error(util_lib.SEARCH_TEXT_TOO_SHORT.format(length = current_app.config["MIN_Q_LENGTH"]))
            elif len(text_search) > current_app.config["MAX_Q_LENGTH"]:
                parse_result.add_error(util_lib.SEARCH_TEXT_TOO_LONG.format(length = current_app.config["MAX_Q_LENGTH"]))
            else:
                parse_result.add_data("text_search", text_search)
    except (TypeError, ValueError) as e:
        parse_result.add_error(util_lib.SEARCH_PARSE_EXCEPTION.format(param = "text_search", exception = e))
    
def _parse_starred(params, parse_result : Parse_Result):
    try:
        starred = util_lib.get_bool_or_none_2(params, "starred")

        if starred is not None:
            parse_result.add_data("is_starred", starred)
    except(TypeError, ValueError) as e:
        parse_result.add_error(util_lib.SEARCH_PARSE_EXCEPTION.format(param = "starred", exception = e))