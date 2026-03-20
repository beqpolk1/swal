import util_lib
from classes import Parse_Result
from flask import current_app
import json, binascii, base64

def parse_search_string(param_obj) -> Parse_Result:
    parse_result = Parse_Result()

    for func in [
        lambda: _parse_text_search(param_obj, parse_result),
        lambda: _parse_starred(param_obj, parse_result),
        lambda: _parse_limit(param_obj, parse_result),
        lambda: _parse_full_cursor(param_obj, parse_result)
        # lambda: _parse_prev_cursor(param_obj, parse_result)
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

# cursor structure:
# {
  # fields: [
    # { field: "artist", order: "asc", last_val: <val> },
    # { field: "album", order: "asc", last_val: <val> },
    # { field: "_id", order: "asc", last_val: <val> }
# ]
# }

def _parse_full_cursor(params, parse_result : Parse_Result):
    try:
        cursor = util_lib.get_str_or_none_2(params, "cursor")

        if cursor is not None:
            cursor_obj = util_lib.base64_enc_to_dict(cursor)

            structure_errors = _parse_cursor_structure(cursor_obj)
            parse_result.add_errors(structure_errors)
            
            content_errors = _parse_cursor_content(cursor_obj)
            parse_result.add_errors(content_errors)

            if not parse_result.has_errors():
                parse_result.add_data("cursor", cursor_obj)
            
    except binascii.Error as e:
        parse_result.add_error(util_lib.CURSOR_BASE64_DECODE_EXCEPTION.format(exception = e))
    except UnicodeDecodeError as e:
        parse_result.add_error(util_lib.CURSOR_TEXT_DECODE_EXCEPTION.format(exception = e))
    except json.JSONDecodeError as e:
        parse_result.add_error(util_lib.CURSOR_JSON_DECODE_EXCEPTION.format(exception = e))
    except(TypeError, ValueError) as e:
        parse_result.add_error(util_lib.SEARCH_PARSE_EXCEPTION.format(param = "cursor", exception = e))    

def _parse_cursor_structure(cursor_obj):
    error_list = []

    if not isinstance(cursor_obj, dict):
        error_list.add_error(util_lib.CURSOR_NOT_DICTIONARY)
        return error_list
    
    if not "fields" in cursor_obj:
        error_list.add_error(util_lib.CURSOR_DOESNT_HAVE_FIELDS)
        return error_list

    if not isinstance(cursor_obj["fields"], list):
        error_list.add_error(util_lib.CURSOR_FIELDS_NOT_LIST)
        return error_list
    
    if len(cursor_obj["fields"]) > current_app.config["CURSOR_FIELD_MAX"]:
        error_list.add_error(util_lib.CURSOR_TOO_MANY_FIELDS.format(max = current_app.config["CURSOR_FIELD_MAX"]))
        return error_list

    for item in cursor_obj["fields"]:
        if not isinstance(item, dict):
            error_list.add_error(util_lib.CURSOR_FIELD_ITEM_NOT_DICT.format(element = item))
            continue

        if not "field" in item:
            error_list.add_error(util_lib.CURSOR_FIELD_ITEM_MISSING_FIELD.format(element = item))
            continue

        if "order" in item:
            item["order"] = item["order"].lower()
            if item["order"] not in current_app.config["VALID_SORT_ORDER"]:
                error_list.add_error(util_lib.CURSOR_FIELD_ITEM_INVALID_ORDER.format(element = item))
                continue
               
    return error_list

def _parse_cursor_content(cursor_obj):
    return []