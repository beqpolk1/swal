from pymongo import MongoClient, errors
from classes import Entry
from flask import current_app
import socket, re

_client = None
_db = None

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
       collection_filter = _build_query(params)
    except Exception as e:
       raise Exception(f"Exception constructing search query: {e}") from e
    
    try:
        db_conn = get_db(current_app.config["MONGO_DB_NAME"])
        entries = db_conn[current_app.config["MONGO_ENTRIES_COLL"]]
        search_results = list(entries.find(collection_filter))
    except ConnectionError as e:
        raise e from e
    except Exception as e:
        raise Exception(f"Other exception adding entry to DB: {e}") from e
    
    return search_results

def _build_query(params : dict):
    filter_dict = {}

    if len(params) > 0:
        and_list = []

        # literal text match search on supported fields
        if ("text_search" in params):
            search_or_list = []
            searchable_fields = ["artist", "album", "genre", "link"]
            search_dict = { "$regex": re.escape(params["text_search"]), "$options": "i"}

            for field in searchable_fields:
                search_or_list.append({ field: search_dict })

            and_list.append({"$or": search_or_list})

        # boolean match search on supported fields
        boolean_fields = ["is_starred", "obtained"]
        for field in boolean_fields:
            if (field in params):
                and_list.append({field: params[field]})

        filter_dict["$and"] = and_list

    return filter_dict