from .error_library import *

def str_to_bool(val):
    if isinstance(val, bool):
        return val
    
    if isinstance(val, str):
        val = val.strip().lower()
        if val in ("true", "1", "yes", "on"):
            return True
        elif val in ("false", "0", "no", "off"):
            return False
        
    raise ValueError(INVALID_BOOL.format(value = val))

def get_str_or_none(d: dict, key: str):
    val = d.get(key) or None
    return str(val) if val not in ["", None] else None

def get_int_or_none(d: dict, key: str):
    val = d.get(key) or None
    return int(val) if val is not None else None

def get_bool_or_none(d: dict, key: str):
    val = d.get(key) or None
    return str_to_bool(val) if val is not None else None