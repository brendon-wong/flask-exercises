from solution import db


class Message(db.Model):

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id

    # Set a custom string representation of message objects
    def __repr__(self):
        return f"User {self.user_id} wrote '{self.content}'"
