# Flask Basics

For this assignment you will be creating a very small flask application. Your application should:

- have a route for `/welcome`, which responds with the string "welcome"
- have a route for `/welcome/home`, which responds with the string "welcome home"
- have a route for `/welcome/back`, which responds with the string "welcome back"

### Bonus

Add another route to `/sum` and inside the function which sends a response, create a variable called `sum` which is equal to 5+5. Respond with the sum variable.

### Brendon's Notes
- For simplicity's sake, I recommend using Python 3's built in venv module to create virtual environments instead of using virtualenvwrapper
- The tests only work with lower case words and no punctuation, feel free to view and change the tests
- For added convenience, to eliminate the use of environment variables, I use app.run() in solution.py to run the app with `python3 solution.py` instead of setting environment variables and using `flask run`