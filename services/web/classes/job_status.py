class Job_Status:    
    def __init__(self):
        self.id = ""
        self.success = False
        self.status = "initialized"
        self.errors = []
    
    def __str__(self):
        all_attr = {
            "id": self.id,
            "success": self.success,
            "status": self.status,
            "errors": self.errors
        }

        return str(all_attr)