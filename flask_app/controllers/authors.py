from flask import render_template, redirect, request
from flask_app import app
from flask_app.models.author import Author
from flask_app.models.book import Book

@app.route('/')
def index():
    return redirect('/authors')


@app.route('/authors')
def home():
    authors = Author.get_info()
    return render_template('index.html', all_authors=authors)


@app.route('/author/create', methods=['POST'])
def create_author():
    Author.add_author(request.form)
    return redirect('/authors')


@app.route('/author/<int:id>')
def show_author(id):
    data = {
        'id': id
    }
    return render_template('show_author.html', author=Author.get_author(data), unfavorited_book = Book.unfavorited_book(data))


@app.route('/join/book',methods=['POST'])
def join_book():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    Author.add_fav(data)
    return redirect(f"/author/{request.form['author_id']}")