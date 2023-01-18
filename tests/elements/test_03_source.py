import pytest
import os

from common import Dbal
from parts_elements import Source

database = './parts_test.db'

def close_database(dbref):
    dbref.sql_close()

def delete_database():
    os.remove(database)

@pytest.fixture
def open_database():
    dbref = Dbal()
    dbref.sql_connect(database)
    return dbref

@pytest.fixture
def create_sources_table():
    dbref = Dbal()
    dbref.sql_connect('parts_test.db')
    dbref.sql_query("DROP TABLE IF EXISTS 'sources'")
    create_table = 'CREATE TABLE "sources" (entry_index INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, source TEXT DEFAULT "")'
    result = dbref.sql_query(create_table)
    return dbref

# set source values from array of values
source_values = dict({'entry_index': 15,
                    'source': 'Moss USA',})

# Test Empty Source
def test_01_constr(open_database):
    dbref = open_database
    source = Source(dbref)
    assert type(source) == Source
    close_database(dbref)

def test_02_get_table(open_database):
    dbref = open_database
    source = Source(dbref)
    assert source.get_table() == 'sources'
    close_database(dbref)
    
def test_03_get_dbref(open_database):
    dbref = open_database
    source = Source(dbref)
    assert source.get_dbref() == dbref
    close_database(dbref)

def test_04_get_properties_type(open_database):
    dbref = open_database
    source = Source(dbref)
    data = source.get_properties()
    assert type(data) == dict
    close_database(dbref)

def test_05_get_properties_size(open_database):
    dbref = open_database
    source = Source(dbref)
    data = source.get_properties()
    assert len(data) == 2
    close_database(dbref)

def test_06_get_property_values_none(open_database):
    dbref = open_database
    source = Source(dbref)
    defaults = source.get_initial_values()
    assert source.get_entry_index() == defaults['entry_index']
    assert source.get_source() == defaults['source']
    source._set_property('entry_index', None)
    
    close_database(dbref)

def test_07_set_functions(open_database):
    # set empty Source
    dbref = open_database
    source = Source(dbref)
    # set source properties from 'source_values'
        #'entry_index': 15, required
    result = source.set_entry_index(None)
    assert not result['valid']
    assert result['entry'] == None
    assert source.get_entry_index() == 0
    result = source.set_entry_index(-1)
    assert not result['valid']
    assert result['entry'] == -1
    assert source.get_entry_index() == 0
    result = source.set_entry_index(source_values['entry_index']) 
    assert result['valid']
    assert result['entry'] == source_values['entry_index']
    assert result['entry'] == source.get_entry_index()
        # 'source': 'Moss USA' required
    source._set_property('source', None);
    assert source.get_source() == ""
    result = source.set_source(None)
    assert not result['valid']
    assert result['entry'] is None
    assert source.get_source() == ''
    result = source.set_source(source_values['source']) 
    assert result['valid']
    assert result['entry'] == source_values['source']
    assert result['entry'] == source.get_source()
    close_database(dbref)

def test_08_set_properties_from_dict(open_database):
    # set Source from array
    dbref = open_database
    source = Source(dbref)
    source.set_properties(source_values)
    assert source_values['entry_index'] == source.get_entry_index()
    assert source_values['source'] == source.get_source()
    close_database(dbref)

def test_09_constructor_missing_key(open_database):
    dbref = open_database
    values = {'entry_index': 15}
    source = Source(dbref, values)
    assert values['entry_index'] == source.get_entry_index()
    assert "" == source.get_source()
    close_database(dbref)

def test_10_add(create_sources_table):
    dbref = create_sources_table
    source = Source(dbref, source_values)
    entry_index = source.add()
    assert entry_index == 1
    assert entry_index == source.get_entry_index()
    assert source_values['source'] == source.get_source()
    close_database(dbref)
    
def test_11_read_db(create_sources_table):
    dbref = create_sources_table
    source = Source(dbref)
    source.set_properties(source_values)
    entry_index = source.add()
    assert entry_index == 1
        #read db for existing part
    source2 = Source(dbref, entry_index)
    assert entry_index == source2.get_entry_index()
    assert source_values['source'] == source2.get_source()
        # read db for non-existing part
    source3 = Source(dbref, 5)
    assert isinstance(source3.get_properties(), dict)
    assert len(source3.get_properties()) == len(source_values)
        # Try direct read thru Element
    source2.set_properties(source2.get_properties_from_db(None, None))
    assert isinstance (source2.get_properties(), dict)
    assert len(source2.get_properties()) == 0
    close_database(dbref)

def test_12_update(create_sources_table):
    dbref = create_sources_table
    source = Source(dbref)
    source.set_properties(source_values)
    entry_index = source.add()
    assert entry_index == 1
    assert source_values['source'] == source.get_source()
        
        # update source
    source.set_source("British Wiring")
    result = source.update()
    assert result
    assert source.get_properties() is not None
    assert entry_index == source.get_entry_index()
    assert not source_values['source'] == source.get_source()
    assert "British Wiring" == source.get_source()
    close_database(dbref)

def test_13_delete(create_sources_table):
    dbref = create_sources_table
    source = Source(dbref)
    source.set_properties(source_values)
    entry_index = source.add()
        #delete part
    result = source.delete()
    assert result
        #make sure it is really gone
    source2 = Source(dbref, source_values['entry_index'])
    assert isinstance (source2.get_properties(), dict)
    assert len(source2.get_properties()) == len(source_values)
    close_database(dbref)

def test_14_cleanup(open_database):
    dbref = open_database
    result = dbref.sql_query("DROP TABLE IF EXISTS 'sources'")
    assert result
    close_database(dbref)
    delete_database()

