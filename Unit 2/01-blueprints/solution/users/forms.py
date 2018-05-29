from flask_wtf import FlaskForm
from wtforms import StringField, validators


class UserForm(FlaskForm):
    first_name = StringField(
        'First Name', [validators.DataRequired(), validators.Length(min=1, max=50)])
    last_name = StringField(
        'Last Name', [validators.DataRequired(), validators.Length(min=1, max=50)])


class DeleteForm(FlaskForm):
    pass
