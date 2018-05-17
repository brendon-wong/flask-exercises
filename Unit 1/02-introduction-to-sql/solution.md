# Solution to CRUD Exercises

1. Create a database called `first_assignment`
    - `create database first_assignment;`
2. Connect to that database
    - `\c first_assignment;`
3. Create a table called `products` with columns for:
    - `id`, which should be a unique auto-incremementing integer
    - `name`, which should be text, and not nullable
    - `price`, which should be a floating point number, and greater than zero
    - `can_be_returned`, which should be a boolean, and not nullable
    - `create table products (id serial primary key, name text not null, price real check (price > 0), can_be_returned boolean not null);`
4. Add a product to the table with the name of "chair", price of 44.00, and can_be_returned of false.
    - `insert into products (name, price, can_be_returned) values ('chair', 44.00, False);`
5. Add a product to the table with the name of "stool", price of 25.99, and can_be_returned of true.
    - `insert into products (name, price, can_be_returned) values ('stool', 25.99, True);`
5. Add a product to the table with the name of "table", price of 124.00, and can_be_returned of false.
    - `insert into products (name, price, can_be_returned) values ('table', 124.00, False);`
6. Display all of the rows and columns in the table.
    - `select * from products;`
7. Display all of the names of the products.
    - `select name from products;`
8. Display all of the names and prices of the products.
    - `select name, price from products;`
9. Add a new product - make up whatever you would like!
    - `insert into products (name, price, can_be_returned) values ('iPhone X', 999.00, True);`
10. Display only the products that `can_be_returned`.
    - `select * from products where can_be_returned = True;`
12. Display only the products that have a price less than 44.00
    - `select * from products where price < 44;`
13. Display only the products that have a price in between 22.50 and 99.99
    - `select * from products where price >= 22.50 and price <= 99.99;`
