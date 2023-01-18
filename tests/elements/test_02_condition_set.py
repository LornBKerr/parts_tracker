import pytest
import os

from common import Dbal
from parts_elements import ConditionSet

database = './parts_test.db'

def close_database(dbref):
    dbref.sql_close()

def delete_database():
    os.remove(database)

@pytest.fixture
def open_database():
    dbref = Dbal()
    # valid connection
    dbref.sql_connect(database)
    return dbref

@pytest.fixture
def create_conditions_table():
    dbref = Dbal()
    dbref.sql_connect('parts_test.db')
    dbref.sql_query("DROP TABLE IF EXISTS conditions")
    create_table = 'CREATE TABLE conditions (entry_index INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, condition TEXT DEFAULT "")'
    result = dbref.sql_query(create_table)
    return dbref

def load_conditions_table(dbref):
    columns = ['entry_index', 'condition']
    value_set = [[1, 'Usable'], [2, 'Replace'], [3, 'Rebuild'], [4, 'Missing'], [5, 'New'], [6, 'Unknown']]
    sql_query = {'type': 'INSERT', 'table': 'conditions'}
    for values in value_set:
        entries = {}
        i = 0
        while i < len(columns):
            entries[columns[i]] = values[i]
            i += 1
        dbref.sql_query_from_array(sql_query, entries)

def test_01_constr(open_database):
    dbref = open_database
    condition_set = ConditionSet(dbref)
    assert isinstance(condition_set, ConditionSet)
    close_database(dbref)
   
def test_02_get_dbref(open_database):
    dbref = open_database
    condition_set = ConditionSet(dbref)
    assert condition_set.get_dbref() == dbref
    close_database(dbref)

def test_03_get_table(open_database):
    dbref = open_database
    condition_set = ConditionSet(dbref)
    assert condition_set.get_table() == 'conditions'
    close_database(dbref)

def test_04_set_table(open_database):
    dbref = open_database
    condition_set = ConditionSet(dbref)
    condition_set.set_table('items')
    assert condition_set.get_table() == 'items'
    close_database(dbref)
    
def test_05_get_property_set(open_database):
    dbref = open_database
    condition_set = ConditionSet(dbref)
    assert isinstance(condition_set.get_property_set(), list)
    close_database(dbref)
    
def test_06_set_property_set_none(open_database):
    dbref = open_database
    condition_set = ConditionSet(dbref)
    assert isinstance(condition_set.get_property_set(), list)
    condition_set.set_property_set(None)
    assert isinstance(condition_set.get_property_set(), list)
    assert len(condition_set.get_property_set()) == 0
    close_database(dbref)
    
def test_07_all_rows_empty(create_conditions_table):
    dbref = create_conditions_table
    conditions_set = ConditionSet(dbref)
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + conditions_set.get_table())
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(conditions_set.get_property_set())
    assert count == conditions_set.get_number_elements()
    close_database(dbref)

def test_08_selected_rows(create_conditions_table):
    dbref = create_conditions_table
    load_conditions_table(dbref)
    conditions_set = ConditionSet(dbref,'condition', 'Missing')
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + conditions_set.get_table() + " WHERE condition = 'Missing'")
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(conditions_set.get_property_set())
    assert count == 1
    close_database(dbref)

def test_09_cleanup(open_database):
    dbref = open_database
    result = dbref.sql_query("DROP TABLE IF EXISTS 'parts'")
    assert result
    close_database(dbref)
    delete_database()

# end test_10_OrderSet
