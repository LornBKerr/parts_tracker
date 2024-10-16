"""
This is a set of Orders in the parts file.

File:       order_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
Version:    1.0.0
"""

from lbk_library import DataFile as PartsFile
from lbk_library import ElementSet

from .order import Order

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}


class OrderSet(ElementSet):
    """Set of Orders in the parts file."""

    def __init__(
        self,
        parts_file: PartsFile,
        where_column: str = None,
        where_value: str = None,
        order_by_column: str = None,
        limit: int = None,
        offset: int = None,
    ):
        """
        Build a set of Orders from the parts file table 'orders'.

        Parameters:
            parts_file (PartsFile): reference to the parts file holding the Orders.
            where_column (str): The key column of the table containing
                the key value to determine the elements being retrieved,
                default is all rows are retrieved.
        where_value (stry): The key value to retrieve. Required if
            where_column is set.
        order_by_column (str): one or more column names separated by
            commas to order the resulting set of elements.
        limit (int): number of rows to retrieve, defaults to all.
        offset (intr): row number to start retrieval, 0 based, defaults
            to row 0.
        """
        table_name = "orders"  # The parts file table for this element
        element_type = Order

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
