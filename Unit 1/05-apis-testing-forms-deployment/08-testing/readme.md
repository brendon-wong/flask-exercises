# Testing Flask Application

It's time to add tests! Use Flask-testing to write tests for each CRUD on your users and messages app from the previous assignment. This includes writing tests for: 

- creating, reading, updating and deleting a user
- creating, reading, updating and deleting a message

**Bonuses**

- Write tests for 404 errors
- Write a test that ensures your edit form is prepopulated with a messages' current values
- It would be weird if a user's `first_name` or `last_name` were empty. Write a test to make sure that neither is an empty string. Then write the code in your application to make the test pass!

### Brendon's Notes
- Rithm's lesson 16 deals with a feature of Flask called "blueprints" which may have been part of a former version of Unit 1, but is currently covered in Unit 2 in this repository; because this lesson references content that hasn't been learned yet and because JSON-related material is covered in Unit 2, this lesson can be skimmed or skipped entirely