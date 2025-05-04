from pymongo import MongoClient
from classes import Entry

mongo_client = MongoClient("mongodb://mongoadmin:secret@db:27017/")
db = mongo_client["swal"]

def add_entry_to_db(new_entry : Entry):
    entries = db["entries"]

    upl_entry = new_entry.to_dict()
    if ("_id" in upl_entry and upl_entry["_id"] is None): del upl_entry["_id"]

    new_entry_id = entries.insert_one(upl_entry).inserted_id
    return new_entry_id