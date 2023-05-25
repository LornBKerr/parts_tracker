"""
Test the assembly_tree_page class.

File:       test_201_assembly_tree_page.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

# import pytest
from lbk_library import Dbal
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QTreeWidget,
    QTreeWidgetItem,
    QTreeWidgetItemIterator,
)
from test_setup import (
    build_test_config,
    db_create,
    db_open,
    directories,
    filesystem,
    item_value_set,
    load_all_db_tables,
    part_value_set,
    test_config,
)

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from dialogs import ItemDialog
from elements import Item, ItemSet, Part
from pages import AssemblyTreePage, MainWindow


def setup_page(db_create, qtbot):
    """Initialize an assembly page for testing"""
    dbref = db_create
    load_all_db_tables(dbref)
    form = uic.loadUi("src/forms/main_window.ui")
    page = AssemblyTreePage(form, dbref)
    qtbot.addWidget(form)
    return (dbref, form, page)


def test_201_01_class_type(db_create, qtbot):
    dbref, form, page = setup_page(db_create, qtbot)
    assert isinstance(page, AssemblyTreePage)
    assert page.get_dbref() == dbref
    assert type(page.tree) == QTreeWidget
    assert page.form == form
    assert type(page.tree) is QTreeWidget


def test_201_02_resize_columns(db_create, qtbot):
    dbref, form, page = setup_page(db_create, qtbot)
    # delete existing tree headings and entries
    page.tree.clear()
    blank_header = [None, None, None, None, None, None, None]
    page.tree.setColumnCount(len(AssemblyTreePage.COL_NAMES))
    page.tree.setHeaderLabels(blank_header)
    page.resize()
    for i in range(0, len(blank_header) - 1):
        assert page.tree.columnWidth(i) == page.tree.header().minimumSectionSize()
    page.tree.setHeaderLabels(AssemblyTreePage.COL_NAMES)
    page.resize()
    for i in range(0, len(AssemblyTreePage.COL_NAMES) - 1):
        assert page.tree.columnWidth(i) > page.tree.header().minimumSectionSize()


def test_201_03_set_tree_headers(db_create, qtbot):
    dbref, form, page = setup_page(db_create, qtbot)
    page.tree.clear()
    blank_header = [None, None, None, None, None, None, None]
    page.tree.setColumnCount(len(AssemblyTreePage.COL_NAMES))
    page.tree.setHeaderLabels(blank_header)
    page.resize()
    page.set_tree_headers()
    assert page.tree.columnCount() == len(page.COL_NAMES)
    header = page.tree.header()
    for i in range(0, len(page.COL_NAMES) - 1):
        assert header.model().headerData(i, header.orientation()) == page.COL_NAMES[i]
        assert page.tree.columnWidth(i) > page.tree.header().minimumSectionSize()


def test_201_03_set_part_description(db_create, qtbot):
    dbref, form, page = setup_page(db_create, qtbot)
    item_number = item_value_set[0][0]
    part_number = item_value_set[0][1]
    item = Item(dbref, item_number)
    part = Part(dbref, item.get_part_number(), "part_number")
    item_properties = page.set_part_description(item.get_properties())
    assert item_properties["description"] == part.get_description()


def test_201_04_set_installed_entry(db_create, qtbot):
    dbref, form, page = setup_page(db_create, qtbot)
    item_number = item_value_set[0][0]
    item = Item(dbref, item_number)
    item.set_installed(True)
    item_properties = page.set_installed_entry(item.get_properties())
    assert item_properties["installed"] == "Yes"
    item.set_installed(False)
    item_properties = page.set_installed_entry(item.get_properties())
    assert item_properties["installed"] == ""


def test_201_05_set_item_values(db_create, qtbot):
    dbref, form, page = setup_page(db_create, qtbot)
    item_number = item_value_set[0][0]
    item = Item(dbref, item_number)
    item_properties = page.set_part_description(item.get_properties())
    item_properties = page.set_installed_entry(item_properties)
    item_values = page.set_item_values(item_properties)
    for value in item_values:
        assert type(value) is str


def test_201_06_find_parent_assy(db_create, qtbot):
    dbref, form, page = setup_page(db_create, qtbot)
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


def test_201_07_add_item_to_tree(db_create, qtbot):
    dbref, form, page = setup_page(db_create, qtbot)
    tree_items = {}
    item_set = ItemSet(dbref, None, None, "assembly")
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


def test_201_09_fill_tree_widget(db_create, qtbot):
    dbref, form, page = setup_page(db_create, qtbot)
    item_set = ItemSet(dbref, None, None, "assembly")
    tree_items = page.fill_tree_widget(item_set)
    assert type(tree_items["A"]) is QTreeWidgetItem
    assert tree_items["AA"].parent() == tree_items["A"]
    assert len(tree_items) == len(item_value_set)


def test_201_10_update_tree(db_create, qtbot):
    dbref, form, page = setup_page(db_create, qtbot)
    item_set = ItemSet(dbref, None, None, "assembly")
    tree_items = page.fill_tree_widget(item_set)
    init_num_items = len(tree_items)
    Item(dbref, 1370).delete()
    Item(dbref, 1328).delete()
    tree_items = page.update_tree()
    assert len(tree_items) < init_num_items
    assert (init_num_items - len(tree_items)) == 2
    assert not "ABFCB" in tree_items.keys()
    assert not "AAACB" in tree_items.keys()


def test_201_11_clear_tree(db_create, qtbot):
    dbref, form, page = setup_page(db_create, qtbot)
    item_set = ItemSet(dbref, None, None, "assembly")
    tree_items = page.fill_tree_widget(item_set)
    top_item_count = page.tree.topLevelItemCount()
    assert top_item_count > 0
    page.clear_tree()
    top_item_count = page.tree.topLevelItemCount()
    assert top_item_count == 0


def test_201_12_action_expand(db_create, qtbot):
    dbref, form, page = setup_page(db_create, qtbot)
    item_set = ItemSet(dbref, None, None, "assembly")
    page.fill_tree_widget(item_set)

    collapsed_width = page.tree.columnWidth(0)
    page.tree.expandAll()
    expanded_width = page.tree.columnWidth(0)
    assert expanded_width >= collapsed_width

    page.tree.clear()
    page.fill_tree_widget(item_set)
    page.form.button_expand_tree.click()
    expanded_width = page.tree.columnWidth(0)
    assert expanded_width >= collapsed_width


def test_201_13_action_collapse(db_create, qtbot):
    dbref, form, page = setup_page(db_create, qtbot)
    item_set = ItemSet(dbref, None, None, "assembly")
    page.fill_tree_widget(item_set)
    collapsed_width = page.tree.columnWidth(0)

    page.form.button_expand_tree.click()
    expanded_width = page.tree.columnWidth(0)
    assert expanded_width >= collapsed_width

    page.tree.collapseAll()
    new_width = page.tree.columnWidth(0)
    assert not new_width == collapsed_width

    page.form.button_collapse_tree.click()
    recollapsed_width = page.tree.columnWidth(0)
