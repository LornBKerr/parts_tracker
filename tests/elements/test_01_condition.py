"""
Test the Condition class.

File:       test_01_condition.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

import pytest

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library import Dbal

from elements import Condition

from test_setup_elements import (
    database_name, close_database, open_database,
)

@pytest.fixture
def create_conditions_table():
    dbref = Dbal()
    dbref.sql_connect('parts_test.db')
    dbref.sql_query("DROP TABLE IF EXISTS 'conditions'")
    create_table = 'CREATE TABLE "conditions" (record_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, condition TEXT DEFAULT "")'
    result = dbref.sql_query(create_table)
    return dbref

# set condition values from array of values
condition_values = dict({'record_id': 15,
                    'condition': 'Replace',})

def test_01_01_constr(open_database):
    dbref = open_database
    condition = Condition(dbref)
    assert type(condition) == Condition
    close_database(dbref)

def test_01_02_get_table(open_database):
    dbref = open_database
    condition = Condition(dbref)
    assert condition.get_table() == 'conditions'
    close_database(dbref)
    
def test_01_03_get_dbref(open_database):
    dbref = open_database
    condition = Condition(dbref)
    assert condition.get_dbref() == dbref
    close_database(dbref)

def test_01_04_set_conditions(open_database):
    # set empty Condition
    dbref = open_database
    condition = Condition(dbref)
        # 'condition': 'Moss USA' required
    condition._set_property('condition', None);
    assert condition.get_condition() == ""
    result = condition.set_condition(None)
    assert not result['valid']
    assert result['entry'] is None
    assert condition.get_condition() == ''
    result = condition.set_condition(condition_values['condition']) 
    assert result['valid']
    assert result['entry'] == condition_values['condition']
    assert result['entry'] == condition.get_condition()
    close_database(dbref)


#def test_01_04_get_properties_type(open_database):
#    dbref = open_database
#    condition = Condition(dbref)
#    data = condition.get_properties()
#    assert type(data) == dict
#    close_database(dbref)
#
#def test_01_05_get_properties_size(open_database):
#    dbref = open_database
#    condition = Condition(dbref)
#    data = condition.get_properties()
#    assert len(data) == 2
#    close_database(dbref)
3
#def test_01_06_get_property_values_none(open_database):
#    dbref = open_database
#    condition = Condition(dbref)
#    defaults = condition.get_initial_values()
#    assert condition.get_record_id() == defaults['record_id']
#    assert condition.get_condition() == defaults['condition']
#    condition._set_property('record_id', None)
#    close_database(dbref)
#def test_01_08_set_properties_from_dict(open_database):
#    # set Condition from array
#    dbref = open_database
#    condition = Condition(dbref)
#    condition.set_properties(condition_values)
#    assert condition_values['record_id'] == condition.get_record_id()
#    assert condition_values['condition'] == condition.get_condition()
#    close_database(dbref)
#
#def test_01_09_constructor_missing_key(open_database):
#    dbref = open_database
#    values = {'record_id': 15}
#    condition = Condition(dbref, values)
#    assert values['record_id'] == condition.get_record_id()
#    assert "" == condition.get_condition()
#    close_database(dbref)
#
#def test_01_10_add(create_conditions_table):
#    dbref = create_conditions_table
#    condition = Condition(dbref, condition_values)
#    record_id = condition.add()
#    assert record_id == 1
#    assert record_id == condition.get_record_id()
#    assert condition_values['condition'] == condition.get_condition()
#    close_database(dbref)
#    
#def test_01_11_read_db(create_conditions_table):
#    dbref = create_conditions_table
#    condition = Condition(dbref)
#    condition.set_properties(condition_values)
#    record_id = condition.add()
#    assert record_id == 1
#        #read db for existing part
#    condition2 = Condition(dbref, record_id)
#    assert record_id == condition2.get_record_id()
#    assert condition_values['condition'] == condition2.get_condition()
#        # read db for non-existing part
#    condition3 = Condition(dbref, 5)
#    assert isinstance(condition3.get_properties(), dict)
#    assert len(condition3.get_properties()) == len(condition_values)
#        # Try direct read thru Element
#    condition2.set_properties(condition2.get_properties_from_db(None, None))
#    assert isinstance (condition2.get_properties(), dict)
#    assert len(condition2.get_properties()) == 0
#    close_database(dbref)
#
#def test_01_12_update(create_conditions_table):
#    dbref = create_conditions_table
#    condition = Condition(dbref)
#    condition.set_properties(condition_values)
#    record_id = condition.add()
#    assert record_id == 1
#    assert condition_values['condition'] == condition.get_condition()
#        
#        # update condition
#    condition.set_condition("British Wiring")
#    result = condition.update()
#    assert result
#    assert condition.get_properties() is not None
#    assert record_id == condition.get_record_id()
#    assert not condition_values['condition'] == condition.get_condition()
#    assert "British Wiring" == condition.get_condition()
#    close_database(dbref)
#
#def test_01_13_delete(create_conditions_table):
#    dbref = create_conditions_table
#    condition = Condition(dbref)
#    condition.set_properties(condition_values)
#    record_id = condition.add()
#        #delete part
#    result = condition.delete()
#    assert result
3        #make sure it is really gone
#    condition2 = Condition(dbref, condition_values['record_id'])
#    assert isinstance (condition2.get_properties(), dict)
#    assert len(condition2.get_properties()) == len(condition_values)
#    close_database(dbref)
#
#def test_01_14_cleanup(open_database):
#    dbref = open_database
#    result = dbref.sql_query("DROP TABLE IF EXISTS 'conditions'")
#    assert result
#    close_database(dbref)
#    delete_database()
#
