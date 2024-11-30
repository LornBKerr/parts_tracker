"""
Edit the set of possible Part source.

File:       edit_sources_dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2024 Lorn B Kerr
License:    MIT, see file License
Version:    1.0.0
"""

from lbk_library import DataFile as PartsFile
from lbk_library.gui import Dialog, TableModel
from PyQt6 import uic
from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import QHeaderView, QMainWindow

from elements import Source, SourceSet

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}


class EditSourcesDialog(Dialog):
    """
    Edit the set of possible Part sources.

    Each part in the data base has a source assigned. In general, the
    source is where the part was purchsed
    """

    ALIGNMENTS = [
        Qt.AlignmentFlag.AlignLeft,
        Qt.AlignmentFlag.AlignLeft,
    ]
    """The alignments for each of the columns."""
    COLUMN_NAMES = ["record_id", "source"]
    """The data names for each of the columns."""
    COLUMN_WIDTHS = [70, 130]
    """The initial widths for each column."""
    HEADER_TITLES = ["Record Id", "Source"]
    """The titles for each of the columns."""
    TOOLTIPS = [
        "Record Id is automatically set.",
        "Required: Edit or add a part source,",
    ]
    """Tooltips for each of the visible elements on the form."""
    NORMAL_BACKGROUND = QBrush(QColor("white"))
    ERROR_BACKGROUND = QBrush(QColor(0xF0C0C0))

    def __init__(self, parent: QMainWindow, parts_file: PartsFile) -> None:
        """
        Initialize the dialog.

        Parameters:
            parent (QMainWindow) The owning widnow for this dialog.
            parts_file (PartsFile) reference to the current open data file.
        """
        super().__init__(parent, parts_file, None)
        self.parts_file = parts_file
        self.form = uic.loadUi("./src/forms/simple_tableview.ui", self)
        self.sources = SourceSet(parts_file)
        self.source_list = self.sources.get_property_set()
        self.dataset = self.build_data_set()

        self.table = self.form.table_view
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
        self.complete_button.clicked.connect(self.close_form)

        # this is used in processing the 'dataChanged" signal
        self.__change_in_process = False

    def build_data_set(self) -> list[list[str]]:
        """
        Convert the properties of the SourceSet to a list of lists.

        Returns:
            (list[list[str]]) The set of source properties as an
                list of lists of strings in table column order.
        """
        data_set = []
        for i in range(len(self.source_list)):
            a_source = []
            source_properties = self.source_list[i].get_properties()
            for name in self.COLUMN_NAMES:
                a_source.append(source_properties[name])
            data_set.append(a_source)
        return data_set

    def setup_form(self) -> None:
        """Configure the table."""
        self.form.setWindowTitle("Edit Part Sources")
        self.form.form_label.setText(
            "<b>Add</b> or <b>Edit</b> the set of Part Sources."
        )

        font = self.form.copyright_label.font()
        font.setPointSize(7)
        self.form.copyright_label.setFont(font)

        self.table.verticalHeader().hide()
        self.table.setColumnHidden(self.COLUMN_NAMES.index("record_id"), True)
        for i in range(len(self.COLUMN_WIDTHS)):
            self.table.setColumnWidth(i, self.COLUMN_WIDTHS[i])
        self.table.horizontalHeader().setSectionResizeMode(
            self.HEADER_TITLES.index("Source"), QHeaderView.ResizeMode.Stretch
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
        if self.__change_in_process:
            return
        else:
            self.__change_in_process = True
            test_result = Source(self.parts_file).set_source(
                self.model.data(index, Qt.ItemDataRole.EditRole)
            )

            if test_result["valid"]:
                if index.row() < len(self.source_list):
                    self.source_list[index.row()].set_condition(test_result["entry"])
                    self.source_list[index.row()].update()
                else:
                    new_source = Source(self.parts_file)
                    new_source.set_source(test_result["entry"])
                    new_source.add()

                self.model.setData(
                    index,
                    self.TOOLTIPS[index.column()],
                    Qt.ItemDataRole.ToolTipRole,
                )
                self.model.setData(
                    index, self.NORMAL_BACKGROUND, Qt.ItemDataRole.BackgroundRole
                )
                self.append_row()
            else:
                self.model.setData(
                    index,
                    test_result["msg"] + ", " + self.TOOLTIPS[index.column()],
                    Qt.ItemDataRole.ToolTipRole,
                )
                self.model.setData(
                    index, self.ERROR_BACKGROUND, Qt.ItemDataRole.BackgroundRole
                )

            self.__change_in_process = False

    def close_form(self) -> None:
        """Close the form when the "close" button is clicked."""
        self.close()
