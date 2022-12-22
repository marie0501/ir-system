class Document:
    
    def __init__(self, id, title, author, place, body):
        self.id=id
        self.title = title
        self.author = author
        self.place = place
        self.body=body
        self.score =0

    
    def __repr__(self):
        return f"ID: {self.id} Title: {self.title} Author: {self.author}"