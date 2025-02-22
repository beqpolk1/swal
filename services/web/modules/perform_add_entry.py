from classes import Entry
from classes import Job_Status
from validators import validate_entry

def perform_add_entry(form_data : dict) -> Job_Status:
    new_entry = _build_entry(form_data)

    result = Job_Status()
    result.errors = validate_entry(new_entry)

    if (len(result.errors) == 0):
        result.status = "entry built"

        _perform_db_add(new_entry)
        result.status = str(new_entry)
    else:
        result.status = "failed"

    return result

def _build_entry(form_data : dict) -> Entry:
    new_entry = Entry(form_data["artist"] if "artist" in form_data and len(form_data["artist"]) > 0 else None, 
                    form_data["album"] if "album" in form_data and len(form_data["album"]) > 0  else None, 
                    form_data["release_year"] if "release_year" in form_data and len(form_data["release_year"]) > 0  else None, 
                    form_data["genre"] if "genre" in form_data and len(form_data["genre"]) > 0 else None, 
                    form_data["interest_level"] if "interest_level" in form_data else None, 
                    form_data["is_starred"] if "is_starred" in form_data else None, 
                    form_data["is_obtained"] if "is_obtained" in form_data else None, 
                    form_data["link"] if "link" in form_data and len(form_data["link"]) > 0 else None)
    return new_entry

def _perform_db_add(new_entry : Entry):
    pass

