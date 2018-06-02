from project import db, bcrypt


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)

    def __init__(self, username, password):
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
