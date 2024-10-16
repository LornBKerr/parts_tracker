# """
# Provide common values and functionality for the PartsTracker testing.
#
# File:       test_setup_elements.py
# Author:     Lorn B Kerr
# Copyright:  (c) 2022, 2024 Lorn B Kerr
# License:    MIT, see file License
#
## This module provides a number of values and functions to help setup the
## test environment for the parts tracker program. All test modules draw on
## a varying selection of these values.
##
## Values Available:
##    condition_columns, condition_value_set: columns andv values for the
##        'condition' db table.
##    item_columns, item_value_set: columns and values for the
##        'item' table.
##    order_columns, order_value_set: columns and values for the
##        'order' table.
##    order_line_columns, order_line_value_set: columns and values for the
##        'order_line' table.
##    part_columns, part_value_set: columns and values for the 'part' table.
##    source_columns, source_value_set: : columns and values for the
##        'source' table.
# """
#
## import os
## from copy import deepcopy
## from pathlib import Path
# from typing import TextIO
#
# import pytest
# from lbk_library import DataFile
from lbk_library.testing_support import load_datafile_table
from PyQt5.QtCore import QSettings

#
## from PyQt5 import QtWidgets
##
from test_data import (
    condition_columns,
    condition_value_set,
    item_columns,
    item_value_set,
    order_columns,
    order_line_columns,
    order_line_value_set,
    order_value_set,
    part_columns,
    part_value_set,
    source_columns,
    source_value_set,
)

# test file name
datafile_name = "test_file.parts"

# Directories for Windows and Linux
directories = [
    ".config",
    "Documents",
    "Documents/parts_tracker",
]

saved_config_file = QSettings("Unnamed Branch", "PartsTrackerSaved")


def save_config_file(original_config_file):
    # Need to save and restore the existing config file so we don't
    # overwrite it during testing.
    for group in original_config_file.childGroups():
        saved_config_file.beginGroup(group)
        original_config_file.beginGroup(group)
        for key in original_config_file.childKeys():
            saved_config_file.setValue(key, original_config_file.value(key))
        original_config_file.endGroup()
        saved_config_file.endGroup()


def restore_config_file(original_config_file):
    # Restore the config file contents from the previously stored values
    for group in saved_config_file.childGroups():
        saved_config_file.beginGroup(group)
        original_config_file.beginGroup(group)
        for key in original_config_file.childKeys():
            original_config_file.setValue(key, saved_config_file.value(key))
        original_config_file.endGroup()
        saved_config_file.endGroup()


def load_all_datafile_tables(test_file):
    load_datafile_table(test_file, "conditions", condition_columns, condition_value_set)
    load_datafile_table(test_file, "items", item_columns, item_value_set)
    load_datafile_table(test_file, "parts", part_columns, part_value_set)
    load_datafile_table(test_file, "orders", order_columns, order_value_set)
    load_datafile_table(
        test_file, "order_lines", order_line_columns, order_line_value_set
    )
    load_datafile_table(test_file, "sources", source_columns, source_value_set)
