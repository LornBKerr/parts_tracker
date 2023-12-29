"""
Test the Order class.

File:       test_011_order.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

from lbk_library import Dbal, Element
from test_setup import db_close, db_create, db_open, filesystem

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


def test_011_01_constr(filesystem):
    """
    Order Extends Element.

    Check the types of class variables and default values.
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
    order = Order(dbref)
    assert isinstance(order, Order)
    assert isinstance(order, Element)
    # default values.
    assert isinstance(order.defaults, dict)
    assert len(order.defaults) == 10
    assert order.defaults["record_id"] == 0
    assert order.defaults["order_number"] == ""
    assert order.defaults["date"] == ""
    assert order.defaults["source"] == ""
    assert order.defaults["subtotal"] == 0.0
    assert order.defaults["shipping"] == 0.0
    assert order.defaults["tax"] == 0.0
    assert order.defaults["total"] == 0.0
    assert order.defaults["remarks"] == ""
    db_close(dbref)


def test_011_02_get_table(filesystem):
    fs_base = filesystem
    dbref = db_open(fs_base)
    order = Order(dbref)
    assert order.get_table() == "orders"
    db_close(dbref)


def test_011_03_get_dbref(filesystem):
    fs_base = filesystem
    dbref = db_open(fs_base)
    order = Order(dbref)
    assert order.get_dbref() == dbref
    db_close(dbref)


def test_011_04_get_set_order_number(filesystem):
    """
    Get and set the order_number property.

    The property 'order_number' is required and is a string matching the
    regular exression 'yy-nnn' where the yy is the two digit year and
    the nnn is a three digit sequential number starting at '001' for the
    next order in the year.
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
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


def test_011_05_get_set_date(filesystem):
    """
    Get and set the date property.

    The property 'date' is required and is a string matching the
    regular exression 'yy-nnn' where the yy is the two digit year and
    the nnn is a three digit sequential number starting at '001' for the
    next order in the year.
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
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


def test_011_06_get_set_source(filesystem):
    """
    Get and set the source property.

    The property 'source' is required and is a string at least 1
    character long. The allowed source values are held in the 'sources'
    table in the database.
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
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


def test_011_07_get_set_subtotal(filesystem):
    """
    Get and set the subtotal property.

    The property 'subtotal' is optional and is displayed as dollars and
    cents (nnn.nn). The subtotal defaults to 0.00.
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
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


def test_011_08_get_set_shipping(filesystem):
    """
    Get and set the shipping property.

    The property 'shipping' is optional and is displayed as dollars and
    cents (nnn.nn). The shipping defaults to 0.00.
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
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


def test_011_09_get_set_discount(filesystem):
    """
    Get and set the discount property.

    The property 'discount' is optional and is displayed as dollars and
    cents (nnn.nn). The discount defaults to 0.00.
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
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


def test_011_10_get_set_tax(filesystem):
    """
    Get and set the tax property.

    The property 'tax' is optional and is displayed as dollars and
    cents (nnn.nn). The tax defaults to 0.00.
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
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


def test_011_11_get_set_total(filesystem):
    """
    Get and set the total property.

    The property 'total' is optional and is displayed as dollars and
    cents (nnn.nn). The total defaults to 0.00.
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
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


def test_011_12_get_default_property_values(filesystem):
    """
    Check the default values.

    With no properties given to constructor, the initial values should
    be the default values.
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
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


def test_011_13_set_order_from_dict(filesystem):
    """
    Check the 'set_properties' function.

    The inital values can be set from a dict input.
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
    order = Order(dbref)
    order.set_properties(order_values)
    assert order_values["record_id"] == order.get_record_id()
    assert order_values["order_number"] == order.get_order_number()
    assert order_values["source"] == order.get_source()
    assert order_values["date"] == order.get_date()
    assert order_values["subtotal"] == order.get_subtotal()
    assert order_values["tax"] == order.get_tax()
    assert order_values["shipping"] == order.get_shipping()
    assert order_values["shipping"] == order.get_shipping()
    assert order_values["discount"] == order.get_discount()
    assert order_values["remarks"] == order.get_remarks()
    db_close(dbref)


def test_011_14_get_properties_size(filesystem):
    """
    Check the size of the properties dict.

    There should be 10 members.
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
    order = Order(dbref)
    data = order.get_properties()
    assert len(data) == len(order_values)
    db_close(dbref)


def test_011_15_set_order_from_partial_dict(filesystem):
    """
    Initialize a new Order with a sparse dict of values.

    The resulting properties should mach the input values with the
    missing values replaced with default values.
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
    del order_values["source"]
    order = Order(dbref, order_values)
    assert order_values["record_id"] == order.get_record_id()
    assert order_values["order_number"] == order.get_order_number()
    assert order_values["source"] == ""
    assert order_values["date"] == order.get_date()
    assert order_values["subtotal"] == order.get_subtotal()
    assert order_values["tax"] == order.get_tax()
    assert order_values["shipping"] == order.get_shipping()
    assert order_values["discount"] == order.get_discount()
    assert order_values["total"] == order.get_total()
    assert order_values["remarks"] == order.get_remarks()
    db_close(dbref)


def test_011_16_correct_column_name(filesystem):
    """
    Check the name of the key column in the database.

    The column name must be one of None, 'record_id', or 'order_number'.
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
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


def test_011_17_get_properties_from_database(filesystem):
    """
    Access the database for the order properties.

    Add an order to the database, then access it with the
    record_id key. The actual read and write funtions are in the
    base class "Element".
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    order = Order(dbref, order_values)
    record_id = order.add()
    assert record_id == 1
    assert record_id == order.get_record_id()

    order = Order(dbref, record_id, "record_id")
    print(record_id)
    print(order.get_properties())
    assert not order.get_record_id() == order_values["record_id"]
    assert order.get_record_id() == 1
    assert order.get_order_number() == order_values["order_number"]
    assert order.get_date() == order_values["date"]
    assert order.get_source() == order_values["source"]
    assert order.get_subtotal() == order_values["subtotal"]
    assert order.get_tax() == order_values["tax"]
    assert order.get_shipping() == order_values["shipping"]
    assert order.get_discount() == order_values["discount"]
    assert order.get_total() == order_values["total"]
    assert order.get_remarks() == order_values["remarks"]

    db_close(dbref)
