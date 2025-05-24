from pymongo import MongoClient, errors
from classes import Entry

_db = None

def get_db(db_name : str):
    global _db

    if _db is None:
        try:
            mongo_client = MongoClient("mongodb://mongoadmin:secret@db:27017/")
            mongo_client.admin.command("ping")
        except errors.PyMongoErrors as e:
            raise ConnectionError(f"Could not connect to MongoDB: {e}")
        except:
            raise ConnectionError(f"Unknown error connecting to MongoDB: {e}")
            _db = mongo_client[db_name]
    
    return _db


def add_entry_to_db(new_entry : Entry):
    upl_entry = new_entry.to_dict()
    if ("_id" in upl_entry and upl_entry["_id"] is None): del upl_entry["_id"]

    try:
        db_conn = get_db("swal")
        entries = db_conn["entries"]
        new_entry_id = entries.insert_one(upl_entry).inserted_id
    except ConnectionError as e:
        raise e
    except Exception as e:
        raise Exception("Other exception adding entry to DB") from e
    
    return new_entry_id