from pymongo import MongoClient, errors
from classes import Entry

_db = None

def get_db():
    global _db

    if _db is None:
        try:
            mongo_client = MongoClient("mongodb://mongoadmin:secret@db:27017/")
            mongo_client.admin.command("ping")
            _db = mongo_client["swal"]
        except errors.PyMongoErrors as e:
            raise ConnectionError(f"Could not connect to MongoDB: {e}")
        except:
            raise ConnectionError(f"Unknown error connecting to MongoDB: {e}")
    
    return _db


def add_entry_to_db(new_entry : Entry):
    db_conn = get_db()
    entries = db_conn["entries"]

    upl_entry = new_entry.to_dict()
    if ("_id" in upl_entry and upl_entry["_id"] is None): del upl_entry["_id"]

    new_entry_id = entries.insert_one(upl_entry).inserted_id
    return new_entry_id