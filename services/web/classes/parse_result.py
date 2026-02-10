class Parse_Result:
    def __init__(self):
        self.errors = []
        self.result_data = {}

    def to_dict(self):
        return {
            "errors": self.errors,
            "result_data": self.result_data
        }
    
    def add_error(self, new_err : str):
        self.errors.append(new_err)

    def has_errors(self) -> bool:
        return len(self.errors) > 0
    
    def add_data(self, key : str, val):
        self.result_data[key] = val

    def get_data(self, key : str):
        return self.result_data.get(key)
    
    def __str__(self):
        return str(self.to_dict())