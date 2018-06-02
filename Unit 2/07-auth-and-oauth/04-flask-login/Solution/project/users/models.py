from project import db, bcrypt
from flask_login import UserMixin


class User(db.Model, UserMixin):

    __tablename__ = "users"

    # Columns in table
    id = db.Column(db.Integer, primary_key=True)
    # 50 characters is a sensible default for the max length of first/last names
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    # 256 characters is a sensible default for the max length of emails/usernames
    username = db.Column(db.String(256), unique=True)
    password = db.Column(db.Text)
    messages = db.relationship('Message', backref='user', lazy='dynamic')

    def __init__(self, first_name, last_name, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')

    # Call the class method with User.authenticate()
    @classmethod
    # Method requires username and password
    def authenticate(cls, username, password):
        found_user = cls.query.filter_by(username=username).first()
        if found_user:
            authenticated_user = bcrypt.check_password_hash(
                found_user.password, password)
            if authenticated_user:
                # Return the user so we can log them in by storing information in the session
                return found_user
        return False

    # Set a custom string representation of user objects
    def __repr__(self):
        return f"User {self.first_name} {self.last_name}"
