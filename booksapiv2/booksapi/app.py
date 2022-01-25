import os
import json
from urllib.parse import unquote
from flask import Flask, jsonify, request, render_template
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

###  basic restful api to interact with a catalog of books

# Pull env vars passed in from our K8 manifest
db_host = os.environ["POSTGRES_HOST"]
db_port = os.environ["POSTGRES_PORT"]
username = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]
database = os.environ["POSTGRES_DB"]

api_host = os.environ["APIHOST"]
api_port = os.environ["APIPORT"]
api_user = os.environ['API_USER']
api_password = os.environ['API_PASSWORD']

auth = HTTPBasicAuth()


''' iniitialize and set resources so we don't throw errors pounding
    away at the database - pools exhaust quickly.
'''
app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{username}:{password}@{db_host}:{db_port}/{database}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_POOL_SIZE"] = 20
app.config["SQLALCHEMY_POOL_TIMEOUT"]=300
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

class BookModel(db.Model):

    __tablename__ = "works"

    work_id = db.Column("work_id", db.Integer, primary_key=True)
    title = db.Column("title", db.Text)
    authors = db.Column("authors", db.Text)
    isbn = db.Column("isbn", db.VARCHAR)
    description = db.Column("description", db.Text)

    def __init__(self, work_id, title, authors, isbn, description):
        self.work_id = work_id
        self.title = title
        self.authors = authors
        self.isbn = isbn
        self.description = description

class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BookModel

book_schema = BookSchema()
books_schema = BookSchema(many=True)

# Flask routes for endpoints - we'll just include them in one file

@app.route("/books", methods=["GET"])
@auth.login_required
def handle_books():
    ''' get all books in the catalog '''
    try:
        books = BookModel.query.all()
        return(books_schema.jsonify(books))
    except Exception as e:
        return(jsonify({'Error': e}))

@app.route('/search/title/', methods=['GET'])
@auth.login_required
def titles():
    if request.args.get('title'):
        q = request.args.get('title')
        book = BookModel.query.filter(BookModel.title.like("%"+q+"%")).all()
        return(books_schema.jsonify(book))
    else:
        return(jsonify({'Error':'Incorrect search param supplied. See /help'}))

@app.route('/search/authors/', methods=['GET'])
@auth.login_required
def authors():
    if request.args.get('authors'):
        q = request.args.get('authors')
        book = BookModel.query.filter(BookModel.authors.like("%"+q+"%")).all()
        return(books_schema.jsonify(book))
    else:
        return(jsonify({'Error':'Incorrect search param. See /help'}))

@app.route('/search/isbn/', methods=['GET'])
@auth.login_required
def isbn():
    if request.args.get('isbn'):
        q = request.args.get('isbn')
        book = BookModel.query.filter(BookModel.isbn.like("%"+q+"%")).first()
        return(book_schema.jsonify(book))
    else:
        return(jsonify({'Error':'Incorrect search params. See /help'}))

@app.route('/', methods=['GET'])
@app.route('/help', methods=['GET'])
def help():
    ''' this function displays help for the user, no auth required '''
    return(render_template('help.html',title='booksapi help'))


@auth.verify_password
def verify_user(user,password):
    if user and password:
        if user == api_user and password == api_password:
            return(True)
        else:
            return(False)
        return(False)


if __name__ == "__main__":
    app.run(api_host,api_port)

