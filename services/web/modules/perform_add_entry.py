from classes import Entry
from classes import Job_Status
from validators import validate_entry

def perform_add_entry(form_data, files_data) -> Job_Status:
    new_entry = Entry(form_data, files_data)

    result = Job_Status()
    result.errors = validate_entry(new_entry)

    if (len(result.errors) == 0):
        result.status = "entry built"

        _perform_db_add(new_entry)
        result.status = str(new_entry)
        result.success = True
    else:
        result.status = "failed"

    return result

def _perform_db_add(new_entry : Entry):
    pass

