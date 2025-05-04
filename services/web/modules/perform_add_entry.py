from classes import Entry, Job_Status
from validators import validate_entry_data
from .db_interface import add_entry_to_db
import os, uuid, ftplib

def perform_add_entry(form_data, files_data) -> Job_Status:
    result = Job_Status()
    result.errors = validate_entry_data(form_data, files_data)

    if (len(result.errors) == 0):
        new_entry = Entry(form_data, files_data)
        result.status = "entry built"

        if (new_entry.artwork_file):
            new_entry.artwork_file_name = _perform_artwork_add(new_entry.artwork_file_name, new_entry.artwork_file, result)
            result.status = "artwork uploaded"

        new_entry_id = _perform_db_add(new_entry)
        result.status = "added to DB"
        result.new_img = new_entry.artwork_file_name
        result.success = True
    else:
        result.status = "failed"

    return result

def _perform_artwork_add(filename : str, file, result : Job_Status) -> str:
    new_filename = str(uuid.uuid4()) + filename[filename.rfind("."):]
    new_filepath = os.path.join('/var/tmp', new_filename)

    file.save(new_filepath)
    result.status = "artwork file saved locally"

    ftp_server = ftplib.FTP("nginx", "swal_image", "swallowth3p4ssword")
    ftp_server.cwd("img")

    with open(new_filepath, "rb") as upl_file:
        ftp_server.storbinary(f"STOR {new_filename}", upl_file)
        result.status = "artwork transferred to server"
    ftp_server.quit

    os.remove(new_filepath)
    result.status = "local artwork file cleaned"

    return new_filename

def _perform_db_add(new_entry : Entry):
    return add_entry_to_db(new_entry)

