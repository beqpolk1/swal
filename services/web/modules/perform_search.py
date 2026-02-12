from classes import Search_Result, Entry
from parsers import parse_search_data
from .db_interface import full_search
import util_lib

def perform_search(raw_params) -> list:
    parse_result = parse_search_data(raw_params)

    search_result = Search_Result()
    search_result.add_errors(parse_result.errors)

    if not search_result.has_errors():
        search_params = _build_params(parse_result.result_data)

        try:
          for result in full_search(search_params):
              new_entry = Entry(result, {})
              if result.get("artwork_file"):
                new_entry.artwork_file_name = result.get("artwork_file_name")
                new_entry.artwork_file = True
              search_result.add_result(new_entry)
          
        except Exception as e:
            search_result.add_error(util_lib.GENERAL_SEARCH_EXCEPTION.format(exception=e))
    
    return search_result

def _build_params(parsed_params) -> dict:    
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
    
    return parsed_params