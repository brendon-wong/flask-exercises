### Objectives:

By the end of this chapter, you should be able to:

*   Explain what a JSON Web Token is
*   Implement authentication with APIs using JSON Web Tokens
*   Build an API with multiple resources

### Securing an API with JSON Web Tokens

Now that we have a better idea how to build APIs, we need to start thinking about how to secure them! We could use cookies and sessions, but this might become problematic if we want our API to interact with other APIs or different clients and mobile devices. A better alternative is to use token-based authentication; specifically, a technology called JSON Web Tokens (or JWT - pronounced JOT). A JSON Web token is a token that stores information and is comprised of three parts:

**Header** - A base64 encoded string which contains the type of token and the name of the algorithm used for the signature (see below)

**Payload** - A base64 encoded string which contains all of the keys and values for the token

**Signature** - A string which is the result of the HMAC SHA256 encrypted base64 encoded header, the base64 encoded payload and the secret key. This signature is what is used to verify the authenticity of the token when it is sent to the server.

**HMAC SHA256** - Very difficult to hack/decrypt without a secret key (this is stored on the server)

**Base64** - Very easy to decode, useful for easily converting into a 64 character length string.

To read more about JWTs, check out [JWT.io](https://jwt.io/) or [this](https://stormpath.com/blog/jwt-the-right-way) blog post.

To get started using JWTs, we will use a module called `Flask-JWT`. You can read more about it [here](https://pythonhosted.org/Flask-JWT/). Let's start by creating a simple application with a User model.

It's important to realize that the header and the payload are **not encrypted**. They are simply encoded using a base64 encoding for ease of transmission across the Internet. In JavaScript, it's very easy to encode and decode base64 using the `atob` and `btoa` functions:

~~~~
btoa('{"secretKey": "secret value"}')
// "eyJzZWNyZXRLZXkiOiAic2VjcmV0IHZhbHVlIn0="

atob("eyJzZWNyZXRLZXkiOiAic2VjcmV0IHZhbHVlIn0=")
// "{"secretKey": "secret value"}"
~~~~

The security from a JWT comes from the signature, which is influenced by a secret key set on the server. Tampering with the payload isn't possible since there's no way for the client to also update the signature accordingly.

Having said that, you shouldn't put sensitive information in the payload: better to put a minimal amount of information (e.g. a user's id), so that if the server needs more information it can get it.

For more on base64 encodings, check out [this](https://www.lifewire.com/base64-encoding-overview-1166412) article or [this](http://stackoverflow.com/questions/201479/what-is-base-64-encoding-used-for) Stack Overflow question.

### A User API

~~~~
mkvirtualenv flask-jwt
createdb flask-jwt
pip install flask flask-jwt ipython flask-sqlalchemy psycopg2 flask-bcrypt flask-restful
~~~~

Let's not worry about blueprints for now (we'll get to that in just a moment). Instead, let's just create some of the basic code we'll need in our `app.py`. Note all of the things we're pulling from `flask_jwt` (we'll get to them momentarily).

~~~~
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_restful import Api, Resource, fields, marshal_with
from flask_jwt import JWT, jwt_required, current_identity

app = Flask(__name__)
bcrypt = Bcrypt(app)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/flask-jwt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Ill never tell'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')

user_fields = {
    'id': fields.Integer,
    'username': fields.String
}

@api.resource('/users')
class UserListAPI(Resource):
    @marshal_with(user_fields)
    def get(self):
        return User.query.all()

    @marshal_with(user_fields)
    def post(self):
        new_user = User(request.json['username'],request.json['password'])
        db.session.add(new_user)
        db.session.commit()
        return new_user

if __name__ == '__main__':
    app.run(debug=True,port=3000)
~~~~

(Note that in this example we've decorated the `UserListAPI` class with `@api.resource('/users')`. This has the same effect as what we did in the last chapter, when we defined the classes without decorators and then called something like `api.add_resource(UserListAPI,'/users')`.)

Before checking out this API, let's hop into `ipython` and add some data to our database:

~~~~
from app import User, db
db.create_all()
matt = User("matt", "foo")
elie = User("elie", "bar")
tim = User("tim", "baz")
db.session.add_all([matt,elie,tim])
db.session.commit()
~~~~

If you start your application and `curl http://localhost:3000/users`, you should get back JSON with each user's id and username. Passwords are intentionally missing: they aren't included in the `user_fields`, because there's no reason for the client to get the hashed password, it should just be used on the server for authentication!

Posting should also work. Try `curl -d '{"username": "janey", "password": "boom"}' http://localhost:3000/users --header "Content-Type: application/json"`.

### Working with JWTs

So far, so good. We've can see all users in our application, and can create new users. But we don't have any authentication yet! We imported a bunch of stuff from `flask_jwt`, so let's put it to use.

The first thing we'll need to do is write an `authenticate` method which we can use to authenticate users. This method **must** be called `authenticate`!

To authenticate a user using `flask_jwt`, you must send a POST request to `/auth` with the user's credentials. We'll authenticate by...

1.  Finding a user based on the username they provide;
2.  Checking the provided password against the hashed password in the database.
3.  If the user is successfully authenticated, send back a JWT that can be used in subsequent requests.

Here's how we can implement `authenticate`:

~~~~
def authenticate(username, password):
    user = User.query.filter(User.username == username).first()
    if bcrypt.check_password_hash(user.password, password):
        return user
~~~~

To set up the authentication functionality, we also need to add the following line towards the bottom of our `app.py` code (you can put it just before the `if __name__ == '__main__'` check):

~~~~
jwt = JWT(app, authenticate)
~~~~

Now if you try to authorize with invalid credentials, you should get an error:

~~~~
curl http://localhost:3000/auth -d '{"username": "matt", "password": "alwkjef"}' --header "Content-Type: application/json"

{
  "description": "Invalid credentials", 
  "error": "Bad Request", 
  "status_code": 401
}
~~~~

However, if you pass in the correct credentials, you should be just fine:

~~~~
curl http://localhost:3000/auth -d '{"username": "matt", "password": "foo"}' --header "Content-Type: application/json"

{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZGVudGl0eSI6MSwibmJmIjoxNDc5MzQ0ODEwLCJpYXQiOjE0NzkzNDQ4MTAsImV4cCI6MTQ3OTM0NTExMH0.LOlkYNsgvUmCSVQHhchGLgJn-HSVTXfatulD8xqubhQ"
}
~~~~

If you decrypt the middle portion of the JWT, you should be able to see the payload explicitly; it should look something like this:

`"{"identity":1,"nbf":1479344810,"iat":1479344810,"exp":1479345110}"`

`Identity` is the unique identifier for the user. `"iat"` is a timestamp indicating when the JWT was issued, and `"exp"` indicates when it expires (by default, five minutes from the `"iat"`). `"nbf"` stands for "not before," and indicates a time before which the JWT should not be accepted for processing. In this case, you see that the `nbf` and the `iat` have the same value.

(Curious about how to get a new token when the old one expires? We discuss that later in this chapter.)

### Authorization

We've got authentication working, but what about authorization? To build this out, we'll first need some routes we want to protect. Let's create a couple more routes, for getting and updating an individual user:

~~~~
@api.resource('/users/<int:id>')
class UserAPI(Resource):
    @marshal_with(user_fields)
    def get(self,id):
        return User.query.get(id)

    @marshal_with(user_fields)
    def patch(self,id):
        user = User.query.get(id)
        user.username = request.json['username']
        user.password = bcrypt.generate_password_hash(request.json['password']).decode('UTF-8')
        db.session.add(user)
        db.session.commit()
        return user
~~~~

Test that these routes work as expected using `curl`.

Now, let's suppose we want to make these routes private, so that you can't access them unless you have authorized yourself as the correct user. We can do that by decorating them with `@jwt_required()`. Inside of functions decorated in this way, we also have access to a `current_identity` variable which refers to the current user:

~~~~
@api.resource('/users/<int:id>')
class UserAPI(Resource):
    @marshal_with(user_fields)
    @jwt_required()
    def get(self,id):
        return current_identity

    @marshal_with(user_fields)
    @jwt_required()
    def patch(self,id):
        current_identity.username = request.json['username']
        current_identity.password = bcrypt.generate_password_hash(request.json['password']).decode('UTF-8')
        db.session.add(current_identity)
        db.session.commit()
        return current_identity
~~~~

This won't work just yet, however, because we need to explicitly tell `flask_jwt` how to define `current_identity`. For that, we need to define an `identity` function, and pass it into `JWT`:

~~~~
def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)

jwt = JWT(app, authenticate, identity)
~~~~

With this, these new routes should be protected! To access, them, you'll need to include a header of the form `Authorization: JWT <INSERT_YOUR_JWT_HERE>`.

### Adding a 1:M Relationship

Now let's look at a more complex example with a 1:M with authentication

~~~~
mkvirtualenv jwt-one-many
pip install flask flask-jwt flask-restful flask-sqlalchemy flask-migrate psycopg2 ipython flask-bcrypt
touch app.py
createdb flask-jwt-example
~~~~

~~~~
from flask import Flask
# current_identity is like current_user
from flask_jwt import JWT, jwt_required, current_identity
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_restful import Api, Resource, reqparse, marshal_with, fields
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

api = Api(app)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://localhost/flask-jwt-example"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    posts = db.relationship('Post', backref='user', lazy='joined')
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,title, body, user_id):
        self.title = title
        self.body = body
        self.user_id = user_id

post_user_fields = {
    'id': fields.Integer,
    'username': fields.String,
}

post_fields= {
    'id': fields.Integer,
    'title': fields.String,
    'body': fields.String,
    'created': fields.DateTime(dt_format='rfc822'),
    'user': fields.Nested(post_user_fields)
}

user_fields= {
    'id': fields.Integer,
    'username': fields.String,
     # don't want people seeing the password...
    'posts': fields.Nested(post_fields),
}

@api.resource('/signup')
class SignupAPI(Resource):
    @marshal_with(user_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='username')
        parser.add_argument('password', type=str, help='password')
        args = parser.parse_args()
        try:
            new_user = User(args['username'], args['password'])
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError as e:
            return "Username already exists"
        return new_user

@api.resource('/users/<int:id>')
class UserAPI(Resource):

    @jwt_required()
    @marshal_with(user_fields)
    def get(self, id):
        return current_identity

    @marshal_with(user_fields)
    @jwt_required()
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='username')
        parser.add_argument('password', type=str, help='password')
        args = parser.parse_args()
        current_identity.name = args['username']
        current_identity.password = bcrypt.generate_password_hash(args['password']).encode('utf-8')
        db.session.add(current_identity)
        db.session.commit()
        return found_user

    @jwt_required()
    def delete(self, id):
        db.session.delete(current_identity)
        db.session.commit()
        return None, 204

@api.resource('/users/<int:user_id>/posts')
class PostsAPI(Resource):
    @marshal_with(post_fields)
    @jwt_required()
    def get(self, user_id):
        return current_identity.posts

    @marshal_with(post_fields)
    def post(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='Name')
        args = parser.parse_args()
        new_post = Post(args['name'], user_id)
        db.session.add(new_post)
        db.session.commit()
        return new_post

@api.resource('/users/<int:user_id>/posts/<int:id>')
class PostAPI(Resource):
    @jwt_required()
    @marshal_with(post_fields)
    def get(self, user_id, id):
        return Post.query.get_or_404(id)

    @marshal_with(post_fields)
    @jwt_required()
    def put(self, user_id, id):
        found_post = Post.query.get_or_404(id)
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='Name')
        args = parser.parse_args()
        found_post.name = args['name']
        db.session.add(found_post)
        db.session.commit()
        return found_post

    @jwt_required()
    def delete(self, user_id, id):
        post = Post.query.get_or_404(id)
        db.session.delete(post)
        db.session.commit()
        return None, 204

# get's run when a post is made to /auth with application/json as a content type
def authenticate(username, password):
    user = User.query.filter(User.username == username).first()
    if bcrypt.check_password_hash(user.password, password):
        return user

# get's run when jwt_required
def identity(payload):
    user_id = payload['identity']
    return User.query.get_or_404(user_id)

jwt = JWT(app, authenticate, identity)

if __name__ == '__main__':
    app.run()
~~~~

Try to refactor this code to use blueprints and finish CRUD on the other resource!

### Further topics

There's much more you could do when it comes to working with tokens and building an API. Here are some topics worth considering if you'd like to push yourself:

#### Deleting Tokens

Ideally, you will be deleting tokens on the client side since they will be stored in `localStorage`. In order to invalidate generated tokens, we can set an expiration time on them by configuring the `JWT_EXPIRATION_DELTA` value in Flask-JWT. Many OAuth2 providers will give access to something called a refresh token, which is a token used to generate new tokens that have a short expiration. You can read more about refresh tokens [here](https://github.com/mattupstate/flask-jwt/issues/29) or using other options like blacklisting tokens [here](http://stackoverflow.com/questions/21978658/invalidating-json-web-tokens). You can also look into `Flask-JWT` extensions like [this](https://github.com/vimalloc/flask-jwt-extended/) one, which streamline the process of creating refresh tokens.

#### Caching API requests

When responding with data from an API call, it's very common that as your application grows it may be more expensive to fetch certain kinds of data. Very commonly, to speed up delivery, a cache is put in place so that if the data does not change, accessing it can be much faster after an initial request. You can learn more about caching requests [here](https://realpython.com/blog/python/caching-external-api-requests/) or through using a module called [Flask-Cache](https://pythonhosted.org/Flask-Cache/) or even with making your own [here](http://flask.pocoo.org/snippets/9/). In development it's fine to use a built in cache like SimpleCache. In production however, you will want to use a better tool like Memcached or Redis.

#### Rate Limiting an API

When you create a public API, you might want to limit the number of requests a user can make (before charging them money or just to keep traffic down). This is done through a process called rate limiting (where you return an expected response or a 429 error if there have been too many requests). You can learn more how to integrate that in your application using a module called [Flask-Limiter](https://flask-limiter.readthedocs.io/en/stable/).

When you're ready, move on to [Testing Flask JSON APIs](/courses/intermediate-flask/testing-flask-json-apis)