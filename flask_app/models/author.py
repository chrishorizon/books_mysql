from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

class Author:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorite_books = []


    @classmethod
    def get_info(cls):
        query = 'SELECT * FROM authors'
        results = connectToMySQL('books_schema').query_db(query)
        authors = []

        for a in results:
            authors.append(cls(a))
        return authors

    @classmethod
    def add_author(cls, data):
        query = "INSERT INTO authors (name) VALUES (%(name)s)"
        return connectToMySQL('books_schema').query_db(query, data)
    
    @classmethod
    def unfavorited_authors(cls,data):
        query = "SELECT * FROM authors WHERE authors.id NOT IN (SELECT author_id FROM favorites WHERE book_id = %(id)s);"
        results = connectToMySQL('books_schema').query_db(query, data)

        author = []
        for row in results:
            author.append(cls(row))
        return author
    
    @classmethod
    def add_fav(cls,data):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s);"
        return connectToMySQL('books_schema').query_db(query, data)

    @classmethod
    def get_author(cls,data):
        query = "SELECT * FROM authors LEFT JOIN favorites ON authors.id = favorites.author_id LEFT JOIN books ON books.id = favorites.book_id WHERE authors.id = %(id)s;"
        results = connectToMySQL('books_schema').query_db(query, data)

        author = cls(results[0])

        for a in results:
            if a['books.id'] == None:
                break
            data = {
                "id": a['books.id'],
                "title": a['title'],
                "num_of_pages": a['num_of_pages'],
                "created_at": a['books.created_at'],
                "updated_at": a['books.updated_at']
            }
            author.favorite_books.append(book.Book(data))
        return author