"""
Edit the set of possible Item conditions.

File:       edit_conditions_dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2024 Lorn B Kerr
License:    MIT, see file License
Version:    1.1.0
"""

from lbk_library import DataFile as PartsFile
from lbk_library.gui import Dialog, TableModel
from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QHeaderView, QMainWindow

from elements import Condition, ConditionSet
from forms import Ui_TableDialog

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
    "1.1.0": "Changed library 'PyQt5' to 'PySide6' and code cleanup",
}


class EditConditionsDialog(Dialog, Ui_TableDialog):
    """
    Edit the set of possible Item conditions.

    Each item in the data base has a Usability condition assigned. These
    conditions range from "Usable" to "Replace".
    """

    ALIGNMENTS = [
        Qt.AlignmentFlag.AlignLeft,
        Qt.AlignmentFlag.AlignLeft,
    ]
    """The alignments for each of the columns."""
    COLUMN_NAMES = ["record_id", "condition"]
    """The data names for each of the columns."""
    COLUMN_WIDTHS = [70, 130]
    """The initial widths for each column."""
    HEADER_TITLES = ["Record Id", "Condition"]
    """The titles for each of the columns."""
    TOOLTIPS = [
        "Record Id is automatically set.",
        "Required: Edit or add an item condition,",
    ]
    """Tooltips for each of the visible elements on the form."""
    NORMAL_BACKGROUND = QBrush(QColor("white"))
    ERROR_BACKGROUND = QBrush(QColor(0xF0C0C0))

    def __init__(self, parent: QMainWindow, parts_file: PartsFile) -> None:
        """
        Initialize the dialog.

        Parameters:
            parent (QMainWindow:) the owning dialog
            parts_file (PartsFile) reference to the current open data file.
        """
        super().__init__(parent, parts_file, None)
        self.setupUi(self)

        self.parts_file = parts_file
        self.conditions = ConditionSet(parts_file)
        self.condition_list = self.conditions.get_property_set()
        self.dataset = self.build_data_set()

        self.table = self.table_view
        self.model = TableModel(
            self.dataset,
            self.HEADER_TITLES,
            self.TOOLTIPS,
            self.ALIGNMENTS,
            self.NORMAL_BACKGROUND,
        )
        self.table.setModel(self.model)
        self.table.setStyleSheet(
            "QTableView {selection-background-color: white; selection-color: blue;}"
        )

        self.setup_form()
        self.append_row()

        self.record_id_checkbox.stateChanged.connect(self.show_record_id)
        self.model.dataChanged.connect(self.data_changed)
        #        self.complete_button.clicked.connect(self.close_form)

        # this is used in processing the 'dataChanged" signal
        self._change_in_process = False

    def build_data_set(self) -> list[list[str]]:
        """
        Convert the properties of the ConditionSet to a list of lists.

        Returns:
            (list[list[str]]) The set of condition properties as an
                list of lists of strings in table column order.
        """
        data_set = []
        for i in range(len(self.condition_list)):
            a_condition = []
            condition_properties = self.condition_list[i].get_properties()
            for name in self.COLUMN_NAMES:
                a_condition.append(condition_properties[name])
            data_set.append(a_condition)
        return data_set

    def setup_form(self) -> None:
        """Configure the table."""
        self.setWindowTitle("Edit Item Conditions")
        self.form_label.setText("<b>Add</b> or <b>Edit</b> the set of Item Conditions.")

        self.table.verticalHeader().hide()
        self.table.setColumnHidden(self.COLUMN_NAMES.index("record_id"), True)
        for i in range(len(self.COLUMN_WIDTHS)):
            self.table.setColumnWidth(i, self.COLUMN_WIDTHS[i])
        self.table.horizontalHeader().setSectionResizeMode(
            self.HEADER_TITLES.index("Condition"), QHeaderView.ResizeMode.Stretch
        )

    def append_row(self) -> None:
        """
        Append an empty row to the data_set.

        Each column value of this empty line will have the value None.
        """
        self.model.insertRows(self.model.rowCount(), 1)
        self.model.layoutChanged.emit()

    def show_record_id(self) -> None:
        """Show or hide the 'record_id' column in the table."""
        if self.record_id_checkbox.isChecked():
            self.table.setColumnHidden(self.COLUMN_NAMES.index("record_id"), False)
        else:
            self.table.setColumnHidden(self.COLUMN_NAMES.index("record_id"), True)

    def data_changed(self, index: QModelIndex, index2: QModelIndex) -> None:
        """
        Validate the change in a table entry.

        Parameters:
            index (QmodelIndex): the first changed table cell.
            index2 (QModelIndex): the last changed table cell. (not used)
        """
        if self._change_in_process:
            return
        else:
            self._change_in_process = True
            test_result = Condition(self.parts_file).set_condition(
                self.model.data(index, Qt.ItemDataRole.EditRole)
            )
            if test_result["valid"]:
                if index.row() < len(self.condition_list):
                    self.condition_list[index.row()].set_condition(test_result["entry"])
                    self.condition_list[index.row()].update()
                else:
                    new_condition = Condition(self.parts_file)
                    new_condition.set_condition(test_result["entry"])
                    new_condition.add()
                    self.append_row()

                self.model.setData(
                    index,
                    self.TOOLTIPS[index.column()],
                    Qt.ItemDataRole.ToolTipRole,
                )
                self.model.setData(
                    index, self.NORMAL_BACKGROUND, Qt.ItemDataRole.BackgroundRole
                )

            else:
                self.model.setData(
                    index,
                    test_result["msg"] + ", " + self.TOOLTIPS[index.column()],
                    Qt.ItemDataRole.ToolTipRole,
                )
                self.model.setData(
                    index, self.ERROR_BACKGROUND, Qt.ItemDataRole.BackgroundRole
                )
            self._change_in_process = False

    def close_form(self) -> None:
        """
        Close the form when the "close" button is clicked.

        Returns:
            bool True if form closes, false if not.
        """
        return self.close()
