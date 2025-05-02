class Job_Status:    
    def __init__(self):
        self.id = ""
        self.success = False
        self.status = "initialized"
        self.errors = []
    
    def to_dict(self):
        return {
            "id": self.id,
            "success": self.success,
            "status": self.status,
            "errors": self.errors
        }

    def __str__(self):
        return str(self.to_dict())