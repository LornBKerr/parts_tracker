"""
Provides the interface to access and manipulate the order line table.

This is used to display the order line table on an Order Dialog. There
is no error checking of values. Each cell information is a dict of
values for cell value, alignment, background color, and tooltip.

File:       order_line_table_model.py
Author:     Lorn B Kerr
Copyright:  (c) 2024 Lorn B Kerr
License:    MIT, see file LICENSE
"""

# from typing import Any

from lbk_library.gui import TableModel  # CellData,

# from PyQt6.QtCore import Qt        #QAbstractTableModel, QModelIndex,
# from PyQt6.QtGui import QBrush  # , QColor


class OrderLineTableModel(TableModel):
    """
    Provide a specific OrderLine table of the Order Dialog.

    The data for this model is contained in a list of lists of strings
    representing th eOrderLineSet
    """

    #
    def __init__(
        #        self,
        #        cell_values: list[list[str]],
        #        background: QBrush,
    ) -> None:
        """
        Initialize the TableModel.

        Parameters:
            cell_values (list[list[str]]): The information to display in
                the table formatted as a list of lists.
            background (Qbrush): The table cell background color.
        """


#        self._data_set: list[list[dict[str, Any]]] = []
#        """The set of cell information to diaplay to display."""
#
#        super().__init__(
#            self._data_set,
#            self._header_titles,
#            self._column_tooltips,
#            self._column_alignments,
#            background,
#        )
#
#
#        for i in range(len(self._table_col_widths)):
#            self.table.setColumnWidth(i, self._table_col_widths[i])
#        self.table.horizontalHeader().setSectionResizeMode(
#            self._header_titles.index("Remarks"), QHeaderView.ResizeMode.Stretch
#        )
#
#        for row in range(len(cell_values)):
#            self._data_set.append([])
#            for column in range(len(cell_values[0])):
#                self._data_set[row].append(
#                    CellData(
#                        cell_values[row][column],
#                        self._column_alignments[column],
#                        background,
#                        self._column_tooltips[column],
#                    )
#                )
#
#    def data(
#        self, index: QModelIndex, role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole
#    ) -> Any:
#        """
#        Get the entry for the requested row/column.
#
#        Parameters:
#            index(QModelIndex): Index to the specific cell requested.
#            role (Qt.ItemDataRole): The type of data requested.
#                Implemented Qt.ItemDataRole types include:
#                    BackgroundRole: set the background color.
#                    DisplayRole: item is display only, default value.
#                    EditRole: item is editable.
#                    ToolTipRole: the item's tooltip.
#                    TextAlignmentRole: the alignment of the text.
#
#            Returns:
#                (str) The data item requested.
#        """
#        entry = None
#        # handle the situation where number of data columns is less than
#        # number of table columns.
#        if index.column() >= len(self._data_set[0]):
#            pass
#
#        elif role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
#            entry = self._data_set[index.row()][index.column()].value
#
#        elif role == Qt.ItemDataRole.ToolTipRole:
#            entry = self._data_set[index.row()][index.column()].tooltip
#
#        elif role == Qt.ItemDataRole.BackgroundRole:
#            entry = self._data_set[index.row()][index.column()].background
#
#        elif role == Qt.ItemDataRole.TextAlignmentRole:
#            entry = self._data_set[index.row()][index.column()].alignment
#
#        return entry
#
#    def setData(
#        self,
#        index: QModelIndex,
#        value: Any,
#        role: Qt.ItemDataRole = Qt.ItemDataRole.EditRole,
#    ) -> bool:
#        """
#        Set the item at index to value.
#
#        The dataChanged() signal is emitted if the data was successfully
#        set.
#
#        Parameters:
#            index(QModelIndex): index to the specific row/column requested.
#            value (Any): the new value of the data item with type as
#                defined in the roles.
#            role (Qt.ItemDataRole) the type of data to be set.
#                 Implemented types include:
#                    BackgroundRole: set the background color (QBrush).
#                    DisplayRole: set the item, display only (#str).
#                    EditRole: set the item, editable (str).
#                    ToolTipRole: Set the tooltip. (str)
#                    TextAlignmentRole: Set the alignment of the text
#                        (Qt.Alignment).
#
#        Returns:
#            (bool) True if successful; otherwise returns False.
#
#        Signals:
#            Emits dataChanged signal if set_data() is successful.
#        """
#        success = False
#
#        # handle the situation where number data columns is less than
#        # number of table columns.
#        if index.column() >= len(self._data_set[0]):
#            success = True
#
#        elif role == Qt.ItemDataRole.EditRole or role == Qt.ItemDataRole.DisplayRole:
#            self._data_set[index.row()][index.column()].value = value
#            success = True
#
#        elif role == Qt.ItemDataRole.ToolTipRole:
#            self._data_set[index.row()][index.column()].tooltip = value
#            success = True
#
#        elif role == Qt.ItemDataRole.BackgroundRole:
#            self._data_set[index.row()][index.column()].background = value
#            success = True
#
#        elif role == Qt.ItemDataRole.TextAlignmentRole:
#            self._data_set[index.row()][index.column()].alignment = value
#            success = True
#
#        if success:
#            self.dataChanged.emit(index, index)
#        return success
#
#    def rowCount(self, index: QModelIndex = QModelIndex()) -> int:
#        """
#        Get the number of rows (elements in the data set).
#
#        Parameters:
#            index QModelIndex): index of parent cell, defaults to an
#                empty QModelIndex.
#
#        Returns:
#            (int) number of rows in table.
#        """
#        return len(self._data_set)
#
#    def columnCount(self, index: QModelIndex = QModelIndex()) -> int:
#        """
#        Get the number of columns.
#
#        Parameters:
#            index (QModelIndex): index of parent cell, defaults to an
#                empty QModelIndex.
#
#        Returns:
#            (int) number of columns in table.
#        """
#        return len(self._header_titles)
#
#    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
#        """
#        Set the flags for specific row/column entry to include editable.
#
#        This adds the ItemIsEditable flag to the default settings of
#        itemIsSelectable and ItemIsEnabled for all columns except
#        'Record Id' and 'Action(s)'.
#
#        Parameters:
#            index (QModelIndex): The cell requesting the flags.
#
#        Returns:
#            (Qt.ItemFlags) The flags for the specific cell.
#        """
#        flags = super().flags(index)
#        if self._header_titles[index.column()] != "Record Id":
#            flags = flags | Qt.ItemFlag.ItemIsEditable
#        return flags
#
#    def headerData(
#        self,
#        section: int,
#        orientation: Qt.Orientation,
#        role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole,
#    ) -> str:
#        """
#        Return the data for the given role and section in the header.
#
#        For horizontal headers, the section number corresponds to the
#        column number; for vertical headers, the row number.
#
#        Parameters:
#            section (int): the row or column number of the header
#            orientation (Qt.Orientation): either Qt.Orientation.Vertical
#                or Qt.Orientation.Horizontal
#            role (Qt.ItemDataRole:): the specific role being set,
#                defaults to Qt.ItemDataRole.DisplayRole
#
#        Returns:
#            The current text contents of the header cell.
#        """
#        entry = None
#        if role == Qt.ItemDataRole.DisplayRole and section < self.columnCount():
#            entry = self._header_titles[section]
#        return entry
#
#    def setHeaderData(
#        self,
#        section: int,
#        orientation: Qt.Orientation,
#        value: str,
#        role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole,
#    ) -> bool:
#        """
#        Set the data for the given role and section in the header.
#
#        For horizontal headers, the section number corresponds to the
#        column number; for vertical headers, the row number.
#
#        Parameters:
#            section (int): the row or column number of the header
#            orientation (Qt.Orientation): either Qt.Orientation.Vertical
#            role (Qt.ItemDataRole:): the specific role being set,
#                defaults to Qt.ItemDataRole.DisplayRole
#
#        Returns:
#            (bool) True if the header data was successfully changed,
#                False otherwise.
#        Signals:
#            Emits headerDataChanged signal if set is successful.
#        """
#        success = False
#        if role == Qt.ItemDataRole.DisplayRole:
#            self._header_titles[section] = value
#            success = True
#            self.headerDataChanged.emit(orientation, section, section)
#        return success
#
#    def insertRows(
#        self, row: int, count: int = 1, parent: QModelIndex = QModelIndex()
#    ) -> bool:
#        """
#        Insert one or more rows into the table.
#
#        Parameters:
#            row (int): The zero based row number to insert the new rows.
#            count (int): the number (1 or greater) of new rows to insert,
#                default is 1.
#            parent (QModelIndex): The parent node of the row position to
#                insert, default is the empty index.
#        Returns:
#            (bool) True if the insert was successful, False if not.
#        """
#        success = False
#        self.beginRemoveRows(parent, row, row + count - 1)
#        count_added = 0
#        while count_added < count:
#            self._data_set.insert(
#                row, [CellData() for i in range(len(self._data_set[0]))]
#            )
#            count_added += 1
#        success = True
#        self.endInsertRows()
#        return success
#
#    def removeRows(
#        self, first_row: int, count: int, parent: QModelIndex = QModelIndex()
#    ) -> bool:
#        """
#        Need to implement this to delete rows for the table.
#        """
#        success = False
#        self.beginRemoveRows(parent, first_row, first_row + count)
#        count_deleted = 0
#        while count_deleted < count:
#            del self._data_set[first_row]
#            count_deleted += 1
#        success = True
#        self.endRemoveRows()
#        return success
