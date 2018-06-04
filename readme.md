# Flask Exercises

This repository contains Flask instructional lessons, exercises, and exercise solutions. Lessons and exercises are based off of Rithm's [Flask Fundamentals](https://www.rithmschool.com/courses/flask-fundamentals) course, shared under [this CC license](https://creativecommons.org/licenses/by-nc-nd/4.0/). The lesson material has been archived here without modification aside from minor error corrections.

To use this repository, you can look at the lessons on Rithm's website or use the lesson material in each lesson folder. I have included notes for each section in each lesson's readme section under "Brendon's Notes." My solutions to each exercise, which pass all tests, are in solution.py or solution.md depending on the section, and Rithm's solutions can be found [here](https://github.com/rithmschool/python_curriculum_exercises/tree/solutions). For the Flask sections of the exercises, write your solution in app.py. There are tests in the test.py module which you can refer to while developing to see what the exercise expects.

The solutions were created with Flask version 1.0.2, Python version 3.6.5, and PostgreSQL version 10.3 and will likely be forward compatible with future releases.

The following setup instructions are for MacOS. For other operating systems see the Flask documentation on
[Installation](http://flask.pocoo.org/docs/latest/installation/) and online Postgres resources which provide setup information for other operating systems.

### Setup
1. `git clone` this repository
2. `python3 -m venv venv` to create a new virtual environment in the root directory of the cloned folder
3. `. venv/bin/activate` to enter the virtual environment (`deactivate` to exit)
4. `pip install -r requirements.txt` to install/update all requirements

### Start Exercises
1. `. venv/bin/activate` if the virtual environment is not activated
2. Complete an exercise, referring to the lesson content, tests, and, if necessary, solution.py
3. `python3 test.py` to run tests of your solution in app.py; to see more details about the tests, use the command `python3 test.py -v`
4. To test solution.py, change the import statement at the top of test.py from `from app import app` to `from solution import app`, make additional import changes if needed, then run `python3 solution.py`
5. Refer to the solution to see alternative ways of solving the same problem and improve your coding skills

### Postgres Setup
- Install [Homebrew](https://brew.sh) if Homebrew is not already installed
- `brew install postgres` to install Postgres
- `brew services start postgresql` to start Postgres
- `brew services stop postgresql` to stop Postgres
- `psql database_name` to connect to a database

### Unit 1 - Flask Fundamentals and Relational Databases (Complete)

- [01 Introduction To Flask](./Unit%201/01-introduction-to-flask/01-flask-intro)
- [02 Routing with Flask](./Unit%201/01-introduction-to-flask/02-flask-routing)
- [03 Templating with Jinja2](./Unit%201/01-introduction-to-flask/03-templating)
- [04 CRUD with Flask](./Unit%201/01-introduction-to-flask/04-flask-crud)
- [05 SQL With Flask and Postgres](./Unit%201/04-sql-with-flask/05-sql-flask)
- [06 SQL Alchemy, Part I](./Unit%201/04-sql-with-flask/06-sql-alchemy-1)
- [07 SQL Alchemy, Part II](./Unit%201/04-sql-with-flask/07-sql-alchemy-2)
- [08 Testing With Flask](./Unit%201/05-apis-testing-forms-deployment/08-testing)
- [09 Server Side Validation with WTForms](./Unit%201/05-apis-testing-forms-deployment/09-forms)

### Unit 2 - Larger Flask Applications and User Authentication (Complete)

- [01 Structuring Larger Flask Applications](./Unit%202/06-larger-applications/01-blueprints)
- [02 Many to Many](./Unit%202/06-larger-applications/02-many-to-many)
- [03 Hashing and Sessions](./Unit%202/07-auth-and-oauth/03-hashing-sessions)
- [04 Authentication with Flask Login](./Unit%202/07-auth-and-oauth/04-flask-login)
- [05 OAuth with Flask](./Unit%202/07-auth-and-oauth/05-oauth)

### Tools that helped create Flask Exercises
- HTML to Markdown converter: https://domchristie.github.io/turndown/
- HTML tables to Markdown tables converter: https://stevecat.net/table-magic
