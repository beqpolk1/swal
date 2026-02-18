from classes import Parse_Result
from bson import ObjectId
from bson.errors import InvalidId
import util_lib

def parse_object_id(_id : str) -> Parse_Result:
    parse_result = Parse_Result()

    try:
        ObjectId(_id)
        parse_result.add_data("_id", _id)
    except (InvalidId, TypeError) as e:
        parse_result.add_error(util_lib.INVALID_OBJECT_ID.format(exception = e))

    return parse_result