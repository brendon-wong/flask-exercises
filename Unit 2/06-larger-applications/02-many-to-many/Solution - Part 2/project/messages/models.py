from project import db
# from project.tags.models import Tag # May not be necessary

MessageTags = db.Table('messages_tags',
                       db.Column('id',
                                 db.Integer,
                                 primary_key=True),
                       db.Column('message_id',
                                 db.Integer,
                                 db.ForeignKey('messages.id', ondelete="cascade")),
                       db.Column('tag_id',
                                 db.Integer,
                                 db.ForeignKey('tags.id', ondelete="cascade")))


class Message(db.Model):

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tags = db.relationship('Tag', secondary=MessageTags,
                           backref=db.backref('messages'))

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id

    # Set a custom string representation of message objects
    def __repr__(self):
        return f"User {self.user_id} wrote '{self.content}'"
