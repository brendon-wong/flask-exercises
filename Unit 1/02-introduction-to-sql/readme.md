# CRUD Exercises

### Part 1

Write the SQL commands necessary to do the following:

1. Create a database called `first_assignment`
2. Connect to that database
3. Create a table called `products` with columns for:
    - `id`, which should be a unique auto-incremementing integer
    - `name`, which should be text, and not nullable
    - `price`, which should be a floating point number, and greater than zero
    - `can_be_returned`, which should be a boolean, and not nullable
    
4. Add a product to the table with the name of "chair", price of 44.00, and can_be_returned of false.
5. Add a product to the table with the name of "stool", price of 25.99, and can_be_returned of true.
5. Add a product to the table with the name of "table", price of 124.00, and can_be_returned of false.
6. Display all of the rows and columns in the table.
7. Display all of the names of the products.
8. Display all of the names and prices of the products.
9. Add a new product - make up whatever you would like!
10. Display only the products that `can_be_returned`. 
12. Display only the products that have a price less than 44.00
13. Display only the products that have a price in between 22.50 and 99.99

### Part 2 - Codewars

Complete the following Codewars problems:

[https://www.codewars.com/kata/sql-basics-simple-where-and-order-by/train/sql](https://www.codewars.com/kata/sql-basics-simple-where-and-order-by/train/sql)

[https://www.codewars.com/kata/1-find-all-active-students/train/sql](https://www.codewars.com/kata/1-find-all-active-students/train/sql)

### Brendon's Notes
- With Postgres 10.3, lesson 6's add column constraint command `ALTER TABLE users ADD CONSTRAINT favorite_number NOT NULL;` does not seem to work; instead, use `ALTER TABLE users ADD UNIQUE (favorite_number);` to add the constraint 
- Use `ALTER TABLE users DROP CONSTRAINT users_favorite_number_key` to remove constraints, where the last part `users_favorite_number_key` is the name of the constraint's index
- A not-null constraint cannot be added as a table constraint so `ALTER TABLE users ALTER COLUMN favorite_number SET NOT NULL;` must be used to add the constraint and `ALTER TABLE users ALTER COLUMN favorite_number DROP NOT NULL;` must be used to remove it
- Lesson 7 has a typo under Not In, where the command should be `SELECT * FROM players WHERE jersey_number NOT IN (0,1);`