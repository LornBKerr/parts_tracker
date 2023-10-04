"""
Provide common values and functionality for the PartsTracker testing.

File:       test_setup_elements.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT, see file License

This module provides a number of values and functions to help setup the
test environment for the parts tracker program. All test modules draw on
a varying selection of these values.

Values Available:
    test_string - A string for testing whereever a string is needed.
    long_string - A string exceeding the base 255 character upper limit.

    condition_columns, condition_value_set: columns andv values for the
        'condition' db table.
    item_columns, item_value_set: columns and values for the 
        'item' table.
    order_columns, order_value_set: columns and values for the
        'order' table.
    order_line_columns, order_line_value_set: columns and values for the
        'order_line' table.
    part_columns, part_value_set: columns and values for the 'part' table.
    source_columns, source_value_set: : columns and values for the
        'source' table.

Database Handling:
    db_open(tmp_path): Pytest fixture to open a database in temporary 
        storage returning a reference to the database.
    db_create(db_open): Pytest fixture to create a new database returning
        a reference to the new database.

    db_close(dbref: Dbal): function to close the open database
    load_db_table(dbref, table_name, column_names, value_set): Funcion
        to load a specific database table.
    load_all_db_tables(dbref)  : Function to load all db tables  

Filesystem, Directories and associated files:
    build_test_config(base_dir): fill a cofig file
    directories (list): List of directories for the filesystem
    filesystem(tmp_path): Pytest fixture to generate a temporary
        filesystem. 
    test_config (dict): an empty configuration setup
"""

import os
from copy import deepcopy

import pytest
from lbk_library import Dbal
from PyQt5 import QtWidgets

# some test strings
test_string = "This is a string"

long_string = ""
while len(long_string) < 255:
    long_string = long_string + ", " + test_string

# open the test database
# Set up and access the database
__db_name = "parts_test.db"


@pytest.fixture
def db_open(tmp_path):
    """
    Open a detabase.

    Parameters:
        tmp_path (pathlib.Path): pytest fixture to create a temporary pth

    Returns:
        (Dbal) reference to an open, empty database.
    """
    path = tmp_path / __db_name
    dbref = Dbal()
    dbref.sql_connect(path)
    return dbref


# close database
def db_close(dbref):
    """
    Close an open database.

    Parameters:
        dbref (Dbal): The open database to be closed.
    """
    dbref.sql_close()


# Create a new Database
# Sql statements to create a test database reflecting the parts database.
__sql_statements = [
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


@pytest.fixture
def db_create(db_open):
    dbref = db_open
    for sql in __sql_statements:
        dbref.sql_query(sql)
    return dbref


def load_db_table(dbref, table_name, column_names, value_set):
    """Load one of the database tables with a set of values."""
    sql_query = {"type": "INSERT", "table": table_name}
    for values in value_set:
        entries = {}
        i = 0
        while i < len(column_names):
            entries[column_names[i]] = values[i]
            i += 1
        sql = dbref.sql_query_from_array(sql_query, entries)
        dbref.sql_query(sql, entries)


def load_all_db_tables(dbref):
    load_db_table(dbref, "conditions", condition_columns, condition_value_set)
    load_db_table(dbref, "items", item_columns, item_value_set)
    load_db_table(dbref, "parts", part_columns, part_value_set)
    load_db_table(dbref, "orders", order_columns, order_value_set)
    load_db_table(dbref, "order_lines", order_line_columns, order_line_value_set)
    load_db_table(dbref, "sources", source_columns, source_value_set)


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
        "assy_list_dir": "",
    }
}


# fill the config directory locations
def build_test_config(base_dir):
    config = deepcopy(test_config)
    config["settings"]["db_file_dir"] = os.path.join(base_dir, directories[2])
    config["settings"]["assy_list_dir"] = os.path.join(
        base_dir, directories[2], "parts_listings"
    )
    return config


@pytest.fixture
def filesystem(tmp_path):
    """
    Setup a temporary filesystem which will be discarded after the test
    sequence is run.

    'source' is the directory structure for saving and retrieving data
    with two directories: '.config' and 'Documents'. This directory
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
    ["731", "17005", "CAABA", "4", "New", "1", "0", ""],
    ["1", "18V672", "A", "1", "Rebuild", "1", "", ""],
    ["2", "Z005", "B", "1", "Usable", "0", "", ""],
    ["3", "Z006", "C", "1", "Usable", "0", "", ""],
    ["4", "Z007", "CA", "1", "Usable", "0", "", ""],
    ["5", "22H1053", "BB", "1", "Usable", "0", "", ""],
    ["6", "268-090", "BC", "1", "Usable", "1", "", ""],
    ["8", "BTB1108", "BD", "1", "Usable", "1", "", ""],
    ["1370", "17005", "ABFCB", "3", "New", "1", "0", ""],
    ["168", "Z001", "AA", "1", "Usable", "1", "0", ""],
    ["172", "12H1387", "AAA", "1", "Usable", "1", "0", ""],
    ["1320", "296-000", "AAAA", "1", "New", "1", "0", ""],
    ["1317", "455-390", "AAAB", "1", "Usable", "1", "0", ""],
    ["1318", "120-000", "AAABA", "1", "New", "1", "0", ""],
    ["1319", "296-340", "AAABB", "1", "New", "1", "0", ""],
    ["1322", "17000", "AAABC", "3", "New", "1", "0", ""],
    ["1323", "17003", "AAABD", "2", "New", "1", "0", ""],
    ["1325", "33078", "AAABE", "5", "New", "1", "0", ""],
    ["1326", "33618", "AAABF", "5", "New", "1", "0", ""],
    ["1324", "17053", "AAAC", "7", "New", "1", "0", ""],
    ["1327", "33080", "AAACA", "7", "New", "1", "0", ""],
    ["1328", "33620", "AAACB", "7", "New", "1", "0", ""],
    ["173", "460-701", "AAB", "1", "Usable", "1", "0", ""],
    ["181", "120-820", "AABA", "1", "New", "1", "0", "Moss part number 120-820"],
    ["182", "120-830", "AABAA", "1", "New", "1", "0", ""],
    ["183", "17052", "AABAB", "4", "New", "1", "0", ""],
    ["184", "17105", "AABB", "2", "New", "1", "0", "top two bolts on rear plate"],
    ["185", "33622", "AABBA", "2", "New", "1", "0", ""],
    ["186", "17105", "AABC", "8", "New", "1", "0", ""],
    ["187", "33622", "AABCA", "8", "New", "1", "0", ""],
    ["193", "297-495", "AABD", "1", "New", "1", "0", ""],
]


# Test values for an Order

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
    [13, "06-013", "2006-08-22", "British car parts", "", 0.0, 0.0, 0.0, 0.0, 0.0],
    [14, "06-015", "2006-12-04", "Ebay", "", 0.0, 0.0, 0.0, 0.0, 0.0],
    [
        15,
        "06-016",
        "2006-05-05",
        "Local Purchase",
        "",
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
        "",
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
        "",
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
        "",
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ],
    [19, "07-004", "2007-12-19", "", "", 0.0, 0.0, 0.0, 0.0, 0.0],
    [41, "09-012", "2009-08-17", "Screw Shop", "", 0.0, 0.0, 0.0, 0.0, 0.0],
]

# Test values for an OrderLine

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
    [159, "09-012", 1, "17000", 0.138, 37, ""],
]

# Test values for an Part

part_columns = ["record_id", "part_number", "source", "description", "remarks"]
part_value_set = [
    [64, "17000", "Screw Shop", "Bolt, Hex Cap, 1/4-28 X 3/8, Grade 5, Zinc", ""],
    [67, "17003", "Screw Shop", "Bolt, Hex Cap, 1/4-28 x 0.75, Grade 5 Zinc", ""],
    [
        69,
        "17005",
        "Screw Shop",
        "Bolt, Hex Cap, 1/4-28 x 1, Grade 5, Zinc",
        "Moss P/N 324-247",
    ],
    [73, "17052", "Screw Shop", "Bolt, Hex Cap, 5/16-24 x 0.625, Grade 5, Zinc", ""],
    [74, "17053", "Screw Shop", "Bolt, Hex Cap, 5/16-24 x 0.75, Grade 5, Zinc", ""],
    [84, "17105", "Screw Shop", "Bolt, Hex Cap, 3/8-24 x 1.0, Grade 5, Zinc", ""],
    [95, "33078", "Screw Shop", "Washer, Flat, 1/4, Zinc", ""],
    [96, "33080", "Screw Shop", "Washer, Flat, 5/16, Zinc", "Moss P/N 365-720"],
    [100, "33618", "Screw Shop", "Washer, Lock, Split, 1/4, Zinc", "Moss P/N 324-020"],
    [101, "33620", "Screw Shop", "Washer, Lock, Split, 5/16, Zinc", "Moss P/N 365-730"],
    [102, "33622", "Screw Shop", "Washer, Lock, Split, 3/8, Zinc", "Moss P/N 324-040"],
    [427, "267-995", "British car parts", "Shock, LHS, Rebuilt", ""],
    [1946, "18V672", "None", "Engine, 18V, 1971-1974", ""],
    [1947, "Z001", "None", "Block, Engine", ""],
    [1920, "12H1387", "", "Plate, Engine, Front", ""],
    [1921, "460-701", "British car parts", "Back Plate", ""],
    [149, "120-820", "British car parts", "Oil Seal, Rear Main", ""],
    [150, "120-830", "British car parts", "Retainer, Oil Seal", ""],
    [
        "477",
        "296-000",
        "British car parts",
        "Gasket, Front Plate to Block",
        "Part of Moss P/N 297-521, Conversion Gasket Set",
    ],
    [826, "455-390", "British car parts", "Cover, Timing", ""],
    [1680, "120-000", "British car parts", "Oil Seal, Crankshaft, Front", ""],
    [
        481,
        "296-340",
        "British car parts",
        "Gasket, Timing Cover",
        "Part of Moss P/N 297-521, Conversion Gasket Set",
    ],
    [
        517,
        "320-125",
        "British car parts",
        "Bolt, Hex Cap, 3/8-24 x 1.000, Grade 5",
        "Replaced by Fastenal P/N 17105",
    ],
    [491, "297-495", "British car parts", "Cover, Gearbox Mount Plate", ""],
    [1951, "Z005", "None", "Drive Train", ""],
    [1955, "Z006", "None", "Cooling and Heating System", ""],
    [1952, "22H1053", "None", "Gearbox", ""],
    [432, "268-090", "British car parts", "Drive Shaft", ""],
    [1954, "BTB1108", "None", "Rear Axle", ""],
]

# Test values for a Source

source_columns = ["record_id", "source"]
source_value_set = [
    [1, "British Car Parts"],
    [2, "None"],
    [3, "Local Purchase"],
    [4, "Tire Store"],
    [5, "Screw Shop"],
    [6, "Ebay"],
]

# ######################################################


class dialog_form(object):
    # define a simple form with various qt objects available for testing.
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
