"""
Set up the sample database for the AIS Canteen Pre-order app.

You write the SQL in this file, then run it:

    python setup_db.py

It is safe to run again. It rebuilds the menu each time, so if you make a
mistake, fix the SQL and run it once more.

Open ais.db in the SQLite Viewer (click the file in VS Code) to see the table
you made. Python includes the sqlite3 library, so there is nothing to install.
"""

import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ais.db")

db = sqlite3.connect(DB_PATH)


# --------------------------------------------------------------------------
# TODO (Period 1): build the menu table.
#
# Write SQL between the triple quotes below. You need three things, in order:
#
#   1. Delete the old table if there is one:     DROP TABLE IF EXISTS menu;
#   2. Create the table with three columns:
#        id     a whole number that counts up by itself (the primary key)
#        name   text that cannot be empty
#        price  a decimal number that cannot be empty
#   3. Insert at least seven canteen items, one INSERT per item, e.g.
#        INSERT INTO menu (name, price) VALUES ('Nasi lemak', 3.50);
#
# Every SQL statement ends with a semicolon.
# --------------------------------------------------------------------------
db.executescript(
    """
    -- write your menu SQL here
    """
)


# --------------------------------------------------------------------------
# TODO (Period 3): build the orders table.
#
# Each row is one student's order of one item. You need these columns:
#   id        a whole number that counts up by itself (the primary key)
#   username  text that cannot be empty   (who ordered)
#   item      text that cannot be empty   (the item name)
#   price     a decimal number that cannot be empty
#   created   text that cannot be empty   (when they ordered)
#
# Use  CREATE TABLE IF NOT EXISTS orders (...)  so re-running keeps old orders.
# --------------------------------------------------------------------------
db.executescript(
    """
    -- write your orders SQL here
    """
)


db.commit()
db.close()
print("Database ready:", DB_PATH)
