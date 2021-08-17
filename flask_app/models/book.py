from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors_favorites = []

    @classmethod
    def get_info(cls):
        query = 'SELECT * FROM books'
        results = connectToMySQL('books_schema').query_db(query)
        books = []

        for b in results:
            books.append(cls(b))
        return books
    
    @classmethod
    def save(cls, data):
        query ="INSERT INTO books (title, num_of_pages) VALUES (%(title)s, %(num_of_pages)s)"
        return connectToMySQL('books_schema').query_db(query,data)

    @classmethod
    def get_book(cls, data):
        query = "SELECT * FROM books LEFT JOIN favorites ON books.id = favorites.book_id LEFT JOIN authors ON authors.id = favorites.author_id WHERE books.id = %(id)s;"

        result = connectToMySQL('books_schema').query_db(query, data)

        book = cls(result[0])
        for b in result:
            if b['authors.id'] == None:
                break
            data = {
                'id': b['authors.id'],
                'name': b['name'],
                'created_at': b['authors.created_at'],
                'updated_at': b['authors.updated_at']
            }
            book.authors_favorites.append(author.Author(data))
        return book

    @classmethod
    def unfavorited_book(cls, data):
        query = "SELECT * FROM books WHERE books.id NOT IN (SELECT book_id FROM favorites WHERE author_id = %(id)s);"
        results = connectToMySQL('books_schema').query_db(query, data)

        book = []
        for row in results:
            book.append(cls(row))
        return book