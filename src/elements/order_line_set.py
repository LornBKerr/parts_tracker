"""
This is a set of Order Lines in the parts file.

File:       order_line_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
Version:    1.0.0
"""

from typing import Any

from lbk_library import DataFile as PartsFile
from lbk_library import ElementSet

from .order_line import OrderLine

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}


class OrderLineSet(ElementSet):
    """Set of Order Lines in the parts file."""

    def __init__(
        self,
        parts_file: PartsFile,
        where_column: str = None,
        where_value: Any = None,
        order_by_column: str = None,
        limit: int = None,
        offset: int = None,
    ) -> None:
        """
        Build a set of OrderLines from the parts file table 'order_lines'.

        Parameters:
            parts_file (PartsFile): reference to the parts file holding the element.
            where_column (str): The key column of the table containing
                the key value to determine the elements being retrieved,
                defaults to all rows are retrieved.
            where_value (Mixed): The key value to retrieve, equired if
                where_column is set.
            order_by_column (str): one or more column names separated
                by commas to order the resulting set of elements.
            limit (int)aa; number of rows to retrieve, defaults to all.
            offset (int): row number to start retrieval, 0 based,
                defaults to row 0.
        """
        table_name = "order_lines"
        element_type = OrderLine

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
