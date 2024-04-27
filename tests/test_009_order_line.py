"""
Test the OrderLine class.

File:       test_009_order_line.py.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

from lbk_library import Dbal
from test_data import order_line_columns, order_line_value_set
from test_setup import (
    filesystem,
    load_parts_file_table,
    parts_file_close,
    parts_file_create,
)

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from elements import OrderLine
from pages import table_definition

parts_filename = "parts_test.parts"
order_line_values = {
    "record_id": order_line_value_set[0][0],
    "order_number": order_line_value_set[0][1],
    "line": order_line_value_set[0][2],
    "part_number": order_line_value_set[0][3],
    "cost_each": order_line_value_set[0][4],
    "quantity": order_line_value_set[0][5],
    "remarks": order_line_value_set[0][6],
}


def base_setup(filesystem):
    filename = filesystem + "/" + parts_filename
    parts_file = parts_file_create(filename, table_definition)
    order_line = OrderLine(parts_file)
    return (order_line, parts_file)


def test_009_01_constr(filesystem):
    """
    OrderLine Extends Element.

    Check the types of class variables and default values.
    """
    order_line, parts_file = base_setup(filesystem)
    assert type(order_line) == OrderLine
    # default values.
    assert isinstance(order_line.defaults, dict)
    assert len(order_line.defaults) == 7
    assert order_line.defaults["record_id"] == 0
    assert order_line.defaults["order_number"] == ""
    assert order_line.defaults["line"] == 0
    assert order_line.defaults["part_number"] == ""
    assert order_line.defaults["cost_each"] == 0.0
    assert order_line.defaults["quantity"] == 0
    assert order_line.defaults["remarks"] == ""
    parts_file_close(parts_file)


def test_009_02_get_parts_file(filesystem):
    """OrderLine needs correct database."""
    order_line, parts_file = base_setup(filesystem)
    assert order_line.get_datafile() == parts_file
    parts_file_close(parts_file)


def test_009_03_get_table(filesystem):
    """OrderLine needs the database table 'order_lines'."""
    order_line, parts_file = base_setup(filesystem)
    assert order_line.get_table() == "order_lines"
    parts_file_close(parts_file)


def test_009_04_get_set_order_number(filesystem):
    """
    Get and set the order_number property.

    The property 'order_number' is required and is a string matching the
    regular exression 'yy-nnn' where the yy is the two digit year and
    the nnn is a three digit sequential number starting at '001' for the
    next order in the year.
    """
    order_line, parts_file = base_setup(filesystem)
    defaults = order_line.get_initial_values()
    order_line._set_property("order_number", None)
    assert order_line.get_order_number() == defaults["order_number"]
    order_line._set_property("order_number", "")
    assert order_line.get_order_number() == defaults["order_number"]
    order_line._set_property("order_number", defaults["order_number"])
    assert order_line.get_order_number() == defaults["order_number"]
    order_line._set_property("order_number", order_line_values["order_number"])
    assert order_line.get_order_number() == order_line_values["order_number"]
    result = order_line.set_order_number(None)
    assert not result["valid"]
    assert result["entry"] == None
    assert order_line.get_order_number() == defaults["order_number"]
    result = order_line.set_order_number("")
    assert not result["valid"]
    assert result["entry"] == defaults["order_number"]
    assert order_line.get_order_number() == defaults["order_number"]
    result = order_line.set_order_number(defaults["order_number"])
    assert not result["valid"]
    assert result["entry"] == defaults["order_number"]
    assert order_line.get_order_number() == defaults["order_number"]
    result = order_line.set_order_number(order_line_values["order_number"])
    assert result["valid"]
    assert result["entry"] == order_line_values["order_number"]
    assert result["entry"] == order_line.get_order_number()
    bad = "109-001"
    result = order_line.set_order_number(bad)
    assert not result["valid"]
    assert result["entry"] == bad
    assert len(result["msg"]) > 0
    parts_file_close(parts_file)


def test_009_05_get_set_line(filesystem):
    """
    Get and set the line property.

    The property 'line', the sequence number of this order line in the
    overall order, is required and is a number btween 1 and the maximum
    integer available. It will normally be a small interger int the
    range of 1 to less than 100.
    """
    order_line, parts_file = base_setup(filesystem)
    defaults = order_line.get_initial_values()
    result = order_line._set_property("line", None)
    assert order_line.get_line() == defaults["line"]
    result = order_line._set_property("line", "")
    assert order_line.get_line() == defaults["line"]
    result = order_line._set_property("line", defaults["line"])
    assert order_line.get_line() == defaults["line"]
    result = order_line._set_property("line", 10)
    assert order_line.get_line() == 10
    result = order_line.set_line(None)
    assert order_line.get_line() == defaults["line"]
    assert result["entry"] == None
    assert result["valid"] == False
    assert len(result["msg"]) > 0
    result = order_line.set_line("")
    assert order_line.get_line() == defaults["line"]
    assert result["entry"] == ""
    assert result["valid"] == False
    result = order_line.set_line(defaults["line"])
    assert order_line.get_line() == defaults["line"]
    assert order_line.get_line() == defaults["line"]
    assert result["entry"] == defaults["line"]
    assert result["valid"] == False
    result = order_line.set_line(0)
    assert order_line.get_line() == defaults["line"]
    assert result["entry"] == defaults["line"]
    assert result["valid"] == False
    result = order_line.set_line(10)
    assert order_line.get_line() == 10
    assert result["entry"] == 10
    assert result["valid"] == True
    assert len(result["msg"]) == 0
    result = order_line.set_line(-10)
    assert order_line.get_line() == defaults["line"]
    assert result["entry"] == -10
    assert result["valid"] == False
    parts_file_close(parts_file)


def test_009_06_get_set_part_number(filesystem):
    """
    Get and set the part_number property.

    The property 'part_number' is required and is a string between 1 and
    30 characters long.
    """
    order_line, parts_file = base_setup(filesystem)
    defaults = order_line.get_initial_values()
    order_line._set_property("part_number", order_line_values["part_number"])
    assert order_line_values["part_number"] == order_line.get_part_number()
    order_line._set_property("part_number", None)
    assert order_line.defaults["part_number"] == order_line.get_part_number()
    result = order_line.set_part_number(None)
    assert not result["valid"]
    assert result["entry"] == None
    result = order_line.set_part_number(order_line_values["part_number"])
    assert result["valid"]
    assert result["entry"] == order_line_values["part_number"]
    assert result["entry"] == order_line.get_part_number()
    parts_file_close(parts_file)


def test_009_07_get_set_cost_ea(filesystem):
    """
    Get and set the cost each in dollars and cents. Thi is a float and
    is 0.0 to max float number.
    """
    order_line, parts_file = base_setup(filesystem)
    order_line._set_property("cost_each", None)
    defaults = order_line.get_initial_values()
    assert order_line.get_cost_each() == defaults["cost_each"]
    assert defaults["cost_each"] == order_line.get_cost_each()
    result = order_line.set_cost_each(None)
    assert not result["valid"]
    assert order_line.get_cost_each() == defaults["cost_each"]
    result = order_line.set_cost_each(-1)
    assert not result["valid"]
    assert order_line.get_cost_each() == defaults["cost_each"]
    result = order_line.set_cost_each(order_line_values["cost_each"])
    assert result["valid"]
    assert result["entry"] == order_line_values["cost_each"]
    assert result["entry"] == order_line.get_cost_each()


def test_009_08_get_set_quantity(filesystem):
    """
    Get and set the quantity for this Order Line. The quantity is a
    small integer from 0 to max integer, normally 1 or greater. Zero
    indicates the order line was cancelled or returned.
    """
    order_line, parts_file = base_setup(filesystem)
    defaults = order_line.get_initial_values()
    result = order_line._set_property("quantity", None)
    assert order_line.get_quantity() == defaults["quantity"]
    result = order_line._set_property("quantity", "")
    assert order_line.get_line() == defaults["quantity"]
    result = order_line._set_property("quantity", defaults["quantity"])
    assert order_line.get_quantity() == defaults["quantity"]
    result = order_line._set_property("quantity", 10)
    assert order_line.get_quantity() == 10

    result = order_line.set_quantity(None)
    assert order_line.get_quantity() == defaults["quantity"]
    assert result["entry"] == None
    assert result["valid"] == False
    assert len(result["msg"]) > 0
    result = order_line.set_quantity("")
    assert order_line.get_quantity() == defaults["quantity"]
    assert result["entry"] == 0
    assert result["valid"] == True

    result = order_line.set_quantity(defaults["quantity"])
    assert order_line.get_quantity() == defaults["quantity"]
    assert result["entry"] == defaults["quantity"]
    assert result["valid"] == True
    result = order_line.set_quantity(0)
    assert order_line.get_quantity() == 0
    assert result["entry"] == 0
    assert result["valid"] == True
    result = order_line.set_quantity(10)
    assert order_line.get_quantity() == 10
    assert result["entry"] == 10
    assert result["valid"] == True
    assert len(result["msg"]) == 0
    result = order_line.set_quantity(-10)
    assert order_line.get_quantity() == defaults["quantity"]
    assert result["entry"] == -10
    assert result["valid"] == False
    parts_file_close(parts_file)


def test_009_09_get_line_cost(filesystem):
    """
    Get the line cost for the order line. The line cost is a dynamically
    calculated number from the cost each value and quantity value. It is
    not stored in the database.
    """
    order_line, parts_file = base_setup(filesystem)
    defaults = order_line.get_initial_values()
    print(order_line.get_properties())
    assert order_line.get_line_cost() == 0
    order_line.set_quantity(2)
    assert order_line.get_quantity() == 2
    assert order_line.get_line_cost() == 0
    order_line.set_cost_each(2.2)
    assert order_line.get_cost_each() == 2.2
    assert (
        order_line.get_line_cost()
        == order_line.get_cost_each() * order_line.get_quantity()
    )
    order_line.set_quantity(0)
    assert order_line.get_quantity() == 0
    assert order_line.get_line_cost() == 0
    assert (
        order_line.get_line_cost()
        == order_line.get_cost_each() * order_line.get_quantity()
    )


def test_009_10_get_default_property_values(filesystem):
    """
    Check the default values.

    With no properties given to constructor, the initial values should
    be the default values.
    """
    order_line, parts_file = base_setup(filesystem)
    defaults = order_line.get_initial_values()
    assert order_line.get_record_id() == defaults["record_id"]
    assert order_line.get_order_number() == defaults["order_number"]
    assert order_line.get_line() == defaults["line"]
    assert order_line.get_part_number() == defaults["part_number"]
    assert order_line.get_cost_each() == defaults["cost_each"]
    assert order_line.get_quantity() == defaults["quantity"]
    assert order_line.get_remarks() == defaults["remarks"]
    parts_file_close(parts_file)


def test_009_11_set_properties_from_dict(filesystem):
    """
    Check the 'set_properties' function.

    The inital values can be set from a dict input.
    """
    order_line, parts_file = base_setup(filesystem)
    order_line.set_properties(order_line_values)
    assert order_line_values["record_id"] == order_line.get_record_id()
    assert order_line_values["order_number"] == order_line.get_order_number()
    assert order_line_values["line"] == order_line.get_line()
    assert order_line_values["part_number"] == order_line.get_part_number()
    assert order_line_values["cost_each"] == order_line.get_cost_each()
    assert order_line_values["quantity"] == order_line.get_quantity()
    assert order_line_values["remarks"] == order_line.get_remarks()
    parts_file_close(parts_file)


def test_009_12_get_properties_size(filesystem):
    """
    Check the size of the properties dict.

    There should be 7 members.
    """
    order_line, parts_file = base_setup(filesystem)
    data = order_line.get_properties()
    assert len(data) == len(order_line_values)
    parts_file_close(parts_file)


def test_009_13_set_from_partial_dict(filesystem):
    """
    Initialize a new OrderLine with a sparse dict of values.

    The resulting properties should mach the input values with the
    missing values replaced with default values.
    """
    order_line, parts_file = base_setup(filesystem)
    del order_line_values["part_number"]
    order_line = OrderLine(parts_file, order_line_values)
    assert order_line_values["record_id"] == order_line.get_record_id()
    assert order_line_values["order_number"] == order_line.get_order_number()
    assert order_line_values["line"] == order_line.get_line()
    assert order_line_values["part_number"] == ""
    assert order_line_values["cost_each"] == order_line.get_cost_each()
    assert order_line_values["quantity"] == order_line.get_quantity()
    assert order_line_values["remarks"] == order_line.get_remarks()
    parts_file_close(parts_file)


def test_001_16_get_properties_from_database(filesystem):
    """
    Access the database for the order_line properties.

    Add an OrderLine to the database, then access it with the
    record_id key. The actual read and write funtions are in the
    base class "Element".
    """
    order_line, parts_file = base_setup(filesystem)
    order_line = OrderLine(parts_file, order_line_values)
    record_id = order_line.add()
    assert record_id == 1
    assert record_id == order_line.get_record_id()

    order_line = OrderLine(parts_file, record_id)
    assert not order_line.get_record_id() == order_line_values["record_id"]
    assert order_line.get_record_id() == 1
    assert order_line.get_part_number() == order_line_values["part_number"]
    assert order_line.get_order_number() == order_line_values["order_number"]
    assert order_line.get_quantity() == order_line_values["quantity"]
    assert order_line.get_line() == order_line_values["line"]
    assert order_line.get_cost_each() == order_line_values["cost_each"]
    assert order_line.get_remarks() == order_line_values["remarks"]

    parts_file_close(parts_file)
