"""
The PartsTracker Dialogs Collection.

This module contains the following classes:
    AssemblyListDialog - Write a Comma Separated Values (CSV) file of
        selected portions of the listing
    BaseDialog - Base class for all dialogs.
    EditConditionsDialog - Change the set of available Item Conditions
    EditSourcesDialog - Edit the set of Part Sources 
    ItemDialog - Edit an Item in the parts file.
    PartDialog - Edit a Part in the parts file.
    OrderDialog - Edit an Order in the parts file.

File       __init__.py
Author     Lorn B Kerr
Copyright  (c) 2020-2024 Lorn B Kerr
License:    MIT, see file License
Version:    1.0.0
"""

from .assembly_list_dialog import AssemblyListDialog
from .base_dialog import BaseDialog
from .edit_conditions_dialog import EditConditionsDialog
from .edit_sources_dialog import EditSourcesDialog
from .item_dialog import ItemDialog
from .order_dialog import OrderDialog
from .part_dialog import PartDialog

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}
