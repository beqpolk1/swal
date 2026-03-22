from classes import Search_Result, Entry
from parsers import parse_search_string, parse_object_id
from .db_interface import full_search, single_search
from flask import current_app
import util_lib
import copy
from pprint import pprint

# search fields/filters
  # text-based search:
    # -artist
    # -album
    # -genre
    # -link
  # value-based filter:
    # -releaseYear (range)
    # -interestLevel (range)
    # -starred (bool)
    # -obtained (bool)

def perform_search(raw_params, single_mode : bool) -> Search_Result:
    if single_mode:
        parse_func = parse_object_id
        search_func = _perform_single_search
        param_func = lambda parsed_params : parsed_params
    else:
        parse_func = parse_search_string
        search_func = _perform_full_search
        param_func = _prep_search_params

    parsed_input = parse_func(raw_params)
    search_result = Search_Result()

    if not parsed_input.has_errors():
        search_params = param_func(parsed_input.result_data)

        try:
            search_result = search_func(search_params)
        except Exception as e:
            search_result.add_error(util_lib.GENERAL_SEARCH_EXCEPTION.format(exception=e))
    
    search_result.add_errors(parsed_input.errors)

    return search_result

def _perform_single_search(search_params) -> Search_Result:
    search_result = Search_Result()
    search_result.add_result(_db_result_to_entry(single_search(search_params)))
    return search_result

def _perform_full_search(search_params) -> Search_Result:
    search_result = Search_Result()

    for db_result in full_search(search_params):
        search_result.add_result(_db_result_to_entry(db_result))

    _fill_in_paging(search_result, search_params)

    return search_result

def _db_result_to_entry(db_result) -> Entry:
    new_entry = Entry(db_result, {})

    if db_result.get("artwork_file"):
        new_entry.artwork_file_name = db_result.get("artwork_file_name")
        new_entry.artwork_file = True

    return new_entry

def _prep_search_params(parsed_params) -> dict:
    final_params = {}

    if "limit" in parsed_params:
        final_params["search_limit"] = parsed_params.pop("limit")
    else:
        final_params["search_limit"] = current_app.config["DEFAULT_SEARCH_LIMIT"]

    final_params["db_limit"] = final_params["search_limit"] + 1

    if "cursor" in parsed_params:
        final_params["search_cursor"] = parsed_params.pop("cursor")
        _normalize_cursor_field_order(final_params["search_cursor"])
    else:
        final_params["search_cursor"] = current_app.config["DEFAULT_SEARCH_CURSOR"]

    final_params["search_params"] = parsed_params
  
    return final_params

def _normalize_cursor_field_order(cursor_obj):
    for item in cursor_obj["fields"]:
        if "order" not in item: item["order"] = current_app.config["DEFAULT_SORT_ORDER"]

def _fill_in_paging(search_result, search_params):
    _add_next_page(search_result, search_params)
    _add_prev_page(search_result, search_params)
    search_result.pages["limit"] = search_params["search_limit"]

def _add_next_page(search_result, search_params):
    if len(search_result.results) > search_params["search_limit"]:
        search_result.results.pop() # remove last item from results list to match "search_limit" constraint

        # build next search cursor based on new last item
        next_cursor = _build_next_cursor(search_result.results[-1], search_params["search_cursor"])
        next_cursor_token = util_lib.dict_to_base64_enc(next_cursor)
        search_result.pages["next"] = next_cursor_token

def _add_prev_page(search_result, search_params):
    prev_cursor = _build_prev_cursor(search_params["search_cursor"])
    # cur_cursor_token = util_lib.dict_to_base64_enc(search_params["cursor"])
    # search_result.pages["current"] = cur_cursor_token

def _build_next_cursor(last_result, prev_cursor):
    next_cursor = copy.deepcopy(prev_cursor)
    last_result_dict = last_result.to_dict()

    for item in next_cursor["fields"]:
        item["last_val"] = last_result_dict[item["field"]]

    return next_cursor

def _build_prev_cursor(current_cursor):
    pass