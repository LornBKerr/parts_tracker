"""
The PartsTracker Dialogs Collection.

This module contains the following classes:
    BaseDialog extends lbk_library.Dialog - Base class for the set
        of dialogs.
    EditStructureDialog extends BaseDialog) - Change the Assembly structure.
    ItemDialog extends BaseDialog - Edit an Item in the database.
    PartDialog(BaseDialog) - Edit a Part in the database.

File       __init__.py
Author     Lorn B Kerr
Copyright  (c) 2020-2023 Lorn B Kerr
License:    MIT, see file License
"""
#   SaveAssyListDialog -  Write an Excel (XLSX) compatible or Comma Separated
#                         Values (CSV) file of selected portions of the listing
#   ChangePartNumberDialog - Change a Part Number in the database.

from .base_dialog import BaseDialog
from .edit_structure_dialog import EditStructureDialog
from .item_dialog import ItemDialog
from .save_assy_list_dialog import SaveAssyListDialog

# from .part_dialog import PartDialog
