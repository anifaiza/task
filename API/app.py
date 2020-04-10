from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

'''
@app.route('/')
def get():
    return jsonify({'msg': 'Hello world'})
    '''
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String)
    admin = db.Column(db.Boolean)

    def __init__(self, public_id, name, username, email, password, x):
        self.public_id = public_id
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.admin = x

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'username', 'email', 'admin', 'public_id')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

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

def token_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        data = jwt.decode(token, app.config.get('SECRET_KEY'))
        current_user = User.query.filter_by(public_id = data['Public_id']).first()
        
        return f(current_user, *args, **kwargs)
    return wrap

@app.route('/user', methods=['POST'])
@token_required
def add_user(current_user):
    if not current_user.admin:
        return jsonify({'message': 'You are not authorized for this function!'})

    name = request.json['name']
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    hashed_pass = generate_password_hash(password, method='sha256')
    pub_id = str(uuid.uuid4())

    new_user = User(pub_id, name, username, email, hashed_pass, False)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'msg': 'new user created'})   

@app.route('/user', methods=['GET'])
@token_required
def get_users(current_user):
    def add_user(current_user):
        if not current_user.admin:
            return jsonify({'message': 'You are not authorized for this function!'})
        all_users = User.query.all()
        result = users_schema.dump(all_users)
        return jsonify(result)


@app.route('/book', methods=['POST'])
@token_required
def add_book(current_user):
    if not current_user.admin:
        return jsonify({'message': 'You are not authorized for this function!'})

    name = request.json['name']
    author = request.json['author']
    publisher = request.json['publisher']
    pub_date = request.json['pub_date']
    new_book = Book(name, author, publisher, pub_date)

    db.session.add(new_book)
    db.session.commit()

    return jsonify({'msg': 'new book added'}) 

@app.route('/book', methods=['GET'])
@token_required
def get_books(current_user):
    all_books = Book.query.all()
    result = books_schema.dump(all_books)
    return jsonify(result)

@app.route('/book/<id>', methods=['GET'])
@token_required
def get_book(current_user, id):
    book = Book.query.get(id)
    return book_schema.jsonify(book)

@app.route('/book/<id>', methods=['PUT'])
@token_required
def update_book(current_user, id):
    if not current_user.admin:
        return jsonify({'message': 'You are not authorized for this function!'})

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
    return jsonify({'msg': 'Book updated'}) 

@app.route('/book/<id>', methods=['DELETE'])
@token_required
def delete_book(current_user, id):
    if not current_user.admin:
        return jsonify({'message': 'You are not authorized for this function!'})

    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()

    return jsonify({'msg': 'book deleted'}) 

@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not varify', 401, {'WWW-Authenticate':'Basic realm="Login required!"'})

    user = User.query.filter_by(username = auth.username).first()

    if not user:
        return make_response('Could not varify', 401, {'WWW-Authenticate':'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'Public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF_8')})

    return make_response('Could not varify', 401, {'WWW-Authenticate':'Basic realm="Login required!"'})

if __name__ == '__main__':
    app.run(debug=True)
