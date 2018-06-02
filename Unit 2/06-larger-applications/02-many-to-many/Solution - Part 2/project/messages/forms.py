from flask_wtf import FlaskForm
from wtforms import StringField, validators, SelectMultipleField, widgets
from project.tags.models import Tag


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class MessageForm(FlaskForm):
    content = StringField(
        'Content', [validators.DataRequired(), validators.Length(min=1, max=100)])

    tags = MultiCheckboxField(
        'Tags',
        coerce=int)

    def set_choices(self):
        self.tags.choices = [(t.id, t.name) for t in Tag.query.all()]


class DeleteForm(FlaskForm):
    pass
