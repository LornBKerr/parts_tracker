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

# ######################################################
# Set up and access the database

# name of test database
db_name = "parts_test.db"

sql_statements = [
    (
        'CREATE TABLE IF NOT EXISTS "items" ('
        '"record_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, '
        '"part_number" TEXT NOT NULL, '
        '"assembly" TEXT NOT NULL, '
        '"quantity" INTEGER NOT NULL, '
        '"condition" TEXT NOT NULL, '
        '"installed" INTEGER NOT NULL DEFAULT 0, '
        '"box" INTEGER DEFAULT NULL, '
        '"remarks" TEXT DEFAULT NULL);'
    ),
    (
        'CREATE TABLE IF NOT EXISTS "parts" ('
        '"record_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, '
        '"part_number" TEXT NOT NULL, '
        '"source" TEXT DEFAULT NULL, '
        '"description" TEXT NOT NULL, '
        '"remarks" TEXT DEFAULT NULL );'
    ),
    (
        'CREATE TABLE "orders" ('
        '"record_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, '
        '"order_number" TEXT DEFAULT "" UNIQUE, '
        '"date" TEXT DEFAULT "", '
        '"source" TEXT DEFAULT "", '
        '"subtotal" FLOAT DEFAULT 0.0, '
        '"shipping" FLOAT DEFAULT 0.0, '
        '"tax" FLOAT DEFAULT 0.0, '
        '"discount" FLOAT DEFAULT 0.0, '
        '"total" FLOAT DEFAULT 0.0, '
        '"remarks" TEXT DEFAULT "");'
    ),
    (
        'CREATE TABLE IF NOT EXISTS "order_lines" ('
        '"record_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, '
        '"order_number" TEXT DEFAULT "", '
        '"line" INTEGER DEFAULT 0.0, '
        '"part_number" TEXT DEFAULT "", '
        '"cost_each" FLOAT DEFAULT 0.0, '
        '"quantity" INTEGER DEFAULT 0, '
        '"remarks" TEXT);'
    ),
    (
        'CREATE TABLE "conditions" ('
        '"record_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, '
        '"condition" TEXT DEFAULT "");'
    ),
    (
        'CREATE TABLE "sources" ('
        '"record_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, '
        '"source" TEXT DEFAULT "");'
    ),
]


# open the test database
@pytest.fixture
def db_open(tmp_path):
    path = tmp_path / db_name
    dbref = Dbal()
    dbref.sql_connect(path)
    return dbref


# close database
def db_close(dbref):
    dbref.sql_close()


@pytest.fixture
def db_create(db_open):
    """create a new database file"""
    dbref = db_open
    for sql in sql_statements:
        dbref.sql_query(sql)
    return dbref


# ######################################################
# Test values for a Condition

# set condition values from array of values
condition_values = {
    "record_id": 15,
    "condition": "Replace",
}


def load_conditions_table(dbref):
    columns = ["record_id", "condition"]
    value_set = [
        [1, "Usable"],
        [2, "Replace"],
        [3, "Rebuild"],
        [4, "Missing"],
        [5, "New"],
        [6, "Unknown"],
    ]
    sql_query = {"type": "INSERT", "table": "conditions"}
    for values in value_set:
        entries = {}
        i = 0
        while i < len(columns):
            entries[columns[i]] = values[i]
            i += 1
        sql = dbref.sql_query_from_array(sql_query, entries)
        dbref.sql_query(sql, entries)


# ######################################################
# Test values for an Item

# Set single item value set and database item table
item_values = {
    "record_id": 9876,
    "part_number": "13215",
    "assembly": "P",
    "quantity": 4,
    "condition": "New",
    "installed": 1,
    "remarks": "test",
    "box": 5,
}


def load_items_table(dbref):
    columns = [
        "record_id",
        "part_number",
        "assembly",
        "quantity",
        "condition",
        "installed",
        "box",
        "remarks",
    ]
    value_set = [
        ["1", "18V672", "A", "1", "Rebuild", "1", "", ""],
        ["2", "BTB1108", "B", "1", "Usable", "0", "", ""],
        ["3", "X036", "D", "1", "Usable", "0", "", ""],
        ["4", "BTB1108", "CA", "1", "Usable", "0", "", ""],
        ["5", "22H1053", "BB", "1", "Usable", "0", "", ""],
        ["6", "268-090", "BC", "1", "Usable", "1", "", ""],
        ["8", "BTB1108", "BD", "1", "Usable", "1", "", ""],
        ["9", "X055", "EB", "1", "Usable", "1", "", ""],
        ["56", "BULB-1895", "JCIB", "2", "Replace", "1", "", "License Plate Lamp"],
        ["59", "158-520", "JCIA", "2", "Replace", "1", "", ""],
        ["70", "BTB1108", "CX", "1", "Usable", "1", "", ""],
    ]
    sql_query = {"type": "INSERT", "table": "items"}
    for values in value_set:
        entries = {}
        i = 0
        while i < len(columns):
            entries[columns[i]] = values[i]
            i += 1
        sql = dbref.sql_query_from_array(sql_query, entries)
        dbref.sql_query(sql, entries)


# ######################################################
# Test values for an Part

# set part values from array of values
part_values = dict(
    {
        "record_id": 9876,
        "part_number": "13215",
        "source": "Moss",
        "description": "bolt",
        "remarks": "From local source",
    }
)


def load_parts_table(dbref):
    columns = ["record_id", "part_number", "source", "description", "remarks"]
    value_set = [
        [
            "1786",
            "X081",
            "Local Purchase",
            "Rivet, Pop,1/8",
            "",
        ],
        ["1787", "X080", "None", "Fenders, Rear", ""],
        ["1788", "X079", "None", "O-Ring Gasket, 1/4 ID, 3/8 ID", ""],
        ["1789", "453-721", "Moss USA", "Dashboard", ""],
        ["1790", "15-112-BL", "Victoria British", "Radio Back Panel", ""],
        ["1791", "472-078", "Moss USA", "Radio Blanking Plate Set", ""],
        ["1792", "12-1124", "Victoria British", "Screw	Radio Console", ""],
        ["1793", "12-5304", "Victoria British", "Nut, Spire, Radio Console", ""],
        ["1794", "281-050", "Moss USA", "Grommet, 1 x 5/16	Choke Cable", ""],
        [
            "1795",
            "282-385",
            "Moss USA",
            "Grommet, 9/16x 3/16",
            "License Plate",
        ],
        ["1796", "324-655", "None", "Washer, Flat, 3/8 ID, 1 1/4 OD, 1/8 Thick", ""],
    ]
    sql_query = {"type": "INSERT", "table": "parts"}
    for values in value_set:
        entries = {}
        i = 0
        while i < len(columns):
            entries[columns[i]] = values[i]
            i += 1
        sql = dbref.sql_query_from_array(sql_query, entries)
        dbref.sql_query(sql, entries)


# ######################################################
# Test values for a Source

# set source values from array of values
source_values = dict(
    {
        "record_id": 15,
        "source": "Moss USA",
    }
)


def load_sources_table(dbref):
    columns = ["record_id", "source"]
    value_set = [
        [1, "Moss USA"],
        [2, "Victoria British"],
        [3, "B-Hive"],
        [4, "Moss Europe"],
        [5, "Roadster Factory"],
        [6, "McMaster-Carr"],
        [7, "None"],
        [8, "Fastenal"],
        [9, "British Parts Northwest"],
        [10, "Ebay"],
        [11, "Advanced Auto Wire"],
        [12, "Little British Car Co"],
        [13, "Strapping Lad Suspension"],
        [14, "Local Purchase"],
        [15, "Tire Rack"],
    ]
    sql_query = {"type": "INSERT", "table": "sources"}
    for values in value_set:
        entries = {}
        i = 0
        while i < len(columns):
            entries[columns[i]] = values[i]
            i += 1
        sql = dbref.sql_query_from_array(sql_query, entries)
        dbref.sql_query(sql, entries)
