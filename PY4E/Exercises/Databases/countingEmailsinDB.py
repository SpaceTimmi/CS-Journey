# Databases

"""
Counting Organizations
This application will read the mailbox data (mbox.txt) and count the number of email messages per organization (i.e. domain name of the email address) using a database with the following schema to maintain the counts.

CREATE TABLE Counts (org TEXT, count INTEGER)
When you have run the program on mbox.txt upload the resulting database file above for grading.
If you run the program multiple times in testing or with different files, make sure to empty out the data before each run.

You can use this code as a starting point for your application: http://www.py4e.com/code3/emaildb.py.

The data file for this application is the same as in previous assignments: http://www.py4e.com/code3/mbox.txt.

Because the sample code is using an UPDATE statement and committing the results to the database as each record is read in the loop, it might take as long as a few minutes to process all the data. The commit insists on completely writing all the data to disk every time it is called.

The program can be speeded up greatly by moving the commit operation outside of the loop. In any database program, there is a balance between the number of operations you execute between commits and the importance of not losing the results of operations that have not yet been committed.
"""

import sqlite3

# Creating the table and cursor
conn = sqlite3.connect('./results/countdb.sqlite')
cursor = conn.cursor()

cursor.executescript("""
DROP TABLE IF EXISTS Counts;

CREATE TABLE Counts (
    org TEXT,
    count INTEGER
)
""")

# adding each org to the database and updating its count as necessary
fh = open('./data/mbox.txt')
numOfEntries = 0
for index, line in enumerate(fh):
    if not line.startswith('From: '): continue

    numOfEntries += 1
    pieces = line.split()
    email = pieces[1]
    org = email.split('@')[1]

    cursor.execute('SELECT count FROM Counts WHERE org = ? ', (org,))
    row = cursor.fetchone()
    if row is None:
        cursor.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (org,))
    else:
        cursor.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (org,))

    # Make a commit for every 50 entries (extra)
    if (numOfEntries % 50) == 0: conn.commit()

# Final commit
conn.commit()

cursor.close()
