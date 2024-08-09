"""
Implement a single Condition in the parts file.

File:       condition.py
Author:     Lorn B Kerr
Copyright:  (c) 2023, 2024 Lorn B Kerr
License:    MIT, see file License
Version:    1.0.0
"""

from copy import deepcopy
from typing import Any

from lbk_library import DataFile, Element

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}


class Condition(Element):
    """
    Implement a single Condition in the parts file.

    A condition reflects the current condition of a specific item.
    Typical conditions are new (for a new item), usable (for something
    that has been removed but is ok to reuse), and a number of others as
    listed in the parts file.
    """

    def __init__(self, parts_file: DataFile, condition_key: str = None) -> None:
        """
        Implement a single Condition.

        The requested Condition is keyed on the condition_key. It can be
        a single integer value (the record_id) or a dict object
        containing the properties of an Condition, or None.

        If the condition_key is a single integer value, the Condition
        will be retrieved from the parts file. If condition_key is a
        dict object, the properties of this Condition are set from the
        dict object. If the condition_key is not provided or the
        parts file does not contain the requested condition, The Condition
        is constructed from the default values. The condition_key dict
        may be sparse and missing entries will be filled from the
        default values.

        Parameters:
            parts_file (DataFile): reference to the parts file holding the element
            condition_key (str | dict): the record_id of the Condition
                being constructed or a dict object of the values for a
                Condition for insertion into the properties array.
        """
        super().__init__(parts_file, "conditions")

        # Default values for the Condition
        self._defaults: dict(str, Any) = {
            "record_id": 0,
            "condition": "",
        }

        self.set_initial_values(deepcopy(self._defaults))

        self.clear_value_valid_flags()

        if isinstance(condition_key, dict):
            # make sure there are no missing keys
            for key in self._defaults:
                if key not in condition_key:
                    condition_key[key] = deepcopy(self._defaults[key])

        if isinstance(condition_key, (int, str)):
            condition_key = self.get_properties_from_datafile(
                "record_id", condition_key
            )

        if not condition_key:
            condition_key = deepcopy(self._defaults)

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
            set_results = super().set_properties(properties)
            # Handle all the other properties here
            for key in properties.keys():
                if key == "condition":
                    set_results[key] = self.set_condition(properties[key])
        return set_results

    def get_condition(self) -> str:
        """
        Get the condition for this Condition object.

        Returns:
            (str) The Condition's condition or, if None, the
                default value.
        """
        condition = self._get_property("condition")
        if condition is None:
            condition = self._defaults["condition"]
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
            self._set_property("condition", self._defaults["condition"])
        self.update_property_flags("condition", result["entry"], result["valid"])
        return result
