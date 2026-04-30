from .search_cursor import Search_Cursor
from flask import current_app

class Search_Index:
    def __init__(self, fields = [], direction = ""):
        self.fields : list[dict] = fields
        self.direction : str = direction

    def make_search_cursor(self) -> Search_Cursor:
        new_cursor = Search_Cursor()
        self._normalize_field_order()

        for item in self.fields:
            field_data = item.copy()

            # if search is running in reverse, flip sort ordering for each field
            if not(self.dir_is_fwd()):
                if field_data["order"] == current_app.config["ASC_SORT_VAL"]:
                    field_data["order"] = current_app.config["DESC_SORT_VAL"]

                elif field_data["order"] == current_app.config["DESC_SORT_VAL"]:
                    field_data["order"] = current_app.config["ASC_SORT_VAL"]
            
            new_cursor.add_field(field_data)
        
        return new_cursor
    
    def to_dict(self) -> dict:
        return {
            "fields": self.fields,
            "direction": self.direction
        }
    
    @classmethod
    def from_dict(cls, d):
        return cls(fields=d["fields"], direction=d["direction"])

    def has_last_vals(self) -> bool:
        for item in self.fields:
            if ("last_val" in item and item["last_val"] is not None):
                return True
            
        return False
    
    def dir_is_fwd(self) -> bool:
        return self.direction == current_app.config["FWD_SEARCH_VAL"]

    def _normalize_field_order(self):
        for item in self.fields:
            if "order" not in item: item["order"] = current_app.config["DEFAULT_SORT_ORDER"]