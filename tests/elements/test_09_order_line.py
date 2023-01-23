"""
Test the OrderLine class.

File:       order_line.py
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
from test_setup_elements import (
    close_database,
    create_orderlines_table,
    database_name,
    open_database,
)

from elements import OrderLine

# set order line values from array of values
order_line_values = {
    "record_id": 10,
    "order_number": "09-001",
    "line": 3,
    "part_number": "13571",
    "cost_each": 10.01,
    "quantity": 3,
    "remarks": "remarks",
}


def test_09_01_constr(open_database):
    dbref = open_database
    order_line = OrderLine(dbref)
    assert type(order_line) == OrderLine
    close_database(dbref)


def test_09_02_get_table(open_database):
    dbref = open_database
    order_line = OrderLine(dbref)
    assert order_line.get_table() == "order_lines"
    close_database(dbref)


def test_09_03_get_dbref(open_database):
    dbref = open_database
    order_line = OrderLine(dbref)
    assert order_line.get_dbref() == dbref
    close_database(dbref)


def test_09_04_get_set_order_number(open_database):
    dbref = open_database
    order_line = OrderLine(dbref)
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
    close_database(dbref)


def test_09_05_get_set_line(open_database):
    dbref = open_database
    order_line = OrderLine(dbref)
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
    close_database(dbref)


def test_09_06_get_set_part_number(open_database):
    dbref = open_database
    order_line = OrderLine(dbref)
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
    close_database(dbref)


def test_09_07_get_set_cost_ea(open_database):
    dbref = open_database
    order_line = OrderLine(dbref)
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


def test_09_08_get_set_quantity(open_database):
    dbref = open_database
    order_line = OrderLine(dbref)
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
    print(result)
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
    close_database(dbref)


def test_09_09_get_set_quantity(open_database):
    dbref = open_database
    order_line = OrderLine(dbref)
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
    print(result)
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
    close_database(dbref)


def test_09_10_get_line_cost(open_database):
    dbref = open_database
    order_line = OrderLine(dbref)
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


def test_09_11_get_properties_type(open_database):
    dbref = open_database
    order_line = OrderLine(dbref)
    data = order_line.get_properties()
    assert isinstance(data, dict)
    close_database(dbref)


def test_09_12_get_default_property_values(open_database):
    dbref = open_database
    order_line = OrderLine(dbref)
    defaults = order_line.get_initial_values()
    assert order_line.get_record_id() == defaults["record_id"]
    assert order_line.get_order_number() == defaults["order_number"]
    assert order_line.get_line() == defaults["line"]
    assert order_line.get_part_number() == defaults["part_number"]
    assert order_line.get_cost_each() == defaults["cost_each"]
    assert order_line.get_quantity() == defaults["quantity"]
    assert order_line.get_remarks() == defaults["remarks"]
    close_database(dbref)


def test_09_13_set_properties_from_dict(open_database):
    dbref = open_database
    order_line = OrderLine(dbref)
    order_line.set_properties(order_line_values)
    assert order_line_values["record_id"] == order_line.get_record_id()
    assert order_line_values["order_number"] == order_line.get_order_number()
    assert order_line_values["line"] == order_line.get_line()
    assert order_line_values["part_number"] == order_line.get_part_number()
    assert order_line_values["cost_each"] == order_line.get_cost_each()
    assert order_line_values["quantity"] == order_line.get_quantity()
    assert order_line_values["remarks"] == order_line.get_remarks()
    close_database(dbref)


def test_09_14_get_properties_size(open_database):
    dbref = open_database
    order_line = OrderLine(dbref)
    data = order_line.get_properties()
    assert len(data) == len(order_line_values)
    close_database(dbref)


def test_09_15_set_from_dict(open_database):
    dbref = open_database
    order_line = OrderLine(dbref, order_line_values)
    assert order_line_values["record_id"] == order_line.get_record_id()
    assert order_line_values["order_number"] == order_line.get_order_number()
    assert order_line_values["line"] == order_line.get_line()
    assert order_line_values["part_number"] == order_line.get_part_number()
    assert order_line_values["cost_each"] == order_line.get_cost_each()
    assert order_line_values["quantity"] == order_line.get_quantity()
    assert order_line_values["remarks"] == order_line.get_remarks()
    close_database(dbref)


def test_09_16_set_from_partial_dict(open_database):
    dbref = open_database
    del order_line_values["part_number"]
    order_line = OrderLine(dbref, order_line_values)
    assert order_line_values["record_id"] == order_line.get_record_id()
    assert order_line_values["order_number"] == order_line.get_order_number()
    assert order_line_values["line"] == order_line.get_line()
    assert order_line_values["part_number"] == ""
    assert order_line_values["cost_each"] == order_line.get_cost_each()
    assert order_line_values["quantity"] == order_line.get_quantity()
    assert order_line_values["remarks"] == order_line.get_remarks()
    close_database(dbref)


def test_09_17_add(open_database):
    dbref = open_database
    create_orderlines_table(dbref)
    order_line = OrderLine(dbref, order_line_values)
    record_id = order_line.add()
    assert record_id == 1
    assert record_id == order_line.get_record_id()
    assert order_line_values["order_number"] == order_line.get_order_number()
    assert order_line_values["line"] == order_line.get_line()
    assert order_line_values["part_number"] == ""
    assert order_line_values["cost_each"] == order_line.get_cost_each()
    assert order_line_values["quantity"] == order_line.get_quantity()
    assert order_line_values["remarks"] == order_line.get_remarks()
    close_database(dbref)
    close_database(dbref)


def test_09_18_read_db(open_database):
    dbref = open_database
    create_orderlines_table(dbref)
    order_line = OrderLine(dbref)
    defaults = order_line.get_initial_values()
    order_line.set_properties(order_line_values)
    record_id = order_line.add()
    assert record_id == 1
    # read db for existing part
    order2 = OrderLine(dbref, record_id)
    assert order2 is not None
    assert order2.get_properties() is not None
    assert record_id == order2.get_record_id()
    assert order_line_values["order_number"] == order2.get_order_number()
    assert order_line_values["line"] == order2.get_line()
    assert order_line_values["part_number"] == order2.get_part_number()
    assert order_line_values["remarks"] == order2.get_remarks()
    # read db for non-existing part
    order3 = OrderLine(dbref, 5)
    assert len(order3.get_properties()) == len(order_line_values)
    assert defaults["record_id"] == order3.get_record_id()
    assert defaults["order_number"] == order3.get_order_number()
    assert defaults["line"] == order3.get_line()
    assert defaults["part_number"] == order3.get_part_number()
    assert defaults["remarks"] == order3.get_remarks()
    # Try direct read thru Element
    order2.set_properties(order2.get_properties_from_db(None, None))
    assert len(order2.get_properties()) == 0
    close_database(dbref)


def test_09_19_update(open_database):
    dbref = open_database
    create_orderlines_table(dbref)
    order_line = OrderLine(dbref)
    defaults = order_line.get_initial_values()
    order_line.set_properties(order_line_values)
    assert order_line.get_record_id() == order_line_values["record_id"]
    assert order_line_values["quantity"] == order_line.get_quantity()
    # update order_line quantity
    order_line.set_quantity(6)
    result = order_line.update()
    assert result
    assert order_line.get_properties() is not None
    assert order_line.get_record_id() == order_line_values["record_id"]
    assert order_line_values["part_number"] == order_line.get_part_number()
    assert not order_line_values["quantity"] == order_line.get_quantity()
    assert order_line.get_quantity() == 6
    close_database(dbref)


def test_09_15_delete(open_database):
    dbref = open_database
    create_orderlines_table(dbref)
    order_line = OrderLine(dbref)
    order_line.set_properties(order_line_values)
    order_line.add()
    # delete orderline
    result = order_line.delete()
    assert result
    # make sure it is really gone
    order_line2 = OrderLine(dbref, 1)
    assert isinstance(order_line2.get_properties(), dict)
    assert len(order_line2.get_properties()) == len(order_line_values)
    close_database(dbref)

