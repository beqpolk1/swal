from classes import Search_Result, Entry
from parsers import parse_search_string, parse_object_id
from .db_interface import full_search, single_search
from flask import current_app
import util_lib

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
        parsed_input = parse_object_id(raw_params.get("_id"))
        search_func = single_search
        search_params = parsed_input.result_data

    else:
        parsed_input = parse_search_string(raw_params)
        search_func = full_search
        search_params = _prep_params(parsed_input.result_data)

    search_result = Search_Result()
    search_result.add_errors(parsed_input.errors)

    if not search_result.has_errors():
        try:
            for result in search_func(search_params):
                new_entry = Entry(result, {})

                if result.get("artwork_file"):
                    new_entry.artwork_file_name = result.get("artwork_file_name")
                    new_entry.artwork_file = True

                search_result.add_result(new_entry)
      
        except Exception as e:
            search_result.add_error(util_lib.GENERAL_SEARCH_EXCEPTION.format(exception=e))
  
    return search_result

def _prep_params(parsed_params) -> dict:
    final_params = {}

    if "limit" in parsed_params:
        final_params["limit"] = parsed_params.pop("limit")
    else:
        final_params["limit"] = current_app.config["DEFAULT_SEARCH_LIMIT"]

    if "cursor" in parsed_params:
        final_params["cursor"] = parsed_params.pop("cursor")

        for item in final_params["cursor"]["fields"]:
            if "order" not in item:
                item["order"] = current_app.config["DEFAULT_SORT_ORDER"]
    else:
        final_params["cursor"] = current_app.config["DEFAULT_SEARCH_CURSOR"]

    final_params["search_params"] = parsed_params
  
    return final_params



