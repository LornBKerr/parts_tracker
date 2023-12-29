"""
Test the SourceSet class.

File:       test_004_source_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

from lbk_library import Dbal, ElementSet
from test_setup import (
    db_close,
    db_create,
    db_open,
    filesystem,
    load_db_table,
    source_columns,
    source_value_set,
)

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from elements import SourceSet


def test_004_01_constr(filesystem):
    """
    SourceSet Extends ElementSet.

    The 'table' must be "conditions" and 'dbref' needs to be the
    initializing dbref.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    source_set = SourceSet(dbref)
    assert isinstance(source_set, SourceSet)
    assert isinstance(source_set, ElementSet)
    assert source_set.get_table() == "sources"
    assert source_set.get_dbref() == dbref
    db_close(dbref)


def test_004_02_set_property_set_empty(filesystem):
    """
    The 'property_set', a list of 'Sources', is empty when set to
    None or when the table is empty.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    source_set = SourceSet(dbref)
    assert isinstance(source_set.get_property_set(), list)
    source_set.set_property_set(None)
    assert isinstance(source_set.get_property_set(), list)
    assert len(source_set.get_property_set()) == 0
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + source_set.get_table())
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(source_set.get_property_set())
    assert count == source_set.get_number_elements()
    db_close(dbref)


def test_004_03_selected_rows(filesystem):
    """
    The 'property_set', a list of 'Sources', should contain the
    requested subset of conditions.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    load_db_table(dbref, "sources", source_columns, source_value_set)
    source_set = SourceSet(dbref, "source", "British Car Parts")
    count_result = dbref.sql_query(
        "SELECT COUNT(*) FROM "
        + source_set.get_table()
        + " WHERE source = 'British Car Parts'"
    )
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(source_set.get_property_set())
    assert count == 1
    db_close(dbref)
