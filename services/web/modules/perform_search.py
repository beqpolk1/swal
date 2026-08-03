from classes import Search_Result, Entry, Search_Index
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
        param_func = lambda parsed_params : parsed_params # no parameter processing needed after parsing - echo back result
        search_func = _perform_single_search        
    else:
        parse_func = parse_search_string
        param_func = _prep_search_params
        search_func = _perform_full_search        

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
    search_result.set_limit(search_params["search_limit"])
    
    # special handling for reversing through search results
    search_result.flip_results = (search_params["search_index"].direction == current_app.config["REV_SEARCH_VAL"])

    for db_result in full_search(search_params):
        search_result.add_result(_db_result_to_entry(db_result))

    _fill_in_paging(search_result, search_params)

    return search_result

# TODO: rework entry structure to avoid this
### TEMP FIX
def _db_result_to_entry(db_result) -> Entry:
    new_entry = Entry(db_result, {})

    if db_result.get("artwork_file"):
        new_entry.artwork_file_name = db_result.get("artwork_file_name")
        new_entry.artwork_file = True

    return new_entry
###

def _prep_search_params(parsed_params) -> dict:
    final_params = {}

    if "limit" in parsed_params:
        final_params["search_limit"] = parsed_params.pop("limit")
    else:
        final_params["search_limit"] = current_app.config["DEFAULT_SEARCH_LIMIT"]

    final_params["db_limit"] = final_params["search_limit"] + 1
    final_params["skip"] = 0

    if "search_index" in parsed_params:
        final_params["search_index"] = parsed_params.pop("search_index")
    else:
        new_index = Search_Index()
        new_index.fields = current_app.config["DEFAULT_SEARCH_FIELDS"]
        new_index.direction = current_app.config["FWD_SEARCH_VAL"]
        final_params["search_index"] = new_index

    final_params["search_params"] = parsed_params
  
    return final_params

def _fill_in_paging(search_result, search_params):
    _add_next_page(search_result, search_params["search_index"])
    _add_prev_page(search_result, search_params["search_index"])

    search_result.pages["addl"] = search_params["search_params"]

    # TODO: standardize attribute name between model (entry) and view (template)
    ### TEMPORARY UGLY FIX
    if ("is_starred" in search_result.pages["addl"]):
        search_result.pages["addl"]["starred"] = search_result.pages["addl"]["is_starred"]
    ### END FIX

def _add_next_page(search_result, search_index):
    if ((search_index.dir_is_fwd() and search_result.has_more()) 
        or not(search_index.dir_is_fwd())):

        # build next search index based on new last item
        next_index = _build_index(search_result.get_results()[-1], search_index, current_app.config["FWD_SEARCH_VAL"])
        next_index_token = util_lib.dict_to_base64_enc(next_index.to_dict())
        search_result.pages["next"] = next_index_token

def _add_prev_page(search_result, search_index):
    if ((not(search_index.dir_is_fwd()) and search_result.has_more())
        or (search_index.dir_is_fwd() and search_index.has_last_vals())):

        # build prev search index based on new first item
        prev_index = _build_index(search_result.get_results()[0], search_index, current_app.config["REV_SEARCH_VAL"])
        prev_cursor_token = util_lib.dict_to_base64_enc(prev_index.to_dict())
        search_result.pages["prev"] = prev_cursor_token

def _build_index(last_vals_result : Entry, cur_index : Search_Index, direction : str):
    new_index = Search_Index()
    new_index.direction = direction
    new_index.fields = copy.deepcopy(cur_index.fields)
    last_vals_dict = last_vals_result.to_dict()

    for item in new_index.fields:
        item["last_val"] = last_vals_dict[item["field"]]

    return new_index