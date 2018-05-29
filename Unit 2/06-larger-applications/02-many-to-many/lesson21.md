### Objectives:

By the end of this chapter, you should be able to:

*   Create a many to many relationship using just SQL
*   Setup SqlAlchemy so that it realizes the database has a many to many relationship
*   Define and implement a recursive self join with SQLAlchemy

### M - M

#### Modeling a M:M in SQLAlchemy

The two resources we will be working on are `employees` and `departments`. We will say that many employees can be part of many different departments.

Let's first imagine what this would look like with SQL. When you want to model a many-to-many relationship between two resources, it turns out that you need THREE tables: one table for each resource, and one to manage the links between the two. This third table is frequently called a join table, or a through table, since you have a many-to-many relationship _through_ this table. Note also that from this perspective, a many-to-many relationship is really just a pair of one-to-many relationships, where each resource is in a one-to-many relationship with the join table.

In the simplest case, our join table will have columns for the foreign keys for both tables, but not much else. In our current example, let's call our join table table `employee_departments` and start with the following commands in the terminal:

~~~~
dropdb many-many-example
createdb many-many-example
psql many-many-example

CREATE TABLE employees (id SERIAL PRIMARY KEY, name TEXT, years_at_company INTEGER);

CREATE TABLE departments (id SERIAL PRIMARY KEY, name TEXT);

CREATE TABLE employee_departments(id SERIAL PRIMARY KEY, employee_id INTEGER REFERENCES employees (id) ON DELETE CASCADE, department_id INTEGER REFERENCES departments (id) ON DELETE CASCADE);

INSERT INTO employees (name, years_at_company) VALUES ('Elie', 2),
                                                      ('Michael', 3),
                                                      ('Angelina', 6),
                                                      ('Matt', 7),
                                                      ('Lorien', 2),
                                                      ('Meg', 4);

INSERT INTO departments (name) VALUES ('leadership'),
                                      ('education'),
                                      ('marketing'),
                                      ('evangelism'),
                                      ('operations'),
                                      ('admissions');

INSERT INTO employee_departments (employee_id, department_id) VALUES (1,1),
                                                                     (1,2),
                                                                     (1,5),
                                                                     (2,1),
                                                                     (2,2),
                                                                     (2,3),
                                                                     (2,4),
                                                                     (3,1),
                                                                     (3,2),
                                                                     (3,3),
                                                                     (3,4),
                                                                     (3,5),
                                                                     (3,6),
                                                                     (4,1),
                                                                     (4,2),
                                                                     (4,3),
                                                                     (4,5),
                                                                     (5,3),
                                                                     (5,4),
                                                                     (6,3),
                                                                     (6,5);
~~~~

Given this data, let's do some quick SQL review. Verify that the following queries generate tables where each row shows data on:

1.  The name of the employee and their department.
    
    ~~~~
    SELECT e.name, d.name
      FROM employees e
        JOIN employee_departments ed
          ON e.id = ed.employee_id
        JOIN departments d
          ON ed.department_id = d.id;
    ~~~~
    
2.  All of the employees' names and the years they've been at the company, provided they are in the `leadership` department.
    
    ~~~~
    SELECT e.name, e.years_at_company
      FROM employees e
        JOIN employee_departments ed
          ON e.id = employee_id
        JOIN departments d
          ON ed.department_id = d.id
      WHERE d.name = 'leadership';
    ~~~~
    
3.  The name of the employee and number of departments that they are in
    
    ~~~~
    SELECT e.name, COUNT(d.name)
      FROM employees e
        JOIN employee_departments ed
          ON e.id = ed.employee_id
        JOIN departments d
          ON d.id = ed.department_id
      GROUP BY e.name;
    ~~~~
    
4.  The name of the deparment and the number of employees
    
    ~~~~
    SELECT d.name, COUNT(e.name)
      FROM employees e
        JOIN employee_departments ed
          ON e.id = employee_id
        JOIN departments d
          ON ed.department_id = d.id
      GROUP BY d.name;
    ~~~~

### Associations Using Flask SQLAlchemy

So far we have seen how to implement one-to-many associations with Flask, but as our applications and schemas grow, we need to handle more complex associations. We are going to examine two of them in this section: many to many and self joins. We will also see how to implement them using SQLAlchemy. Let's get started with a new virtual environment!

Our goal will be to move from our understanding of associations using pure SQL to using Flask SQLAlchemy. For that reason, let's drop our database so that we can start fresh.

~~~~
mkvirtualenv many-many-example
workon many-many-example
dropdb many-many-example
createdb many-many-example
pip install flask ipython psycopg2 flask-sqlalchemy flask-migrate flask-wtf flask-modus
~~~~

As before, let's work with two resources: `employees` and `departments`. Many employees can be part of many different departments and vice versa. Let's write these models inside of an `app.py` file. Here's what those models could look like:

~~~~
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/many-many-example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

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
~~~~

Notice that we don't need a class for our join table: in the event that your join table just stores records of foreign keys, the ORM abstracts away this table from you entirely, and you can work with the many-to-many relationship without needing to directly manipulate the join table. Now let's generate a migration and upgrade!

~~~~
flask db init
flask db migrate -m "creating employees and departments tables"
flask db upgrade
~~~~

Let's see what this looks like by entering an `ipython` REPL and playing around with this association!

~~~~
from app import db, Employee, Department

e1 = Employee('Elie', 2)
e2 = Employee('Michael', 3)
e3 = Employee('Angelina', 6)
e4 = Employee('Matt', 7)
e5 = Employee('Lorien', 2)
e6 = Employee('Meg', 4)

d1 = Department('leadership')
d2 = Department('education')
d3 = Department('marketing')
d4 = Department('evangelism')
d5 = Department('operations')
d6 = Department('admissions')

d1.employees.extend([e1,e2,e3,e4])
d2.employees.extend([e1,e2,e3,e4])
d3.employees.extend([e2,e3,e4,e5,e6])
e1.departments.extend([d5])

e1.departments
"""   [<Department (transient 4384905312)>,  <Department (transient 4384905424)>,  <Department (transient 4384905760)>]  """

[d.name for d in e2.departments] # ['leadership', 'education', 'marketing']
~~~~

### Changes With Multiple Blueprints

Now that we have multiple blueprint files, our folder structure will be slightly different than the previous chapter. Below is a sample structure with employees and departments:

~~~~
.
├── app.py
├── project
│   ├── __init__.py
│   |── departments
│   │   ├── templates
│   │   |   ├── departments
│   │   │   │   ├── index.html
│   │   │   │   └── show.html
│   │   └── views.py
│   ├── employees
│   │   ├── templates
│   │   |   ├── employees
│   │   │   |   ├── edit.html
│   │   │   |   ├── index.html
│   │   │   |   ├── new.html
│   │   │   |   └── show.html
│   │   └── views.py
│   ├── models.py
│   └── templates
│       └── base.html
└── requirements.txt
~~~~

Notice that for now, the `models.py` file is in the `project` directory. In this structure, models are in 1 file that is shared between all blueprints. Since our models are relatively small, there's not much of a tradeoff between separating our models out versus keeping them in a single file.

Here is the `views.py` setup code for creating the employees blueprint:

~~~~
from flask import redirect, render_template, request, url_for, Blueprint
from project.models import Employee

employees_blueprint = Blueprint(
    'employees',
    __name__,
    template_folder='templates'
)

#  Routes for employees go below here
~~~~

### Adding a Many to Many in a Flask application

Now that you have an understanding of different kinds of associations, let's think about what else needs to change when we work with a many-to-many!

Remember, we do not need to use nested routes since each of these resources are independent, but we do need to be mindful of how our forms will work. Believe it or not, one of the most challenging parts of working with many to many associations is how to build forms that keep all of that data in mind!

Let's take a look at the application [here](https://github.com/rithmschool/python_curriculum/tree/master/Unit-02/examples/many_to_many). In this application we simply have a many to many with departments and employees. Our `models.py` should look almost the same as the `app.py` above, just without the creation of our app and a different import line:

~~~~
from project import db

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
~~~~

We simply have two models along with a join table that we are calling EmployeeDepartment which contains two id's that are foreign keys. Things get a bit more interesting if you start thinking about the forms. For instance, let's say that you want to be able to select the departments to assing to an employee when you create that employee. You might think that you need a form that looks something like this:

~~~~
from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired
from project.models import Department

class NewEmployeeForm(FlaskForm):
    name = TextField('Name', validators=[DataRequired()])
    years_at_company = IntegerField('Years At Company',
                                    validators=[DataRequired()])
    departments = SelectMultipleField('Departments',
                                     coerce=int,
                                     choices=[(d.id, d.name) for d in Department.query.all()])
~~~~

Here, we're basically saying that we want a select element on the page with options for each department, where we get the departments from the database in order to create the form.

There are a couple of problems with this approach, however. First, the departments table will only be queried once, when the app starts. This means that if we add some departments and then try to add an employee, we won't be able to tag that employee with the new departments!

Another problem is with the UI - the select element that you get out of the box isn't very nice looking, and while it's possible to select multiple rows, it's not convenient, and the user interface doesn't make it clear that it is even possible.

To fix these problems, we need to do a couple of things:

1.  Create an instance method to get departments on the fly when we're building a form, so that we're guaranteed to have the most up-to-date information,
2.  Overwrite the default HTML that gets generated by `SelectMultipleField` so that we can get some checkboxes showing up on the page.

To see how to implement these solutions, you can head over [here](https://github.com/rithmschool/python_curriculum/blob/master/Unit-02/examples/many_to_many/project/employees/forms.py). Our modified form looks like this:

~~~~
from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, SelectMultipleField, widgets
from wtforms.validators import DataRequired
from project.models import Department

class NewEmployeeForm(FlaskForm):
    name = TextField('Name', validators=[DataRequired()])
    years_at_company = IntegerField('Years At Company',
                                    validators=[DataRequired()])

    departments = SelectMultipleField(
        'Departments', 
        coerce=int, 
        widget=widgets.ListWidget(prefix_label=True),
        option_widget=widgets.CheckboxInput())

    def set_choices(self):
        self.departments.choices = [(d.id, d.name) for d in Department.query.all()]
~~~~

Don't be too intimidated by this code. First, note that by passing in values for `widget` and `option_widget` inside of `SelectMultipleField`, we can customize the HTML in our form. In this case, we're telling WTForms that we want to use a `ul` for our options, and for each option, we want to use a checkbox to receive user input.

Secondly, we've created an instance method called `set_choices` to grab the department data from the database. If you look at the routing logic for our app, you can see that this function is called on the form before it is passed into any of our templates, so that we can be sure that our forms always have the most up-to-date department information.

To read more about `SelectMultipleField`, including why our choices need to be formatted as a list of tuples, check out the [WTForms docs](http://wtforms.simplecodes.com/docs/0.6/fields.html#wtforms.fields.SelectMultipleField).

### Additional Types of Joins

Along with the joins we have seen, there are also a few other types of joins which can be used to model special kinds of data. Let's see two examples:

#### Self Join

What happens if we want to add the idea of a "manager" for our employees? Our manager is going to have the same exact columns as the employee, so what do we do? Create a new table? The answer is a _self join_, where we join a table on itself! Let's see what that looks like when we add a property called `manager_id` for each employee and a property called employees which refers to each instance that is an employee of another. Here's how we can modify the model:

~~~~
class Employee(db.Model):

    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    years_at_company = db.Column(db.Integer)
    manager_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    departments = db.relationship("Department",
                                  secondary=EmployeeDepartment,
                                  backref=db.backref('employees'))
    employees = db.relationship("Employee",
                                lazy="joined",
                                backref=db.backref('manager',remote_side=[id]))
    # curious about the remote_side? See what happens if you try to remove it!

    def __init__(self, first_name, last_name, manager_id=None):
        self.first_name = first_name
        self.years_at_company = years_at_company
        self.manager_id = manager_id
~~~~

To see what this looks like, run a migration, upgrade, and hop into `ipython` to verify that the relationship is set up correctly. Try creating a manager, saving that manager, and then creating some more employes who are managed by that manager. You should be able to get the employees via `manager.employees`, and from any employee get back to the manager via `employee.manager`.

#### Recursive Self Join

There are times where we also want to have parents of parents. This idea is a _recursive_ self join. We can model that in a very similar way like this:

~~~~
# recursive nested selections
class Node(db.Model):
    __tablename__ = 'node'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    data = db.Column(db.String(50))
    children = db.relationship("Node",
                    lazy="joined")

n= Node(data="first")
n2= Node(parent_id=1, data="second")
n3= Node(parent_id=2, data="third")
n4= Node(parent_id=3, data="fourth")
n5= Node(parent_id=4, data="fifth")

db.session.add_all([n,n2,n3,n4,n5])
db.session.commit()

n.children[0].children[0].children[0].children[0].data # fifth
~~~~

You can read more about self joins [here](http://stackoverflow.com/questions/3362038/what-is-self-join-and-when-would-you-use-it).

When you're ready, move on to [Intermediate Flask Exercises](/courses/intermediate-flask/intermediate-flask-exercises)