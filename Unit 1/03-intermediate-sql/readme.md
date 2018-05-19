# Joins Exercises

### Part 1

Given the following SQL.

```sql
DROP DATABASE IF EXISTS joins_exercise;

CREATE DATABASE joins_exercise;

\c joins_exercise

CREATE TABLE owners (id SERIAL PRIMARY KEY, first_name TEXT, last_name TEXT);

CREATE TABLE vehicles (id SERIAL PRIMARY KEY, make TEXT, model TEXT, year INTEGER, price REAL, owner_id INTEGER REFERENCES owners (id));

INSERT INTO owners (first_name, last_name) VALUES ('Bob', 'Hope');
INSERT INTO owners (first_name, last_name) VALUES ('Jane', 'Smith');
INSERT INTO owners (first_name, last_name) VALUES ('Melody', 'Jones');
INSERT INTO owners (first_name, last_name) VALUES ('Sarah', 'Palmer');
INSERT INTO owners (first_name, last_name) VALUES ('Alex', 'Miller');
INSERT INTO owners (first_name, last_name) VALUES ('Shana', 'Smith');
INSERT INTO owners (first_name, last_name) VALUES ('Maya', 'Malarkin');

INSERT INTO vehicles (make, model, year, price, owner_id) VALUES ('Toyota', 'Corolla', 2002, 2999.99, 1);
INSERT INTO vehicles (make, model, year, price, owner_id) VALUES ('Honda', 'Civic', 2012, 12999.99, 1);
INSERT INTO vehicles (make, model, year, price, owner_id) VALUES ('Nissan', 'Altima', 2016, 23999.99, 2);
INSERT INTO vehicles (make, model, year, price, owner_id) VALUES ('Subaru', 'Legacy', 2006, 5999.99, 2);
INSERT INTO vehicles (make, model, year, price, owner_id) VALUES ('Ford', 'F150', 2012, 2599.99, 3);
INSERT INTO vehicles (make, model, year, price, owner_id) VALUES ('GMC', 'Yukon', 2016, 12999.99, 3);
INSERT INTO vehicles (make, model, year, price, owner_id) VALUES ('GMC', 'Yukon', 2014, 22999.99, 4);
INSERT INTO vehicles (make, model, year, price, owner_id) VALUES ('Toyota', 'Avalon', 2009, 12999.99, 4);
INSERT INTO vehicles (make, model, year, price, owner_id) VALUES ('Toyota', 'Camry', 2013, 12999.99, 4);
INSERT INTO vehicles (make, model, year, price, owner_id) VALUES ('Honda', 'Civic', 2001, 7999.99, 5);
INSERT INTO vehicles (make, model, year, price, owner_id) VALUES ('Nissan', 'Altima', 1999, 1899.99, 6);
INSERT INTO vehicles (make, model, year, price, owner_id) VALUES ('Lexus', 'ES350', 1998, 1599.99, 6);
INSERT INTO vehicles (make, model, year, price, owner_id) VALUES ('BMW', '300', 2012, 22999.99, 6);
INSERT INTO vehicles (make, model, year, price, owner_id) VALUES ('BMW', '700', 2015, 52999.99, 6);
```

Write the following SQL commands to produce the necessary output

- Join the two tables so that every column and record appears, regardless of if there is not an owner_id. Your output should look like this:

```sql
/*
 id | first_name | last_name | id |  make  |  model  | year |  price  | owner_id
----+------------+-----------+----+--------+---------+------+---------+----------
  1 | Bob        | Hope      |  1 | Toyota | Corolla | 2002 | 2999.99 |        1
  1 | Bob        | Hope      |  2 | Honda  | Civic   | 2012 |   13000 |        1
  2 | Jane       | Smith     |  3 | Nissan | Altima  | 2016 |   24000 |        2
  2 | Jane       | Smith     |  4 | Subaru | Legacy  | 2006 | 5999.99 |        2
  3 | Melody     | Jones     |  5 | Ford   | F150    | 2012 | 2599.99 |        3
  3 | Melody     | Jones     |  6 | GMC    | Yukon   | 2016 |   13000 |        3
  4 | Sarah      | Palmer    |  7 | GMC    | Yukon   | 2014 |   23000 |        4
  4 | Sarah      | Palmer    |  8 | Toyota | Avalon  | 2009 |   13000 |        4
  4 | Sarah      | Palmer    |  9 | Toyota | Camry   | 2013 |   13000 |        4
  5 | Alex       | Miller    | 10 | Honda  | Civic   | 2001 | 7999.99 |        5
  6 | Shana      | Smith     | 11 | Nissan | Altima  | 1999 | 1899.99 |        6
  6 | Shana      | Smith     | 12 | Lexus  | ES350   | 1998 | 1599.99 |        6
  6 | Shana      | Smith     | 13 | BMW    | 300     | 2012 |   23000 |        6
  6 | Shana      | Smith     | 14 | BMW    | 700     | 2015 |   53000 |        6
  7 | Maya       | Malarkin  |    |        |         |      |         |         
(15 rows)
*/
```

- Count the number of cars for each owner. Display the owners `first_name`, `last_name` and `count` of vehicles. The first_name should be ordered in ascending order. Your output should look like this:

```sql
/*
 first_name | last_name | count 
------------+-----------+-------
 Alex       | Miller    |     1
 Bob        | Hope      |     2
 Jane       | Smith     |     2
 Melody     | Jones     |     2
 Sarah      | Palmer    |     3
 Shana      | Smith     |     4
(6 rows)
*/
```

- Count the number of cars for each owner and display the average price for each of the cars as integers. Display the owners `first_name`, `last_name`, average price and count of vehicles. The `first_name` should be ordered in descending order. Only display results with more than one vehicle and an average price greater than 10000. Your output should look like this:

```sql
/*
 first_name | last_name | average_price | count 
------------+-----------+---------------+-------
 Shana      | Smith     |         19875 |     4
 Sarah      | Palmer    |         16333 |     3
 Jane       | Smith     |         15000 |     2
*/
```

### Part 2 - Codewars

Complete the following Codewars problems:

[https://www.codewars.com/kata/sql-basics-simple-join/train/sql](https://www.codewars.com/kata/sql-basics-simple-join/train/sql)

[https://www.codewars.com/kata/sql-basics-simple-join-with-count](https://www.codewars.com/kata/sql-basics-simple-join-with-count)

### Bonus

[https://www.codewars.com/kata/sql-bug-fixing-fix-the-join/train/sql](https://www.codewars.com/kata/sql-bug-fixing-fix-the-join/train/sql)

### Brendon's Notes:
- For lesson 8, to sort joins by ascending people.id, use `order by people.id` at the end of queries (ascending order is the default for order by)
- For lesson 9, the coverage of normal forms was a bit sparse, this [four part series](https://www.essentialsql.com/get-ready-to-learn-sql-database-normalization-explained-in-simple-english/) provides a clearer explanation
    - Database normalization involves following best practices in database design to eliminate problems with performing CRUD (create, read, update delete) operations on a database and decrease the storage space a database needs
    - First normal form: each row in a column should only contain one unit of information; for example having multiple phone numbers or addresses separated by commas in one data value are not allowed
    - Second normal form: each table should have a specific purpose which means all columns should relate to the primary key; for example if the primary key is the employee ID, employee name is an acceptable column but information about the address and phone number of the employee's office should go in a separate table
    - Third normal form: all columns should depend on what the primary key is and should not depend on the values in other columns too; for example if there is a column for "employee performance score" from 1–100 and a column for whether the employee is a "top achiever" based on having a score between 90–100, the top achiever value depends on the employee performance value and the relationship between the score and being a top achiever should go in a separate table instead of requiring updates to both the "performance" and "top achiever" columns whenever the employee's performance score enters or leaves the 90–100 range
- For lesson 10, [the ERDPlus website](https://erdplus.com) is a tool for creating entity relationship diagrams online for free