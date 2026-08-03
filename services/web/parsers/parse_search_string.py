import util_lib
from classes import Parse_Result, Search_Index
from flask import current_app
import json, binascii, base64

def parse_search_string(param_obj) -> Parse_Result:
    parse_result = Parse_Result()

    for func in [
        lambda: _parse_text_search(param_obj, parse_result),
        lambda: _parse_starred(param_obj, parse_result),
        lambda: _parse_limit(param_obj, parse_result),
        lambda: _parse_search_index(param_obj, parse_result)
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

def _parse_limit(params, parse_result : Parse_Result):
    try:
        limit = util_lib.get_int_or_none_2(params, "limit")

        if limit is not None:
            if (limit > current_app.config["SEARCH_LIMIT_MAX"] or limit < current_app.config["SEARCH_LIMIT_MIN"]):
                parse_result.add_error(util_lib.SEARCH_LIMIT_OUT_OF_BOUNDS.format(min = current_app.config["SEARCH_LIMIT_MIN"], max = current_app.config["SEARCH_LIMIT_MAX"]))
            else:
                parse_result.add_data("limit", limit)
    
    except(TypeError, ValueError) as e:
        parse_result.add_error(util_lib.SEARCH_PARSE_EXCEPTION.format(param = "limit", exception = e))

def _parse_search_index(params, parse_result : Parse_Result):
    try:
        index = util_lib.get_str_or_none_2(params, "index")

        if index is not None:
            index_dict = util_lib.base64_enc_to_dict(index)
            dict_error = _parse_index_structure(index_dict)

            if (dict_error is None):
                search_index = Search_Index.from_dict(index_dict)
                parse_result.add_data("search_index", search_index)
            else:
                parse_result.add_error(dict_error)

    except binascii.Error as e:
        parse_result.add_error(util_lib.INDEX_BASE64_DECODE_EXCEPTION.format(exception = e))
    except UnicodeDecodeError as e:
        parse_result.add_error(util_lib.INDEX_TEXT_DECODE_EXCEPTION.format(exception = e))
    except json.JSONDecodeError as e:
        parse_result.add_error(util_lib.INDEX_JSON_DECODE_EXCEPTION.format(exception = e))
    except(TypeError, ValueError) as e:
        parse_result.add_error(util_lib.SEARCH_PARSE_EXCEPTION.format(param = "index", exception = e))

def _parse_index_structure(index_dict):
    if not isinstance(index_dict, dict): return (util_lib.INDEX_NOT_DICTIONARY)
    
    if not "fields" in index_dict: return (util_lib.INDEX_DOESNT_HAVE_FIELDS)

    if not isinstance(index_dict["fields"], list): return (util_lib.INDEX_FIELDS_NOT_LIST)
    
    if len(index_dict["fields"]) > current_app.config["INDEX_FIELD_MAX"]:
        return (util_lib.INDEX_TOO_MANY_FIELDS.format(max = current_app.config["INDEX_FIELD_MAX"]))
    
    if not "direction" in index_dict: return (util_lib.INDEX_DOESNT_HAVE_DIR)
    
    if not isinstance(index_dict["direction"], str): return (util_lib.INDEX_DIR_NOT_STR)
    
    return None