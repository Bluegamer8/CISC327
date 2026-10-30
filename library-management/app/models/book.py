class Book:
    def __init__(self, id, title, author, genre, isbn, total_copies, available_copies):
        self.id = id
        self.title = title
        self.author = author
        self.genre = genre
        self.isbn = isbn
        self.total_copies = total_copies
        self.available_copies = available_copies

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "isbn": self.isbn,
            "total_copies": self.total_copies,
            "available_copies": self.available_copies,
        }
