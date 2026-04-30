class Search_Result:
    def __init__(self):
        self.errors = []
        self.results = []
        self.flip_results = False

        self.pages = {
            "prev": None,
            "next": None,
            "limit": None,
            "addl": None
        }

    def to_dict(self):
        return {
            "errors": self.errors,
            "flip_results": self.flip_results,
            "has_more": self.has_more,
            "results": self.results,
            "pages": self.pages
        }
    
    def add_error(self, new_err : str):
        self.errors.append(new_err)

    def add_errors(self, new_errors : list):
        self.errors.extend(new_errors)

    def has_errors(self) -> bool:
        return len(self.errors) > 0
    
    def add_result(self, val):
        self.results.append(val)

    def add_results(self, new_results : list):
        self.results.extend(new_results)
    
    def get_results(self) -> list:
        if self.flip_results:
            return self.results[:self.pages["limit"]][::-1]
        else:
            return self.results[:self.pages["limit"]]

    def set_limit(self, new_limit : int):
        if new_limit < 1:
            raise Exception("xxx")
        self.pages["limit"] = new_limit

    def has_more(self) -> bool:
        if (self.pages["limit"] is not None and len(self.results) > self.pages["limit"]):
            return True
        else:
            return False

    def __str__(self):
        return str(self.to_dict())