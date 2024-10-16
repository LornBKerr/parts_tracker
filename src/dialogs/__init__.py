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
Copyright  (c) 2020-2024 Lorn B Kerr
License:    MIT, see file License
Version:    1.0.0
"""

# SaveAssyListDialog -  Write an Excel (XLSX) compatible or Comma Separated
#                         Values (CSV) file of selected portions of the listing
#   ChangePartNumberDialog - Change a Part Number in the database.

from .assembly_list_dialog import AssemblyListDialog
from .base_dialog import BaseDialog
from .change_part_number_dialog import ChangePartNumberDialog
from .edit_conditions_dialog import EditConditionsDialog
from .edit_sources_dialog import EditSourcesDialog
from .edit_structure_dialog import EditStructureDialog
from .item_dialog import ItemDialog
from .order_dialog import OrderDialog
from .part_dialog import PartDialog

# from .conditions_table_model import ConditionsTableModel
# from .element_table_model import ElementTableModel
# from .sources_table_model import SourcesTableModel

# from .comboboxdelegate import ComboBoxDelegate
# from .table_button import TableButton
# from .table_button_group import TableButtonGroup
# from .table_model import TableModel

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}
