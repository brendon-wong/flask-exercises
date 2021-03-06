from flask_wtf import FlaskForm
from wtforms import StringField, validators, SelectMultipleField, widgets
from project.messages.models import Message


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class TagForm(FlaskForm):
    name = StringField(
        'Name', [validators.DataRequired(), validators.Length(min=1, max=100)])

    messages = MultiCheckboxField(
        'Messages',
        coerce=int)

    def set_choices(self):
        self.messages.choices = [(m.id, m.content)
                                 for m in Message.query.all()]


class DeleteForm(FlaskForm):
    pass
