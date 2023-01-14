"""
This is the list displaying the Parts in the database

File:       parts_list_page.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

from lbk_library import Dbal
from PyQt6.QtWidgets import QMainWindow


class PartsListPage:
    """
    This is the list displaying the Parts in the database
    """
    def __init__(self, main_window: QMainWindow, dbref:Dbal) -> None:
        """
        Initialize and display the Part List

        Parameters
            main_window (QMainWindow): the parent window
            dbref (Dbal): reference to the database for this item.
        """
        self.main_window: QMainWindow  = main_window
        self.dbref: Dbal = dbref

            # set up the Parts Listing Table
        self.table = self.main_window.parts_table_widget
            # set the table headers and load the table
#        self.set_table_headers()
#
#        if self.dbref.sql_is_connected():
#            self.update_table()
#
#        # connect the table signal for 'part clicked'
#        self.table.itemClicked.connect(self.action_part_clicked)
#    # end __init__()

    def update_table(self) -> None:
        """
        Read the database part table and update the display table.
        """
        pass
#        self.table.setSortingEnabled(False)
#        part_list = PartSet(self.dbref, "part_number", None, "part_number")
#
#            # clear the current contents and set the new row count
#        self.table.clearContents()
#        self.table.setRowCount(part_list.get_number_elements())
#
#            # fill each of the rows
#        row = 0
#        for part in part_list:
#            col = 0
#            entry_index = part.get_entry_index()
#            entry_index_sortable = TableWidgetIntItem(entry_index)
#            entry_index_sortable.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
#            self.table.setItem(row, col, entry_index_sortable)
#
#            col += 1
#            part_number = QTableWidgetItem(part.get_part_number())
#            self.table.setItem(row, col, part_number)
#
#            col += 1
#            self.table.setItem(row, col, QTableWidgetItem(part.get_description()))
#
#            col += 1
#            self.table.setItem(row, col, QTableWidgetItem(part.get_source()))
#
#            col += 1
#            quantity = part.get_total_quantity()
#            qty_item = TableWidgetIntItem(quantity)
#            qty_item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
#            self.table.setItem(row, col, qty_item)
#
#            col += 1
#            self.table.setItem(row, col, QTableWidgetItem(part.get_remarks()))
#
#            row += 1
#        self.table.setSortingEnabled(True)
#    # end update_table

    def clear_table(self):
        """
        Clear the contents of the Parts Table.
        """
        self.table.clearContents()
    # end clear_table()

#    ##
#    # Set the table headers.
#    #
#    # The header names are set and the column widths to match the size of the
#    # entries are set.
#    #
#    def set_table_headers(self) -> None:
#        column_names = ["Part Id", "Part Number", "Description", "Source", "Qty Used", "Part Remarks"]
#        header = self.table.horizontalHeader()
#        self.table.setColumnCount(len(column_names))
#        self.table.setHorizontalHeaderLabels(column_names)
#        self.table.setColumnWidth(0, 50)
#        self.table.setColumnWidth(1, 120)
#        self.table.setColumnWidth(2, 400)
#        self.table.setColumnWidth(3, 150)
#        self.table.setColumnWidth(4, 70)
#        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
#        self.table.setColumnHidden(0, True)
#    # end set_table_headers
#
#    ##
#    # Display the Part Editing dialog for the part number clicked
#    #
#    # @ param table_item (QTableWidgetItem) The QTableWidgetItem clicked on
#    #
#    def action_part_clicked(self, table_item: QTableWidgetItem) -> None:
#        row = table_item.row()
#        column = table_item.column()
#        part_index = self.table.item(row, 0)
#        dialog = PartDialog(
#            self.main_window.tab_widget, self.dbref, part_index.text()
#        )
#        result = dialog.exec()
#        self.update_table()
#    # end action_part_clicked
#
## end class PartsListPage
#
