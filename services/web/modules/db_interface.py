from pymongo import MongoClient
from classes import Entry

mongo_client = MongoClient("mongodb://mongoadmin:secret@db:27017/")
db = mongo_client["swal"]

def add_entry_to_db(new_entry : Entry):
    entries = db["entries"]

    new_entry_id = entries.insert_one(new_entry.to_dict()).inserted_id
    return new_entry_id