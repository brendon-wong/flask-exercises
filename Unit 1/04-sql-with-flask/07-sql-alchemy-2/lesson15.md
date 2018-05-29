## One To Many Associations

### Objectives

By the end of this chapter, you should be able to:

*   Create a one-to-many association using Flask-SQLAlchemy and Flask Migrate

### Associations

Let's add an association. We're going to start with a one-to-many as they are much easier to implement. Let's build off of our application and imagine that one student has many excuses. Go ahead and modify your Student model so that it has one more attribute:

~~~~
class Student(db.Model):

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    excuses = db.relationship('Excuse', backref='student',
                                lazy='dynamic')

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
~~~~

So everything looks normal, but we have this property called `excuses`! What we are doing here is establishing a relationship between a student and that student's excuses. Every student is going to have a property called 'excuses' which will return a list of all of the excuses for that student. By default, SQLAlchemy will look for a foreign key in the `excuses` table to the id column in the `students` table.

What about the keyword arguments? The `backref` allows us to go from an excuse back to the student who made the excuse. By using a `backref`, each `excuse` will have a property called `student`, which refers to the entire student object who has that specific excuse.

What about `lazy`? Lazy defines when SQLAlchemy will load the data from the database. There are four different options for this keyword. The Flask-SQLAlchemy [docs](http://flask-sqlalchemy.pocoo.org/2.3/models/#one-to-many-relationships) explain the different values as follows:

> `'select'` / `True` (which is the default, but explicit is better than implicit) means that SQLAlchemy will load the data as necessary in one go using a standard select statement.
> 
> `'joined'` / `False` tells SQLAlchemy to load the relationship in the same query as the parent using a `JOIN` statement.
> 
> `'subquery'` works like `'joined'` but instead SQLAlchemy will use a subquery.
> 
> `'dynamic'` is special and can be useful if you have many items and always want to apply additional SQL filters to them. Instead of loading the items SQLAlchemy will return another query object which you can further refine before loading the items.

We'll be able to dig into this a bit more concretely after we have an excuses table. So let's make one! Here's what that might look like (you can put this in your `app.py`, just like with the Student model):

~~~~
class Excuse(db.Model):

    __tablename__ = "excuses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    is_believable = db.Column(db.Boolean)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

    def __init__(self, name, is_believable, student_id):
        self.name = name
        self.is_believable = is_believable
        self.student_id = student_id
~~~~

Since we set up a `backref` in our `Student` model, we do not need to do much more heavy lifting here aside from make sure we have a foreign key! (Though if you want, you can define a **repr** instance method on excuses so that you get more helpful messages when you look at an excuse in the terminal.)

At this point, your `app.py` should look something like this:

~~~~
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/learn-flask-migrate'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db)

class Student(db.Model):

    __tablename__ = "students" # table name will default to name of the model

    # Create the three columns for our table
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    excuses = db.relationship('Excuse', backref='student',
                                lazy='dynamic')

    # define what each instance or row in the DB will have (id is taken care of for you)
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    # this is not essential, but a valuable method to overwrite as this is what we will see when we print out an instance in a REPL.
    def __repr__(self):
        return f"The student's name is {self.first_name} {self.last_name}"

class Excuse(db.Model):

    __tablename__ = "excuses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    is_believable = db.Column(db.Boolean)
    # remember - the name of our table is "students"
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

    def __init__(self, name, is_believable, student_id):
        self.name = name
        self.is_believable = is_believable
        self.student_id = student_id
~~~~

Since we just added another model, we'll also need to create and run a new migration. Remember, we only need to `init` once: this time, we just need to run the following commands:

~~~~
flask db migrate
flask db upgrade
~~~~

You should now have a second table in your database, as well as an association between the two tables! You should also see both of your migrations inside of `migrations/versions`.

Now let's open up an `ipython` REPL and use DML to add some students and excuses!

~~~~
from app import db, Student, Excuse

elie = Student('Elie', 'Schoppik')
matt = Student('Matt', 'Lane')
michael = Student('Michael', 'Hueter')

db.session.add_all([elie, matt, michael])

db.session.commit()

len(Student.query.all()) # 3

elie = Student.query.get(1)

excuse1 = Excuse('My homework ate my dog', False, 1)

db.session.add(excuse1)
db.session.commit()

elie.excuses.all() # list of excuses
elie.excuses.first().is_believable # False

Excuse.query.get(1).student # The student's name is Elie Schoppik

excuse2 = Excuse('I overslept', True, 1)

db.session.add(excuse2)
db.session.commit()

len(elie.excuses.all()) # 2
~~~~

If you want to double-check that your data is stored in the database, we can also hop into the database using `psql learn-flask-migrate` and run some SQL commands! You should see something like this:

~~~~
SELECT * FROM students;

/*
 id | first_name | last_name
----+------------+-----------
  1 | Elie       | Schoppik
  2 | Matt       | Lane
  3 | Michael    | Hueter
(3 rows)
*/

SELECT * FROM excuses;

/*
 id |          name          | is_believable | student_id
----+------------------------+---------------+------------
  1 | My dog ate my homework | f             |          1
  2 | I overslept            | t             |          1
(2 rows)
*/
~~~~

We can also revisit the `lazy` kwarg that we established in the ORM relationship. When we have `lazy='dynamic'`, you should be able to see the following in iPython:

~~~~
from app import db, Student, Excuse
elie = Student.query.get(1)
elie.excuses
# <sqlalchemy.orm.dynamic.AppenderBaseQuery at 0x10f273198>
~~~~

Note that the excuses attribute returns a query object - not the actual data itself. If you have `SQLALCHEMY_ECHO` set to `True`, you should also see that no query is run on the `excuses` table in any of the lines above. It's only if you execute the excuses query (e.g. with `elie.excuses.all()`) that you'll see some SQL being run on the `excuses` table.

For comparison, if you change the `lazy` value to `'select'` and do the same thing, you should see that the query against the excuses table gets run as soon as you look at `elie.excuses`. The `excuses` attribute automatically contains the data, not just a query object.

What about `'joined'` and `'subquery'`? With `'joined'`, the query to `excuses` is run immediately when we get the student, rather than being delayed until we look at `elie.excuses`. In this case, only one query is made to the database, it's just a bit more complicated, since it gets the student and all of that student's excuses at the same time. `'subquery'` has the same effect, but the query issued is different. If you'd like to learn more about joins vs. subqueries, check out this [article](https://www.essentialsql.com/what-is-the-difference-between-a-join-and-subquery/). For now, we won't emphasis this distinction much - none of the later examples will ever set `lazy` to be `'subquery'`.

### Screencast

If you'd like to see an example of building an application with a 1:M association and migrations, feel free to watch the screencast below.

Screencast: https://www.youtube.com/watch?v=81UwMhpuxJk

### Exercise

Complete the [Second Flask-SQLAlchemy](https://github.com/rithmschool/python_curriculum_exercises/blob/master/Unit-01/07-sql-alchemy-2/readme.md) exercise.

When you're ready, move on to [Responding with JSON](/courses/flask-fundamentals/using-jsonify)