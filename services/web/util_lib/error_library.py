####### ENTRY ADD MESSAGES #######
GENERAL_EXCEPTION = "Exception adding entry: {exception}"

TEMP_FILE_NOT_FOUND = "Could not find temp file {path}"
TEMP_FILE_DELETE_PERM = "Do not have permissions to delete temp file {filename}"
OS_ERROR_DELETING_FILE = "OSError deleting temp file {path}"
UNKNOWN_DELETE_ERROR = "Other exception deleting temp file {path}"

ARTWORK_SAVE_MISSING = "{filepath} does not exist"
ARTWORK_SAVE_NO_PERMISSION = "Do not have permissions to write to {filepath}"
ARTWORK_SAVE_OS_ERROR = "OSError accessing filesystem to save temp artwork file"
ARTWORK_SAVE_OTHER_ERROR = "Other exception saving temp artwork file: {exception}"

FTP_NETWORK_ERROR = "Network/connection error connecting to FTP server"
FTP_PERMANENT_ERROR = "Permanent FTP error (e.g. login failed)"
FTP_GENERAL_ERROR = "General FTP error"
FTP_OTHER_ERROR = "Other exception performing FTP op on artwork file: {exception}"

####### ENTRY VALIDATION MESSAGES #######
artist_must_be_string = "Artist name must be a string"
artist_too_long = "Artist name must be 255 characters or less"
artist_required = "Artist name must be present"

album_must_be_string = "Album name must be a string"
album_too_long = "Album name must be 500 characters or less"
album_required = "Album name must be present"

release_year_must_be_int = "Release year must be an integer"
release_year_range = "Release year must be between 1900 and 2100"
release_year_required = "Release year must be present"

genre_must_be_string = "Genre must be a string"
genre_too_long = "Genre must be 255 characters or less"

interest_level_must_be_int = "Interest level must be an integer"
interest_level_range = "Interest level must be 1, 2, or 3"

starred_invalid = "Starred must be true or false"

artwork_filename_must_be_string = "Artwork file name must be a string"
artwork_file_mismatch = "Artwork file name and artwork file must both be present"

obtained_invalid = "Is obtained must be true or false"
obtained_required = "Is obtained must be present"

link_must_be_string = "Link must be a string"
link_invalid_format = "Link must be in a valid URL format"