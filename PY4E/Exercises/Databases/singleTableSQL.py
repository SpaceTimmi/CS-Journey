# Databases

"""
If you don't already have it, install the SQLite Browser from http://sqlitebrowser.org/.

Then, create a SQLITE database or use an existing database and create a table in the database called "Ages":

CREATE TABLE Ages (
  name VARCHAR(128),
  age INTEGER
)
Then make sure the table is empty by deleting any rows that you previously inserted, and insert these rows and only these rows with the following commands:

DELETE FROM Ages;
INSERT INTO Ages (name, age) VALUES ('Kori', 35);
INSERT INTO Ages (name, age) VALUES ('Ailie', 39);
INSERT INTO Ages (name, age) VALUES ('Arman', 33);
INSERT INTO Ages (name, age) VALUES ('Caryn', 39);
INSERT INTO Ages (name, age) VALUES ('Khansa', 35);
INSERT INTO Ages (name, age) VALUES ('Erika', 40);
Once the inserts are done, run the following SQL command:
SELECT hex(name || age) AS X FROM Ages ORDER BY X
Find the first row in the resulting record set and enter the long string that looks like 53656C696E613333.
Note: This assignment must be done using SQLite - in particular, the SELECT query above will not work in any other database.
"""

import sqlite3

conn = sqlite3.connect('./results/agesdb.sqlite')
cursor = conn.cursor()

# Creating, Deleting existing data & Inserting into the table.
cursor.executescript("""
DROP TABLE IF EXISTS Ages;

CREATE TABLE Ages (
    name VARCHAR(123),
    age INTEGER
) ;

DELETE FROM Ages;
INSERT INTO Ages (name, age) VALUES ('Kori', 35);
INSERT INTO Ages (name, age) VALUES ('Ailie', 39);
INSERT INTO Ages (name, age) VALUES ('Arman', 33);
INSERT INTO Ages (name, age) VALUES ('Caryn', 39);
INSERT INTO Ages (name, age) VALUES ('Khansa', 35);
INSERT INTO Ages (name, age) VALUES ('Erika', 40);
""")

# Selecting the hex data and printing it out .
cursor.execute('SELECT hex(name || age) AS X FROM Ages ORDER BY X')
result = cursor.fetchone()[0]
print(result)
cursor.close()

