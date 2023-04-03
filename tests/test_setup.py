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
from PyQt6 import QtWidgets

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
    dbref = db_open
    for sql in sql_statements:
        dbref.sql_query(sql)
    return dbref


# Directories for Windows and Linux
directories = [
    ".config",
    "Documents",
    "Documents/parts_tracker",
]

# a basic empty config file for part_tracker testing.
test_config = {
    "settings": {
        "recent_files": [],
        "db_file_dir": "",
        "xls_file_loc": "",
    }
}


def load_db_table(dbref, table_name, column_names, value_set):
    """Load one of the database tables with a set of values."""
    sql_query = {"type": "INSERT", "table": "items"}
    for values in value_set:
        entries = {}
        i = 0
        while i < len(columns):
            entries[columns[i]] = values[i]
            i += 1
        sql = dbref.sql_query_from_array(sql_query, entries)
        dbref.sql_query(sql, entries)


@pytest.fixture
def filesystem(tmp_path):
    """
    Setup a temporary filesystem which will be discarded after the test
    sequence is run.

    'source' is the directory structure for saving and retrieving data
    with tow directories: '.config' and 'Documents'. This directory
    structure will be discarded after the test sequence is run.

    Parameters:
        tmp_path: pytest fixture to setup a path to a temperary location

    Returns:
        ( pathlib.Path ) The temparary file paths to use.
    """
    source = tmp_path / "source"
    source.mkdir()

    # make a set of source directories and files
    for dir in directories:
        a_dir = source / dir
        a_dir.mkdir()

    fp = open(source / "Documents/parts_tracker/test_file1.db", "w")
    fp.close()
    fp = open(source / "Documents/parts_tracker/test_file2.db", "w")
    fp.close()

    return source


# ######################################################
# Test values for a Condition

# set condition values from array of values
condition_values = {
    "record_id": 15,
    "condition": "Replace",
}

condition_columns = ["record_id", "condition"]
condition_value_set = [
    [1, "Usable"],
    [2, "Replace"],
    [3, "Rebuild"],
    [4, "Missing"],
    [5, "New"],
    [6, "Unknown"],
]

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

item_columns = [
    "record_id",
    "part_number",
    "assembly",
    "quantity",
    "condition",
    "installed",
    "box",
    "remarks",
]
item_value_set = [
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
    ["731", "17005", "CAABA", "4", "New", "1", "0", ""],
    ["1370", "17005", "ABFCB", "3", "New", "1", "0", ""],
]

# Test values for an Order

order_values = {
    "record_id": 9876,
    "order_number": "09-001",
    "date": "10/02/2009",
    "source": "Moss",
    "subtotal": 25.25,
    "shipping": 2.95,
    "discount": -1.02,
    "tax": 1.77,
    "total": 28.95,
    "remarks": "From local source",
}

order_columns = [
    "record_id",
    "order_number",
    "date",
    "source",
    "remarks",
    "subtotal",
    "shipping",
    "tax",
    "discount",
    "total",
]
order_value_set = [
    [13, "06-013", "2006-08-22", "B-Hive", "", 0.0, 0.0, 0.0, 0.0, 0.0],
    [14, "06-015", "2006-12-04", "Ebay", "", 0.0, 0.0, 0.0, 0.0, 0.0],
    [
        15,
        "06-016",
        "2006-05-05",
        "Local Purchase",
        "Napa Auto Parts",
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ],
    [
        16,
        "07-001",
        "2007-07-02",
        "Local Purchase",
        "From David Deutsch, MG Experience member",
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ],
    [
        17,
        "07-002",
        "2007-09-28",
        "Local Purchase",
        "From Steve Adamski, MG Experience member",
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ],
    [
        18,
        "07-003",
        "2007-12-06",
        "Local Purchase",
        "Professional Crygenic Metallurgy and Coatings",
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ],
    [19, "07-004", "2007-12-19", "Advanced Auto Wire", "", 0.0, 0.0, 0.0, 0.0, 0.0],
    [41, "09-012", "2009-08-17", "Fastenal", "", 0.0, 0.0, 0.0, 0.0, 0.0],
]

# Test values for an OrderLine

order_line_values = {
    "record_id": 10,
    "order_number": "09-001",
    "line": 3,
    "part_number": "13571",
    "cost_each": 10.01,
    "quantity": 3,
    "remarks": "remarks",
}

order_line_columns = [
    "record_id",
    "order_number",
    "line",
    "part_number",
    "cost_each",
    "quantity",
    "remarks",
]
order_line_value_set = [
    [27, "06-015", 1, "373-830", 23.5, 1, ""],
    [28, "06-015", 2, "Z0033", 91.0, 1, "P/N Replaced by ZE005"],
    [
        29,
        "07-001",
        1,
        "267-995",
        13.0,
        1,
        "Used as core for new shocks from NOSIMPORTS",
    ],
    [
        30,
        "07-001",
        2,
        "267-985",
        13.0,
        1,
        "Used as core for new shocks from NOSIMPORTS",
    ],
    [31, "07-002", 1, "458-885", 187.5, 1, "includes shipping"],
    [32, "07-002", 2, "458-875", 187.5, 1, "includes shipping"],
    [33, "07-003", 1, "X5005", 800.0, 1, ""],
    [163, "09-012", 5, "17005", 0.141, 11, ""],
]

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

part_columns = ["record_id", "part_number", "source", "description", "remarks"]

part_value_set = [
    [
        69,
        "17005",
        "Fastenal",
        "Bolt, Hex Cap, 1/4-28 x 1.000, Grade 5, Zinc",
        "Moss P/N 324-247",
    ],
    [
        1786,
        "X081",
        "Local Purchase",
        "Rivet, Pop,1/8",
        "",
    ],
    [1787, "X080", "None", "Fenders, Rear", ""],
    [1788, "X079", "None", "O-Ring Gasket, 1/4 ID, 3/8 ID", ""],
    [1789, "453-721", "Moss USA", "Dashboard", ""],
    [1790, "15-112-BL", "Victoria British", "Radio Back Panel", ""],
    [1791, "472-078", "Moss USA", "Radio Blanking Plate Set", ""],
    [1792, "12-1124", "Victoria British", "Screw	Radio Console", ""],
    [1793, "12-5304", "Victoria British", "Nut, Spire, Radio Console", ""],
    [1794, "281-050", "Moss USA", "Grommet, 1 x 5/16	Choke Cable", ""],
    [
        1795,
        "282-385",
        "Moss USA",
        "Grommet, 9/16x 3/16",
        "License Plate",
    ],
    [1796, "324-655", "None", "Washer, Flat, 3/8 ID, 1 1/4 OD, 1/8 Thick", ""],
]

# Test values for a Source

# set source values from array of values
source_values = dict(
    {
        "record_id": 15,
        "source": "Moss USA",
    }
)


source_columns = ["record_id", "source"]
source_value_set = [
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


# ######################################################

# Load a database table


def load_db_table(dbref, table, columns, value_set):
    sql_query = {"type": "INSERT", "table": table}
    for values in value_set:
        entries = {}
        i = 0
        while i < len(columns):
            entries[columns[i]] = values[i]
            i += 1
        sql = dbref.sql_query_from_array(sql_query, entries)
        dbref.sql_query(sql, entries)


# ######################################################
# define a simple form with various qt objects available for testing.


class dialog_form(object):
    def __init__(self, dialog_form):
        self.setupUi(dialog_form)

    def setupUi(self, dialog_form):
        """Initialize comment."""
        dialog_form.setObjectName("dialog_form")
        dialog_form.resize(910, 580)
        self.record_id_label = QtWidgets.QLabel(parent=dialog_form)
        self.record_id_combo = QtWidgets.QComboBox(parent=dialog_form)
        self.remarks_label = QtWidgets.QLabel(parent=dialog_form)
        self.remarks_edit = QtWidgets.QLineEdit(parent=dialog_form)
        self.save_new_button = QtWidgets.QPushButton(parent=dialog_form)
        self.save_done_button = QtWidgets.QPushButton(parent=dialog_form)
        self.part_number_combo = QtWidgets.QComboBox(parent=dialog_form)
        self.order_table = QtWidgets.QTableWidget(parent=dialog_form)
