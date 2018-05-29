# Solution to Blueprints Part I - Questions

1. Describe the MVC pattern.
    - The MVC pattern has three parts: model, view, and controller. The model represents the data, the view is what a user sees, and the controller retrieves data from the models if necessary to present the user with the requested view. In Flask, the models are the SQLAlchemy classes representing database tables. The views are the HTML files with Jinja2 templating. And the controllers are the view functions (with the @app.route decorator) that display the view/HTML file according to what URL route the user requests, passing relevant database information to the render_template function if needed.
2. In the MVC pattern, does the model communicate directly with the view?
    - No, the controller interacts with the model if necessary to provide the user with the appropriate view.
2. What is the purpose of blueprints?
    - Blueprints are a feature of Flask that help with organizing Flask applications. They come in handy as the amount of code in a Flask project grows.
3. How does using blueprints help us organize bigger applications?
    - Flask allows bigger applications to separate models, views, and controllers into separate files in categorized folders for better organization.