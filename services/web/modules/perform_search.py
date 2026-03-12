from classes import Search_Result, Entry
from parsers import parse_search_string, parse_object_id
from .db_interface import full_search, single_search
from flask import current_app
import util_lib

def perform_search(raw_params, single_mode : bool) -> Search_Result:
    if (single_mode and "_id" in raw_params):
      parse_result = parse_object_id(raw_params.get("_id"))
    else:
      parse_result = parse_search_string(raw_params)

    search_result = Search_Result()
    search_result.add_errors(parse_result.errors)

    if not search_result.has_errors():
        if single_mode:
          search_func = single_search
          search_params = parse_result.result_data
        else:
          search_func = full_search
          search_params = _build_params(parse_result.result_data)

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

def _build_params(parsed_params) -> dict:
    final_params = {}

    if "limit" in parsed_params:
       final_params["limit"] = parsed_params.pop("limit")
       final_params["user_params"] = parsed_params
    
    else:
       final_params["limit"] = current_app.config["DEFAULT_SEARCH_LIMIT"]
       final_params["user_params"] = parsed_params


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

    # sorting
        
    # cursor/pagination
    
    # validate parameters
    
    return final_params