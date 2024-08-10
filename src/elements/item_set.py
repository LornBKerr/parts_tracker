"""
This is a set of Items in the parts file.

File:       item_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT, see file License
Version:    1.0.0
"""

from lbk_library import DataFile, ElementSet

from .item import Item

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}


class ItemSet(ElementSet):
    """Provides set of Items from parts file table 'items'."""

    def __init__(
        self,
        parts_file: DataFile,
        where_column: str = None,
        where_value: str = None,
        order_by_column: str = None,
        limit: int = None,  # No limit
        offset: int = None,
    ) -> None:
        """
        Build a set of Items from the parts file table 'items'.

        Parameters:
            parts_file (DataFile): the dababase instance to use.
            where_column (str): The key column of the table containing
                the key value to determine the elements being retrieved.
                If None, all rows are retrieved.
            where_value (str): The key value to retrieve. Required if
                where_column is set.
            order_by_column (str): column of the 'item' table to set the
                order of the item_set.
            limit (int): number of rows to retrieve, defaults to all.
            offset (int): row number to start retrieval, 0 based,
                defaults to row 0.
        """
        table_name = "items"  # The parts file table for this element
        element_type = Item

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
