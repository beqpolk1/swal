class Entry:
    def __init__(self, artist, album, release_year, genre, interest, starred, obtained, link):
        self.artist = artist
        self.album = album
        self.release_year = release_year
        self.genre = genre
        self.interest = interest
        self.starred = starred
        self.obtained = obtained
        self.link = link

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

