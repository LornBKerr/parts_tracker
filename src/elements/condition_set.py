"""
This is a set of Conditions in the parts file.

File:       condition_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

from lbk_library import DataFile, ElementSet

from .condition import Condition


class ConditionSet(ElementSet):
    """Provide a set of Conditions from parts file table 'conditions'."""

    def __init__(
        self,
        parts_file: DataFile,
        where_column: str = None,
        where_value: str | int = None,
        order_by_column: str = None,
    ) -> None:
        """
        Build a set of Conditions from the parts file table 'conditions'.

        Note: This set does not support 'limit' and 'offset' entries
        when creating the set.

        Parameters:
            parts_file (DataFile): reference to the parts file holding the element
            where_column (str): The key column of the table containing
                the key value to determine the elements being retrieved.
                Default is all rows are retrieved.
            where_value (int | str): The key value to retrieve. Required
                if where_column is set.
            order_by_column (str): zero or more column names separated by
                commas to order the resulting set of elements.
        """
        table_name = "conditions"
        element_type = Condition

        super().__init__(
            parts_file,
            table_name,
            element_type,
            where_column,
            where_value,
            order_by_column,
        )
