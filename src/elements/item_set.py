"""
This is a set of Items in the database.

File:       item_setl.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT, see file License
"""

from lbk_library import Dbal, ElementSet

from . import Item

class ItemSet(ElementSet):
    """
    Provides a set of Items from the database table 'items'.
    """
    def __init__(
        self,
        dbref: Dbal,
        where_column: str = None,
        where_value: str = None,
        order_by_column: str = None,
        limit: int = None,    # No limit
        offset: int = None,
    ) -> None:
        """
        Builds a set of Items from the database table 'items'.

        Parameters:
            dbref (Dbal): the dababase instance to use.
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
        table_name = "items"  # The database table for this element
        element_type = Item

        super().__init__(
            dbref,
            table_name,
            element_type,
            where_column,
            where_value,
            order_by_column,
            limit,
            offset,
        )

        # end __init__()

# end Class ItemSet
