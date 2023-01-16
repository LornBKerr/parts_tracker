"""
This is a set of Partss in the database.

File:       part_setl.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

from typing import Any

from lbk_library import Dbal, ElementSet

from . import Part


class PartSet(ElementSet):
    """
    This is a set of Parts in the database.
    """

    def __init__(
        self,
        dbref: Dbal,
        where_column: str = None,
        where_value: Any = None,
        order_by_column: str = None,
        limit: int = None,
        offset: int = None,
    ) -> None:
        """
        Builds a set of Parts from the database table 'parts'.

        Parameters:
            dbref (Dbal): reference to the database holding the parts
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
        table_name = "parts"  # The database table for this element
        element_type = Part

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


# end PartSet
