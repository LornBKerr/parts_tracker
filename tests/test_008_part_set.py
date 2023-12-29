"""
Test the ItemSet class.

File:       test_008_part_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

from lbk_library import Dbal, ElementSet

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from test_setup import (
    db_close,
    db_create,
    db_open,
    filesystem,
    load_db_table,
    part_columns,
    part_value_set,
)

from elements import Part, PartSet


def test_008_01_constr(filesystem):
    """
    PartSet Extends ElementSet.

    The 'table' must be "parts" and 'dbref' needs to be the
    initializing dbref.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    part_set = PartSet(dbref)
    assert isinstance(part_set, PartSet)
    assert isinstance(part_set, ElementSet)
    assert part_set.get_table() == "parts"
    assert part_set.get_dbref() == dbref
    db_close(dbref)


def test_008_02_set_property_set_empty(filesystem):
    """
    The 'property_set', a list of 'Parts', is empty when set to
    None or when the table is empty.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    part_set = PartSet(dbref)
    assert isinstance(part_set.get_property_set(), list)
    part_set.set_property_set(None)
    assert isinstance(part_set.get_property_set(), list)
    assert len(part_set.get_property_set()) == 0
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + part_set.get_table())
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(part_set.get_property_set())
    assert count == part_set.get_number_elements()
    db_close(dbref)


def test_008_03_selected_rows(filesystem):
    """
    The 'property_set', a list of 'Parts', should contain the
    requested subset of Parts.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    load_db_table(dbref, "parts", part_columns, part_value_set)
    part_set = PartSet(dbref, "source", "None")
    count_result = dbref.sql_query(
        "SELECT COUNT(*) FROM " + part_set.get_table() + " WHERE source = 'None'"
    )
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(part_set.get_property_set())
    assert count == 6
    db_close(dbref)


def test_008_4_selected_rows_limit(filesystem):
    """
    The 'property_set', a list of 'Parts', should contain the
    requested subset of Items ordered by record_id and the number of
    rows given by 'limit'.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    load_db_table(dbref, "parts", part_columns, part_value_set)
    limit = 5
    part_set = PartSet(dbref, None, None, "record_id", limit)
    assert limit == len(part_set.get_property_set())
    assert part_set.get_property_set()[0].get_record_id() == part_value_set[0][0]
    db_close(dbref)


def test_008_05_selected_rows_limit_offset(filesystem):
    """
    The 'property_set', a list of 'Parts', should contain the
    requested subset of Items ordered by record_id and the number of
    rows given by 'limit' starting at 'offset' number of records.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    load_db_table(dbref, "parts", part_columns, part_value_set)
    limit = 5
    offset = 2
    part_set = PartSet(dbref, None, None, "record_id", limit, offset)
    assert limit == len(part_set.get_property_set())
    assert part_set.get_property_set()[0].get_record_id() == part_value_set[2][0]
    db_close(dbref)
