class Search_Result:
    def __init__(self):
        self.errors = []
        self.results = []

        self.pages = {
            "prev": None,
            "next": None,
            "limit": None
        }

    def to_dict(self):
        return {
            "errors": self.errors,
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
    
    def __str__(self):
        return str(self.to_dict())