"""
Implement a single Part in the database.

File:       part.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file License
"""


from copy import deepcopy
from typing import Any

from lbk_library import Dbal, Element

from .item_set import ItemSet


class Part(Element):
    """Implement a single Part in the database."""

    def __init__(self, dbref: Dbal, part_key: Any = None, column: str = None) -> None:
        """
        Initialize a single Part.

        The 'column' can be set to None, "record_id", or "part_number".
        If not one of these three choices, both 'part_key' and 'column'
        are set to "None" and a Part with default values is constructed.
        The general defaults are: string values are set to
        empty string, numeric values are set to 0, and logical values
        are set to False.
        If 'part_key' is not given, the 'column' is ignored and an empty
        Part is constructed with all properties set to default values.

        If part_key is a dict{} object, the properties of this Part are
        set from the dict object.

        If 'part_key' is given as a single value, it must be either an
        'record_id' or an 'part_number' as indicated by 'column'. If
        'column' is not given, 'record_id' is the default. The Part
        will be constructed from the database for the specific value
        given by 'column' and 'part_key'

        Parameters:
            dbref (Dbal): reference to the database holding the element
            part_key (Mixed): the specific key of the Part being
                constructed or an dict object of the values for an Part
                for direct insertion into the properties array.
                If a specific key, it must be either an record_id or
                part_number value and must be consistent with the type
                given by the column name.
            column (String): Either 'record_id' or 'part_number',
                default is None. Column name and part value must be
                consistent.
        """
        super().__init__(dbref, "parts")

        # Default values for the Part
        self.defaults: dict[str, Any] = {
            "record_id": 0,
            "part_number": "",
            "source": "",
            "description": "",
            "remarks": "",
        }

        self.set_initial_values(deepcopy(self.defaults))
        self.clear_value_valid_flags()

        if isinstance(part_key, dict):
            # make sure there are no missing keys
            for key in self.defaults:
                if key not in part_key:
                    part_key[key] = deepcopy(self.defaults[key])

        if column is None:
            column = "record_id"

        if column not in ("record_id", "part_number"):
            part_key = None
            column = None

        if isinstance(part_key, (int, str)):
            part_key = self.get_properties_from_db(column, part_key)

        if not part_key:
            part_key = deepcopy(self.defaults)

        self.set_properties(part_key)
        self.set_initial_values(self.get_properties())
        self.clear_value_changed_flags()

    def set_properties(self, properties: dict[str, Any]) -> None:
        """
        Set the values of the Part properties array.

        Each property is validated for type and value within an acceptable
        range, with unacceptable values set to default values. Properties
        not part of the element are discarded.

        Parameters:
            properties (dict): holding the element values. Keys must
            match the required keys of the element being modified,
            properties may be sparse.
        """
        if properties is not None and isinstance(properties, dict):
            super().set_properties(properties)

            for key in properties.keys():
                if key == "part_number":
                    self.set_part_number(properties[key])
                elif key == "source":
                    self.set_source(properties[key])
                elif key == "description":
                    self.set_description(properties[key])

        self.set_initial_values(self.get_properties())
        self.clear_value_changed_flags()

    def get_part_number(self) -> str:
        """
        Get the Part's part number.

        Return:
            (str) The part number as a string or, if None, an
                empty string.
        """
        part_number = self._get_property("part_number")
        if part_number is None:
            part_number = self.defaults["part_number"]
        return part_number

    def set_part_number(self, part_number: str) -> dict[str, Any]:
        """
        Set the Part's part number.

        The part number is required and must be between 2 and 30
        characters long. The valid and changed flags are updated based
        on the result of the set operation.

        Parameters:
            part_number (str): the new part number for the Part. If the
                supplied part number is not valid, the part number is
                set to the default empty string.

        Returns:
            (dict) {
                ['entry'] (str) the updated Part Number
                ['valid'] (bool) True if the operation suceeded,
                    false otherwise
                ['msg'] (Str) Error message if not valid
            }
        """
        result = self.validate.text_field(part_number, self.validate.REQUIRED, 2, 30)
        if result["valid"]:
            self._set_property("part_number", result["entry"])
        else:
            self._set_property("part_number", self.defaults["part_number"])

        self.update_property_flags("part_number", result["entry"], result["valid"])
        return result

    def get_source(self) -> str:
        """
        Get the Part's source.

        Return:
            (str) The Part's source or, if None, an empty string
        """
        source = self._get_property("source")
        if source is None:
            source = self.defaults["source"]
        return source

    def set_source(self, source: str) -> dict[str, Any]:
        """
        Set the Part's source.

        The source is selected from a drop down box of the sources
        (venders). The valid and changed flags are updated based on the
        result of the set operation.

        Parameters:
            source (str): the new source for the Part. If the supplied
                source is not valid, the source is set to an empty string.

        Returns:
            (dict) {
                ['entry'] (str) the updated Source
                ['valid'] (bool) True if the operation suceeded,
                    false otherwise
                ['msg'] (Str) Error message if not valid
            }
        """
        result = self.validate.text_field(source, self.validate.REQUIRED)
        if result["valid"]:
            self._set_property("source", result["entry"])
        else:
            self._set_property("source", self.defaults["source"])
        self.update_property_flags("source", result["entry"], result["valid"])
        return result

    def get_description(self) -> str:
        """
        Get the Part's desciption.

        Return:
            (str) The Part's description or, if None, an empty string.
        """
        description = self._get_property("description")
        if description is None:
            description = self.defaults["description"]
        return description

    def set_description(self, description: str) -> dict[str, Any]:
        """
        Set the Part's description.

        The description is a text field of up to 255 characters.
        The valid and changed flags are updated based on the result of
        the set operation.

        Parameters:
            description (str): the description for the Part. If the
            supplied description is not valid, the description is set to
            the empty string

        Returns:
            (dict) {
                ['entry'] (str) the updated Description
                ['valid'] (bool) True if the operation suceeded,
                    false otherwise
                ['msg'] (Str) Error message if not valid
            }
        """
        result = self.validate.text_field(description, self.validate.REQUIRED)
        if result["valid"]:
            self._set_property("description", result["entry"])
        else:
            self._set_property("description", self.defaults["description"])
        self.update_property_flags("description", result["entry"], result["valid"])
        return result

    def get_total_quantity(self) -> int:
        """
        Get the total quantity for this part number from the 'items' table.

        The items table is searched for the items using this part number
        then the quantities for each of these items is summed and returned.

        Return (integer) the total quantity of this part number used.
        """
        item_set = ItemSet(
            self.get_dbref(),
            "part_number",
            self.get_part_number(),
            "record_id",
        )
        quantity = 0
        for item in item_set:
            quantity += item.get_quantity()
        return quantity
