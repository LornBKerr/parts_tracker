"""
Provide common support functionality for several test files.
"""
# import os
# import pathlib
# import sys
# import time
import pathlib

import pytest

# Directories for Windows and Linux
directories = [
    ".config",
    "Documents",
    "Documents/parts_tracker",
]

# a basic empty config file for part_tracker testing.
test_config = {
    "settings": {
        "recent_files": [],
        "xls_file_loc": "",
    }
}


@pytest.fixture
def filesystem(tmp_path):
    """
    Setup a temporary filesystem which will be discarded after the test
    sequence is run.

    'source' is the directory structure for saving and retrieving data
    with tow directories: '.config' and 'Documents'. This directory
    structure will be discarded after the test sequence is run.

    Parameters:
        tmp_path: pytest fixture to setup a path to a temperary location

    Returns:
        ( pathlib.Path ) The temparary file paths to use.
    """
    source = tmp_path / "source"
    source.mkdir()

    # make a set of source directories and files
    for dir in directories:
        a_dir = source / dir
        a_dir.mkdir()

    fp = open(source / "Documents/parts_tracker/test_file1.db", "w")
    fp.close()
    fp = open(source / "Documents/parts_tracker/test_file2.db", "w")
    fp.close()

    return source
