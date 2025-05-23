"""
Implement a single Source in the parts file.

File:       source.py
Author:     Lorn B Kerr
Copyright:  (c) 2023, 2024 Lorn B Kerr
License:    MIT, see file License
Version:    1.0.0
"""

from copy import deepcopy
from typing import Any

from lbk_library import DataFile as PartsFile
from lbk_library import Element

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}


class Source(Element):
    """
    Implement a single Source in the parts file.

    A source is where a part is bought.
    """

    def __init__(self, parts_file: PartsFile, source_key: str = None) -> None:
        """
        Build a single Source.

        The requested Source is keyed on the source_key. It can be
        a single integer value (the record_id) or a dict object
        containing the properties of an Source, or None.

        If the source_key is a single integer value, the Source
        will be retrieved from the parts file. If source_key is a
        dict object, the properties of this Source are set from the
        dict object. If the source_key is not provided or the
        parts file does not contain the requested source, The Source
        is constructed from the default values. The source_key dict
        may be sparse and missing entries will be filled from the
        default values.

        Parameters:
            parts_file (PartsFile): reference to the parts file holding
                the element.
            source_key (str | dict): the record_id of the Source
                being constructed or an dict object of the values for a
                Source for direct insertion into the properties array.
        """
        super().__init__(parts_file, "sources")

        # Default values for the Source
        self._defaults: dict(str, Any) = {
            "record_id": 0,
            "source": "",
        }

        self.set_initial_values(deepcopy(self._defaults))
        self.clear_value_valid_flags()

        if isinstance(source_key, dict):
            # make sure there are no missing keys
            for key in self._defaults:
                if key not in source_key:
                    source_key[key] = deepcopy(self._defaults[key])

        if isinstance(source_key, (int, str)):
            source_key = self.get_properties_from_datafile("record_id", source_key)

        if not source_key:
            source_key = deepcopy(self._defaults)

        self.set_properties(source_key)
        self.set_initial_values(self.get_properties())
        self.clear_value_changed_flags()

    def set_properties(self, properties: dict[str, Any]) -> None:
        """
        Set the values of the Source properties array.

        Each property is validated for type and value within an
        acceptable range, with unacceptable values set to default
        values. Properties not part of the element are discarded.

        Parameteres:
            properties (dict) the element values; keys must match the
            required keys of the Source being creates/modified
        """
        if properties is not None and isinstance(properties, dict):
            # Handle the 'record_id' and 'remarks' entries
            set_results = super().set_properties(properties)
            # Handle all the other properties here
            for key in properties.keys():
                if key == "source":
                    set_results[key] = self.set_source(properties[key])
        return set_results

    def get_source(self) -> str:
        """
        Get the source for this Source object.

        Returns:
            (str) The Source's source or, if None, the
                default value.
        """
        source = self._get_property("source")
        if source is None:
            source = self._defaults["source"]
        return source

    def set_source(self, source: str) -> dict[str, Any]:
        """
        Set the source for this Source.

        The valid and changed flags are updated based on the result of
        the set operation.

        Parameters:
            source ((String) thesource for this Source,
                required and between 1 and 31 characters

        Returns:
            (dict)
                ['entry'] - the updated source
                ['valid'] - (bool) True if the operation suceeded,
                    False otherwise
                ['msg'] - (str) Error message if not valid
        """
        result = self.validate.text_field(source, self.validate.REQUIRED, 1, 31)
        if result["valid"]:
            self._set_property("source", result["entry"])
        else:
            self._set_property("source", self._defaults["source"])
        self.update_property_flags("source", result["entry"], result["valid"])
        return result
