# Import Flask class, render_template function, and request object
from flask import Flask, render_template, request

# Make HTTP requests with Python
import requests

# HTML parser
from bs4 import BeautifulSoup

# Create instance of Flask class, set custom template folder
app = Flask(__name__, template_folder="solution_templates")


@app.route('/person/<name>/<age>')
def person(name, age):
    return render_template("person.html", name=name, age=str(age))


@app.route('/calculate')
def calculate():
    return render_template("calc.html")


@app.route('/math')
def math():
    n1 = int(request.args.get('num1'))
    n2 = int(request.args.get('num2'))
    calculation = request.args.get('calculation')
    if calculation == "add":
        result = str(n1 + n2)
    elif calculation == "subtract":
        result = str(n1 - n2)
    elif calculation == "multiply":
        result = str(n1 * n2)
    elif calculation == "divide":
        try:
            result = str(n1 / n2)
        except ZeroDivisionError:
            result = "Division by zero"
    else:
        return "Error processing request"
    return result


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/results')
def results():
    url = 'https://news.google.com'
    keyword = request.args.get('keyword')
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")
    titles = soup.select(".titletext")
    articles = [{
        'title': title.text,
        'href': title.parent['href']
    } for title in titles]

    matching_articles = [
        article
        for article in articles
        if keyword.lower() in article['title'].lower()
    ]
    return render_template('results.html', articles=matching_articles)


# Allows app to be run with python3 file_name.py
if __name__ == '__main__':
    # Enable development mode
    app.config['ENV'] = 'development'
    # Enable debug mode
    app.config['DEBUG'] = True
    app.run()
