from flask import Blueprint, render_template, url_for, request, redirect, flash

from project import db
from project.tags.forms import TagForm, DeleteForm
from project.tags.models import Tag

tags_blueprint = Blueprint('tags', __name__, template_folder='templates')


@tags_blueprint.route('/', methods=["GET", "POST"])
def tags():
    if request.method == "POST":
        form = TagForm(request.form)
        if form.validate():
            new_tag = Tag(request.form["name"])
            db.session.add(new_tag)
            db.session.commit()
            flash("Tag Created!")
        else:
            flash("Form Error: Tag Not Created")
            return render_template('tags/new.html', form=form)
    return render_template('tags/index.html', tags=Tag.query.all())


@tags_blueprint.route('/new', methods=["GET"])
def new():
    form = TagForm()
    form.set_choices()
    return render_template('tags/new.html', form=form)


@tags_blueprint.route('/<int:id>', methods=["GET", "PATCH", "DELETE"])
def show(id):
    selected_tag = Tag.query.get(id)
    # Use b"PATCH" because Flask Modus makes request.method a bytes literal
    if request.method == b"PATCH":
        tag_form = TagForm(request.form)
        if tag_form.validate():
            selected_tag.name = request.form['name']
            db.session.add(selected_tag)
            db.session.commit()
            flash("Tag Updated!")
            return redirect(url_for('tags.tags'))
        else:
            flash("Form Error: Tag Not Updated")
            return render_template('tags/edit.html', tag=selected_tag, tag_form=tag_form, delete_form=DeleteForm())
    if request.method == b"DELETE":
        delete_form = DeleteForm(request.form)
        if delete_form.validate():
            db.session.delete(selected_tag)
            db.session.commit()
            flash("Tag Deleted!")
            return redirect(url_for('tags.tags'))
        else:
            flash("Form Error: Tag Not Deleted")
            return redirect(url_for('tags.tags'))
    return render_template('tags/show.html', tag=selected_tag)


@tags_blueprint.route('/<int:id>/edit', methods=["GET"])
def edit(id):
    selected_tag = Tag.query.get(id)
    tag_form = TagForm(obj=selected_tag)
    tag_form.set_choices()
    return render_template('tags/edit.html', tag=selected_tag, tag_form=tag_form, delete_form=DeleteForm())
