"""
This is the list displaying the Orders in the database.

File:       orders_list_page.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

from lbk_library import DataFile
from lbk_library.gui import Dialog, TableWidgetIntItem
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem

from dialogs import OrderDialog
from elements import OrderLineSet, OrderSet


class OrdersListPage:
    """Display the Orders in the database."""

    COLUMN_NAMES = [
        "Order Id",
        "Order Number",
        "Date",
        "Source",
        "Num of Lines",
        "Order Remarks",
    ]

    def __init__(self, table: QTableWidget, parts_file: DataFile) -> None:
        """
        Initialize and display the Order List.

        Parameters:
            main_window (QMainWindow): the parent window.
            parts_file (DataFile): reference to the parts file.
        """
        self.parts_file: DataFile = parts_file
        self.table = table

        # # set up the Orders Listing Table
        self.set_table_headers()

        # load the table
        if self.parts_file.sql_is_connected():
            self.update_table()

        # connect the order list table signal for 'item clicked'
        self.table.itemClicked.connect(self.action_order_clicked)

    def update_table(self) -> None:
        """Read database order table and update the display table."""
        self.table.setSortingEnabled(False)
        order_list = OrderSet(self.parts_file, "order_number", None, "order_number")
        # clear the current contents and set the new row count
        self.table.clearContents()
        self.table.setRowCount(order_list.get_number_elements())

        # fill each of the rows
        row = 0
        for order in order_list:
            col = 0
            record_id = order.get_record_id()
            record_id_sortable = TableWidgetIntItem(record_id)
            record_id_sortable.setTextAlignment(
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
            )
            self.table.setItem(row, col, record_id_sortable)

            col += 1
            self.table.setItem(row, col, QTableWidgetItem(order.get_order_number()))

            col += 1
            self.table.setItem(row, col, QTableWidgetItem(order.get_date()))

            col += 1
            self.table.setItem(row, col, QTableWidgetItem(order.get_source()))

            col += 1
            num_lines = self.get_number_lines(order.get_order_number())
            number_lines = TableWidgetIntItem(num_lines)
            number_lines.setTextAlignment(
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
            )
            self.table.setItem(row, col, number_lines)

            col += 1
            self.table.setItem(row, col, QTableWidgetItem(order.get_remarks()))
            row += 1

        self.table.setSortingEnabled(True)

    def clear_table(self) -> None:
        """Clear the Order Line table."""
        self.table.clearContents()
        self.table.setRowCount(0)

    def set_table_headers(self):
        """
        Set the table headers.

        Set the header names and set the column widths to match the size
        of the entries.
        """
        self.table.verticalHeader().setVisible(False)
        header = self.table.horizontalHeader()
        self.table.setColumnCount(len(self.COLUMN_NAMES))
        self.table.setHorizontalHeaderLabels(self.COLUMN_NAMES)

        self.table.setColumnWidth(0, 70)
        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(2, 120)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 100)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        # self.table.setColumnHidden(0, True)

    def get_number_lines(self, order_number: str) -> int:
        """
         Get the total number of lines for this order number.

        The order_lines table is searched for the lines using this order
        number.

        Parameters:
            order_number (str): Order being searched for.

        Returns:
            (int) the total number of order lines found.
        """
        order_line_set = OrderLineSet(self.parts_file, "order_number", order_number)
        return order_line_set.get_number_elements()

    def action_order_clicked(self, table_item: QTableWidgetItem) -> None:
        """
        Show the Order Editing dialog for the specified order.

        Parameters:
            table_item (QTableWidgetItem): The clicked item.
        """
        row = table_item.row()
        column = table_item.column()
        order_number = self.table.item(row, 1).text()
        dialog = OrderDialog(
            self.table,
            self.parts_file,
            order_number,
            Dialog.EDIT_ELEMENT,
        )
        result = dialog.open()
        self.update_table()
        return dialog

    def get_parts_file(self) -> DataFile:
        """
        Return the parts file reference.

        Return (DataFile): the current parts file reference.
        """
        return self.parts_file
