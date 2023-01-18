import pytest
import os

from common import Dbal
from parts_elements import SourceSet

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
def create_sources_table():
    dbref = Dbal()
    dbref.sql_connect('parts_test.db')
    dbref.sql_query("DROP TABLE IF EXISTS sources")
    create_table = 'CREATE TABLE sources (entry_index INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, source TEXT DEFAULT "")'
    result = dbref.sql_query(create_table)
    return dbref

def load_sources_table(dbref):
    columns = ['entry_index', 'source']
    value_set = [[1, 'Moss USA'], [2, 'Victoria British'], [3, 'B-Hive'], [4, 'Moss Europe'], [5, 'Roadster Factory'],
                 [6, 'McMaster-Carr'], [7, 'None'], [8, 'Fastenal'], [9, 'British Parts Northwest'], [10, 'Ebay'],
                 [11, 'Advanced Auto Wire'], [1, 'Little British Car Co'], [13, 'Strapping Lad Suspension'],
                 [14, 'Local Purchase'], [15, 'Tire Rack']]
    sql_query = {'type': 'INSERT', 'table': 'sources'}
    for values in value_set:
        entries = {}
        i = 0
        while i < len(columns):
            entries[columns[i]] = values[i]
            i += 1
        dbref.sql_query_from_array(sql_query, entries)

def test_01_constr(open_database):
    dbref = open_database
    source_set = SourceSet(dbref)
    assert isinstance(source_set, SourceSet)
    close_database(dbref)
   
def test_02_get_dbref(open_database):
    dbref = open_database
    source_set = SourceSet(dbref)
    assert source_set.get_dbref() == dbref
    close_database(dbref)

def test_03_get_table(open_database):
    dbref = open_database
    source_set = SourceSet(dbref)
    assert source_set.get_table() == 'sources'
    close_database(dbref)

def test_04_set_table(open_database):
    dbref = open_database
    source_set = SourceSet(dbref)
    source_set.set_table('items')
    assert source_set.get_table() == 'items'
    close_database(dbref)
    
def test_05_get_property_set(open_database):
    dbref = open_database
    source_set = SourceSet(dbref)
    assert isinstance(source_set.get_property_set(), list)
    close_database(dbref)
    
def test_06_set_property_set_none(open_database):
    dbref = open_database
    source_set = SourceSet(dbref)
    assert isinstance(source_set.get_property_set(), list)
    source_set.set_property_set(None)
    assert isinstance(source_set.get_property_set(), list)
    assert len(source_set.get_property_set()) == 0
    close_database(dbref)
    
def test_07_all_rows_empty(create_sources_table):
    dbref = create_sources_table
    source_set = SourceSet(dbref)
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + source_set.get_table())
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(source_set.get_property_set())
    assert count == source_set.get_number_elements()
    close_database(dbref)

def test_08_selected_rows(create_sources_table):
    dbref = create_sources_table
    load_sources_table(dbref)
    source_set = SourceSet(dbref,'source', 'Local Purchase')
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + source_set.get_table() + " WHERE source = 'Local Purchase'")
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(source_set.get_property_set())
    assert count == 1
    close_database(dbref)

def test_09_cleanup(open_database):
    dbref = open_database
    result = dbref.sql_query("DROP TABLE IF EXISTS 'sources'")
    assert result
    close_database(dbref)
    delete_database()

# end test_14_SourceSet

