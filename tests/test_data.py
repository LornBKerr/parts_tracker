"""
Provide common data value sets for the PartsTracker testing.

File:       test_data.py
Author:     Lorn B Kerr
Copyright:  (c) 2024 Lorn B Kerr
License:    MIT, see file License
This provides a complete minimal set of values to use in testing the
various files making up the PartsTracker program.
"""

# Test values for a Condition element

condition_columns = ["record_id", "condition"]
condition_value_set = [
    [1, "Usable"],
    [2, "Replace"],
    [3, "Rebuild"],
    [4, "Missing"],
    [5, "New"],
    [6, "Unknown"],
]

# Test values for an Item element

item_columns = [
    "record_id",
    "part_number",
    "assembly",
    "quantity",
    "condition",
    "installed",
    "box",
    "remarks",
]
item_value_set = [
    [731, "17005", "CAABA", 4, 5, 0, 0, ""],
    [1, "18V672", "A", 1, 3, 1, "", ""],
    [2, "Z005", "B", 1, 1, 0, "", ""],
    [3, "Z006", "C", 1, 1, 0, "", ""],
    [4, "Z007", "CA", 1, 1, 0, "", ""],
    [5, "22H1053", "BB", 1, 1, 0, "", ""],
    [6, "268-090", "BC", 1, 1, 1, "", ""],
    [8, "BTB1108", "BD", 1, 1, 1, "", ""],
    [1370, "17005", "ABFCB", 3, 5, 1, 0, ""],
    [168, "Z001", "AA", 1, 1, 1, 0, ""],
    [172, "12H1387", "AAA", 1, 1, 1, 0, ""],
    [1320, "296-000", "AAAA", 1, 5, 1, 0, ""],
    [1317, "455-390", "AAAB", 1, 1, 1, "", ""],
    [1318, "120-000", "AAABA", 1, 5, 1, 0, ""],
    [1319, "296-340", "AAABB", 1, 5, 1, 0, ""],
    [1322, "17000", "AAABC", 3, 5, 1, 0, ""],
    [1323, "17003", "AAABD", 2, 5, 1, 0, ""],
    [1325, "33078", "AAABE", 5, 5, 1, 0, ""],
    [1326, "33618", "AAABF", 5, 5, 1, 0, ""],
    [1324, "17053", "AAAC", 7, 5, 1, 0, ""],
    [1327, "33080", "AAACA", 7, 5, 1, 0, ""],
    [1328, "33620", "AAACB", 7, 5, 1, 0, ""],
    [173, "460-701", "AAB", 1, 1, 1, 0, ""],
    [181, "120-820", "AABA", 1, 5, 1, 0, "Moss part number 120-820"],
    [182, "120-830", "AABAA", 1, 5, 1, 0, ""],
    [183, "17052", "AABAB", 4, 5, 1, 0, ""],
    [184, "17105", "AABB", 2, 5, 1, 0, "top two bolts on rear plate"],
    [185, "33622", "AABBA", 2, 5, 1, 0, ""],
    [186, "17105", "AABC", 8, 5, 1, 0, ""],
    [187, "33622", "AABCA", 8, 5, 1, 0, ""],
    [193, "297-495", "AABD", 1, 5, 1, 0, ""],
]

# Test values for an Order element

order_columns = [
    "record_id",
    "order_number",
    "date",
    "source",
    "remarks",
    "subtotal",
    "shipping",
    "tax",
    "discount",
    "total",
]
order_value_set = [
    [
        13,
        "06-013",
        "2006-08-22",
        1,
        "a remark",
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ],
    [14, "06-015", "2006-12-04", 6, "", 0.0, 0.0, 0.0, 0.0, 0.0],
    [
        15,
        "06-016",
        "2006-05-05",
        3,
        "",
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ],
    [
        16,
        "07-001",
        "2007-07-02",
        3,
        "",
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ],
    [
        17,
        "07-002",
        "2007-09-28",
        3,
        "",
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ],
    [
        18,
        "07-003",
        "2007-12-06",
        3,
        "",
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ],
    [19, "07-004", "2007-12-19", "", "", 0.0, 0.0, 0.0, 0.0, 0.0],
    [41, "09-012", "2009-08-17", 5, "", 0.0, 0.0, 0.0, 0.0, 0.0],
]

# Test values for an OrderLine element

order_line_columns = [
    "record_id",
    "order_number",
    "line",
    "part_number",
    "cost_each",
    "quantity",
    "remarks",
]
order_line_value_set = [
    [27, "06-015", 1, "373-830", 23.5, 1, ""],
    [28, "06-015", 2, "Z0033", 91.0, 1, "P/N Replaced by ZE005"],
    [
        29,
        "07-001",
        1,
        "267-995",
        13.0,
        1,
        "Used as core for new shocks from NOSIMPORTS",
    ],
    [
        30,
        "07-001",
        2,
        "267-985",
        13.0,
        1,
        "Used as core for new shocks from NOSIMPORTS",
    ],
    [31, "07-002", 1, "458-885", 187.5, 1, "includes shipping"],
    [32, "07-002", 2, "458-875", 187.5, 1, "includes shipping"],
    [33, "07-003", 1, "X5005", 800.0, 1, ""],
    [159, "09-012", 1, "17000", 0.138, 37, ""],
]

# Test values for an Part element

part_columns = ["record_id", "part_number", "source", "description", "remarks"]
part_value_set = [
    [64, "17000", 5, "Bolt, Hex Cap, 1/4-28 X 3/8, Grade 5, Zinc", ""],
    [67, "17003", 5, "Bolt, Hex Cap, 1/4-28 x 0.75, Grade 5 Zinc", ""],
    [
        69,
        "17005",
        5,
        "Bolt, Hex Cap, 1/4-28 x 1, Grade 5, Zinc",
        "Moss P/N 324-247",
    ],
    [73, "17052", 5, "Bolt, Hex Cap, 5/16-24 x 0.625, Grade 5, Zinc", ""],
    [74, "17053", 5, "Bolt, Hex Cap, 5/16-24 x 0.75, Grade 5, Zinc", ""],
    [84, "17105", 5, "Bolt, Hex Cap, 3/8-24 x 1.0, Grade 5, Zinc", "a part"],
    [95, "33078", 5, "Washer, Flat, 1/4, Zinc", ""],
    [96, "33080", 5, "Washer, Flat, 5/16, Zinc", "Moss P/N 365-720"],
    [100, "33618", 5, "Washer, Lock, Split, 1/4, Zinc", "Moss P/N 324-020"],
    [101, "33620", 5, "Washer, Lock, Split, 5/16, Zinc", "Moss P/N 365-730"],
    [102, "33622", 5, "Washer, Lock, Split, 3/8, Zinc", "Moss P/N 324-040"],
    [427, "267-995", 1, "Shock, LHS, Rebuilt", ""],
    [1946, "18V672", 2, "Engine, 18V, 1971-1974", ""],
    [1947, "Z001", 2, "Block, Engine", ""],
    [1920, "12H1387", "", "Plate, Engine, Front", ""],
    [1921, "460-701", 1, "Back Plate", ""],
    [149, "120-820", 1, "Oil Seal, Rear Main", ""],
    [150, "120-830", 1, "Retainer, Oil Seal", ""],
    [
        "477",
        "296-000",
        1,
        "Gasket, Front Plate to Block",
        "Part of Moss P/N 297-521, Conversion Gasket Set",
    ],
    [826, "455-390", 1, "Cover, Timing", ""],
    [1680, "120-000", 1, "Oil Seal, Crankshaft, Front", ""],
    [
        481,
        "296-340",
        1,
        "Gasket, Timing Cover",
        "Part of Moss P/N 297-521, Conversion Gasket Set",
    ],
    [
        517,
        "320-125",
        1,
        "Bolt, Hex Cap, 3/8-24 x 1.000, Grade 5",
        "Replaced by Fastenal P/N 17105",
    ],
    [491, "297-495", 1, "Cover, Gearbox Mount Plate", ""],
    [1951, "Z005", 2, "Drive Train", ""],
    [1955, "Z006", 2, "Cooling and Heating System", ""],
    [1952, "22H1053", 2, "Gearbox", ""],
    [432, "268-090", 1, "Drive Shaft", ""],
    [1954, "BTB1108", 2, "Rear Axle", ""],
]

# Test values for a Source element

source_columns = ["record_id", "source"]
source_value_set = [
    [1, "British Car Parts"],
    [2, "None"],
    [3, "Local Purchase"],
    [4, "Tire Store"],
    [5, "Screw Shop"],
    [6, "Ebay"],
]
