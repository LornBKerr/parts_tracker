"""
Implements a single OrderLine in the parts file.

File:       order_line.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT, see file License
"""

from copy import deepcopy
from typing import Any

from lbk_library import DataFile, Element


class OrderLine(Element):
    """Implements single OrderLine in the parts file."""

    def __init__(self, parts_file: DataFile, order_line_key: Any = None) -> None:
        """
        Implement a single OrderLine.

        The requested OrderLine is keyed on the order_line_key. It can
        be a single integer value (the record_id), a dict object
        containing the properties of an OrderLine, or None.

        If the order_line_key is a single integer value, the OrderLine
        will be retrieved from the parts file. If order_line_key is a
        dict{} object, the properties of this OrderLine are set from
        the dict object. If the order_line_key is not provided or the
        parts file does not contain the requested item, the OrderLine is
        constructed from the default values. The order_line_key dict may
        be sparse and missing entries will be filled from the default
        values.

        Parameters:
            parts_file (DataFile): reference to the parts file holding the element
            order_line_key (int | str | dict): the specific key of the
                OrderLine being constructed or an dict object of the
                values for an OrderLine for direct insertion into the
                properties array.
        """
        super().__init__(parts_file, "order_lines")

        # Default values for the Order
        self.defaults: dict[str, Any] = {
            "record_id": 0,
            "order_number": "",
            "line": 0,
            "part_number": "",
            "cost_each": 0.0,
            "quantity": 0,
            "remarks": "",
        }

        self.set_initial_values(deepcopy(self.defaults))
        self.clear_value_valid_flags()

        if isinstance(order_line_key, dict):
            # make sure there are no missing keys
            for key in self.defaults:
                if key not in order_line_key:
                    order_line_key[key] = deepcopy(self.defaults[key])

        if isinstance(order_line_key, (int, str)):
            order_line_key = self.get_properties_from_datafile(
                "record_id", order_line_key
            )

        if not order_line_key:
            order_line_key = deepcopy(self.defaults)

        self.set_properties(order_line_key)
        self.set_initial_values(self.get_properties())
        self.clear_value_changed_flags()

    def set_properties(self, properties: dict[str, Any]) -> None:
        """
        Set the values of the OrderLine properties array.

        Each property is validated for type and value within an
        acceptable range with unacceptable values set to default values.
        Properties not part of the element are discarded.

        Parameters:
            properties (dict): the element values; keys must match the
                required keys of the element being modified, value set
                may be sparse.
        """
        if properties is not None and isinstance(properties, dict):
            super().set_properties(properties)

            for key in properties.keys():
                if key == "order_number":
                    self.set_order_number(properties[key])
                elif key == "line":
                    self.set_line(properties[key])
                elif key == "part_number":
                    self.set_part_number(properties[key])
                elif key == "cost_each":
                    self.set_cost_each(properties[key])
                elif key == "quantity":
                    self.set_quantity(properties[key])

        self.set_initial_values(deepcopy(self.get_properties()))
        self.clear_value_changed_flags()

    def get_order_number(self) -> str:
        """
        Get the order number of the Order owning this order line.

        Returns:
            (str) The Order's order number or the default empty string
            if no order number is assigned.
        """
        order_number = self._get_property("order_number")
        if order_number is None:
            order_number = self.defaults["order_number"]
        return order_number

    def set_order_number(self, order_number: str) -> dict[str, Any]:
        """
        Set the order number of the Order owning this order line.

        The valid and changed flags are updated based on the result of
        the set operation.

        Parameters:
            order_number (str): the new order number for the Order.
                Format for the order number is DD-DDD, two digit year,
                    dash, then 3 digit sequential number for each order
                    in the year.
        Returns:
            (dict)
                ['entry'] - (str) the updated Order Number
                ['valid'] - (bool) True if the operation succeeded,
                    False otherwise
                ['msg'] - (str) Error message if not valid
        """
        result = self.validate.reg_exp_field(
            order_number, r"\d\d-\d\d\d", self.validate.REQUIRED
        )
        self.set_validated_property(
            "order_number",
            result["valid"],
            result["entry"],
            self.defaults["order_number"],
        )
        self.update_property_flags("order_number", result["entry"], result["valid"])
        return result

    def get_line(self) -> int:
        """
        Get the line number for this Order Line.

        Returns:
            (int) The line number for this OrderLine, otherwise the
            default value if not assigned yet (None or blank).
        """
        line = self._get_property("line")
        if line in (None, ""):
            line = self.defaults["line"]
        return line

    def set_line(self, line: int) -> dict[str, Any]:
        """
        Set the line number for this OrderLine.

        An order may have multiple lines.The valid and changed flags
        are updated based on the result of the set operation.

        Parameters:
            line (int): the OrderLine line number, required and must be
                a positive integer 1 or greater.

        Returns:
            (dict)
                ['entry'] - (str) the updated Order Number
                ['valid'] - (bool) True if the operation succeeded,
                    False otherwise
                ['msg'] - (str) Error message if not valid
        """
        result = self.validate.integer_field(line, self.validate.REQUIRED, 1)
        self.set_validated_property(
            "line", result["valid"], result["entry"], self.defaults["line"]
        )
        self.update_property_flags("line", result["entry"], result["valid"])
        return result

    def get_part_number(self) -> str:
        """
        Get the part number for this Order Line.

        Returns:
        (str) The part number for this OrderLine, the default value if
        not assigned yet.
        """
        part_number = self._get_property("part_number")
        if part_number is None:
            part_number = self.defaults["part_number"]
        return part_number

    def set_part_number(self, part_number: str) -> dict[str, Any]:
        """
        Set the order line's part number.

        The part number is selected from the set of Parts existing in
        the Part parts file. The Part Number is required. The valid and
        changed flags are updated based on the result of the set
        operation.

        Parameters:
            part_number (str): the new part number for the Item. If the
            supplied part number is not valid, the part number is set to
            the default value.

        Returns:
            (dict)
                ['entry'] - (str) the updated Part Number
                ['valid'] - (bool) True if the operation succeeded,
                    False otherwise
                ['msg'] - (str) Error message if not valid
        """
        result = self.validate.text_field(part_number, self.validate.REQUIRED, 2, 30)
        self.set_validated_property(
            "part_number",
            result["valid"],
            result["entry"],
            self.defaults["part_number"],
        )
        self.update_property_flags("part_number", result["entry"], result["valid"])
        return result

    def get_cost_each(self) -> float:
        """
        Get the 'cost each' for the part on this Order Line.

        Returns:
            (float) The cost each for the part on this Order, otherwise
            the default value if not assigned yet.
        """
        cost_each = self._get_property("cost_each")
        if cost_each is None:
            cost_each = self.defaults["cost_each"]
        return cost_each

    def set_cost_each(self, cost_each: float | str) -> dict[str, Any]:
        """
        Set the cost each in dollars and cents.

        The valid and changed flags are updated based on the result of
        the set operation.

        Parameters:
            cost_each (float): cost of a single item. If None or empty
            string is provided, the cost_each is set to the default value.

        Returns:
            (dict)
                ['entry'] - (str) the updated cost each
                ['valid'] - (bool) True if the operation succeeded,
                    False otherwise
                ['msg'] - (str) Error message if not valid
        """
        result = self.validate.float_field(cost_each, self.validate.OPTIONAL, 0.0)
        self.set_validated_property(
            "cost_each", result["valid"], result["entry"], self.defaults["cost_each"]
        )
        if result["valid"]:
            self._set_property("cost_each", result["entry"])
        else:
            self._set_property("cost_each", self.defaults["cost_each"])
        self.update_property_flags("cost_each", result["entry"], result["valid"])
        return result

    def get_quantity(self) -> int:
        """
        Get the quantity for this Order Line.

        Returns:
            (int) The quantity for this OrderLine, the default value
                if not assigned yet.
        """
        quantity = self._get_property("quantity")
        if not quantity:
            quantity = self.defaults["quantity"]
        return quantity

    def set_quantity(self, quantity: int | str) -> dict[str, Any]:
        """
        Set the quantity for this OrderLine.

        The valid and changed flags are updated based on the result of
        the set operation.

        Parameters:
            quantity (integer) the quantity ordered on this OrderLine

        Returns:
            (dict)
                ['entry'] - (str) the updated quantity
                ['valid'] - (bool) True if the operation succeeded,
                    False otherwise
                ['msg'] - (str) Error message if not valid
        """
        result = self.validate.integer_field(quantity, self.validate.OPTIONAL, 0)
        self.set_validated_property(
            "quantity", result["valid"], result["entry"], self.defaults["quantity"]
        )
        self.update_property_flags("quantity", result["entry"], result["valid"])
        return result

    def get_line_cost(self) -> float:
        """
        Get dollar/cents cost for the quantity of parts.

        Line cost is calculated as the quantity * cost_each in cents
        (rounded to nearest cent.)

        Returns:
            (float) the calculated line cost in cents for this
            OrderLine, 0 if quantity and/or cost_each are not set or are zero
        """
        line_cost = 0
        if self._get_property("cost_each") > 0 and self._get_property("quantity") > 0:
            line_cost = self._get_property("cost_each") * self._get_property("quantity")
        return line_cost
