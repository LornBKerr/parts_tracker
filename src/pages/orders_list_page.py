"""
This is the list displaying the Orders in the database

File:       orders_list_page.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""


from lbk_library import Dbal
from PyQt6.QtWidgets import QMainWindow



class OrdersListPage:
    """
    This is the list displaying the Orders in the database
    """
    def __init__(self, main_window: QMainWindow, dbref:Dbal) -> None:
        """
        Initialize and display the Order List

        Parameters:
        main_window (QMainWindow): the parent window
        dbref (Dbal): reference to the database for this item.
        """
        self.main_window: QMainWindow  = main_window
        self.dbref: Dbal = dbref

            # set up the Orders Listing Table
        self.table = self.main_window.orders_table_widget
#        self.set_table_headers()
#
#            # load the table
#        if self.dbref.sql_is_connected():
#            self.update_table()
#
#            # connect the order list table signal for 'item clicked'
#        self.table.itemClicked.connect(self.action_order_clicked)
#    # end __init__()

    def update_table(self) -> None:
        """
        Read the database order table and update the display table.
        """
        pass
#        self.table.setSortingEnabled(False)
#        order_list = OrderSet(self.dbref, "order_number", None, "order_number")
#            # clear the current contents and set the new row count
#        self.table.clearContents()
#        self.table.setRowCount(order_list.get_number_elements())
#        
#        # fill each of the rows
#        row = 0
#        for order in order_list:
#            entry_index = order.get_entry_index()
#            entry_index_sortable = TableWidgetIntItem(entry_index)
#            entry_index_sortable.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
#            self.table.setItem(row, 0, entry_index_sortable)
#
#            order_number = QTableWidgetItem(order.get_order_number())
#            self.table.setItem(row, 1, order_number)
#
#            self.table.setItem(row, 2, QTableWidgetItem(order.get_date()))
#
#            self.table.setItem(row, 3, QTableWidgetItem(order.get_source()))
#
#            num_lines = self._get_number_lines(order.get_order_number())
#            number_lines = TableWidgetIntItem(num_lines)
#            number_lines.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
#            self.table.setItem(row, 4, number_lines)
#
#            self.table.setItem(row, 5, QTableWidgetItem(order.get_remarks()))
#            row += 1
#
#        self.table.setSortingEnabled(True)
#    # end update_table()

    def clear_table(self) -> None:
        """
        Clear the contents of the Order Line table
        """
        self.table.clearContents()
    # end clear_table()

#    ##
#    # Set the table headers.
#    #
#    # The header names are set and the column widths to match the size of the
#    # entries are set.
#    #
#    def set_table_headers(self):
#        column_names = list(
#            [
#                "Order Id",
#                "Order Number",
#                "Date",
#                "Source",
#                "Num of Lines",
#                "Order Remarks",
#            ]
#        )
#        header = self.table.horizontalHeader()
#        self.table.setColumnCount(len(column_names))
#        self.table.setHorizontalHeaderLabels(column_names)
#
#        self.table.setColumnWidth(0, 70)
#        self.table.setColumnWidth(1, 120)
#        self.table.setColumnWidth(2, 120)
#        self.table.setColumnWidth(3, 150)
#        self.table.setColumnWidth(4, 100)
#        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
#        self.table.setColumnHidden(0, True)
#    # end set_table_headers
#
#    ##
#    # Get the total number of lines for this order number from the 'order_lines' table.
#    #
#    # The order_lines table is searched for the lines using this order number. The total
#    #  number of order lines found is returned
#    #
#    # @param order_number (str) being searched for
#    #
#    # @return (int) the total number of order lines found
#    #
#    def _get_number_lines(self, order_number: str) -> int:
#        order_line_set = OrderLineSet(self.dbref, "order_number", order_number)
#        return order_line_set.get_number_elements()
#    # end _get_number_lines()
#
#    ##
#    # Display the Order Editing dialog for the order clicked
#    #
#    # @param table_item (QTableWidgetItem) The QTableWidgetItem clicked on
#    #
#    def action_order_clicked(self, table_item: QTableWidgetItem) -> None:
#        row = table_item.row()
#        column = table_item.column()
#        order_number = self.table.item(row, 1).text()
#        dialog = OrderDialog(self.main_window.tab_widget, self.dbref, order_number, EDIT_ELEMENT)
#        result = dialog.exec()
#        self.update_table()
#    # end action_order_clicked()
#
## end class OrdersListPage
#
