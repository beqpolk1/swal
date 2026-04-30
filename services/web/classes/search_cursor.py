from dataclasses import field
from flask import current_app
import util_lib

# cursor structure:
# {
  # fields: [
    # { field: "artist", order: "asc", last_val: <val> },
    # { field: "album", order: "asc", last_val: <val> },
    # { field: "_id", order: "asc", last_val: <val> }
#   ]
# }

class Search_Cursor:
    def __init__(self):
        self.fields : list[dict] = []

    def add_field(self, new_field : dict):
        self._validate_field_structure(new_field)
        self._validate_field_content(new_field)

        self.fields.append(new_field)

    def _validate_field_structure(self, new_field : dict):
        if not isinstance(new_field, dict):
            raise Exception(util_lib.CURSOR_FIELD_ITEM_NOT_DICT.format(element = new_field))

        if not "field" in new_field:
            raise Exception(util_lib.CURSOR_FIELD_ITEM_MISSING_FIELD.format(element = new_field))

        if "order" in new_field:
            new_field["order"] = new_field["order"].lower()             

    def _validate_field_content(self, new_field : dict):
        if "order" in new_field and new_field["order"] not in current_app.config["VALID_SORT_ORDER"]:
            raise Exception(util_lib.CURSOR_FIELD_ITEM_INVALID_ORDER.format(element = new_field))  
    