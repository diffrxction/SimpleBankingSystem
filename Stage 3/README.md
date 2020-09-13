# Bang Bang, SQL Gang !!
 Description

It's very upsetting when the data about registered users disappears after the program is completed. To avoid this problem, you need to create a database where you will store all the necessary information about the created credit cards. We will use SQLite to create the database.

SQLite is a database engine. It is software that allows users to interact with a relational database. In SQLite, a database is stored in a single file — a trait that distinguishes it from other database engines. This allows for greater accessibility: copying a database is no more complicated than copying the file that stores the data, and sharing a database implies just sending an email attachment.

You can use the sqlite3 module to manage SQLite database from Python. You don't need to install this module. It is included in the standard library.

To use the module, you must first create a `Connection` object that represents the database. Here the data will be stored in the `example.s3db file`:
```SQL
import sqlite3
conn = sqlite3.connect('example.s3db')
```
Once you have a Connection, you can create a Cursor object and call its execute() method to perform SQL queries:
```SQL
cur = conn.cursor()

# Executes some SQL query
cur.execute('SOME SQL QUERY')

# After doing some changes in DB don't forget to commit them!
conn.commit()
```
To get data returned by SELECT query you can use fetchone(), fetchall() methods:
```SQL
{
cur.execute('SOME SELECT QUERY')

# Returns the first row from the response
cur.fetchone()

# Returns all rows from the response
cur.fetchall()
}
```
Instruction

In this stage, create a database named card.s3db with a table titled card. It should have the following columns:

   - id INTEGER
   - number TEXT
   - pin TEXT
   - balance INTEGER DEFAULT 0

Pay attention: your database file should be created when the program starts, if it hasn’t yet been created. And all created cards should be stored in the database from now.

> Do not forget to commit your DB changes right after executing a query!

Example

The symbol `>` represents the user input. Notice that it's not a part of the input.

```
{
1. Create an account
2. Log into account
0. Exit
>1

Your card has been created
Your card number:
4000003429795087
Your card PIN:
6826

1. Create an account
2. Log into account
0. Exit
>2

Enter your card number:
>4000003429795087
Enter your PIN:
>4444

Wrong card number or PIN!

1. Create an account
2. Log into account
0. Exit
>2

Enter your card number:
>4000003429795087
Enter your PIN:
>6826

You have successfully logged in!

1. Balance
2. Log out
0. Exit
>1

Balance: 0

1. Balance
2. Log out
0. Exit
>2

You have successfully logged out!

1. Create an account
2. Log into account
0. Exit
>0

Bye!
}
```
