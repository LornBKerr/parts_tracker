"""
Test the Order class.

File:       test_011_order.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

import pytest
from lbk_library import Dbal
from test_setup import db_close, db_create, db_open

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from elements import Order

order_values = {
    "record_id": 9876,
    "order_number": "09-001",
    "date": "10/02/2009",
    "source": "Moss",
    "subtotal": 25.25,
    "shipping": 2.95,
    "discount": -1.02,
    "tax": 1.77,
    "total": 28.95,
    "remarks": "From local source",
}


# Test Empty Order
def test_011_01_constr(db_open):
    dbref = db_open
    order = Order(dbref)
    assert type(order) == Order
    db_close(dbref)


def test_011_02_get_table(db_open):
    dbref = db_open
    order = Order(dbref)
    assert order.get_table() == "orders"
    db_close(dbref)


def test_011_03_get_dbref(db_open):
    dbref = db_open
    order = Order(dbref)
    assert order.get_dbref() == dbref
    db_close(dbref)


def test_011_04_get_set_order_number(db_open):
    dbref = db_open
    order = Order(dbref)
    defaults = order.get_initial_values()
    order._set_property("order_number", order_values["order_number"])
    assert order_values["order_number"] == order.get_order_number()
    order._set_property("order_number", None)
    assert order.defaults["order_number"] == order.get_order_number()
    result = order.set_order_number(None)
    assert not result["valid"]
    assert result["entry"] == None
    result = order.set_order_number(order_values["order_number"])
    assert result["valid"]
    assert result["entry"] == order_values["order_number"]
    assert result["entry"] == order.get_order_number()
    db_close(dbref)


def test_011_05_get_set_date(db_open):
    dbref = db_open
    order = Order(dbref)
    defaults = order.get_initial_values()
    order._set_property("date", None)
    assert defaults["date"] == order.get_date()
    result = order.set_date(None)
    assert not result["valid"]
    assert result["entry"] is None
    assert order.get_date() == defaults["date"]
    result = order.set_date("")
    assert not result["valid"]
    assert order.get_date() == defaults["date"]
    assert result["entry"] == ""
    result = order.set_date(order_values["date"])
    assert result["valid"]
    assert result["entry"] == order_values["date"]
    assert result["entry"] == order.get_date()
    result = order.set_date("2009-02-29")
    assert not result["valid"]
    assert order.get_date() == defaults["date"]
    order._set_property("date", "2009-02-28")
    assert order.get_date() == "02/28/2009"
    result = order.set_date("2009-02-28")
    assert result["valid"]
    assert result["entry"] == "02/28/2009"
    assert order.get_date() == "02/28/2009"
    db_close(dbref)


def test_011_06_get_set_source(db_open):
    dbref = db_open
    order = Order(dbref)
    defaults = order.get_initial_values()
    order._set_property("source", None)
    assert defaults["source"] == order.get_source()
    result = order.set_source(None)
    assert not result["valid"]
    assert result["entry"] is None
    assert order.get_source() == defaults["source"]
    result = order.set_source(order_values["source"])
    assert result["valid"]
    assert result["entry"] == order_values["source"]
    assert result["entry"] == order.get_source()
    db_close(dbref)


def test_011_07_get_set_subtotal(db_open):
    dbref = db_open
    order = Order(dbref)
    defaults = order.get_initial_values()
    order._set_property("subtotal", None)
    assert defaults["subtotal"] == order.get_subtotal()
    result = order.set_subtotal(None)
    assert result["valid"]
    assert order.get_subtotal() == defaults["subtotal"]
    result = order.set_subtotal(-1)
    assert not result["valid"]
    assert order.get_subtotal() == defaults["subtotal"]
    result = order.set_subtotal(order_values["subtotal"])
    assert result["valid"]
    assert result["entry"] == order_values["subtotal"]
    assert result["entry"] == order.get_subtotal()
    db_close(dbref)


def test_011_08_get_set_shipping(db_open):
    dbref = db_open
    order = Order(dbref)
    defaults = order.get_initial_values()
    order._set_property("shipping", None)
    assert defaults["shipping"] == order.get_shipping()
    result = order.set_shipping(None)
    assert result["valid"]
    assert order.get_shipping() == defaults["shipping"]
    result = order.set_shipping(-1)
    assert not result["valid"]
    assert order.get_shipping() == defaults["shipping"]
    result = order.set_shipping(order_values["shipping"])
    assert result["valid"]
    assert result["entry"] == order_values["shipping"]
    assert result["entry"] == order.get_shipping()
    db_close(dbref)


def test_011_09_get_set_discount(db_open):
    dbref = db_open
    order = Order(dbref)
    defaults = order.get_initial_values()
    order._set_property("discount", None)
    assert defaults["discount"] == order.get_discount()
    result = order.set_discount(None)
    assert result["valid"]
    assert order.get_discount() == defaults["discount"]
    result = order.set_discount(1.0)
    assert not result["valid"]
    result = order.set_discount(-1.0)
    assert result["valid"]
    assert order.get_discount() == -1.0
    result = order.set_discount(order_values["discount"])
    assert result["valid"]
    assert result["entry"] == order_values["discount"]
    assert result["entry"] == order.get_discount()
    db_close(dbref)


def test_011_10_get_set_tax(db_open):
    dbref = db_open
    order = Order(dbref)
    defaults = order.get_initial_values()
    order._set_property("tax", None)
    assert defaults["tax"] == order.get_tax()
    result = order.set_tax(None)
    assert result["valid"]
    assert order.get_tax() == defaults["tax"]
    result = order.set_tax(-1)
    assert not result["valid"]
    assert order.get_tax() == defaults["tax"]
    result = order.set_tax(order_values["tax"])
    assert result["valid"]
    assert result["entry"] == order_values["tax"]
    assert result["entry"] == order.get_tax()
    db_close(dbref)


def test_011_11_get_set_total(db_open):
    dbref = db_open
    order = Order(dbref)
    defaults = order.get_initial_values()
    order._set_property("total", None)
    assert defaults["total"] == order.get_total()
    result = order.set_total(None)
    assert result["valid"]
    assert order.get_total() == defaults["total"]
    result = order.set_total(-1)
    assert not result["valid"]
    assert order.get_total() == defaults["total"]
    result = order.set_total(order_values["total"])
    assert result["valid"]
    assert result["entry"] == order_values["total"]
    assert result["entry"] == order.get_total()
    db_close(dbref)


def test_011_12_get_properties_type(db_open):
    dbref = db_open
    order = Order(dbref)
    data = order.get_properties()
    assert type(data) == dict
    db_close(dbref)


def test_011_011_13_get_properties_size(db_open):
    dbref = db_open
    order = Order(dbref)
    data = order.get_properties()
    assert len(data) == len(order_values)
    db_close(dbref)


def test_011_14_get_default_property_values(db_open):
    dbref = db_open
    order = Order(dbref)
    defaults = order.get_initial_values()
    assert order.get_record_id() == defaults["record_id"]
    assert order.get_order_number() == defaults["order_number"]
    assert order.get_date() == defaults["date"]
    assert order.get_source() == defaults["source"]
    assert order.get_subtotal() == defaults["subtotal"]
    assert order.get_tax() == defaults["tax"]
    assert order.get_shipping() == defaults["shipping"]
    assert order.get_discount() == defaults["discount"]
    assert order.get_total() == defaults["total"]
    assert order.get_remarks() == defaults["remarks"]
    db_close(dbref)


def test_011_15_set_order_from_dict(db_open):
    dbref = db_open
    order = Order(dbref, order_values)
    assert order_values["record_id"] == order.get_record_id()
    assert order_values["order_number"] == order.get_order_number()
    assert order_values["source"] == order.get_source()
    assert order_values["date"] == order.get_date()
    assert order_values["subtotal"] == order.get_subtotal()
    assert order_values["tax"] == order.get_tax()
    assert order_values["shipping"] == order.get_shipping()
    assert order_values["total"] == order.get_total()
    assert order_values["remarks"] == order.get_remarks()
    db_close(dbref)


def test_011_16_set_order_from_partial_dict(db_open):
    dbref = db_open
    del order_values["source"]
    order = Order(dbref, order_values)
    assert order_values["record_id"] == order.get_record_id()
    assert order_values["order_number"] == order.get_order_number()
    assert order_values["source"] == ""
    assert order_values["date"] == order.get_date()
    assert order_values["subtotal"] == order.get_subtotal()
    assert order_values["tax"] == order.get_tax()
    assert order_values["shipping"] == order.get_shipping()
    assert order_values["total"] == order.get_total()
    assert order_values["remarks"] == order.get_remarks()
    db_close(dbref)


def test_011_17_bad_column_name(db_open):
    dbref = db_open
    order = Order(dbref, None, "a_column")
    defaults = order.get_initial_values()
    assert order.get_record_id() == defaults["record_id"]
    assert order.get_order_number() == defaults["order_number"]
    assert order.get_date() == defaults["date"]
    assert order.get_source() == defaults["source"]
    assert order.get_subtotal() == defaults["subtotal"]
    assert order.get_tax() == defaults["tax"]
    assert order.get_shipping() == defaults["shipping"]
    assert order.get_discount() == defaults["discount"]
    assert order.get_total() == defaults["total"]
    assert order.get_remarks() == defaults["remarks"]
    db_close(dbref)


def test_011_18_order_add(db_create):
    dbref = db_create
    order = Order(dbref, order_values)
    record_id = order.add()
    assert record_id == 1
    assert record_id == order.get_record_id()
    assert order_values["order_number"] == order.get_order_number()
    assert order_values["source"] == order.get_source()
    assert order_values["date"] == order.get_date()
    assert order.get_subtotal() == order_values["subtotal"]
    assert order.get_tax() == order_values["tax"]
    assert order.get_shipping() == order_values["shipping"]
    assert order.get_discount() == order_values["discount"]
    assert order.get_total() == order_values["total"]
    assert order_values["remarks"] == order.get_remarks()
    db_close(dbref)


def test_011_19_order_read_db(db_create):
    dbref = db_create
    order = Order(dbref, order_values)
    record_id = order.add()
    assert record_id == 1
    # read db for existing part
    order2 = Order(dbref, order_values["order_number"])
    assert order2 is not None
    assert order2.get_properties() is not None
    assert record_id == order2.get_record_id()
    assert order_values["order_number"] == order2.get_order_number()
    assert order_values["source"] == order2.get_source()
    assert order_values["date"] == order2.get_date()
    assert order_values["remarks"] == order2.get_remarks()
    # read db for non-existing part
    order3 = Order(dbref, 5)
    assert len(order3.get_properties()) == len(order_values)
    # Try direct read thru Element
    order2.set_properties(order2.get_properties_from_db(None, None))
    assert len(order2.get_properties()) == 0
    db_close(dbref)


def test_011_20_order_update(db_create):
    dbref = db_create
    order = Order(dbref, order_values)
    record_id = order.add()
    assert record_id == 1
    assert order_values["date"] == order.get_date()
    # update part description
    order.set_date("10/02/2011")
    result = order.update()
    assert result
    assert order.get_properties() is not None
    assert order_values["order_number"] == order.get_order_number()
    assert order_values["source"] == order.get_source()
    assert not order_values["date"] == order.get_date()
    assert "10/02/2011" == order.get_date()
    assert order_values["remarks"] == order.get_remarks()
    db_close(dbref)


def test_011_21_order_delete(db_create):
    dbref = db_create
    order = Order(dbref, order_values)
    record_id = order.add()
    # delete order
    result = order.delete()
    assert result
    # make sure it is really gone
    order = Order(dbref, order_values["order_number"])
    assert isinstance(order.get_properties(), dict)
    assert len(order.get_properties()) == len(order_values)
