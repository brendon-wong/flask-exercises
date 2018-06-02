from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectMultipleField, validators, widgets

# Create instance of Flask class, set custom template and static folder
app = Flask(__name__)

# Configure Flask Modus
modus = Modus(app)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/many-many-example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure Flask migrate
migrate = Migrate(app, db)

# Configure WTForms
# For production set secret key in env variable: os.environ.get('SECRET_KEY')
app.config['SECRET_KEY'] = "this_is_an_insecure_development_key"


# Models


EmployeeDepartment = db.Table('employee_departments',
                              db.Column('id',
                                        db.Integer,
                                        primary_key=True),
                              db.Column('employee_id',
                                        db.Integer,
                                        db.ForeignKey('employees.id', ondelete="cascade")),
                              db.Column('department_id',
                                        db.Integer,
                                        db.ForeignKey('departments.id', ondelete="cascade")))


class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    years_at_company = db.Column(db.Integer)
    departments = db.relationship("Department",
                                  secondary=EmployeeDepartment,
                                  backref=db.backref('employees'))

    def __init__(self, name, years_at_company):
        self.name = name
        self.years_at_company = years_at_company


class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.name = name


# Forms


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class EmployeeForm(FlaskForm):
    name = StringField(
        'Name', [validators.DataRequired(), validators.Length(min=1, max=100)])
    years_at_company = IntegerField('Years At Company',
                                    [validators.DataRequired()])

    departments = MultiCheckboxField(
        'Departments',
        coerce=int)

    def set_choices(self):
        self.departments.choices = [(d.id, d.name)
                                    for d in Department.query.all()]


class DepartmentForm(FlaskForm):
    name = StringField(
        'Name', [validators.DataRequired(), validators.Length(min=1, max=100)])

    employees = MultiCheckboxField(
        'Employees',
        coerce=int)

    def set_choices(self):
        self.employees.choices = [(e.id, e.name) for e in Employee.query.all()]


class DeleteForm(FlaskForm):
    pass


# Main Routes


@app.route('/', methods=["GET"])
def home():
    return redirect('employees')


# Employee Routes


@app.route('/employees', methods=["GET", "POST"])
def employees():
    if request.method == "POST":
        form = EmployeeForm(request.form)
        if form.validate():
            new_employee = Employee(request.form["name"],
                                    request.form["years_at_company"])
            db.session.add(new_employee)
            db.session.commit()
            flash("Employee Successfully Added")
        else:
            flash("Form Error: Employee Not Added")
            return render_template('employees/new.html', form=form)
    return render_template('employees/index.html', employees=Employee.query.all())


@app.route('/employees/new', methods=["GET"])
def new_employee():
    form = EmployeeForm()
    form.set_choices()
    return render_template('employees/new.html', form=form)


@app.route('/employees/<int:id>', methods=["GET", "PATCH", "DELETE"])
def show_employee(id):
    selected_employee = Employee.query.get(id)
    # Use b"PATCH" because Flask Modus makes request.method a bytes literal
    if request.method == b"PATCH":
        employee_form = EmployeeForm(request.form)
        if employee_form.validate():
            selected_employee.name = request.form['name']
            selected_employee.years_at_company = request.form['years_at_company']
            db.session.add(selected_employee)
            db.session.commit()
            flash("Employee Successfully Edited")
            return redirect(url_for('employees'))
        else:
            flash("Form Error: Employee Not Edited")
            return render_template('employees/edit.html', employee=selected_employee, employee_form=employee_form, delete_form=DeleteForm())
    if request.method == b"DELETE":
        delete_form = DeleteForm(request.form)
        if delete_form.validate():
            db.session.delete(selected_employee)
            db.session.commit()
            flash("Employee Successfully Deleted")
            return redirect(url_for('employees'))
        else:
            flash("Form Error: Employee Not Deleted")
            return redirect(url_for('employees'))
    return render_template('employees/show.html', employee=selected_employee)


@app.route('/employees/<int:id>/edit', methods=["GET"])
def edit_employee(id):
    selected_employee = Employee.query.get(id)
    employee_form = EmployeeForm(obj=selected_employee)
    employee_form.set_choices()
    return render_template('employees/edit.html', employee=selected_employee, employee_form=employee_form, delete_form=DeleteForm())


# Department Routes


@app.route('/departments', methods=["GET", "POST"])
def departments():
    if request.method == "POST":
        form = DepartmentForm(request.form)
        if form.validate():
            new_department = Department(request.form["name"])
            db.session.add(new_department)
            db.session.commit()
            flash("Department Successfully Added")
        else:
            flash("Form Error: Department Not Added")
            return render_template('departments/new.html', form=form)
    return render_template('departments/index.html', departments=Department.query.all())


@app.route('/departments/new', methods=["GET"])
def new_department():
    form = DepartmentForm()
    form.set_choices()
    return render_template('departments/new.html', form=form)


@app.route('/departments/<int:id>', methods=["GET", "PATCH", "DELETE"])
def show_department(id):
    selected_department = Department.query.get(id)
    # Use b"PATCH" because Flask Modus makes request.method a bytes literal
    if request.method == b"PATCH":
        department_form = DepartmentForm(request.form)
        if department_form.validate():
            selected_department.name = request.form['name']
            db.session.add(selected_department)
            db.session.commit()
            flash("Department Successfully Edited")
            return redirect(url_for('departments'))
        else:
            flash("Form Error: Department Not Edited")
            return render_template('departments/edit.html', department=selected_department, department_form=department_form, delete_form=DeleteForm())
    if request.method == b"DELETE":
        delete_form = DeleteForm(request.form)
        if delete_form.validate():
            db.session.delete(selected_department)
            db.session.commit()
            flash("Department Successfully Deleted")
            return redirect(url_for('departments'))
        else:
            flash("Form Error: Department Not Deleted")
            return redirect(url_for('departments'))
    return render_template('departments/show.html', department=selected_department)


@app.route('/departments/<int:id>/edit', methods=["GET"])
def edit_department(id):
    selected_department = Department.query.get(id)
    department_form = DepartmentForm(obj=selected_department)
    department_form.set_choices()
    return render_template('departments/edit.html', department=selected_department, department_form=department_form, delete_form=DeleteForm())


# Allows app to be run with python3 file_name.py
if __name__ == '__main__':
    # Enable development mode
    app.config['ENV'] = 'development'
    # Enable debug mode
    app.config['DEBUG'] = True
    app.run()
