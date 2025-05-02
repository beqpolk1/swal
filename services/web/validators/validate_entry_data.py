import re
import util_lib

def validate_entry_data(entry_data, entry_files) -> list:
    errors = []

    _validate_artist(entry_data.get("artist") or None, errors)
    _validate_album(entry_data.get("album") or None, errors)
    _validate_release_year(entry_data.get("release_year") or None, errors)
    _validate_genre(entry_data.get("genre") or None, errors)
    _validate_interest_level(entry_data.get("interest_level"), errors)
    _validate_starred(entry_data.get("is_starred"), errors)
    _validate_artwork(entry_files.get("artwork_file").filename or None, entry_files.get("artwork_file"), errors)
    _validate_obtained(entry_data.get("is_obtained"), errors)
    _validate_link(entry_data.get("link") or None, errors)

    return errors
    
def _validate_artist(artist, errors):
    if (artist not in [None, ""]):
        if (not isinstance(artist, str)):
            try:
                artist = str(artist)
            except:
                errors.append({"code": "A01", "msg": "Artist name must be a string"})
                return
               
        if (len(artist) > 255):
            errors.append({"code": "A02", "msg": "Artist name must be 255 characters or less"})
    else:
        errors.append({"code": "A03", "msg": "Artist name must be present"})

def _validate_album(album, errors):
    if (album not in [None, ""]):
        if (not isinstance(album, str)):
            try:
                album = str(album)
            except:
                errors.append({"code": "A04", "msg": "Album name must be a string"})
                return
            
        if (len(album) > 500):
            errors.append({"code": "A05", "msg": "Album name must be 500 characters or less"})
    else:
        errors.append({"code": "A06", "msg": "Album name must be present"})

def _validate_release_year(release_year, errors):
    if (release_year != None):
        if (not isinstance(release_year, int)):
            try:
                release_year = int(release_year)
            except:
                errors.append({"code": "A07", "msg": "Release year must be an integer"})
                return
            
        if (release_year < 1900 or release_year > 2100):
            errors.append({"code": "A08", "msg": "Release year must be between 1900 and 2100"})  
    else:
        errors.append({"code": "A09", "msg": "Release year must be present"})

def _validate_genre(genre, errors):  
    if ("genre" != None):
        if (not isinstance(genre, str)):
            try:
                genre = str(genre)
            except:
                errors.append({"code": "A10", "msg": "Genre must be a string"})
                return
            
        if (len(genre) > 255):
            errors.append({"code": "A11", "msg": "Genre must be 255 characters or less"})

def _validate_interest_level(interest_level, errors):
    if (interest_level != None):
        if (not isinstance(interest_level, int)):
            try:
                interest_level = int(interest_level)
            except:
                errors.append({"code": "A12", "msg": "Interest level must be an integer"})
                return
            
        if (interest_level < 1 or interest_level > 3):
            errors.append({"code": "A13", "msg": "Interest level must be 1, 2, or 3"})

def _validate_starred(starred, errors):
    if (starred != None):
        if (not isinstance(starred, bool)):
            try:
                starred = util_lib.str_to_bool(starred)
            except:
                errors.append({"code": "A14", "msg": "Starred must be true or false"})

def _validate_artwork(artwork, artwork_file, errors):
    if (artwork != None):
        if (not isinstance(artwork, str)):
            try:
                artwork = str(artwork)
            except:
                errors.append({"code": "A19", "msg": "artwork file name must be a string"})
    
    if ((artwork != None and not artwork_file) or (artwork == None and artwork_file)):
        errors.append({"code": "A20", "msg": "artwork file name and artwork file must both be present"})

def _validate_obtained(obtained, errors):
    if (obtained != None):
        if (not isinstance(obtained, bool)):
            try:
                obtained = util_lib.str_to_bool(obtained)
            except:
                errors.append({"code": "A15", "msg": "Is obtained must be true or false"})
    else:
        errors.append({"code": "A16", "msg": "Is obtained must be present"})

def _validate_link(link, errors):
    url_pattern = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
    
    if (link != None):
        if (not isinstance(link, str)):
            try:
                link = str(link)
            except:
                errors.append({"code": "A18", "msg": "Link must be a string"})
                return
            
        if (not re.fullmatch(url_pattern, link)):
            errors.append({"code": "A17", "msg": "Link must be in a valid URL format"})