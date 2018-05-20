# SQL With Flask

For this application you will be refactoring CRUD on the resouce `snacks`. Instead of using a list, your application should use postgres and the `psycopg2` module! 

Make sure that you isolate your `psycopg2` related code into a file called `db.py` so that you do not have one large `app.py` file.

Make sure you create a database called `flask-sql-snacks` for your application and in order to run the tests, make sure you create a database called `flask-sql-snacks-test`

Your application should:

- display all the `snacks`
- allow a user to create `snacks` 
    -  each snack should have a `name` and `kind`
- allow a user to edit a snack
- allow a user to delete a snack

### Brendon's Notes
- For the SQL With Flask exercise, copy paste your snack app from the Flask CRUD section including app.py, the templates folder, the the static folder if you have one, but excluding snack.py because it will be replaced by db.py
- How to run the application
    - `createdb flask-sql-snacks` and `createdb flask-sql-snacks-test` to create the primary and testing databases
    - `python3 -i db.py` to open db.py in the Python interpreter where you can execute commands
        - You can test the output of your CRUD functions in the Python interpreter
    - `create_table()` to create the snacks table
    - The database and snacks database table are now set up and the application can run correctly
    - `DROP SCHEMA public CASCADE;` and `CREATE SCHEMA public;` will reset the database; in solution_db.py I created a reset_db function to run these commands to reset the database
        - Whenever the database is reset, `create_table()` needs to be run again
- In order to pass the tests I had to make the app connect to the testing database by switching the database in the connect function in solution_db.py to `flask-sql-snacks-test`