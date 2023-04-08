"""
Implement a single Condition in the database.

File:       condition.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

from copy import deepcopy
from typing import Any

from lbk_library import Dbal, Element


class Condition(Element):
    """Implement a single Condition in the database."""

    def __init__(self, dbref: Dbal, condition_key: str = None) -> None:
        """
        Implement a single Condition.

        The requested Condition is keyed on the condition_key. It can be
        a single integer value (the record_id) or a dict object
        containing the properties of an Condition, or None.

        If the condition_key is a single integer value, the Condition
        will be retrieved from the database. If condition_key is a
        dict object, the properties of this Condition are set from the
        dict object. If the condition_key is not provided or the
        database does not contain the requested condition, The Condition
        is constructed from the default values. The condition_key dict
        may be sparse and missing entries will be filled from the
        default values.

        Parameters:
            dbref (Dbal): reference to the database holding the element
            condition_key (str | dict): the record_id of the Condition
                being constructed or an dict object of the values for a
                Condition for direct insertion into the properties array.
        """
        super().__init__(dbref, "conditions")

        # Default values for the Condition
        self.defaults: dict(str, Any) = {
            "record_id": 0,
            "condition": "",
        }

        self.set_initial_values(deepcopy(self.defaults))

        self.clear_value_valid_flags()

        if isinstance(condition_key, dict):
            # make sure there are no missing keys
            for key in self.defaults:
                if key not in condition_key:
                    condition_key[key] = deepcopy(self.defaults[key])

        if isinstance(condition_key, (int, str)):
            condition_key = self.get_properties_from_db("record_id", condition_key)

        if not condition_key:
            condition_key = deepcopy(self.defaults)

        self.set_properties(condition_key)
        self.set_initial_values(self.get_properties())
        self.clear_value_changed_flags()

    def set_properties(self, properties: dict[str, Any]) -> None:
        """
        Set the values of the Condition properties array.

        Each property is validated for type and value within an
        acceptable range, with unacceptable values set to default
        values. Properties not part of the element are discarded.

        Parameters:
            properties (dict) the element values; keys must match the
            required keys of the Condition being creates/modified
        """
        if properties is not None and isinstance(properties, dict):
            # Handle the 'record_id' and 'remarks' entries
            super().set_properties(properties)
            # Handle all the other properties here
            for key in properties.keys():
                if key == "condition":
                    self.set_condition(properties[key])

    def get_condition(self) -> str:
        """
        Get the condition for this Condition object.

        Returns:
            (str) The Condition's condition or, if None, the
                default value.
        """
        condition = self._get_property("condition")
        if condition is None:
            condition = self.defaults["condition"]
        return condition

    def set_condition(self, condition: str) -> dict[str, Any]:
        """
        Set the conditon for this Condition.

        The valid and changed flags are updated based on the result of
        the set operation.

        Parameters:
            condition ((String) the conditon for this Condition,
                required and between 1 and 31 characters

        Returns:
            (dict)
                ['entry'] - the updated storage box
                ['valid'] - (bool) True if the operation suceeded,
                    False otherwise
                ['msg'] - (str) Error message if not valid
        """
        result = self.validate.text_field(condition, self.validate.REQUIRED, 1, 31)
        if result["valid"]:
            self._set_property("condition", result["entry"])
        else:
            self._set_property("condition", self.defaults["condition"])
        self.update_property_flags("condition", result["entry"], result["valid"])
        return result
