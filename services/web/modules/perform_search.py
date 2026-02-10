#from classes import Entry, Parse_Result
from parsers import parse_search_data

def perform_search(raw_params) -> list:
    parse_result = parse_search_data(raw_params)

    if parse_result.has_errors():
        return {"errors": parse_result.errors}
    else:
        return {"entries": parse_result.result_data}

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