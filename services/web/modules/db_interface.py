from pymongo import MongoClient, errors, collation
import pymongo
from classes import Entry
from flask import current_app
from bson import ObjectId
import socket, re

from pprint import pprint

_client = None
_db = None
_case_insensitive = collation.Collation(locale='en', strength=2)

def get_db(db_name : str):
    global _db, _client
    
    if _client is None:
        _client = MongoClient(current_app.config["MONGO_CONN_STR"], serverSelectionTimeoutMS=current_app.config["MONGO_CONN_TIMEOUT"])

    try:
        _client.admin.command("ping")
        if _db is None: _db = _client[db_name]
    except (errors.PyMongoError, socket.gaierror, ConnectionRefusedError, socket.timeout, OSError) as e:
        raise ConnectionError("Could not connect to MongoDB") from e

    return _db

def add_entry_to_db(new_entry : Entry):
    upl_entry = new_entry.to_dict()
    if ("_id" in upl_entry and upl_entry["_id"] is None): del upl_entry["_id"]

    try:
        db_conn = get_db(current_app.config["MONGO_DB_NAME"])
        entries = db_conn[current_app.config["MONGO_ENTRIES_COLL"]]

        new_entry_id = entries.insert_one(upl_entry).inserted_id

    except ConnectionError as e:
        raise e from e
    except Exception as e:
        raise Exception(f"Other exception adding entry to DB: {e}") from e
    
    return new_entry_id

def full_search(params : dict):
    try:
       find_filter = _build_filter(params["search_params"], params["cursor"])
       search_limit = params["limit"]
       sort_list = _build_sort_list(params["cursor"])
       print(f"[DEBUG] sort_list = {pprint(sort_list)}", flush=True)

    except Exception as e:
       raise Exception(f"Exception constructing search query: {e}") from e
    
    try:
        db_conn = get_db(current_app.config["MONGO_DB_NAME"])
        entries = db_conn[current_app.config["MONGO_ENTRIES_COLL"]]

        results_cursor = entries.find(find_filter).limit(search_limit).sort(sort_list).collation(_case_insensitive)

    except ConnectionError as e:
        raise e from e
    except Exception as e:
        raise Exception(f"Other exception performing search: {e}") from e
    
    return results_cursor

def single_search(params : dict):
    try:
        db_conn = get_db(current_app.config["MONGO_DB_NAME"])
        entries = db_conn[current_app.config["MONGO_ENTRIES_COLL"]]
        result = entries.find({"_id": ObjectId(params.get("_id"))})
    except ConnectionError as e:
        raise e from e
    except Exception as e:
        raise Exception(f"Other exception finding document: {e}") from e
    
    return result



def _build_filter(search_params : dict, cursor):
    final_list = []
    
    #print(f"[DEBUG] cursor = {pprint(cursor)}", flush=True)

    final_list.extend(_build_search_params(search_params))
    final_list.extend(_build_cursor_params(cursor))

    filter_dict = { }
    if len(final_list) > 0: filter_dict["$and"] = final_list

    #print(f"[DEBUG] filter_dict = {pprint(filter_dict)}", flush=True)
    return filter_dict

def _build_search_params(search_params: dict) -> list:
    and_list = []

    if len(search_params) > 0:
        # literal text match search on supported fields
        if ("text_search" in search_params):
            search_or_list = []
            searchable_fields = ["artist", "album", "genre", "link"]
            search_dict = { "$regex": re.escape(search_params["text_search"]), "$options": "i"}

            for field in searchable_fields:
                search_or_list.append({ field: search_dict })

            and_list.append({"$or": search_or_list})

        # boolean match search on supported fields
        boolean_fields = ["is_starred", "obtained"]
        for field in boolean_fields:
            if (field in search_params):
                and_list.append({field: search_params[field]})

    return and_list

def _build_cursor_params(cursor) -> list:
    or_list = []
    prev_fields = []

    for item in cursor["fields"]:
        if "last_val" in item:
            # ...and (
            # artist > last_val
            # or (artist = last_val and album > last_val)
            # or (artist = last_val and album = last_val and _id >  last_val)
            # )
            
            field_and_list = []

            for prev_field in prev_fields:
                field_and_list.append( { prev_field["field"] : prev_field["last_val"] } )
            
            field_and_list.append({ item["field"] : { "$gt" if item["order"] == "asc" else "$lt": item["last_val"]} })

            prev_fields.append(item)            
            or_list.append({ "$and": field_and_list })
    
    ret_list = []
    if len(or_list) > 0: ret_list.append({ "$or": or_list })
    return ret_list

# cursor structure:
# {
  # fields: [
    # { field: "artist", order: "asc", last_val: <val> },
    # { field: "album", order: "asc", last_val: <val> },
    # { field: "_id", order: "asc", last_val: <val> }
  # ]
# }

def _build_sort_list(cursor) -> list:
    sort_list = []

    for item in cursor["fields"]:
        sort_list.append(( item["field"], pymongo.ASCENDING if item["order"] == "asc" else pymongo.DESCENDING ))

    return sort_list