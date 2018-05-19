### Part 1

Write the following SQL commands to produce the necessary output

- Join the two tables so that every column and record appears, regardless of if there is not an owner_id.
    - `select * from owners full join vehicles on owners.id = vehicles.owner_id;`
- Count the number of cars for each owner. Display the owners `first_name`, `last_name` and `count` of vehicles. The first_name should be ordered in ascending order.
    - `select o.first_name, o.last_name, count(v.id) from owners as o join vehicles as v on o.id = v.owner_id group by o.first_name, o.last_name order by o.first_name;`
- Count the number of cars for each owner and display the average price for each of the cars as integers. Display the owners `first_name`, `last_name`, average price and count of vehicles. The `first_name` should be ordered in descending order. Only display results with more than one vehicle and an average price greater than 10000.
    - `select o.first_name, o.last_name, avg(v.price)::integer, count(v.id) from owners as o join vehicles as v on o.id = v.owner_id group by o.first_name, o.last_name having count(v.id) > 1 and avg(v.price) > 10000 order by o.first_name desc;`

### Part 2 - Codewars

Complete the following Codewars problems:

[https://www.codewars.com/kata/sql-basics-simple-join/train/sql](https://www.codewars.com/kata/sql-basics-simple-join/train/sql)
    - `SELECT p.*, c.name AS company_name FROM products AS p JOIN companies AS c ON company_id = c.id;`

[https://www.codewars.com/kata/sql-basics-simple-join-with-count](https://www.codewars.com/kata/sql-basics-simple-join-with-count)
    - `SELECT p.*, count(t.id) as toy_count FROM people AS p JOIN toys AS t ON p.id = t.people_id GROUP BY p.id;`

### Bonus

[https://www.codewars.com/kata/sql-bug-fixing-fix-the-join/train/sql](https://www.codewars.com/kata/sql-bug-fixing-fix-the-join/train/sql)

~~~~
  SELECT 
    j.job_title,
    ROUND(AVG(j.salary),2)::FLOAT AS average_salary,
    COUNT(p.id) as total_people,
    ROUND(SUM(j.salary),2)::FLOAT AS total_salary
    FROM people AS p
      JOIN job AS j ON p.id = j.people_id 
    GROUP BY j.job_title
    ORDER BY average_salary DESC;
  ~~~~