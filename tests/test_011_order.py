"""
Test the Order class.

File:       test_011_order.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file License
Version:    1.0.0
"""

import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library import Element
from lbk_library.testing_support import datafile_close, datafile_create, filesystem
from test_data import order_value_set

from elements import Order
from pages import table_definition

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}

parts_filename = "parts_test.parts"
order_values = {
    "record_id": order_value_set[0][0],
    "order_number": order_value_set[0][1],
    "date": "2006-08-22",
    "source": order_value_set[0][3],
    "remarks": order_value_set[0][4],
    "subtotal": order_value_set[0][5],
    "shipping": order_value_set[0][6],
    "discount": order_value_set[0][7],
    "tax": order_value_set[0][8],
    "total": order_value_set[0][9],
}


def base_setup(tmp_path):
    base_directory = filesystem(tmp_path)
    filename = base_directory + "/" + parts_filename
    parts_file = datafile_create(filename, table_definition)
    order = Order(parts_file)
    return (order, parts_file)


def test_011_01_constr(tmp_path):
    """
    Order Extends Element.

    Check the types of class variables and default values.
    """
    order, parts_file = base_setup(tmp_path)
    assert isinstance(order, Order)
    assert isinstance(order, Element)
    # default values.
    assert isinstance(order._defaults, dict)
    assert len(order._defaults) == 10
    assert order._defaults["record_id"] == 0
    assert order._defaults["order_number"] == ""
    assert order._defaults["date"] == ""
    assert order._defaults["source"] == 0
    assert order._defaults["subtotal"] == 0.0
    assert order._defaults["shipping"] == 0.0
    assert order._defaults["tax"] == 0.0
    assert order._defaults["total"] == 0.0
    assert order._defaults["remarks"] == ""
    datafile_close(parts_file)


def test_011_02_get_table(tmp_path):
    order, parts_file = base_setup(tmp_path)
    assert order.get_table() == "orders"
    datafile_close(parts_file)


def test_011_03_get_parts_file(tmp_path):
    order, parts_file = base_setup(tmp_path)
    assert order.get_datafile() == parts_file
    datafile_close(parts_file)


def test_011_04_get_set_order_number(tmp_path):
    """
    Get and set the order_number property.

    The property 'order_number' is required and is a string matching the
    regular exression 'yy-nnn' where the yy is the two digit year and
    the nnn is a three digit sequential number starting at '001' for the
    next order in the year.
    """
    order, parts_file = base_setup(tmp_path)
    defaults = order.get_initial_values()
    order._set_property("order_number", order_values["order_number"])
    assert order_values["order_number"] == order.get_order_number()
    order._set_property("order_number", None)
    assert order._defaults["order_number"] == order.get_order_number()
    result = order.set_order_number(None)
    assert not result["valid"]
    assert result["entry"] == None
    result = order.set_order_number(order_values["order_number"])
    assert result["valid"]
    assert result["entry"] == order_values["order_number"]
    assert result["entry"] == order.get_order_number()
    datafile_close(parts_file)


def test_011_05_get_set_date(tmp_path):
    """
    Get and set the date property.

    The property 'date' is required and is a string matching the
    regular expression 'yy-nnn' where the yy is the two digit year and
    the nnn is a three digit sequential number starting at '001' for the
    next order in the year.
    """
    order, parts_file = base_setup(tmp_path)
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
    result = order.set_date("2006-08-22")
    assert result["valid"]
    assert result["entry"] == "08/22/2006"
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
    datafile_close(parts_file)


def test_011_06_get_set_source(tmp_path):
    """
    Get and set the source property.

    The property 'source' is required and is the record_id of a Source
    entry in the datafile, a small intege. The allowed source values
    are held in the 'sources' table in the datafile.
    """
    order, parts_file = base_setup(tmp_path)
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
    datafile_close(parts_file)


def test_011_07_get_set_subtotal(tmp_path):
    """
    Get and set the subtotal property.

    The property 'subtotal' is optional and is displayed as dollars and
    cents (nnn.nn). The subtotal defaults to 0.00.
    """
    order, parts_file = base_setup(tmp_path)
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
    datafile_close(parts_file)


def test_011_08_get_set_shipping(tmp_path):
    """
    Get and set the shipping property.

    The property 'shipping' is optional and is displayed as dollars and
    cents (nnn.nn). The shipping defaults to 0.00.
    """
    order, parts_file = base_setup(tmp_path)
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
    datafile_close(parts_file)


def test_011_09_get_set_discount(tmp_path):
    """
    Get and set the discount property.

    The property 'discount' is optional and is displayed as dollars and
    cents (nnn.nn). The discount defaults to 0.00.
    """
    order, parts_file = base_setup(tmp_path)
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
    datafile_close(parts_file)


def test_011_10_get_set_tax(tmp_path):
    """
    Get and set the tax property.

    The property 'tax' is optional and is displayed as dollars and
    cents (nnn.nn). The tax defaults to 0.00.
    """
    order, parts_file = base_setup(tmp_path)
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
    datafile_close(parts_file)


def test_011_11_get_set_total(tmp_path):
    """
    Get and set the total property.

    The property 'total' is optional and is displayed as dollars and
    cents (nnn.nn). The total defaults to 0.00.
    """
    order, parts_file = base_setup(tmp_path)
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
    datafile_close(parts_file)


def test_011_12_get_default_property_values(tmp_path):
    """
    Check the default values.

    With no properties given to constructor, the initial values should
    be the default values.
    """
    order, parts_file = base_setup(tmp_path)
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
    datafile_close(parts_file)


def test_011_13_set_order_from_dict(tmp_path):
    """
    Check the 'set_properties' function.

    The inital values can be set from a dict input.
    """
    order, parts_file = base_setup(tmp_path)
    order.set_properties(order_values)
    assert order.get_record_id() == order_values["record_id"]
    assert order.get_order_number() == order_values["order_number"]
    assert order.get_source() == order_values["source"]
    assert order.get_date() == "08/22/2006"
    assert order.get_subtotal() == order_values["subtotal"]
    assert order.get_tax() == order_values["tax"]
    assert order.get_shipping() == order_values["shipping"]
    assert order.get_shipping() == order_values["shipping"]
    assert order.get_discount() == order_values["discount"]
    assert order.get_remarks() == order_values["remarks"]
    datafile_close(parts_file)


def test_011_14_get_properties_size(tmp_path):
    """
    Check the size of the properties dict.

    There should be 10 members.
    """
    order, parts_file = base_setup(tmp_path)
    data = order.get_properties()
    assert len(data) == len(order_values)
    datafile_close(parts_file)


def test_011_15_set_order_from_partial_dict(tmp_path):
    """
    Initialize a new Order with a sparse dict of values.

    The resulting properties should mach the input values with the
    missing values replaced with default values.
    """
    order, parts_file = base_setup(tmp_path)
    del order_values["source"]
    order = Order(parts_file, order_values)
    assert order.get_record_id() == order_values["record_id"]
    assert order.get_order_number() == order_values["order_number"]
    assert order.get_source() == 0
    assert order.get_date() == "08/22/2006"
    assert order.get_subtotal() == order_values["subtotal"]
    assert order.get_tax() == order_values["tax"]
    assert order.get_shipping() == order_values["shipping"]
    assert order.get_shipping() == order_values["shipping"]
    assert order.get_discount() == order_values["discount"]
    assert order.get_remarks() == order_values["remarks"]
    datafile_close(parts_file)


def test_011_16_correct_column_name(tmp_path):
    """
    Check the name of the key column in the database.

    The column name must be one of None, 'record_id', or 'order_number'.
    """
    order, parts_file = base_setup(tmp_path)
    order = Order(parts_file, None, "a_column")
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
    datafile_close(parts_file)


def test_011_17_get_properties_from_database(tmp_path):
    """
    Access the database for the order properties.

    Add an order to the database, then access it with the
    record_id key. The actual read and write funtions are in the
    base class "Element".
    """
    order, parts_file = base_setup(tmp_path)
    order = Order(parts_file, order_values)
    record_id = order.add()
    assert record_id == 1
    assert record_id == order.get_record_id()

    order = Order(parts_file, record_id, "record_id")
    print(record_id)
    print(order.get_properties())
    assert not order.get_record_id() == order_values["record_id"]
    assert order.get_record_id() == 1
    assert order.get_order_number() == order_values["order_number"]
    assert order.get_date() == "08/22/2006"
    assert order.get_source() == order_values["source"]
    assert order.get_subtotal() == order_values["subtotal"]
    assert order.get_tax() == order_values["tax"]
    assert order.get_shipping() == order_values["shipping"]
    assert order.get_discount() == order_values["discount"]
    assert order.get_total() == order_values["total"]
    assert order.get_remarks() == order_values["remarks"]

    datafile_close(parts_file)
