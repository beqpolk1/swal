from .error_library import *
import base64, json

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

def get_str_or_none_2(d: dict, key: str) -> str | None:
    val = d.get(key)
    if val is None: return None
    
    val = val.strip()
    if val == "": return None

    return val

def get_int_or_none(d: dict, key: str):
    val = d.get(key) or None
    return int(val) if val is not None else None

def get_int_or_none_2(d: dict, key: str):
    val = get_str_or_none_2(d, key)
    if val is None: return None
    return int(val)

def get_bool_or_none(d: dict, key: str):
    val = d.get(key) or None
    return str_to_bool(val) if val is not None else None

def get_bool_or_none_2(d: dict, key: str):
    val = get_str_or_none_2(d, key)
    if val is None: return None

    return str_to_bool(val)

def base64_enc_to_dict(base64_enc: str) -> dict:
    decoded_bytes = base64.urlsafe_b64decode(base64_enc + "===")
    decoded_text = decoded_bytes.decode("utf-8")
    obj = json.loads(decoded_text)
    return obj