from classes import Entry, Job_Status
from validators import validate_entry_data
from .db_interface import add_entry_to_db
import util_lib
import os, uuid, ftplib, socket

def perform_add_entry(form_data, files_data) -> Job_Status:
    result = Job_Status()

    try:
        result.add_errors(validate_entry_data(form_data, files_data))

        if (len(result.errors) == 0):
            try:
                new_entry = Entry(form_data, files_data)
                result.update_status("entry built")
            except Exception as e:
                result.update_status("failed to build entry")
                raise e from e

            if (new_entry.artwork_file):
                try:
                    new_entry.artwork_file_name = _perform_artwork_add(new_entry.artwork_file_name, new_entry.artwork_file, result)
                    result.update_status("artwork uploaded")
                except Exception as e:
                    result.update_status("failed to process and upload artwork file")
                    raise e from e

            try:
                new_entry._id = str(_perform_db_add(new_entry))
                result.update_status("new entry added to DB")
            except Exception as e:
                if (new_entry.artwork_file):
                    _cleanup_artwork_file(new_entry.artwork_file_name, result)
                result.update_status("failed to add entry to database")
                raise e from e
            
            #boilerplate/negligible
            result.update_status(new_entry._id)
            result.new_img = new_entry.artwork_file_name
            result.success = True
        else:
            result.update_status("new entry data failed validation")
    except Exception as e:
        result.add_error(util_lib.GENERAL_EXCEPTION.format(exception = e))

    return result

def _perform_artwork_add(filename : str, file, result : Job_Status) -> str:
    #generate filename and save a temp version locally
    try:
        new_filename = str(uuid.uuid4()) + filename[filename.rfind("."):]
        new_filepath = os.path.join('/var/tmp', new_filename)

        file.save(new_filepath)
        result.update_status("artwork file saved locally")

    except FileNotFoundError as e:
        raise Exception(util_lib.ARTWORK_SAVE_MISSING.format(filepath = new_filepath)) from e
    except PermissionError as e:
        raise Exception(util_lib.ARTWORK_SAVE_NO_PERMISSION.format(filepath = new_filepath)) from e
    except OSError as e:
        raise Exception(util_lib.ARTWORK_SAVE_OS_ERROR) from e
    except Exception as e:
        raise Exception(util_lib.ARTWORK_SAVE_OTHER_ERROR.format(exception = e)) from e        

    #FTP local temp file to nginx server for static storage
    try:
        ftp_server = ftplib.FTP("nginx", "swal_image", "swallowth3p4ssword")
        ftp_server.cwd("img")
        
        with open(new_filepath, "rb") as upl_file:
            ftp_server.storbinary(f"STOR {new_filename}", upl_file)
            result.update_status("artwork transferred to static server")
        ftp_server.quit

    except (socket.gaierror, socket.timeout, ConnectionRefusedError) as e:
        raise Exception(util_lib.FTP_NETWORK_ERROR) from e
    except ftplib.error_perm as e:
        raise Exception(util_lib.FTP_PERMANENT_ERROR) from e
    except ftplib.all_errors as e:
        raise Exception(util_lib.FTP_GENERAL_ERROR) from e
    except Exception as e:
        raise Exception(util_lib.FTP_OTHER_ERROR.format(exception = e)) from e
    
    finally:
        #cleanup local temp file
        try:
            os.remove(new_filepath)
            result.update_status("local artwork file cleaned")

        except FileNotFoundError as e:
            result.add_error(util_lib.TEMP_FILE_NOT_FOUND.format(path = new_filepath))
        except PermissionError as e:
            result.add_error(util_lib.TEMP_FILE_DELETE_PERM.format(filename = new_filename))
        except OSError as e:
            result.add_error(util_lib.OS_ERROR_DELETING_FILE.format(path = new_filepath))
        except Exception as e:
            result.add_error(util_lib.UNKNOWN_DELETE_ERROR.format(path = new_filepath))

    return new_filename

def _perform_db_add(new_entry : Entry):
    return add_entry_to_db(new_entry)

def _cleanup_artwork_file(filename : str, result : Job_Status):
    try:
        ftp_server = ftplib.FTP("nginx", "swal_image", "swallowth3p4ssword")
        ftp_server.cwd("img")
        ftp_server.delete(filename)
        ftp_server.quit
        result.update_status("artwork removed from static server")

    except (socket.gaierror, socket.timeout, ConnectionRefusedError) as e:
        result.add_error(util_lib.FTP_NETWORK_ERROR)
        result.update_status("failed to cleanup artwork from static server")
    except ftplib.error_perm as e:
        result.add_error(util_lib.FTP_PERMANENT_ERROR)
        result.update_status("failed to cleanup artwork from static server")
    except ftplib.all_errors as e:
        result.add_error(util_lib.FTP_GENERAL_ERROR)
        result.update_status("failed to cleanup artwork from static server")
    except Exception as e:
        result.add_error(util_lib.FTP_OTHER_ERROR.format(exception = e))
        result.update_status("failed to cleanup artwork from static server")