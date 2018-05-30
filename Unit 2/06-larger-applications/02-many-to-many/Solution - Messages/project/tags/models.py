from project import db


class Tag(db.Model):

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name

    # Set a custom string representation of message objects
    def __repr__(self):
        return f"Tag {self.name}"