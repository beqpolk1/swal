####### SEARCH/FILTER VALIDATION MESSAGES #######
GENERAL_SEARCH_EXCEPTION = "Exception performing search: {exception}"

SEARCH_PARSE_EXCEPTION = "Exception parsing {param} parameter: {exception}"
SEARCH_TEXT_TOO_SHORT = "Text search string must be {length} characters or more"
SEARCH_TEXT_TOO_LONG = "Text search string must be {length} characters or less"

SEARCH_LIMIT_OUT_OF_BOUNDS = "Limit on search results must be more than {min} and less than {max}"

INVALID_OBJECT_ID = "Exception parsing _id value: {exception}"

####### ENTRY VALIDATION MESSAGES #######
ARTIST_MUST_BE_STRING = "Artist name must be a string"
ARTIST_TOO_LONG = "Artist name must be {length} characters or less"
ARTIST_REQUIRED = "Artist name must be present"

ALBUM_MUST_BE_STRING = "Album name must be a string"
ALBUM_TOO_LONG = "Album name must be {length} characters or less"
ALBUM_REQUIRED = "Album name must be present"

RELEASE_YEAR_MUST_BE_INT = "Release year must be an integer"
RELEASE_YEAR_RANGE = "Release year must be between {min_year} and {max_year}"
RELEASE_YEAR_REQUIRED = "Release year must be present"

GENRE_MUST_BE_STRING = "Genre must be a string"
GENRE_TOO_LONG = "Genre must be {length} characters or less"

INTEREST_LEVEL_MUST_BE_INT = "Interest level must be an integer"
INTEREST_LEVEL_RANGE = "Interest level must be one of {valid_levels}"

STARRED_INVALID = "Starred must be true or false"

ARTWORK_FILENAME_MUST_BE_STRING = "Artwork file name must be a string"
ARTWORK_FILE_MISMATCH = "Artwork file name and artwork file must both be present"

OBTAINED_INVALID = "Is obtained must be true or false"
OBTAINED_REQUIRED = "Is obtained must be present"

LINK_MUST_BE_STRING = "Link must be a string"
LINK_INVALID_FORMAT = "Link must be in a valid URL format"

####### ENTRY ADD MESSAGES #######
GENERAL_ADD_EXCEPTION = "Exception adding entry: {exception}"

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

####### TEMPLATE MESSAGES #######
GENERAL_TEMPLATE_EXCEPTION = "Exception rendering template: {exception}"

####### UTIL MESSAGES #######
INVALID_BOOL = "Invalid boolean value: {value}"