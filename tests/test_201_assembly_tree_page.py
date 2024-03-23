"""
Test the assembly_tree_page class.

File:       test_201_assembly_tree_page.py
Author:     Lorn B Kerr
Copyright:  (c) 2023, 2024 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

#from PyQt5 import uic
#from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from test_setup import (
    db_create,
    filesystem,
    item_value_set,
    load_all_db_tables,
)

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from dialogs import ItemDialog
from elements import Item, ItemSet, Part
from pages import AssemblyTreePage      #, MainWindow


def setup_page(qtbot, filesystem):
    """Initialize an assembly page for testing"""
    fs_base = filesystem
    parts_file = db_create(fs_base)
    load_all_db_tables(parts_file)
    tree = QTreeWidget()
    page = AssemblyTreePage(tree, parts_file)
    qtbot.addWidget(tree)
    return (parts_file, tree, page)


def test_201_01_class_type(qtbot, filesystem):
    parts_file, tree, page = setup_page(qtbot, filesystem)
    assert isinstance(page, AssemblyTreePage)
    assert page.get_parts_file() == parts_file
    assert type(page.tree) == QTreeWidget
    assert page.tree == tree


def test_201_02_resize_columns(qtbot, filesystem):
    parts_file, tree, page = setup_page(qtbot, filesystem)
    # delete existing tree headings and entries
    page.tree.clear()
    blank_header = [None, None, None, None, None, None, None]
    page.tree.setColumnCount(len(AssemblyTreePage.COL_NAMES))
    page.tree.setHeaderLabels(blank_header)
    page.resize_columns()
    for i in range(0, len(blank_header) - 1):
        assert page.tree.columnWidth(i) == page.tree.header().minimumSectionSize()
    page.tree.setHeaderLabels(AssemblyTreePage.COL_NAMES)
    page.resize_columns()
    for i in range(0, len(AssemblyTreePage.COL_NAMES) - 1):
        assert page.tree.columnWidth(i) > page.tree.header().minimumSectionSize()


def test_201_03_set_tree_headers(qtbot, filesystem):
    parts_file, tree, page = setup_page(qtbot, filesystem)
    page.tree.clear()
    blank_header = [None, None, None, None, None, None, None]
    page.tree.setColumnCount(len(AssemblyTreePage.COL_NAMES))
    page.tree.setHeaderLabels(blank_header)
    page.resize_columns()
    page.set_tree_headers()
    assert page.tree.columnCount() == len(page.COL_NAMES)
    header = page.tree.header()
    for i in range(0, len(page.COL_NAMES) - 1):
        assert header.model().headerData(i, header.orientation()) == page.COL_NAMES[i]
        assert page.tree.columnWidth(i) > page.tree.header().minimumSectionSize()


def test_201_04_set_part_description(qtbot, filesystem):
    parts_file, tree, page = setup_page(qtbot, filesystem)
    item_number = item_value_set[0][0]
    part_number = item_value_set[0][1]
    item = Item(parts_file, item_number)
    part = Part(parts_file, item.get_part_number(), "part_number")
    item_properties = page.set_part_description(item.get_properties())
    assert item_properties["description"] == part.get_description()


def test_201_05_set_installed_entry(qtbot, filesystem):
    parts_file, tree, page = setup_page(qtbot, filesystem)
    item_number = item_value_set[0][0]
    item = Item(parts_file, item_number)
    item.set_installed(True)
    item_properties = page.set_installed_entry(item.get_properties())
    assert item_properties["installed"] == "Yes"
    item.set_installed(False)
    item_properties = page.set_installed_entry(item.get_properties())
    assert item_properties["installed"] == ""


def test_201_06_set_item_values(qtbot, filesystem):
    parts_file, tree, page = setup_page(qtbot, filesystem)
    item_number = item_value_set[0][0]
    item = Item(parts_file, item_number)
    item_properties = page.set_part_description(item.get_properties())
    item_properties = page.set_installed_entry(item_properties)
    item_values = page.set_item_values(item_properties)
    for value in item_values:
        assert type(value) is str


def test_201_07_find_parent_assy(qtbot, filesystem):
    parts_file, tree, page = setup_page(qtbot, filesystem)
    tree_items = {}
    assembly = "A"
    parent = page.find_parent_assy(assembly, tree_items)
    assert parent is None
    tree_items[assembly] = parent
    assembly = "AAA"
    parent = page.find_parent_assy(assembly, tree_items)
    assert parent == "A"
    tree_items[assembly] = parent
    assembly = "HHH"
    parent = page.find_parent_assy(assembly, tree_items)
    assert parent is None
    tree_items[assembly] = parent


def test_201_08_add_item_to_tree(qtbot, filesystem):
    parts_file, tree, page = setup_page(qtbot, filesystem)
    tree_items = {}
    item_set = ItemSet(parts_file, None, None, "assembly")
    item = item_set.get(0)
    item_properties = page.set_part_description(item.get_properties())
    assembly1 = item_properties["assembly"]
    item_properties = page.set_installed_entry(item_properties)
    item_values = page.set_item_values(item_properties)
    parent = page.find_parent_assy(assembly1, tree_items)
    tree_items = page.add_item_to_tree(assembly1, item_values, parent, tree_items)
    assert tree_items[assembly1].parent() is None
    item = item_set.get(1)
    item_properties = page.set_part_description(item.get_properties())
    assembly2 = item_properties["assembly"]
    item_properties = page.set_installed_entry(item_properties)
    item_values = page.set_item_values(item_properties)
    parent = page.find_parent_assy(assembly2, tree_items)
    tree_items = page.add_item_to_tree(assembly2, item_values, parent, tree_items)
    assert tree_items[assembly2].parent() == tree_items[assembly1]


def test_201_09_fill_tree_widget(qtbot, filesystem):
    parts_file, tree, page = setup_page(qtbot, filesystem)
    item_set = ItemSet(parts_file, None, None, "assembly")
    tree_items = page.fill_tree_widget(item_set)
    assert type(tree_items["A"]) is QTreeWidgetItem
    assert tree_items["AA"].parent() == tree_items["A"]
    assert len(tree_items) == len(item_value_set)


def test_201_10_update_tree(qtbot, filesystem):
    parts_file, tree, page = setup_page(qtbot, filesystem)
    item_set = ItemSet(parts_file, None, None, "assembly")
    tree_items = page.fill_tree_widget(item_set)
    init_num_items = len(tree_items)
    Item(parts_file, 1370).delete()
    Item(parts_file, 1328).delete()
    tree_items = page.update_tree()
    assert len(tree_items) < init_num_items
    assert (init_num_items - len(tree_items)) == 2
    assert not "ABFCB" in tree_items.keys()
    assert not "AAACB" in tree_items.keys()


def test_201_11_clear_tree(qtbot, filesystem):
    parts_file, tree, page = setup_page(qtbot, filesystem)
    item_set = ItemSet(parts_file, None, None, "assembly")
    tree_items = page.fill_tree_widget(item_set)
    top_item_count = page.tree.topLevelItemCount()
    assert top_item_count > 0
    page.clear_tree()
    top_item_count = page.tree.topLevelItemCount()
    assert top_item_count == 0


def test_201_12_action_item_clicked(qtbot, filesystem):
    parts_file, tree, page = setup_page(qtbot, filesystem)

    item_set = ItemSet(parts_file, None, None, "assembly")
    page.fill_tree_widget(item_set)
    item = page.tree.itemAt(0, 0)
    dialog = page.action_item_clicked(item, 0)
    assert type(dialog) == ItemDialog

