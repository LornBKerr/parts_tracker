"""
Write a Comma Separated Values (CSV) file of portions of listing.

File:       save_assembly_list_dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
Version:    1.0.0
"""

import base64
import csv
import os

from lbk_library import DataFile as PartsFile
from lbk_library.gui import Dialog
from PyQt6 import uic
from PyQt6.QtCore import QSettings
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QFileDialog, QMainWindow, QMessageBox

from elements import Item, Part

from .base_dialog import BaseDialog

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}


class AssemblyListDialog(BaseDialog):
    """Write a Comma Separated Values file of portions of listing."""

    FOLDER_OPEN_PNG = b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAilJREFUeNqMU89rE0EYfTuz1m790ZJoQeghaqulXoSIp568CQpePOit4EHw4D8gQkWo/0TxXFAIePEgxaMQBLXWH1VqW9NWC6HGkGyyOzPr901mN1lQcNjHzM5+7+173+541QXY4XmYo6mE/xsbSYLHvPATt0Mbp2auP7rXqn2CRzcjx04iGJuAkEN5qu+junjzYXZrTPZIHDo+hZHiaUTNPbR2P2P7wytMla/l+F4QgDgiI2my4CCMVjBRF/7BUYydmUWnE6HZ6kATIyFXFrTm2pQnNDlwkInWyKBITEVoNEPs7jX6AgSuTXk+1abDCrALa00ItMMuCi6jcbOgGrpk0usbfNXvgTQ6hlaxC+chVjojpjM3gDiSVmUSeD0YwTdMsNYZGoo2mTgI7sGleXOXHs0Z6yAXQfUjaGkdcObeZ3YzCTTCkMSti1wEchDDuAiGeqDooXHENIJH8367zTF8+6J3m2A1q8jWtQOvldZ/jXBrvWjrmSfuLwEsEisM2f+AGtmDsg5sqwc+IQvU621bzzz+o4IHT1D4HeJowk2zn7L3L3CTpJQ5eHRo7lQOP3uxgiXiBZxjmFB4u4GdyZdPm6XpC8OjxRMH+E1b39Z+vVmZX+WsxSOI0mat/8TO4jI+MpcF9hlffuD219Xq87X31cuF8Ymzk+culsjB5kIFN2anUb9aRjcVoNp+5wcPChEqFLuyXaud/75Vu0Imxmm7Tuj+61z/EWAAclGWg0KibYEAAAAASUVORK5CYII="
    """Representation of the folder_open.png image."""

    HEADER_NAMES = [
        "Assembly",
        "Item",
        "Part Number",
        "Description",
        "Quantity",
        "Condition",
        "Installed",
        "Item Remarks",
        "Part Remarks",
    ]
    """List of names for the first row of the csv file."""

    TOOLTIPS = {
        "start_assy": "Required: Enter the start Assembly code, 1 to 15 characters.",
        "stop_assy": "Required: Enter the stop Assembly code, 1 to 15 characters.",
        "save_loc": "Enter the location to save the generated file.\nClick the icon to select a different file location.",
        "cancel": "Close the form.",
        "generate": "Generate and save the requested listing, then clear the form",
    }
    """The default tool tips."""

    def __init__(
        self,
        parent: QMainWindow,
        parts_file: PartsFile,
        config: QSettings,
        operation: int = Dialog.EDIT_ELEMENT,
    ) -> None:
        """
        Initialize the dialog.

        Parameters:
            parent (QMainWindow) the owning dialog.
            parts_file (PartsFile) reference to the current open data file.
            config (QSettings) the current configuration settings.
        """
        super().__init__(parent, parts_file, Dialog.EDIT_ELEMENT)
        self.parent = parent
        self.parts_file = parts_file
        self.config = config
        self.form = uic.loadUi("./src/forms/assembly_list_dialog.ui", self)
        self.set_tool_tips()

        folder_open_pixmap = QPixmap()
        folder_open_pixmap.loadFromData(base64.b64decode(self.FOLDER_OPEN_PNG))

        self.new_location_action = self.form.save_location_edit.addAction(
            QIcon(folder_open_pixmap), self.form.save_location_edit.TrailingPosition
        )
        self.form.save_location_edit.setText(config.value("settings/list_files_dir"))

        self.form.start_edit.editingFinished.connect(self.action_start_changed)
        self.form.stop_edit.editingFinished.connect(self.action_stop_changed)
        self.new_location_action.triggered.connect(self.action_new_location)
        self.save_location_edit.editingFinished.connect(
            self.action_save_location_changed
        )
        self.form.save_button.clicked.connect(self.action_write_file)
        self.form.cancel_button.clicked.connect(self.close)

    def set_tool_tips(self):
        """Set the tab order for the dialog elements."""
        self.form.start_edit.setToolTip(self.TOOLTIPS["start_assy"])
        self.form.stop_edit.setToolTip(self.TOOLTIPS["stop_assy"])
        self.form.save_location_edit.setToolTip(self.TOOLTIPS["save_loc"])
        self.form.cancel_button.setToolTip(self.TOOLTIPS["cancel"])
        self.form.save_button.setToolTip(self.TOOLTIPS["generate"])

    def action_start_changed(self):
        """Force Start value to upper case."""
        self.form.start_edit.setText(self.form.start_edit.text().upper())

    def action_stop_changed(self):
        """Force Stop value to upper case."""
        self.form.stop_edit.setText(self.form.stop_edit.text().upper())

    def action_new_location(self):
        """Set the directory to save the generated file."""
        location = self.form.save_location_edit.text()
        directory = QFileDialog.getExistingDirectory(
            self,
            "Open Directory",
            location,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )
        if directory:
            self.form.save_location_edit.setText(directory)

            if directory != self.config.value("settings/list_files_dir"):
                # update the config file
                self.config.setValue("settings/list_files_dir", directory)

    def action_save_location_changed(self):
        """Validate tor create he save location directory."""
        location = self.form.save_location_edit.text()
        if not os.path.exists(location):
            os.makedirs(location, 0o644)

        if location != self.config.value("settings/list_files_dir"):
            # update the config file
            self.config.setValue("settings/list_files_dir", location)

    def action_write_file(self):
        """Generate a CSV file."""
        start, stop = self.get_start_stop_points()
        itemset = self.get_itemset(start, stop)

        # Get the location to save the file
        location = self.form.save_location_edit.text()

        filename = location + os.sep + "" + start + "_" + stop + ".csv"
        msg_string = ""

        result = self.write_csv_file(filename, itemset)
        if result:
            msg_string += (
                str(len(itemset)) + " Items have been written to \n" + filename
            )
        else:
            msg_string += "Write to " + filename + ".csv failed\n\n."

        msg_box = self.message_information_close(msg_string + ".\nDo another?")
        action = self.message_box_exec(msg_box)
        if action == QMessageBox.StandardButton.Yes:
            self.form.start_edit.setText("")
            self.form.stop_edit.setText("")
        else:
            self.close()

    def get_start_stop_points(self) -> tuple[str, str]:
        """
        Validate the start and end points.

        If start and stop points are not present, set the the start
        to "A: and the end to "ZZZ" generating a full list of all items.
        If only a start point is entered, set the end point to the
        start pointwith "ZZZ" appended.

        Returns:
            tuple
                start (str) the start assembly code.
                stop (str) the last assembly code to be processed.
        """
        start = self.form.start_edit.text().upper()
        stop = self.form.stop_edit.text().upper()

        # if both start and end are blank, set full listing
        if start == "" and stop == "":
            start = "A"
            stop = "ZZZ"

        # start point but no end point
        elif stop == "" and start != "":
            stop = start + "ZZZ"
        return (start, stop)

    def get_itemset(self, start, end):
        """
        Build the item set.

        Parameters:
            start (str) The start assembly code.
            end (str) The stop (not included) assembly code.

        Returns:
            (list) The requested set of items.
        """
        items = []  # hold the raw item info from data file
        itemset = []  # hold the Items converted from the raw db info
        sql = (
            "SELECT * FROM items WHERE assembly >= '"
            + start
            + "' AND assembly < '"
            + end
            + "' ORDER BY assembly"
        )
        result = self.parts_file.sql_query(sql)
        items = self.parts_file.sql_fetchrowset(result)

        for item in items:
            itemset.append(Item(self.parts_file, item))

        return itemset

    def write_csv_file(self, filename, itemset):
        """
        Write a csv file in the 'excel' dialect.

        Parameters:
            filename (str) the full path to the csv file (path/name.csv).
        itemset (list) the set of items to save.

        Returns:
            (bool) True always
        """
        return_value = False
        with open(filename, "w") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self.HEADER_NAMES)
            # write the Item lines to the file
            for item in itemset:
                part = Part(self.parts_file, item.get_part_number(), "part_number")
                self.write_item_line(item, part, writer)
            return_value = True

        return return_value

    def write_item_line(self, item, part, writer):
        """
        Write a line to the csv file.

        Parameters:
            item (Item) to write.
            part (Part) to use for the item description.
            writer (csv.writer) the writer object to write the file
                contents.
        """
        installed = ""
        if item.get_installed():
            installed = "X"

        line = [
            item.get_assembly(),
            item.get_record_id(),
            item.get_part_number(),
            part.get_description(),
            item.get_quantity(),
            item.get_condition(),
            installed,
            item.get_remarks(),
            part.get_remarks(),
        ]
        writer.writerow(line)
