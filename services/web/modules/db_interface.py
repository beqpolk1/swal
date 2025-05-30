from pymongo import MongoClient, errors
from classes import Entry
from flask import current_app
import socket

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