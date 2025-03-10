class Entry:
    def __init__(self, new_vals, new_files):
        self.artist = new_vals.get("artist") or None
        self.album = new_vals.get("album") or None
        self.release_year = new_vals.get("release_year") or None
        self.genre = new_vals.get("genre") or None
        self.interest = new_vals.get("interest_level")
        self.starred = new_vals.get("is_starred")
        self.obtained = new_vals.get("is_obtained")

    def __str__(self):
        all_attr = {
            "artist": self.artist,
            "album": self.album,
            "release_year": self.release_year,
            "genre": self.genre,
            "interest_level": self.interest,
            "is_starred": self.starred,
            "is_obtained": self.obtained,
            "link": self.link
        }

        return str(all_attr)

