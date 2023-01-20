"""
Implement a single Item in the database.

File:       item.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT, see file License
"""

from copy import deepcopy
from typing import Any

from lbk_library import Dbal, Element


class Item(Element):
    """
    Implement a single Item in the database
    """

    def __init__(self, dbref: Dbal, item_key: str | dict[str, Any] = None) -> None:
        """
        Define a single replacable Item from the car.

        The requested Item is keyed on the item_key. It can be a single
        integer value (the item_number/record_id), a dict object
        containing the properties of an Item, or None.

        If the item_key is a single integer value, the Item will be
        retrieved from the database. If item_key is a dict{} object, the
        properties of this Item are set from the dict object. If the
        item_key is not provided or the database does not contain the
        requested item, the Item is constructed from the default values.
        The item_key dict may be sparse and missing entries will be
        filled from the default values.

        Parameters:
            dbref (Dbal): reference to the database holding the element
            item_key (int | str | dict) the item number of the Item being
                constructed or an dict object of the values for an Item
                for direct insertion into the properties array.
        """
        super().__init__(dbref, "items")

        # Default values for the Item
        self.defaults: dict[str, Any] = {
            "record_id": 0,
            "part_number": "",
            "assembly": "",
            "quantity": 0,
            "condition": "",
            "installed": False,
            "remarks": "",
            "box": 0,
        }
        self.set_initial_values(deepcopy(self.defaults))
        self.clear_value_valid_flags()

        if isinstance(item_key, dict):
            # make sure there are no missing keys
            for key in self.defaults:
                if key not in item_key:
                    item_key[key] = deepcopy(self.defaults[key])

        if isinstance(item_key, (int, str)):
            item_key = self.get_properties_from_db("record_id", item_key)

        if not item_key:
            item_key = deepcopy(self.defaults)

        self.set_properties(item_key)
        self.set_initial_values(self.get_properties())
        self.clear_value_changed_flags()

    # end __init__()

    def set_properties(self, properties: dict[str, Any]) -> None:
        """
        Set the values of the Item properties array.

        Each property is validated for type and value within an
        acceptable range, with unacceptable values set to the default
        values. Properties not part of the Item are discarded.

        Parameters:
            properties (dict): holding the element values. Keys must
            match the required keys of the Item being creates/modified
        """
        if properties is not None and isinstance(properties, dict):
            # Handle the 'record_id' and 'remarks' entries
            super().set_properties(properties)
            # Handle all the other properties here
            for key in properties:
                if key == "part_number":
                    self.set_part_number(properties[key])
                elif key == "assembly":
                    self.set_assembly(properties[key])
                elif key == "quantity":
                    self.set_quantity(properties[key])
                elif key == "condition":
                    self.set_condition(properties[key])
                elif key == "installed":
                    self.set_installed(properties[key])
                elif key == "box":
                    self.set_box(properties[key])

        self.set_initial_values(self.get_properties())
        self.clear_value_changed_flags()

    # end set_properties()

    def get_part_number(self) -> str:
        """
        Get the Item's part number.

        Returns:
            (str) The Item's part number or, if None, the default value.
        """
        part_number = self._get_property("part_number")
        if part_number is None:
            part_number = self.defaults["part_number"]
        return part_number

    # end get_part_number()

    def set_part_number(self, part_number: str) -> dict[str, Any]:
        """
        Set the Item's part number.

        The part number is selected from the set of Parts existing in
        the Part database. The Part Number is required. The valid and
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
        result = self.validate.text_field(part_number, self.validate.REQUIRED, 0, 30)
        if result["valid"]:
            self._set_property("part_number", result["entry"])
        else:
            self._set_property("part_number", self.defaults["part_number"])

        self.update_property_flags("part_number", result["entry"], result["valid"])
        return result

    # end set_part_number()

    def get_assembly(self) -> str:
        """
        Get the Item's assembly code.

        Returns:
            (str) The Item's assembly code as a string or if None, the
                default value
        """
        assembly = self._get_property("assembly")
        if assembly is None:
            assembly = self.defaults["assembly"]
        return assembly

    # end get_assembly()

    def set_assembly(self, assembly: str) -> dict[str, Any]:
        """
        Set the Item's assembly code, where it appears in the car.

        The assembly code is required. The valid and changed flags are
        updated based on the result of this operation.

        Parameters:
            assembly (str) A string of text between 1 and 15 characters.
            The assembly code is forced to uppercase. If the supplied
            assembly code is not valid, the assembly code is set to the
            default value.

        Returns:
            (dict)
                ['entry'] - the updated Assembly code
                ['valid'] - (bool) True if the operation suceeded,
                    False otherwise
                ['msg'] - (str) Error message if not valid
        """
        if assembly:
            assembly = assembly.upper()
        result = self.validate.text_field(assembly, self.validate.REQUIRED, 1, 15)
        if result["valid"]:
            self._set_property("assembly", result["entry"])
        else:
            self._set_property("assembly", self.defaults["assembly"])
        self.update_property_flags("assembly", result["entry"], result["valid"])
        return result

    # end set_assembly()

    def get_quantity(self) -> int:
        """
        Get the quantity of items represented by this Item.

        Returns:
            (int) The Item's quantity (0 or more)
        """
        quantity = self._get_property("quantity")
        if quantity is None:
            quantity = self.defaults["quantity"]
        return quantity

    # end get_quantity()

    def set_quantity(self, quantity: int | float | str) -> dict[str, Any]:
        """
        Set the quantity of items represented by this Item.

        The quantity is required and mey be zero. The valid and changed
        flags are updated based on the result of this operation.

        Parameters:
            quantity (int) The quantity of items represented by this
            Item. It must be in the range of zero to 999. If the
            quantity is provided as a string or float value, it is
            converted to an integer if possible. If the supplied
            quantity is not valid, the quantity is set to 0.

        Returns:
            (dict)
                ['entry'] - the updated Quantity of the item
                ['valid'] - (bool) True if the operation suceeded,
                    False otherwise
                ['msg'] - (str) Error message if not valid
        """
        result = self.validate.integer_field(quantity, self.validate.REQUIRED, 0, 999)
        if result["valid"]:
            self._set_property("quantity", result["entry"])
        else:
            self._set_property("quantity", self.defaults["quantity"])

        self.update_property_flags("quantity", result["entry"], result["valid"])
        return result

    # end set_quantity()

    def get_condition(self) -> str:
        """
        Get the Item's condition.

        Returns:
            (str) The Item's condition as a string or if None, the
                default value.
        """
        condition = self._get_property("condition")
        if condition is None:
            condition = self.defaults["condition"]
        return condition

    # end get_condition()

    def set_condition(self, condition: str) -> dict[str, Any]:
        """
        Set the Item's condition.

        The condition is required. The item's condition is selected from
        the set of Conditions in the Condition database table. The valid
        and changed flags are updated based on the result of this
        operation.

        Parameters:
        condition (str) The Item's Condition. The condition is a
            selection from the 'condition' table in the database. If the
            supplied condition is not valid, the condition is set to the
            default value.

        Returns:
            (dict)
                ['entry'] - the updated item Condition
                ['valid'] - (bool) True if the operation suceeded, False
                    otherwise
                ['msg'] - (str) Error message if not valid
        """
        result = self.validate.text_field(condition, self.validate.REQUIRED, 1, 15)
        if result["valid"]:
            self._set_property("condition", result["entry"])
        else:
            self._set_property("condition", self.defaults["condition"])

        self.update_property_flags("condition", result["entry"], result["valid"])
        return result

    # end set_condition()

    def get_installed(self) -> bool:
        """
        Get the Item's installation status.

        Returns:
            (bool) The Item's installation status: True if the item
            has been installed on the car, False if not or if installed
            is None.
        """
        installed = self._get_property("installed")
        if installed is None:
            installed = self.defaults["installed"]
        return installed

        # end get_installed()

    def set_installed(self, installed: bool) -> dict[str, Any]:
        """
        Set the Item's installation status.

        The valid and changed flags are updated based on the result of
        this operation.

        Parameters:
            installed (bool): The Item's installation status: True if
            the item has been installed on the car, False if not.

        Returns:
            (dict)
                ['entry'] - the updated item Installed status
                ['valid'] - (bool) True if the operation suceeded,
                    False otherwise
                ['msg'] - (str) Error message if not valid
        """
        result = self.validate.boolean(installed)
        if result["valid"]:
            self._set_property("installed", result["entry"])
        else:
            self._set_property("installed", self.defaults["installed"])

        self.update_property_flags("installed", result["entry"], result["valid"])
        return result

    # end set_installed()

    def get_box(self) -> int:
        """
        Get the storage box containing this item

        Returns:
            (int) The storage box number (integer between 1 and 99 if
            stored in box, zero if not stored in a box) or, if None, 0.
        """
        box = self._get_property("box")
        if box is None:
            box = self.defaults["box"]
        return box

    # end get_box()

    def set_box(self, box: int = 0) -> dict[str, Any]:
        """
        Set the number of the storage box containing this item.

        The valid and changed flags are updated based on the result of
        this operation.

        Parameters:
            box (int) The storage box number (integer between 0 and 99),
            default is 0 (item is not stored in a box)

        Returns:
            (dict)
                ['entry'] - the updated storage box
                ['valid'] - (bool) True if the operation suceeded,
                    False otherwise
                ['msg'] - (str) Error message if not valid
        """
        result = self.validate.integer_field(box, self.validate.OPTIONAL, 0, 99)
        if result["valid"]:
            self._set_property("box", result["entry"])
        else:
            self._set_property("box", self.defaults["box"])

        self.update_property_flags("box", result["entry"], result["valid"])
        return result

    # end set_box()


# end Item
