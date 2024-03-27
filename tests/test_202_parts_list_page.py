"""
Test the parts_list_page class.

File:       test_202_parts_list_page.py
Author:     Lorn B Kerr
Copyright:  (c) 2023, 2024 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (  # QMainWindow,; QTreeWidgetItem,; QTreeWidgetItemIterator,
    QTableWidget,
)
from test_setup import (  # build_test_config,; db_open,; directories,; ; part_value_set,; test_config,
    db_close,
    db_create,
    filesystem,
    load_all_db_tables,
    part_value_set,
)

# from lbk_library import Dbal


src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from dialogs import PartDialog
from elements import Part, PartSet  # Item,
from pages import PartsListPage


def setup_page(qtbot, filesystem):
    """Initialize  parts list page for testing"""
    fs_base = filesystem
    parts_file = db_create(fs_base)
    load_all_db_tables(parts_file)
    table = QTableWidget()
    page = PartsListPage(table, parts_file)
    qtbot.addWidget(table)
    return (parts_file, table, page)


def test_202_01_class_type(qtbot, filesystem):
    parts_file, table, page = setup_page(qtbot, filesystem)

    assert isinstance(page, PartsListPage)
    assert page.get_parts_file() == parts_file
    assert type(page.table) == QTableWidget
    assert page.table == table


def test_202_02_set_table_headers(qtbot, filesystem):
    parts_file, table, page = setup_page(qtbot, filesystem)

    page.table.clear()
    page.table.setColumnCount(0)
    assert page.table.columnCount() == 0

    page.set_table_headers()
    assert page.table.columnCount() == len(page.COLUMN_NAMES)
    header = page.table.horizontalHeader()
    for i in range(1, len(page.COLUMN_NAMES) - 1):
        assert (
            header.model().headerData(i, header.orientation()) == page.COLUMN_NAMES[i]
        )
        assert page.table.columnWidth(i) > header.minimumSectionSize()


def test_202_03_update_table(qtbot, filesystem):
    parts_file, table, page = setup_page(qtbot, filesystem)

    part_set = PartSet(parts_file, None, None, "part_number")
    initial_num_parts = page.table.rowCount()
    Part(parts_file, part_value_set[0][1], "part_number").delete()
    Part(parts_file, part_value_set[1][1], "part_number").delete()
    page.update_table()
    assert page.table.rowCount() < initial_num_parts
    assert (initial_num_parts - page.table.rowCount()) == 2
    assert not page.table.findItems(part_value_set[0][1], Qt.MatchExactly)
    assert not page.table.findItems(part_value_set[1][1], Qt.MatchExactly)

    db_close(parts_file)


def test_202_04_clear_table(qtbot, filesystem):
    parts_file, table, page = setup_page(qtbot, filesystem)

    page.clear_table()
    assert page.table.rowCount() == 0
    db_close(parts_file)

    db_close(parts_file)


def test_202_05_action_part_clicked(qtbot, filesystem):
    parts_file, table, page = setup_page(qtbot, filesystem)

    part_item = page.table.itemAt(0, 0)
    dialog = page.action_part_clicked(part_item)
    assert type(dialog) == PartDialog

    db_close(parts_file)


# end
