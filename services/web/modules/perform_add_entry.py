from classes import Entry, Job_Status
from validators import validate_entry_data
from .db_interface import add_entry_to_db
import os, uuid, ftplib, socket

def perform_add_entry(form_data, files_data) -> Job_Status:
    result = Job_Status()

    try:
        result.errors = validate_entry_data(form_data, files_data)

        if (len(result.errors) == 0):
            try:
                new_entry = Entry(form_data, files_data)
                result.status = "entry built"
            except Exception as e:
                result.status = "failed to build entry"
                raise e from e

            if (new_entry.artwork_file):
                try:
                    new_entry.artwork_file_name = _perform_artwork_add(new_entry.artwork_file_name, new_entry.artwork_file, result)
                    result.status = "artwork uploaded"
                except Exception as e:
                    result.status = "failed to process and upload artwork file"
                    raise e from e
            try:
                new_entry._id = str(_perform_db_add(new_entry))
                result.status = "added to DB"
            except Exception as e:
                result.status = "failed to add entry to database"
                raise e from e
            
            #boilerplate/negligible
            result.status = new_entry._id
            result.new_img = new_entry.artwork_file_name
            result.success = True
        else:
            result.status = "failed"
    except Exception as e:
        result.status = "failed"
        result.errors.append({"code": "AEX05", "msg": f"Exception adding entry: {e}"})

    return result

def _perform_artwork_add(filename : str, file, result : Job_Status) -> str:
    #generate filename and save a temp version locally
    try:
        new_filename = str(uuid.uuid4()) + filename[filename.rfind("."):]
        new_filepath = os.path.join('/var/tmp', new_filename)

        file.save(new_filepath)
        result.status = "artwork file saved locally"

    except FileNotFoundError as e:
        raise Exception(f"{new_filepath} does not exist") from e
    except PermissionError as e:
        raise Exception(f"Do not have permissions to write to {new_filepath}") from e
    except OSError as e:
        raise Exception("OSError accessing filesystem to save temp artwork file") from e
    except Exception as e:
        raise Exception("Other exception saving temp artwork file") from e        

    #FTP local temp file to nginx server for static storage
    try:
        ftp_server = ftplib.FTP("nginx", "swal_image", "swallowth3p4ssword")
        ftp_server.cwd("img")
        
        with open(new_filepath, "rb") as upl_file:
            ftp_server.storbinary(f"STOR {new_filename}", upl_file)
            result.status = "artwork transferred to server"
        ftp_server.quit

    except (socket.gaierror, socket.timeout, ConnectionRefusedError) as e:
        raise Exception("Network/connection error connecting to FTP server") from e
    except ftplib.error_perm as e:
        raise Exception("Permanent FTP error (e.g., login failed)") from e
    except ftplib.all_errors as e:
        raise Exception("General FTP error") from e
    except Exception as e:
        raise Exception("Other exception transferring artwork file") from e
    
    finally:
        #cleanup local temp file
        try:
            os.remove(new_filepath)
            result.status = "local artwork file cleaned"

        except FileNotFoundError:
            result.errors.append({"code": "AEX01", "msg": f"Could not find temp file {new_filepath}"})
        except PermissionError:
            result.errors.append({"code": "AEX02", "msg": f"Do not have permissions to delete temp file {new_filename}"})
        except OSError as e:
            result.errors.append({"code": "AEX03", "msg": f"OSError deleting temp file {new_filepath}"})
        except Exception as e:
            result.errors.append({"code": "AEX04", "msg": f"Ohter exception deleting temp file {new_filepath}"})

    return new_filename

def _perform_db_add(new_entry : Entry):
    return add_entry_to_db(new_entry)

