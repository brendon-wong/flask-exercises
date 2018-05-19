## Database Performance

### Objectives:

By the end of this chapter, you should be able to:

*   Define **n + 1 queries** and learn how to avoid them
*   Understand how proper **indexing** can make or break DB performance
*   Learn how to quantify database query performance with `EXPLAIN ANALYZE`

### n + 1 Queries

1:M and M:N relationships can sometimes be difficult to manage in your application code, even if you're using an ORM. Consider an application where you have a 1:M relationship with managers:employees, and you are displaying a page which has each manager's profile listed with all of their employees' profiles listed underneath.

Naively, you might do something like this:

1.  Query all the managers
   ~~~~
   SELECT * FROM managers;
   ~~~~
1.  For each manager,
   ~~~~
   SELECT * FROM employees where manager_id = '?';
   ~~~~
In this instance, you execute _n_ + 1 queries, where _n_ is the number of employees, and the +1 is the original query for managers.

This is a lot of strain to put on your database, especially if _n_ is a very large number.

It's also completely inefficient! You can do the same thing with two queries:

1.  Query all the managers the same
2.  Query all employees

Then, in your application code, loop through employees in your application code to match `manager.id == employee.manager_id`.

In other words, load all the data before iterating through it to minimize the number of queries against the database.

Your application code will almost always perform a large iteration faster than the equivalent number of roundtrips to the database, as most production databases incur substantial network latency (the time it takes the query instruction and its response data to transmit back-and-forth over the internet).

For more info on n + 1 queries, [read this article](https://medium.com/@bretdoucette/n-1-queries-and-how-to-avoid-them-a12f02345be5).

### Indexing

Say you have a physics textbook and you're looking for all the sections that mention the word "Einstein." If there were no index section in the back of the book, you would have to go through every page, cover-to-cover in order to fulfill your query. In the same way, database tables with no indices can make searching for specific column values very slow.

A database index is a special data structure that efficiently stores column values to speed up row retrieval via `SELECT` and `WHERE` (i.e. "read") queries. For instance, if you place an index on a `name` column in a `people` table, then any query using `name` will generally execute faster since fewer rows have to be scanned due to the efficient structure.

#### How efficient are indexes?

In general, database software (including PostgreSQL) use tree-like data structures to store the data, which can retrieve values in logarithmic time instead of linear time. Translation: If have 1,000,000 rows and are looking for a single column value, instead of examining every row, we can examine approximately log2(1000000) ≈ 20 rows to get our answer, which is an incredible improvement! For more information on time complexity [click here](/courses/javascript-computer-science-fundamentals/introduction-to-big-o-notation) and for more on tree structures [click here](/courses/javascript-computer-science-fundamentals/introduction-to-binary-search-trees).

#### Why don't we just index everything?

There is a tradeoff with indexing! For every indexed column, a copy of that column's data has to be stored as a tree, which can take up a lot of space. Also, every `INSERT` and `UPDATE` query becomes more expensive, since data in both the regular table AND the index have to be dealt with.

#### Indexing in PostgreSQL

Indexing is part of DDL, but indexes can be created or dropped at any time. The more records in the database at the time of creation, the slower the indexing process will be.

Here is how indexes are specified in Postgres:

~~~~
CREATE INDEX index_name ON table_name (column_name);
~~~~

_Note: `index_name` is optional._

You can also create a multi-column index, which is useful if you are constantly querying by two fields at once (e.g. `first_name` and `last_name`):

~~~~
CREATE INDEX index_name ON table_name (column1_name, column2_name);
~~~~

Indexes can also be unique:

~~~~
CREATE UNIQUE INDEX full_name ON people (first_name, last_name);
~~~~

And can be dropped simply by name:

~~~~
DROP INDEX full_name;
~~~~

For more information on PostgreSQL index syntax, [click here](https://www.postgresql.org/docs/current/static/sql-createindex.html).

#### When to Index

Indexes are used in every PostgreSQL table by default on the primary key column. In general, if you are building an application that is more read-heavy than write-heavy, indexes are your friend and can be safely placed on columns that are used frequently in queries to speed up performance. However, there are other index types besides the default that may be more efficient for your data, so definitely read up on some PostgreSQL performance optimizations [here](https://robots.thoughtbot.com/postgresql-performance-considerations) and [here](https://devcenter.heroku.com/articles/postgresql-indexes).

### Measuring Database Query Performance

For every query that you enter into `psql`, PostgreSQL builds a **query plan** which is its best guess at the most optimal way to actually execute the query. This query plan includes things like choice of data structures, algorithms, and operations that Postgres will execute under the hood to satisfy your query.

Lucky for us, Postgres will tell us what the query planner is thinking with a simple command. For any DML operation, simply type `EXPLAIN` before the query. The query will NOT actually execute, but a query plan will be built and printed out for you to see:

~~~~
EXPLAIN SELECT * FROM people
            JOIN interests ON people.id=interests.people_id;
~~~~

~~~~
                              QUERY PLAN
----------------------------------------------------------------------
 Hash Join  (cost=29.12..66.27 rows=1200 width=108)
   Hash Cond: (interests.people_id = people.id)
   ->  Seq Scan on interests  (cost=0.00..22.00 rows=1200 width=40)
   ->  Hash  (cost=18.50..18.50 rows=850 width=68)
         ->  Seq Scan on people  (cost=0.00..18.50 rows=850 width=68)
(5 rows)
~~~~

We're not going to delve to deeply into the definitions here, but just know that the `Hash Join` represents the operation/algorithm, and `cost` units have arbitrary relative value (made up by Postgres), and the `rows` are the totaly number of rows output by each step.

Arbitrary cost might not very useful on its own, but we can add another keyword `ANALYZE` to our query to _actually execute_ the query and give us some more concrete units:

~~~~
EXPLAIN ANALYZE SELECT * FROM people
    JOIN interests ON people.id=interests.people_id;
~~~~

~~~~
                                                   QUERY PLAN
----------------------------------------------------------------------------------------------------------------
 Hash Join  (cost=29.12..66.27 rows=1200 width=108) (actual time=0.062..0.065 rows=4 loops=1)
   Hash Cond: (interests.people_id = people.id)
   ->  Seq Scan on interests  (cost=0.00..22.00 rows=1200 width=40) (actual time=0.010..0.011 rows=4 loops=1)
   ->  Hash  (cost=18.50..18.50 rows=850 width=68) (actual time=0.010..0.010 rows=3 loops=1)
         Buckets: 1024  Batches: 1  Memory Usage: 9kB
         ->  Seq Scan on people  (cost=0.00..18.50 rows=850 width=68) (actual time=0.004..0.005 rows=3 loops=1)
 Planning time: 0.153 ms
 Execution time: 0.112 ms
(8 rows)
~~~~

Notice now our query plan includes the actual benchmarks in time and memory as well as things like the number of loops it executed! This can be a great tool for debugging queries that are executing unusually slow or slower than expected.

The idea is that if you find a particularly slow query, consider rewriting it to optimize performance. Sometimes, it may be necessary to restructure the data itself or adjust PostgreSQL configs.

In this lesson we just want you to be aware of the `EXPLAIN ANALYZE` paradigm; it's far too advanced to cover in-depth right now, but you can read more on the [PostgreSQL docs](https://www.postgresql.org/docs/current/static/using-explain.html), as well as two helpful articles [here](https://robots.thoughtbot.com/reading-an-explain-analyze-query-plan) and [here](https://robots.thoughtbot.com/advanced-postgres-performance-tips).

When you're ready, move on to [Intermediate SQL Exercises](/courses/flask-fundamentals/intermediate-sql-exercise)