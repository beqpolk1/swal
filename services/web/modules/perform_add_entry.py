from .entry import Entry

def perform_add_entry(newEntry : Entry):
    if (_perform_validation(newEntry)):
        return str(newEntry)

def _perform_validation(newEntry : Entry):
    return True

def _perform_db_add(newEntry : Entry):
    pass