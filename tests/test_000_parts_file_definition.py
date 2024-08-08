"""
Test the parts file definition.

File:       test_000_data_file_definitiion.py
Author:     Lorn B Kerr
Copyright:  (c) 2024 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

from lbk_library.testing_support import datafile_close, datafile_create, filesystem

# from test_setup import

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from pages import table_definition


def test_000_01_table_set(filesystem):
    """Create an empty parts file and verify the required set of tables."""
    base_directory = filesystem
    filepath = base_directory + "/testfile.parts"
    datafile = datafile_create(filepath, table_definition)
    table_names = ["conditions", "items", "order_lines", "orders", "parts", "sources"]

    sql_query = "SELECT name FROM sqlite_master WHERE type='table' and name != 'sqlite_sequence';"
    sqlite_cursor = datafile.sql_query(sql_query)
    tables = datafile.sql_fetchrowset(sqlite_cursor)
    assert len(tables) == len(table_names)
    for table_entry in tables:
        assert table_entry["name"] in table_names
    datafile_close(datafile)


def test_000_02_conditions_table(filesystem):
    """Create an empty parts file and verify the required set of tables."""
    base_directory = filesystem
    filepath = base_directory + "/testfile.db"
    datafile = datafile_create(filepath, table_definition)

    condition_column_set = [
        {"name": "record_id", "type": "INTEGER"},
        {"name": "condition", "type": "TEXT"},
    ]
    sql_query = "SELECT * FROM pragma_table_info('conditions')"
    sqlite_cursor = datafile.sql_query(sql_query)
    columns = datafile.sql_fetchrowset(sqlite_cursor)
    for column_info in columns:
        if column_info["name"] == condition_column_set[0]["name"]:
            assert column_info["type"] == "INTEGER"
        elif column_info["name"] == condition_column_set[1]["name"]:
            assert column_info["type"] == "TEXT"
        else:
            print(column_info["name"] + " not in defined column names.")
            assert False
    datafile_close(datafile)


def test_000_03_items_table(filesystem):
    """Create an empty parts file and verify the required set of tables."""
    base_directory = filesystem
    filepath = base_directory + "/testfile.db"
    datafile = datafile_create(filepath, table_definition)

    items_column_set = [
        {"name": "record_id", "type": "INTEGER"},
        {"name": "part_number", "type": "TEXT"},
        {"name": "assembly", "type": "TEXT"},
        {"name": "quantity", "type": "INTEGER"},
        {"name": "condition", "type": "INTEGER"},
        {"name": "installed", "type": "INTEGER"},
        {"name": "box", "type": "INTEGER"},
        {"name": "remarks", "type": "TEXT"},
    ]
    sql_query = "SELECT * FROM pragma_table_info('items')"
    sqlite_cursor = datafile.sql_query(sql_query)
    columns = datafile.sql_fetchrowset(sqlite_cursor)
    for column_info in columns:
        if (
            column_info["name"] == items_column_set[0]["name"]
            or column_info["name"] == items_column_set[3]["name"]
            or column_info["name"] == items_column_set[4]["name"]
            or column_info["name"] == items_column_set[5]["name"]
            or column_info["name"] == items_column_set[6]["name"]
        ):
            assert column_info["type"] == "INTEGER"
        elif (
            column_info["name"] == items_column_set[1]["name"]
            or column_info["name"] == items_column_set[2]["name"]
            or column_info["name"] == items_column_set[7]["name"]
        ):
            assert column_info["type"] == "TEXT"
        else:
            print(column_info["name"] + " not in defined column names.")
            assert False
    datafile_close(datafile)


def test_000_04_orderlines_table(filesystem):
    """Create an empty parts file and verify the required set of tables."""
    base_directory = filesystem
    filepath = base_directory + "/testfile.db"
    datafile = datafile_create(filepath, table_definition)

    orderlines_column_set = [
        {"name": "record_id", "type": "INTEGER"},
        {"name": "order_number", "type": "TEXT"},
        {"name": "line", "type": "INTEGER"},
        {"name": "part_number", "type": "TEXT"},
        {"name": "cost_each", "type": "FLOAT"},
        {"name": "quantity", "type": "INTEGER"},
        {"name": "remarks", "type": "TEXT"},
    ]
    sql_query = "SELECT * FROM pragma_table_info('order_lines')"
    sqlite_cursor = datafile.sql_query(sql_query)
    columns = datafile.sql_fetchrowset(sqlite_cursor)
    for column_info in columns:
        if (
            column_info["name"] == orderlines_column_set[0]["name"]
            or column_info["name"] == orderlines_column_set[2]["name"]
            or column_info["name"] == orderlines_column_set[5]["name"]
        ):
            assert column_info["type"] == "INTEGER"
        elif (
            column_info["name"] == orderlines_column_set[1]["name"]
            or column_info["name"] == orderlines_column_set[3]["name"]
            or column_info["name"] == orderlines_column_set[6]["name"]
        ):
            assert column_info["type"] == "TEXT"
        elif column_info["name"] == orderlines_column_set[4]["name"]:
            assert column_info["type"] == "FLOAT"
        else:
            print(column_info["name"] + " not in defined column names.")
            assert False
    datafile_close(datafile)


def test_000_05_orders_table(filesystem):
    """Create an empty parts file and verify the required set of tables."""
    base_directory = filesystem
    filepath = base_directory + "/testfile.db"
    datafile = datafile_create(filepath, table_definition)

    orders_column_set = [
        {"name": "record_id", "type": "INTEGER"},
        {"name": "order_number", "type": "TEXT"},
        {"name": "date", "type": "TEXT"},
        {"name": "source", "type": "INTEGER"},
        {"name": "subtotal", "type": "FLOAT"},
        {"name": "shipping", "type": "FLOAT"},
        {"name": "tax", "type": "FLOAT"},
        {"name": "discount", "type": "FLOAT"},
        {"name": "total", "type": "FLOAT"},
        {"name": "remarks", "type": "TEXT"},
    ]
    sql_query = "SELECT * FROM pragma_table_info('orders')"
    sqlite_cursor = datafile.sql_query(sql_query)
    columns = datafile.sql_fetchrowset(sqlite_cursor)
    for column_info in columns:
        if  (
            column_info["name"] == orders_column_set[0]["name"]
            or column_info["name"] == orders_column_set[3]["name"]
        ):
            assert column_info["type"] == "INTEGER"
        elif (
            column_info["name"] == orders_column_set[1]["name"]
            or column_info["name"] == orders_column_set[2]["name"]
            or column_info["name"] == orders_column_set[9]["name"]
        ):
            assert column_info["type"] == "TEXT"
        elif (
            column_info["name"] == orders_column_set[4]["name"]
            or column_info["name"] == orders_column_set[5]["name"]
            or column_info["name"] == orders_column_set[6]["name"]
            or column_info["name"] == orders_column_set[7]["name"]
            or column_info["name"] == orders_column_set[8]["name"]
        ):
            assert column_info["type"] == "FLOAT"
        else:
            print(column_info["name"] + " not in defined column names.")
            assert False
    datafile_close(datafile)


def test_000_06_parts_table(filesystem):
    """Create an empty parts file and verify the required set of tables."""
    base_directory = filesystem
    filepath = base_directory + "/testfile.db"
    datafile = datafile_create(filepath, table_definition)

    parts_column_set = [
        {"name": "record_id", "type": "INTEGER"},
        {"name": "part_number", "type": "TEXT"},
        {"name": "source", "type": "INTEGER"},
        {"name": "description", "type": "TEXT"},
        {"name": "remarks", "type": "TEXT"},
    ]
    sql_query = "SELECT * FROM pragma_table_info('parts')"
    sqlite_cursor = datafile.sql_query(sql_query)
    columns = datafile.sql_fetchrowset(sqlite_cursor)
    for column_info in columns:
        if (
            column_info["name"] == parts_column_set[0]["name"]
            or column_info["name"] == parts_column_set[2]["name"]
        ):
            assert column_info["type"] == "INTEGER"
        elif (
            column_info["name"] == parts_column_set[1]["name"]
            or column_info["name"] == parts_column_set[3]["name"]
            or column_info["name"] == parts_column_set[4]["name"]
        ):
            assert column_info["type"] == "TEXT"
        else:
            print(column_info["name"] + " not in defined column names.")
            assert False
    datafile_close(datafile)


def test_000_07_sources_table(filesystem):
    """Create an empty parts file and verify the required set of tables."""
    base_directory = filesystem
    filepath = base_directory + "/testfile.db"
    datafile = datafile_create(filepath, table_definition)

    sources_column_set = [
        {"name": "record_id", "type": "INTEGER"},
        {"name": "source", "type": "TEXT"},
    ]
    sql_query = "SELECT * FROM pragma_table_info('sources')"
    sqlite_cursor = datafile.sql_query(sql_query)
    columns = datafile.sql_fetchrowset(sqlite_cursor)
    for column_info in columns:
        if column_info["name"] == sources_column_set[0]["name"]:
            assert column_info["type"] == "INTEGER"
        elif column_info["name"] == sources_column_set[1]["name"]:
            assert column_info["type"] == "TEXT"
        else:
            print(column_info["name"] + " not in defined column names.")
            assert False
    datafile_close(datafile)
