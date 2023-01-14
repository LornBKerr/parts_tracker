import pytest
import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library import Dbal, ElementSet
from elements import Item, ItemSet

database = 'parts_test.db'

def close_database(dbref):
    dbref.sql_close()

@pytest.fixture
def create_items_table(tmpdir):
    path = tmpdir.join(database)
    dbref = Dbal()
    dbref.sql_connect(path)
    dbref.sql_query("DROP TABLE IF EXISTS 'items'")
    create_table = 'CREATE TABLE IF NOT EXISTS "items"' + \
                          '("record_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,' + \
                          ' "part_number" TEXT NOT NULL,' + \
                          ' "assembly" TEXT NOT NULL,' + \
                          ' "quantity" INTEGER NOT NULL,' + \
                          ' "condition" TEXT NOT NULL,' + \
                          ' "installed" INTEGER NOT NULL DEFAULT 0,' + \
                          ' "box" INTEGER DEFAULT NULL,' + \
                          ' "remarks" TEXT DEFAULT NULL)'
    dbref.sql_query(create_table)
    return dbref

def load_items_table(dbref):
    columns = ['record_id', 'part_number', 'assembly', 'quantity', 'condition', 'installed', 'box', 'remarks']
    value_set = [[ '1', '18V672', 'A', '1', 'Rebuild', '1', '', ''],
                 ['2', 'BTB1108', 'B', '1', 'Usable', '0', '', ''],
                 ['3', 'X036', 'D', '1', 'Usable', '0', '', ''],
                 ['4', 'BTB1108', 'CA', '1', 'Usable', '0', '', ''],
                 ['5', '22H1053', 'BB', '1', 'Usable', '0', '', ''],
                 ['6', '268-090', 'BC', '1', 'Usable', '1', '', ''],
                 ['8', 'BTB1108', 'BD', '1', 'Usable', '1', '', ''],
                 ['9', 'X055', 'EB', '1', 'Usable', '1', '', ''],
                 ['56', 'BULB-1895', 'JCIB', '2', 'Replace', '1', '', 'License Plate Lamp'],
                 ['59', '158-520', 'JCIA', '2', 'Replace', '1', '', ''],
                 ['70', 'BTB1108', 'CX', '1', 'Usable', '1', '', ''],
                ]
    sql_query = {'type': 'INSERT', 'table': 'items'}
    for values in value_set:
        entries = {}
        i = 0
        while i < len(columns):
            entries[columns[i]] = values[i]
            i += 1
        sql = dbref.sql_query_from_array(sql_query, entries)
        dbref.sql_query(sql, entries)


def test_02_01_constructor(create_items_table):
    dbref = create_items_table
    item_set = ItemSet(dbref)
    assert isinstance(item_set, ItemSet)
    assert isinstance(item_set, ElementSet)
    close_database(dbref)
    
def test_02_02_get_dbref(create_items_table):
    dbref = create_items_table
    item_set = ItemSet(dbref)
    assert item_set.get_dbref() == dbref
    close_database(dbref)

def test_02_03_get_table(create_items_table):
    dbref = create_items_table
    item_set = ItemSet(dbref)
    assert item_set.get_table() == 'items'
    close_database(dbref)

def test_02_04_set_table(create_items_table):
    dbref = create_items_table
    item_set = ItemSet(dbref)
    item_set.set_table('parts')
    assert item_set.get_table() == 'parts'
    close_database(dbref)
    
def test_02_05_get_property_set(create_items_table):
    dbref = create_items_table
    item_set = ItemSet(dbref)
    assert isinstance(item_set.get_property_set(), list)
    close_database(dbref)
    
def test_02_06_set_property_set_none(create_items_table):
    dbref = create_items_table
    item_set = ItemSet(dbref)
    assert isinstance(item_set.get_property_set(), list)
    item_set.set_property_set(None)
    assert isinstance(item_set.get_property_set(), list)
    assert len(item_set.get_property_set()) == 0
    close_database(dbref)

def test_02_07_all_rows_empty(create_items_table):
    dbref = create_items_table
    item_set = ItemSet(dbref)
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + item_set.get_table())
    count = dbref.sql_fetchrow(count_result)['COUNT(*)']
    assert count == len(item_set.get_property_set())
    assert count == item_set.get_number_elements()
    close_database(dbref)

def test_02_08_selected_rows(create_items_table):
    dbref = create_items_table
    load_items_table(dbref)
    item_set = ItemSet(dbref, 'part_number', 'BTB1108')
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + item_set.get_table() + " WHERE part_number = 'BTB1108'")
    count = dbref.sql_fetchrow(count_result)['COUNT(*)']
    assert count == len(item_set.get_property_set())
    close_database(dbref)

def test_02_09_ordered_selected_rows(create_items_table):
    dbref = create_items_table
    load_items_table(dbref)
    item_set = ItemSet(dbref,'part_number', 'BTB1108', 'assembly')
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + item_set.get_table() + " WHERE part_number = 'BTB1108'")
    count = dbref.sql_fetchrow(count_result)['COUNT(*)']
    selected_set = item_set.get_property_set()
    assert count == len(selected_set)
    for counter in range(0, count - 2):
        item1 = selected_set[counter]
        item2 = selected_set[counter + 1]
        assert item1.get_assembly() < item2.get_assembly()
    close_database(dbref)

def test_02_10_selected_rows_limit(create_items_table):
    dbref = create_items_table
    load_items_table(dbref)
    limit = 5
    item_set = ItemSet(dbref, None, None, 'record_id', limit)
    assert limit == len(item_set.get_property_set())
    assert item_set.get_property_set()[0].get_record_id() == 1
    close_database(dbref)

def test_02_11_selected_rows_limit_offset(create_items_table):
    dbref = create_items_table
    load_items_table(dbref)
    limit = 5
    offset = 2
    item_set = ItemSet(dbref, None, None, 'record_id', limit, offset)
    assert limit == len(item_set.get_property_set())
    assert item_set.get_property_set()[0].get_record_id() == 3
    close_database(dbref)

def test_02_12_iterator(create_items_table):
    dbref = create_items_table
    load_items_table(dbref)
    limit = 5
    item_set = ItemSet(dbref, None, None, 'record_id', limit)
    i = 1
    for item in item_set:
        assert item.get_record_id() == i
        i += 1
    close_database(dbref)

# end test_02_elements_item_set.py
