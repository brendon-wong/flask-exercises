# Flask Exercises

This repository contains Flask instructional lessons, exercises, and exercise solutions. Lessons and exercises are based off of Rithm's [Flask Fundamentals](https://www.rithmschool.com/courses/flask-fundamentals) course, shared under [this CC license](https://creativecommons.org/licenses/by-nc-nd/4.0/). The lesson text has been archived here without modification.

To use this repository, you can look at a lesson on Rithm's website or use the archived lesson text in each lesson folder. Complete the lesson's associated exercises in app.py. I have included notes for each section in each lesson's readme section under "Brendon's Notes." Each lesson has tests in the test.py module which you can refer to while developing to see what the exercise expects. My solutions to each exercise, which pass all tests, are in solution.py. Rithm's official solutions can be found [here](https://github.com/rithmschool/python_curriculum_exercises/tree/solutions).

The solutions were created with Flask version 1.0.2 and Python version 3.6.5 and will likely be forward compatible with future releases.

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

### Postgres
- Install [Homebrew](https://brew.sh) if Homebrew is not already installed
- `brew install postgres` to install Postgres
- `brew services start postgresql` to start Postgres
- `brew services stop postgresql` to stop Postgres
- `psql database name` to connect to a database

### Unit 1 - Flask Fundamentals and Relational Databases

- [01 Introduction To Flask](./Unit-01/01-flask-intro/readme.md)
- [02 Routing with Flask](./Unit-01/02-flask-routing/readme.md)
- [03 Templating with Jinja2](./Unit-01/03-templating/readme.md)
- [04 CRUD with Flask](./Unit-01/04-flask-crud/readme.md)
- [05 SQL With Flask and Postgres](./Unit-01/05-sql-flask/readme.md)
- [06 SQL Alchemy, Part I](./Unit-01/06-sql-alchemy-1/readme.md)
- [07 SQL Alchemy, Part II](./Unit-01/07-sql-alchemy-2/readme.md)
- [08 Testing With Flask](./Unit-01/08-testing/readme.md)
- [09 Server Side Validation with WTForms](./Unit-01/09-forms/readme.md)

### Unit 2 - Flask and Users

- [01 Structuring Larger Flask Applications](./Unit-02/01-blueprints/readme.md)
- [02 Many to Many](./Unit-02/02-many-to-many/readme.md)
- [03 Hashing and Sessions](./Unit-02/03-hashing-sessions/readme.md)
- [04 Authentication with Flask Login](./Unit-02/04-flask-login/readme.md)
- [05 OAuth with Flask](./Unit-02/05-oauth/readme.md)
