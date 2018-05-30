# Many to Many

### Part 1 

1. Finish building CRUD in the many to many application with employees and departments. You can find the starter code [here](https://github.com/rithmschool/flask-many-many-example)

Your app should have the following features:

* Full CRUD on employees
* Full CRUD on departments 
* The index or show page for employees should show the department name for each employee
* The index or show page for departments should show all employees in the department
* Use WTForms for all CRUD operations for both employees and departments 

### Part 2 

Add another resource to your users and messages application! Create a resource for tags which has a many to many relationship with messages. 

- You should be able to create full CRUD on tags 
- When you create a message, you should be able to add existing tags to it. 
- When you edit a message, you should be able to modify the tags associated to it. 
- When you create a tag, you should be able to add existing messages to it.
- When you edit a tag, you should be able to modify the messages associated to it. 

### Brendon's Notes
- The starter code for the employee and departments app is currently not available
- I made the solution for the employee and departments app as a one file Flask app, and the solution for the users, messages, and tags app as a structured Flask app
- I wrote custom tests to test tagging and displaying tags in the messages and vice versa for the messaging/tags app, which is not included in Rithm's default test.py file