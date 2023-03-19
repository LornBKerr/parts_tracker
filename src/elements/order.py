"""
Implement a single Order in the database.

File:       order.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file License
"""


import re
from copy import deepcopy
from typing import Any

from lbk_library import Dbal, Element

# from .order_line_set import OrderLineSet


class Order(Element):
    """Implement a single Order in the database."""

    def __init__(
        self, dbref: Dbal, order_key: int | dict[str, Any] = None, column: str = None
    ) -> None:
        """
        Initialize a single Order.

        The 'column' can be set to None, "record_id", or "order_number".
        If not one of these three choices, both 'order_key' and 'column'
        are set to "None" and an Order with default values  is
        constructed. The defaults are: string values are set to empty
        string, numeric values are set to 0, and logical values are
        set to False.

        If 'order_key' is not given, the 'column' is ignored and an
        empty Order is constructed with all properties set to the
        default values

        If order_key is a dict{} object, the properties of this Order
        are set from the dict object.

        If 'order_key' is given as a single value, it must be either a
        'record_id' or an 'order_number' as indicated by 'column'. If
        'column' is not given, 'record_id' is the default. The Order
        will be constructed from the database for the specific value
        given by 'column' and 'record_id'

        Parameters:
            dbref (Dbal): reference to the database holding the element.
            order_key (int | dict[str, Any]): the specific key of the
                Order being constructed or an dict object of the values
                for an Order for direct insertion into the properties
                array. If a specific key, must be either an record_id
                or order_number value and must be consistent with the
                type given by the column name.
            column (str): Either 'record_id' or 'order_number',
                default is None. Column name and order_key value must
                be consistent.
        """
        super().__init__(dbref, "orders")

        # Default values for the Order
        self.defaults: dict[str, Any] = {
            "record_id": 0,
            "order_number": "",
            "date": "",
            "source": "",
            "subtotal": 0.00,
            "shipping": 0.00,
            "discount": 0.00,
            "tax": 0.00,
            "total": 0.00,
            "remarks": "",
        }

        self.set_initial_values(deepcopy(self.defaults))
        self.clear_value_valid_flags()

        if isinstance(order_key, dict):
            # make sure there are no missing keys
            for key in self.defaults:
                if key not in order_key:
                    order_key[key] = deepcopy(self.defaults[key])

        if column is None:
            column = "order_number"

        if column not in ("record_id", "order_number"):
            order_key = None
            column = None

        if isinstance(order_key, (int, str)):
            order_key = self.get_properties_from_db(column, order_key)

        if not order_key:
            order_key = deepcopy(self.defaults)

        self.set_properties(order_key)
        self.set_initial_values(self.get_properties())
        #        self.order_lines = OrderLineSet(
        #            self.get_dbref(), "order_number", self.get_order_number()
        #        )
        self.clear_value_changed_flags()

    def set_properties(self, properties: dict) -> None:
        """
        Set the values of the Order properties array.

        Each property is validated for type and value within an
        acceptable range, with unacceptable values set to the default
        settings. Properties not part of the element are discarded.

        Parameters:
            properties (dict) holding the element values. Keys must
            match the required keys of the element being modified,
            properties may be sparse.
        """
        if properties is not None and isinstance(properties, dict):
            super().set_properties(properties)

            for key in properties.keys():
                if key == "order_number":
                    self.set_order_number(properties[key])
                elif key == "date":
                    self.set_date(properties[key])
                elif key == "source":
                    self.set_source(properties[key])
                elif key == "subtotal":
                    self.set_subtotal(properties[key])
                elif key == "shipping":
                    self.set_shipping(properties[key])
                elif key == "discount":
                    self.set_discount(properties[key])
                elif key == "tax":
                    self.set_tax(properties[key])
                elif key == "total":
                    self.set_total(properties[key])

        self.set_initial_values(deepcopy(self.get_properties()))
        self.clear_value_changed_flags()

    def get_order_number(self) -> str:
        """
        Get the Order's order number.

        Returns:
            (str) The Order's order number as a string or, if None,
                an empty string
        """
        order_number = self._get_property("order_number")
        if order_number is None:
            order_number = self.defaults["order_number"]
        return order_number

    def set_order_number(self, order_number: str) -> dict[str, Any]:
        """
        Set the Order's order_number.

        The valid and changed flags are updated based on the result of
        the set operation.

        Parameters:
            order_number (int): the new order number for the Order.
            Format for the order number is DD-DDD, two digit year, dash,
            then 3 digit sequential number for each order in the year.

        Returns:
            (dict)
                ['entry'] - (str) the updated order number
                ['valid'] - (bool) True if the operation succeeded,
                    False otherwise
                ['msg'] - (str) Error message if not valid
        """
        result = self.validate.reg_exp_field(
            order_number, r"\d\d\-\d\d\d", self.validate.REQUIRED
        )
        if result["valid"]:
            self._set_property("order_number", result["entry"])
        else:
            self._set_property("order_number", self.defaults["order_number"])
        self.update_property_flags("order_number", result["entry"], result["valid"])
        return result

    def get_date(self) -> str:
        """
        Get the date of this Order.

        The date is converted to MM/DD/YYYY if necessary.

        Returns:
            (str) the date in 'mm/dd/yyyy' format or, if invalid, an
                empty string
        """
        date = self._get_property("date")

        if date:
            # date stored as YYYY-MM-DD, displayed as MM/DD/YYYY
            if re.match(r"\d\d\d\d-\d\d-\d\d", date):
                date_array = date.split("-")
                date = date_array[1] + "/" + date_array[2] + "/" + date_array[0]

        result = self.validate.date_field(date, self.validate.REQUIRED)
        if result["valid"]:
            date = result["entry"]
        else:
            date = self.defaults["date"]

        return date

    def set_date(self, date: str) -> dict[str, Any]:
        """
        Set the date for this Order.

        The valid and changed flags are updated based on the result of
        the set operation.

        Parameters:
            date (str): the date of this order. The date may be formatted
                 as yyyy-mm-dd or mm/dd/yyyy.

        Returns:
            (dict)
                ['entry'] - (str) the updated date.
                ['valid'] - (bool) True if the operation succeeded,
                    False otherwise.
                ['msg'] - (str) Error message if not valid.
        """
        if date and re.match(r"\d\d\d\d-\d\d-\d\d", date):
            date_array = date.split("-")
            date = date_array[1] + "/" + date_array[2] + "/" + date_array[0]

        result = self.validate.date_field(date, self.validate.REQUIRED)
        if result["valid"]:
            self._set_property("date", result["entry"])
        else:
            self._set_property("date", self.defaults["date"])
        self.update_property_flags("date", result["entry"], result["valid"])
        return result

    def get_source(self) -> str:
        """
        Get the source (vendor) of this Order.

        Returns:
            (str) the source if assigned, otherwise the default
                empty string.
        """
        source = self._get_property("source")
        if source is None:
            source = self.defaults["source"]
        return source

    def set_source(self, source) -> dict[str, Any]:
        """
        Set the source (vendor) for this Order.

        The valid and changed flags are updated based on the result of
        the set operation.

        Parameters:
            source (str): the source for this order, may be None if no
                source is yet assigned.

        Returns:
            (dict)
                ['entry'] - (str) the updated source.
                ['valid'] - (bool) True if the operation succeeded,
                    False otherwise.
                ['msg'] - (str) Error message if not valid.
        """
        result = self.validate.text_field(source, self.validate.REQUIRED, 1, 256)
        if result["valid"]:
            self._set_property("source", result["entry"])
        else:
            self._set_property("source", self.defaults["source"])
        self.update_property_flags("source", result["entry"], result["valid"])
        return result

    def get_subtotal(self) -> float:
        """
        Get the subtotal of the line cost for the lines on this Order.

        Returns:
            (float) The subtotal on this Order, otherwise the default
                value if not assigned yet.
        """
        subtotal = self._get_property("subtotal")
        if subtotal in (None, ""):
            subtotal = self.defaults["subtotal"]
        return subtotal

    def set_subtotal(self, subtotal: float | str) -> dict[str, Any]:
        """
        Set the subtotal of the lines on this Order.

        The valid  and changed flags are updated based on the result of
        the set operation.

        Paramters:
            subtotal (float): the sum of the order lines. Must be 0 or
                greater. If None or empty string is provided, the
                subtotal is set to the default value 0.0.

        Returns:
            (dict)
                ['entry'] - (str) the updated subtotal.
                ['valid'] - (bool) True if the operation succeeded,
                    False otherwise.
                ['msg'] - (str) Error message if not valid.
        """
        if subtotal in (None, ""):
            subtotal = self.defaults["subtotal"]
        else:
            subtotal = float(subtotal)
        result = self.validate.float_field(subtotal, self.validate.OPTIONAL, 0.0)
        if result["valid"]:
            self._set_property("subtotal", result["entry"])
        else:
            self._set_property("subtotal", self.defaults["subtotal"])
        self.update_property_flags("subtotal", result["entry"], result["valid"])
        return result

    def get_shipping(self) -> float:
        """
        Get the shipping cost on this Order.

        Returns:
            (float) The shipping on this Order in dollars and cents,
            otherwise the default value if not assigned yet.
        """
        shipping = self._get_property("shipping")
        if shipping in (None, ""):
            shipping = self.defaults["shipping"]
        return shipping

    def set_shipping(self, shipping: str | float) -> dict[str, Any]:
        """
        Set the shipping of the lines on this Order.

        The valid and changed flags are updated based on the result of
        the set operation.

        Parameters:
            shipping (float) the shipping cost, if any. Must be 0 or
                greater. If None or empty string is provided, the
                shipping is set to the default value 0.0.
        Returns:
            (dict)
                ['entry'] - (str) the updated shipping.
                ['valid'] - (bool) True if the operation succeeded,
                    False otherwise.
                ['msg'] - (str) Error message if not valid.
        """
        if shipping in (None, ""):
            shipping = self.defaults["shipping"]
        else:
            shipping = float(shipping)

        result = self.validate.float_field(shipping, self.validate.REQUIRED, 0.0)
        if result["valid"]:
            self._set_property("shipping", result["entry"])
        else:
            self._set_property("shipping", self.defaults["shipping"])
        self.update_property_flags("shipping", result["entry"], result["valid"])
        return result

    def get_discount(self) -> float:
        """
        Get the discount on this Order.

        Return:
            (float) The discount on this Order, or the default value
                if not assigned yet.
        """
        discount = self._get_property("discount")
        if discount in (None, ""):
            discount = self.defaults["discount"]
        return discount

    def set_discount(self, discount: str | float) -> dict[str, Any]:
        """
        Set the discount of the lines on this Order.

        The valid and changed flags are updated based on the result of
        the set operation.

        Parameters:
            discount (float) the discount on this order. If None or
                empty string is provided, the discount is set to the
                default value. Discount must be zero or negative.

        Returns:
            (dict)
                ['entry'] - (str) the updated discount.
                ['valid'] - (bool) True if the operation succeeded,
                    False otherwise.
                ['msg'] - (str) Error message if not valid.
        """
        if discount in (None, ""):
            discount = self.defaults["discount"]
        else:
            discount = float(discount)

        result = self.validate.float_field(
            discount, self.validate.REQUIRED, -10000.0, 0
        )
        if result["valid"]:
            self._set_property("discount", result["entry"])
        else:
            self._set_property("discount", self.defaults["discount"])
        self.update_property_flags("discount", result["entry"], result["valid"])
        return result

    def get_tax(self) -> float:
        """
        Get the tax on this Order.

        Returns:
            (int) The tax on this Order, otherwise the default value
                if not assigned yet.
        """
        tax = self._get_property("tax")
        if tax in (None, ""):
            tax = self.defaults["tax"]
        return tax

    def set_tax(self, tax: str | float) -> dict[str, Any]:
        """
        Set the tax of the lines on this Order.

        The valid and changed flags are updated based on the result of the set operation.

        Parameters:
            tax (float)the tax on this order, if any. If None or empty
                string is provided, the tax is set to the default value.

        Returns:
            (dict)
                ['entry'] - (str) the updated discount.
                ['valid'] - (bool) True if the operation succeeded,
                    False otherwise.
                ['msg'] - (str) Error message if not valid.
        """
        if tax in (None, ""):
            tax = self.defaults["tax"]
        else:
            tax = float(tax)
        result = self.validate.float_field(tax, self.validate.REQUIRED, 0.0)
        if result["valid"]:
            self._set_property("tax", result["entry"])
        else:
            self._set_property("tax", self.defaults["tax"])
        self.update_property_flags("tax", result["entry"], result["valid"])
        return result

    def get_total(self) -> float:
        """
        Get the total on this Order.

        Returns:
        (float) The total on this Order in dollars and cents, otherwise
            the default value if not assigned yet.
        """
        total = self._get_property("total")
        if total in (None, ""):
            total = self.defaults["total"]
        return total

    def set_total(self, total: str | float) -> dict[str, Any]:
        """
        Set the total of the lines on this Order.

        The valid and changed flags are updated based on the result of the set operation.

        Parameters:
            total (float) the total cost (sum of the subtotal, shipping,
            tax, and discount) for this order. If None or empty string
            is provided, the total is set to the default value.

        Returns:
            (dict)
                ['entry'] - (str) the updated total.
                ['valid'] - (bool) True if the operation succeeded,
                    False otherwise.
                ['msg'] - (str) Error message if not valid.
        """
        if total in (None, ""):
            total = self.defaults["total"]
        else:
            total = float(total)
        result = self.validate.float_field(total, self.validate.REQUIRED, 0.0)
        if result["valid"]:
            self._set_property("total", result["entry"])
        else:
            self._set_property("total", self.defaults["total"])
        self.update_property_flags("total", result["entry"], result["valid"])
        return result
