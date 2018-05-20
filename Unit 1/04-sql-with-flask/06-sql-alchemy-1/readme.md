# Flask-SQLAlchemy, Part I

It's time for more refactoring! This time, refactor your `snack` app to use Flask SQLAlchemy. You should have a `Snack` model to serve as an interface between instances in Python and rows in your `snacks` table.

### Bonus

Research how to handle 404 errors using Flask-SQLAlchemy, and add a 404 page to your app that will get sent if someone tries to find a snack with an invalid id.

### Brendon's Notes
- IPython is unnecessary for this lesson, all commands can be executed by importing app.py with SQLAlchemy configured with `python3 -i app.py`
- Under the "Update" part of lesson 13, the command to change the model of the computer should be  `first_computer.name = "Commodore 64"` to correspond to the name and memory_in_gb instance attributes of Computer objects