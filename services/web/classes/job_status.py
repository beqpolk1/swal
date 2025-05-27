class Job_Status:    
    def __init__(self):
        self.id = ""
        self.success = False
        self.status = []
        self.errors = []
        self.update_status("initialized")
    
    def to_dict(self):
        return {
            "id": self.id,
            "success": self.success,
            "status": self.status,
            "errors": self.errors
        }
    
    def update_status(self, new_status : str):
        self.status.append(new_status)

    def get_status (self):
        return self.status[-1]
    
    def add_error(self, new_error : str):
        self.errors.append(new_error)

    def add_errors(self, new_errors : list):
        self.errors.extend(new_errors)

    def __str__(self):
        return str(self.to_dict())