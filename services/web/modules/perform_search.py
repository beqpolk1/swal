from classes import Search_Result
from parsers import parse_search_data

def perform_search(raw_params) -> list:
    parse_result = parse_search_data(raw_params)

    search_result = Search_Result()
    search_result.add_errors(parse_result.errors)

    if search_result.has_errors():
        return {"errors": search_result.errors}
    else:
        search_result.add_results(parse_result.result_data.items())
        return {"entries": search_result.results}

def _build_params(raw_params) -> dict:    
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
    
    pass