from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

'''
@app.route('/')
def get():
    return jsonify({'msg': 'Hello world'})
    '''
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)
    role = db.Column(db.String(20))

    def __init__(self, name, username, email, role):
        self.name = name
        self.username = username
        self.email = email
        self.role = role


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    author = db.Column(db.String(100))
    publisher = db.Column(db.String(100))
    pub_date = db.Column(db.String(100))

    def __init__(self, name, author, publisher, pub_date):
        self.name = name
        self.author = author
        self.publisher = publisher
        self.pub_date = pub_date


class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'author', 'publisher', 'pub_date')

book_schema = BookSchema()
books_schema = BookSchema(many=True,)

@app.route('/book', methods=['POST'])
def add_book():
    name = request.json['name']
    author = request.json['author']
    publisher = request.json['publisher']
    pub_date = request.json['pub_date']
    
    new_book = Book(name, author, publisher, pub_date)

    db.session.add(new_book)
    db.session.commit()

    return book_schema.jsonify(new_book)

@app.route('/book', methods=['GET'])
def get_books():
    all_books = Book.query.all()
    result = books_schema.dump(all_books)
    return jsonify(result)

@app.route('/book/<id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)
    return book_schema.jsonify(book)

@app.route('/book/<id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)

    name = request.json['name']
    author = request.json['author']
    publisher = request.json['publisher']
    pub_date = request.json['pub_date']

    book.name = name
    book.author = author
    book.publisher = publisher
    book.pub_date = pub_date

    db.session.commit()
    return book_schema.jsonify(book)

@app.route('/book/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()

    return book_schema.jsonify(book)

if __name__ == '__main__':
    app.run(debug=True)
