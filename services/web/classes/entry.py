import util_lib

class Entry:
    def __init__(self, new_vals, new_files):
        #required fields
        self.artist = str(new_vals.get("artist"))
        self.album = str(new_vals.get("album"))
        self.release_year = int(new_vals.get("release_year"))
        self.obtained = util_lib.str_to_bool(new_vals.get("is_obtained"))

        #optional fields
        self._id = util_lib.get_str_or_none(new_vals, "id")
        self.genre = util_lib.get_str_or_none(new_vals, "genre")
        self.interest = util_lib.get_int_or_none(new_vals, "interest_level")
        self.link = util_lib.get_str_or_none(new_vals, "link")
        self.artwork_file_name = new_files.get("artwork_file").filename or None
        self.artwork_file = new_files.get("artwork_file")
        self.starred = util_lib.get_bool_or_none(new_vals, "is_starred")

    def to_dict(self):
        return {
            "_id": self._id,
            "artist": self.artist,
            "album": self.album,
            "release_year": self.release_year,
            "genre": self.genre,
            "interest_level": self.interest,
            "is_starred": self.starred,
            "artwork_file_name": self.artwork_file_name,
            "artwork_file": True if (self.artwork_file) else False,
            "is_obtained": self.obtained,
            "link": self.link
        }

    def __str__(self):
        return str(self.to_dict)

