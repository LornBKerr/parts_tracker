"""
This is a set of Sources in the database.

File:       source_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

from typing import Any

from lbk_library import Dbal, ElementSet

from . import Source


class SourceSet(ElementSet):
    """
    Provides a set of Sources from the database table 'sources'.
    """

    def __init__(
        self,
        dbref: Dbal,
        where_column: str = None,
        where_value: Any = None,
        order_by_column: str = None,
    ) -> None:
        """
        Builds a set of Sources from the database table 'sources'.

        Note: This set does not support 'limit' and 'offset' entries
        when creating the set.

        Parameters:
            dbref (Dbal): reference to the database holding the element
            where_column (str): The key column of the table containing
                the key value to determine the elements being retrieved.
                Default is all rows are retrieved.
            where_value (int | str): The key value to retrieve. Required
                if where_column is set.
            order_by_column (str): zero or more column names separated by
                commas to order the resulting set of elements.
        """
        table_name = "sources"
        element_type = Source

        super().__init__(
            dbref, table_name, element_type, where_column, where_value, order_by_column
        )

    # end __init__()


# end SourceSet
