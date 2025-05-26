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

    def __str__(self):
        return str(self.to_dict())