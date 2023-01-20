"""
Provide common values and functionallity for the PartsTracker element
testing

File:       test_setup_elements.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT, see file License
"""

import pytest
from lbk_library import Dbal

# name of test database
database_name = "parts_test.db"

# close database
def close_database(dbref):
    dbref.sql_close()


# open the test database
@pytest.fixture
def open_database(tmpdir):
    path = tmpdir.join(database_name)
    dbref = Dbal()
    # valid connection
    dbref.sql_connect(path)
    return dbref


# create an items table
def create_items_table(dbref):
    dbref.sql_query("DROP TABLE IF EXISTS 'items'")
    create_table = (
        'CREATE TABLE IF NOT EXISTS "items"'
        + '("record_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,'
        + ' "part_number" TEXT NOT NULL,'
        + ' "assembly" TEXT NOT NULL,'
        + ' "quantity" INTEGER NOT NULL,'
        + ' "condition" TEXT NOT NULL,'
        + ' "installed" INTEGER NOT NULL DEFAULT 0,'
        + ' "box" INTEGER DEFAULT NULL,'
        + ' "remarks" TEXT DEFAULT NULL)'
    )
    dbref.sql_query(create_table)
    return dbref


def create_parts_table(dbref):
    dbref.sql_query("DROP TABLE IF EXISTS 'parts'")
    create_table = (
        'CREATE TABLE IF NOT EXISTS "parts"'
        + ' ("record_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
        + ' "part_number" TEXT NOT NULL,'
        + ' "source" TEXT DEFAULT NULL,'
        + ' "description" TEXT NOT NULL,'
        + ' "remarks" TEXT DEFAULT NULL );'
    )
    result = dbref.sql_query(create_table)
