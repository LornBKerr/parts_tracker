"""
Define the PartsTracker database table as a sequence of sql statements.

File:       parts_table_definition.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2024 Lorn B Kerr
License:    MIT, see file License
Version:    1.0.0
"""

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}

table_definition = [
    (
        'CREATE TABLE "conditions" '
        "(record_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
        'condition TEXT DEFAULT "")'
    ),
    (
        'CREATE TABLE "items" '
        "(record_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
        'part_number TEXT DEFAULT "", '
        'assembly TEXT DEFAULT "", '
        "quantity INTEGER DEFAULT 0, "
        "condition INTEGER DEFAULT 0, "
        "installed INTEGER DEFAULT 0, "
        "box INTEGER DEFAULT 0, "
        'remarks TEXT DEFAULT "")'
    ),
    (
        'CREATE TABLE "order_lines" '
        "(record_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
        'order_number TEXT DEFAULT "", '
        "line INTEGER DEFAULT 0, "
        'part_number TEXT DEFAULT "", '
        "cost_each FLOAT DEFAULT 0.0, "
        "quantity INTEGER DEFAULT 0, "
        'remarks TEXT DEFAULT "")'
    ),
    (
        'CREATE TABLE "orders" '
        "(record_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
        'order_number TEXT DEFAULT "" UNIQUE, '
        'date TEXT DEFAULT "", '
        "source INTEGER DEFAULT 0, "
        "subtotal FLOAT DEFAULT 0.0, "
        "shipping FLOAT DEFAULT 0.0, "
        "tax FLOAT DEFAULT 0.0, "
        "discount FLOAT DEFAULT 0.0, "
        "total FLOAT DEFAULT 0.0, "
        'remarks TEXT DEFAULT "")'
    ),
    (
        'CREATE TABLE "parts" '
        "(record_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
        'part_number TEXT DEFAULT "", '
        "source INTEGER DEFAULT 0, "
        'description TEXT DEFAULT "", '
        'remarks TEXT DEFAULT "")'
    ),
    (
        'CREATE TABLE "sources" '
        "(record_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
        'source TEXT DEFAULT "")'
    ),
    "CREATE INDEX idx_item_assembly ON items (assembly)",
    "CREATE INDEX idx_item_condition ON items (condition)",
    "CREATE INDEX idx_item_installed ON items (installed)",
    "CREATE INDEX idx_item_part_number ON items (part_number)",
    "CREATE INDEX idx_order_line_line ON order_lines (line)",
    "CREATE INDEX idx_order_line_order_number ON order_lines (order_number)",
    "CREATE INDEX idx_order_line_part_number ON order_lines (part_number)",
    "CREATE INDEX idx_orders_company ON orders (source)",
    "CREATE INDEX idx_orders_date ON orders (date)",
    "CREATE INDEX idx_orders_order_number ON orders (order_number)",
    "CREATE INDEX idx_part_description ON parts (description)",
    "CREATE INDEX idx_part_part_number ON parts (part_number)",
    "CREATE INDEX idx_part_source ON parts (source)",
]
