import re
import util_lib

def validate_entry_data(entry_data, entry_files) -> list:
    errors = []

    for func in [
        lambda: _validate_artist(entry_data.get("artist") or None),
        lambda: _validate_album(entry_data.get("album") or None),
        lambda: _validate_release_year(entry_data.get("release_year") or None),
        lambda: _validate_genre(entry_data.get("genre") or None),
        lambda: _validate_interest_level(entry_data.get("interest_level")),
        lambda: _validate_starred(entry_data.get("is_starred")),
        lambda: _validate_artwork(
            entry_files.get("artwork_file").filename or None,
            entry_files.get("artwork_file")
        ),
        lambda: _validate_obtained(entry_data.get("is_obtained")),
        lambda: _validate_link(entry_data.get("link") or None)
    ]:
        result = func()
        if result:
            errors.append(result)

    return errors

def _validate_artist(artist):
    if artist not in [None, ""]:
        try:
            artist = str(artist)
        except:
            return util_lib.artist_must_be_string
        if len(artist) > 255:
            return util_lib.artist_too_long
    else:
        return util_lib.artist_required

def _validate_album(album):
    if album not in [None, ""]:
        try:
            album = str(album)
        except:
            return util_lib.album_must_be_string
        if len(album) > 500:
            return util_lib.album_too_long
    else:
        return util_lib.album_required

def _validate_release_year(release_year):
    if release_year is not None:
        try:
            release_year = int(release_year)
        except:
            return util_lib.release_year_must_be_int
        if release_year < 1900 or release_year > 2100:
            return util_lib.release_year_range
    else:
        return util_lib.release_year_required

def _validate_genre(genre):
    if genre is not None:
        try:
            genre = str(genre)
        except:
            return util_lib.genre_must_be_string
        if len(genre) > 255:
            return util_lib.genre_too_long

def _validate_interest_level(interest_level):
    if interest_level is not None:
        try:
            interest_level = int(interest_level)
        except:
            return util_lib.interest_level_must_be_int
        if interest_level not in [1, 2, 3]:
            return util_lib.interest_level_range

def _validate_starred(starred):
    if starred is not None:
        try:
            util_lib.str_to_bool(starred)
        except:
            return util_lib.starred_invalid

def _validate_artwork(artwork, artwork_file):
    if artwork is not None:
        try:
            artwork = str(artwork)
        except:
            return util_lib.artwork_filename_must_be_string
    if (artwork and not artwork_file) or (not artwork and artwork_file):
        return util_lib.artwork_file_mismatch

def _validate_obtained(obtained):
    if obtained is not None:
        try:
            util_lib.str_to_bool(obtained)
        except:
            return util_lib.obtained_invalid
    else:
        return util_lib.obtained_required

def _validate_link(link):
    url_pattern = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
    if link is not None:
        try:
            link = str(link)
        except:
            return util_lib.link_must_be_string
        if not re.fullmatch(url_pattern, link):
            return util_lib.link_invalid_format