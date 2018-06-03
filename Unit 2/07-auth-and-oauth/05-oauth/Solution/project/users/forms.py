from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators


class UserForm(FlaskForm):
    first_name = StringField(
        'First Name', [validators.DataRequired(), validators.Length(min=1, max=50)])
    last_name = StringField(
        'Last Name', [validators.DataRequired(), validators.Length(min=1, max=50)])
    username = StringField('Username', validators=[
                           validators.DataRequired(), validators.Length(min=1, max=256)])
    password = PasswordField('Password', validators=[
                             validators.DataRequired()])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           validators.DataRequired(), validators.Length(min=1, max=256)])
    password = PasswordField('Password', validators=[
                             validators.DataRequired()])


class DeleteForm(FlaskForm):
    pass
