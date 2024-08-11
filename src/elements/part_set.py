"""
This is a set of Partss in the parts file.

File:       part_setl.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
Version:    1.0.0
"""

from typing import Any

from lbk_library import DataFile, ElementSet

from .part import Part

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}


class PartSet(ElementSet):
    """Provides set of Parts in the parts file."""

    def __init__(
        self,
        parts_file: DataFile,
        where_column: str = None,
        where_value: Any = None,
        order_by_column: str = None,
        limit: int = None,
        offset: int = None,
    ) -> None:
        """
        Build a set of Parts from the parts file table 'parts'.

        Parameters:
            parts_file (DataFile): reference to the parts file holding the parts
            where_column (String): The key column of the table
                containing the key value to determine the elements being
                retrieved. Default is all rows are retrieved.
        where_value (Mixed) The key value to retrieve. Required if
            where_column is set.
        order_by_column (String) one or more column names separated by
            commas to order the resulting set of elements.
        limit (Integer) number of rows to retrieve, defaults to all.
        offset (Integer) row number to start retrieval, 0 based,
            defaults to row 0.
        """
        table_name = "parts"  # The parts file table for this element
        element_type = Part
        super().__init__(
            parts_file,
            table_name,
            element_type,
            where_column,
            where_value,
            order_by_column,
            limit,
            offset,
        )
