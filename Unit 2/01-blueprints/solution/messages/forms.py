from flask_wtf import FlaskForm
from wtforms import StringField, validators


class MessageForm(FlaskForm):
    content = StringField(
        'Content', [validators.DataRequired(), validators.Length(min=1, max=100)])


class DeleteForm(FlaskForm):
    pass
