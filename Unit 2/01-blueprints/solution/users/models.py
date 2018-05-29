from solution import db


class User(db.Model):

    __tablename__ = "users"

    # Columns in table
    id = db.Column(db.Integer, primary_key=True)
    # 50 characters is a sensible default for the max length of first/last names
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    messages = db.relationship('Message', backref='user', lazy='dynamic')

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    # Set a custom string representation of user objects
    def __repr__(self):
        return f"User {self.first_name} {self.last_name}"
