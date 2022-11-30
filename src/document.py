class Document:
    
    def __init__(self, id, body):
        self.id=id
        self.body=body

    
    def __repr__(self):
        return f"ID: {self.id}\n"