"""
Write an Excel (XLSX) compatible or Comma Separated Values (CSV) file of selected
portions of the listing

File:       save_assembly_list_dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import base64
from typing import Any

from lbk_library import Dbal
from lbk_library.gui import Dialog
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QFileDialog, QMainWindow

from .base_dialog import BaseDialog


class SaveAssyListDialog(BaseDialog):
    FOLDER_OPEN_PNG = b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAilJREFUeNqMU89rE0EYfTuz1m790ZJoQeghaqulXoSIp568CQpePOit4EHw4D8gQkWo/0TxXFAIePEgxaMQBLXWH1VqW9NWC6HGkGyyOzPr901mN1lQcNjHzM5+7+173+541QXY4XmYo6mE/xsbSYLHvPATt0Mbp2auP7rXqn2CRzcjx04iGJuAkEN5qu+junjzYXZrTPZIHDo+hZHiaUTNPbR2P2P7wytMla/l+F4QgDgiI2my4CCMVjBRF/7BUYydmUWnE6HZ6kATIyFXFrTm2pQnNDlwkInWyKBITEVoNEPs7jX6AgSuTXk+1abDCrALa00ItMMuCi6jcbOgGrpk0usbfNXvgTQ6hlaxC+chVjojpjM3gDiSVmUSeD0YwTdMsNYZGoo2mTgI7sGleXOXHs0Z6yAXQfUjaGkdcObeZ3YzCTTCkMSti1wEchDDuAiGeqDooXHENIJH8367zTF8+6J3m2A1q8jWtQOvldZ/jXBrvWjrmSfuLwEsEisM2f+AGtmDsg5sqwc+IQvU621bzzz+o4IHT1D4HeJowk2zn7L3L3CTpJQ5eHRo7lQOP3uxgiXiBZxjmFB4u4GdyZdPm6XpC8OjxRMH+E1b39Z+vVmZX+WsxSOI0mat/8TO4jI+MpcF9hlffuD219Xq87X31cuF8Ymzk+culsjB5kIFN2anUb9aRjcVoNp+5wcPChEqFLuyXaud/75Vu0Imxmm7Tuj+61z/EWAAclGWg0KibYEAAAAASUVORK5CYII="
    """Representation of the folder_open.png image."""

    TOOLTIPS = {
        "start_assy": "Required: Enter the Starting Assembly code, 1 to 15 characters.",
        "stop_assy": "Required: Enter the Ending Assembly code, 1 to 15 characters.",
        "xlsx_file": "Not currently implemented.",
        "cvs_file": "Check to generat a comma separated file listing.",
        "save_loc": "Enter the location to save the generated file.\nClick the icon to select a different file location.",
        "cancel": "Close the form, optionally saving any changed information",
        "generate": "Generate and save the requested listing, then clear the form",
    }
    """The default tool tips."""

    def __init__(
        self,
        parent: QMainWindow,
        dbref: Dbal,
        config: dict[str, Any],
        operation: int = Dialog.EDIT_ELEMENT,
    ) -> None:
        """
        Initialize the dialog.

        Parameters:
            parent (QMainWindow) the owning dialog.
            dbref   - reference to the current open database.
            config (dict) the current configuration settings.
        """
        super().__init__(parent, dbref, Dialog.EDIT_ELEMENT)
        self.parent = parent
        self.dbref = dbref
        self.config = config

        self.form = uic.loadUi("./src/forms/save_assy_list.ui", self)
        self.set_tool_tips()

        folder_open_pixmap = QPixmap()
        folder_open_pixmap.loadFromData(base64.b64decode(self.FOLDER_OPEN_PNG))

        save_location_action = self.form.save_location_edit.addAction(
            QIcon(folder_open_pixmap), self.form.save_location_edit.TrailingPosition
        )
        self.form.save_location_edit.setText(config["settings"]["list_files_dir"])

        # Temporarily disable the Excel file generation and check the CSV box
        self.form.xlsx_check_box.setEnabled(False)
        self.form.csv_check_box.setChecked(True)
        #
        #        self.form.start_edit.editingFinished.connect(self.action_start_changed)
        #        self.form.stop_edit.editingFinished.connect(self.action_stop_changed)
        save_location_action.triggered.connect(self.action_save_file_location)

    #        self.form.cancel_button.clicked.connect(self.close)
    #        self.form.generate_button.clicked.connect(self.action_write_files)

    def set_tool_tips(self):
        """Set the tab order for the dialog elements."""
        self.form.start_edit.setToolTip(self.TOOLTIPS["start_assy"])
        self.form.stop_edit.setToolTip(self.TOOLTIPS["stop_assy"])
        self.form.xlsx_check_box.setToolTip(self.TOOLTIPS["xlsx_file"])
        self.form.csv_check_box.setToolTip(self.TOOLTIPS["cvs_file"])
        self.form.save_location_edit.setToolTip(self.TOOLTIPS["save_loc"])
        self.form.cancel_button.setToolTip(self.TOOLTIPS["cancel"])
        self.form.generate_button.setToolTip(self.TOOLTIPS["generate"])

    #
    #    def action_start_changed(self):
    #        """
    #        Force Start value to upper case.
    #        """
    #        self.form.Start.setText(self.form.Start.text().upper())
    #
    #    def action_stop_changed(self):
    #        """
    #        Force Stop value to upper case.
    #        """
    #        self.form.Stop.setText(self.form.Stop.text().upper())

    def action_save_file_location(self):
        """
        Set the directory to save the generated file.
        """
        location = self.form.save_location_edit.text()
        directory = QFileDialog.getExistingDirectory(
            self,
            "Open Directory",
            location,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )
        if directory:
            self.form.save_location_edit.setText(directory)

        if directory != self.config["settings"]["list_files_dir"]:
            # update the config file
            self.config["settings"]["list_files_dir"] = directory
            self.parent.update_config_file(self.config)


#    def action_write_files(self):
#        """
#        Generate a CSV file and/or an Excel xlsx file.
#        """
#        # Make sure we have a file type
#        if self.form.XlsxCheckBox.isChecked() or self.form.CsvCheckBox.isChecked():
#            # Validate the starting and ending points
#            start = self.form.Start.text()
#            end = self.form.Stop.text()
#
#            # if both start and end are blank, set full listing
#            if start == "" and end == "":
#                start = "A"
#                end = "ZZZ"
#            elif end == "" and start != "":  # starting point but no end point
#                end = start + "ZZZ"
#
#            itemset = self.get_itemset(start, end)
#            # Get the location to save the file
#            location = self.form.SaveLocation.text()
#            if not location:
#                location = Path.home
#
#                # file is file name is full path to be saved without suffix.
#            filename = location + os.sep + "" + start + "_" + end
#
#            msg_string = ""
#            if self.form.XlsxCheckBox.isChecked():
#                result = self.write_excel_file(filename, itemset)
#                if result:
#                    msg_string += (
#                        str(len(itemset))
#                        + " Items have been written to \n"
#                        + filename
#                        + ".xlsx.\n\n"
#                    )
#                else:
#                    msg_string += "Write to " + filename + ".xlsx failed.\n\n"
#
#            if self.form.CsvCheckBox.isChecked():
#                result = self.write_csv_file(filename, itemset)
#                if result:
#                    msg_string += (
#                        str(len(itemset))
#                        + " Items have been written to \n"
#                        + filename
#                        + ".csv. \n\n"
#                    )
#                else:
#                    msg_string += "Write to " + filename + ".csv failed\n\n."
#
#            action = self.message_information_close(msg_string + "Do another?")
#            if action == QMessageBox.Yes:
#                self.form.Start.setText("")
#                self.form.Stop.setText("")
#            else:
#                self.close()
#        else:
#            self.message_warning_selection(
#                "A Save File type", "do. Select one or both file types"
#            )
#
#    def get_itemset(self, start, end):
#        """
#        Build the item set.
#
#        Parameters:
#            start (str) The starting assembly code.
#            end (str) The ending (not included) assembly code.
#
#        Returns:
#            (list) The requested set of items.
#        """
#        items = []  # hold the raw item info from database
#        itemset = []  # hold the Items converted from the raw db info
#        sql = (
#            "SELECT * FROM items WHERE assembly >= '"
#            + start
#            + "' AND assembly < '"
#            + end
#            + "' ORDER BY assembly"
#        )
#        result = self.dbref.sql_query(sql)
#        items = self.dbref.sql_fetchrowset(result)
#
#        for item in items:
#            itemset.append(Item(self.dbref, item))
#        return itemset
#    # end get_itemset()
#
#    def write_excel_file(self, filename, itemset):
#        """
#        Place Holder until I get around to writing this section.
#        """
#        #workbook_defs = [
#        #  ['A', 'Engine', [['AA', 'Block'], ['AB', 'Interior'],
#        #      ['AC', 'Head'], ['AD', 'General']]],
#        #  ['B', 'Drive Train', [['BA', 'Clutch'], ['BB', 'Gearbox'],
#        #      ['BC', 'Drive Shaft'], ['BD', 'Rear Axle']]],
#        #  ['C', 'Cooling and Heating', [['CA', 'Cooling System'],
#        #      ['CB', 'Heating System']]],
#        #  ['D', 'Fuel System', [['DA', 'Fueld Tank and Piping'],
#        #      ['DB', 'Intake'], ['DC', 'Emissions']]],
#        #  ['E', 'Suspension and Steering', [['EA', 'Front Suspension'],
#        #      ['EB', 'Rear Suspension'], ['EC', 'Steering']]],
#        #  ['F', 'Brakes', [['FA', 'Front Brakes'], ['FB', 'Rear Brakes'],
#        #      ['FC', 'Handbrake'], ['FD', 'Brake Hydraulics'], ['FE', 'Pedal Box']]],
#        #  ['G', 'Body Exterior', [['HA', 'Hood'], ['GB', 'Front Apron'],
#        #      ['GC', 'Front Fenders'], ['GD', 'Front Cowl'], ['GE', 'Rear Fenders'],
#        #      ['GF', 'Rear cowl'], ['GG', 'Trunk Area'], ['GI', 'Front Bumper'],
#        #      ['GJ', 'Rear Bumper'], ['GK', 'Side Moulding'],
#        #      ['GL', 'Underbody Fittings'], ['GM', 'Top']]],
#        #  ['H', 'Body Interior', [['HA', 'Dash Area'], ['Floor Area'],
#        #      ['HC', 'Door Fittings and Windows'], ['HD', 'Rear Cockpit Area'],
#        #      ['HE', 'Trunk interior'], ['HF', 'Interior Kit'],
#        #      ['HG', 'Seats'], ['HH', 'Labels and Plates']]],
#        #  ['J', 'Electrical System', [['JA', 'Starting and Charging'],
#        #       ['JB', 'Ignition'], ['JC', 'Lighting'], ['JD', 'Dash'],
#        #       ['JE', 'Engine Fittings'], ['JF', 'Wiring Harness']]],
#        #  ['L', 'Exhaust System', []],
#        #  ['M', 'Wheels and Tires', []],
#        #  ['T', 'Tools', []]
#        #]
#        #
#        #column_defs = ['Assembly', 'Item', 'Part Number', 'Description',
#        #    'Quantity', 'Cond', 'Installed', 'Item Remarks', 'Part Remarks']
#
#        return False
#
#    def write_csv_file(
#        self,
#        filename,
#        itemset,
#    ):
#        """
#        Write a csv file in the 'excel' dialect.
#
#        Parameters:
#            filename (strg) the full path to the file (without the
#                filename suffix).
#        itemset (list) the set of items to save.
#
#        Returns:
#            (bool) True always
#        """
#        csv_file = open(filename + ".csv", "w")
#        writer = csv.writer(csv_file)
#        self.write_headers(writer)
#        # write the Item lines to the file
#        for item in itemset:
#            part = Part(self.get_dbref(), item.get_part_number(), "part_number")
#            self.write_item_line(item, part, writer)
#
#        csv_file.close()
#        self.config["LOCATIONS"]["assy_file_dir"] = os.path.dirname(filename)
#        self.parentWidget().update_config_file(self.config)
#        return True
#
#
#    ##
#    # Write the headers to the csv file
#    #
#    # @param writer (csv.writer) the writer object to write the file contents
#    #
#    def write_headers(self, writer):
#        headers = [
#            "Assembly",
#            "Item",
#            "Part Number",
#            "Description",
#            "Quantity",
#            "Condition",
#            "Installed",
#            "Item Remarks",
#            "Part Remarks",
#        ]
#        writer.writerow(headers)
#    # end write_headers()
#
#    def write_item_line(self, item, part, writer):
#        """
#        Write a line to the csv file.
#
#        Parameters:
#            item (Item) to print.
#            part (Part) to use for the item description.
#            writer (csv.writer) the writer object to write the file
#                contents.
#        """
#        installed = ""
#        if item.get_installed():
#            installed = "X"
#
#        line = [
#            item.get_assembly(),
#            item.get_entry_index(),
#            item.get_part_number(),
#            part.get_description(),
#            item.get_quantity(),
#            item.get_condition(),
#            installed,
#            item.get_remarks(),
#            part.get_remarks(),
#        ]
#
#        writer.writerow(line)
#
