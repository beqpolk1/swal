import re, util_lib
from flask import current_app

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
            return util_lib.ARTIST_MUST_BE_STRING
        if len(artist) > current_app.config["MAX_ARTIST_LENGTH"]:
            return util_lib.ARTIST_TOO_LONG.format(length = current_app.config["MAX_ARTIST_LENGTH"])
    else:
        return util_lib.ARTIST_REQUIRED

def _validate_album(album):
    if album not in [None, ""]:
        try:
            album = str(album)
        except:
            return util_lib.ALBUM_MUST_BE_STRING
        if len(album) > current_app.config["MAX_ALBUM_LENGTH"]:
            return util_lib.ALBUM_TOO_LONG.format(length = current_app.config["MAX_ALBUM_LENGTH"])
    else:
        return util_lib.ALBUM_REQUIRED

def _validate_release_year(release_year):
    if release_year is not None:
        try:
            release_year = int(release_year)
        except:
            return util_lib.RELEASE_YEAR_MUST_BE_INT
        if release_year < current_app.config["MIN_RELEASE_YEAR"] or release_year > current_app.config["MAX_RELEASE_YEAR"]:
            return util_lib.RELEASE_YEAR_RANGE.format(min_year = current_app.config["MIN_RELEASE_YEAR"], max_year = current_app.config["MAX_RELEASE_YEAR"])
    else:
        return util_lib.RELEASE_YEAR_REQUIRED

def _validate_genre(genre):
    if genre is not None:
        try:
            genre = str(genre)
        except:
            return util_lib.GENRE_MUST_BE_STRING
        if len(genre) > current_app.config["MAX_GENRE_LENGTH"]:
            return util_lib.GENRE_TOO_LONG.format(length = current_app.config["MAX_GENRE_LENGTH"])

def _validate_interest_level(interest_level):
    if interest_level is not None:
        try:
            interest_level = int(interest_level)
        except:
            return util_lib.INTEREST_LEVEL_MUST_BE_INT
        if interest_level not in current_app.config["VALID_INTEREST_LVL"]:
            return util_lib.INTEREST_LEVEL_RANGE.format(valid_levels = current_app.config["VALID_INTEREST_LVL"])

def _validate_starred(starred):
    if starred is not None:
        try:
            util_lib.str_to_bool(starred)
        except:
            return util_lib.STARRED_INVALID

def _validate_artwork(artwork, artwork_file):
    if artwork is not None:
        try:
            artwork = str(artwork)
        except:
            return util_lib.ARTWORK_FILENAME_MUST_BE_STRING
    if (artwork and not artwork_file) or (not artwork and artwork_file):
        return util_lib.ARTWORK_FILE_MISMATCH

def _validate_obtained(obtained):
    if obtained is not None:
        try:
            util_lib.str_to_bool(obtained)
        except:
            return util_lib.OBTAINED_INVALID
    else:
        return util_lib.OBTAINED_REQUIRED

def _validate_link(link):
    url_pattern = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
    if link is not None:
        try:
            link = str(link)
        except:
            return util_lib.LINK_MUST_BE_STRING
        if not re.fullmatch(url_pattern, link):
            return util_lib.LINK_INVALID_FORMAT