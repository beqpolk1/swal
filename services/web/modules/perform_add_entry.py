from classes import Entry
from classes import Job_Status
from validators import validate_entry
import os, uuid, ftplib

def perform_add_entry(form_data, files_data) -> Job_Status:
    new_entry = Entry(form_data, files_data)

    result = Job_Status()
    result.errors = validate_entry(new_entry)

    if (len(result.errors) == 0):
        result.status = "entry built"

        if (new_entry.artwork_file):
            new_entry.artwork_file_name = _perform_artwork_add(new_entry.artwork_file_name, new_entry.artwork_file)
            result.status = "artwork uploaded"

        _perform_db_add(new_entry)
        result.status = str(new_entry)
        result.success = True
    else:
        result.status = "failed"

    return result

def _perform_artwork_add(filename : str, file) -> str:
    new_filename = str(uuid.uuid4()) + filename[filename.rfind("."):]
    new_filepath = os.path.join('/var/tmp', new_filename)

    file.save(new_filepath)

    ftp_server = ftplib.FTP("nginx", "swal_image", "swallowth3p4ssword")
    ftp_server.cwd("img")

    with open(new_filepath, "rb") as upl_file:
        ftp_server.storbinary(f"STOR {new_filename}", upl_file)
    
    ftp_server.quit
    os.remove(new_filepath)

    return new_filename

def _perform_db_add(new_entry : Entry):
    pass

