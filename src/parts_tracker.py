"""
Run the 'Parts Tracker' Application.

File:       PartsTracker.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file License
Version:    1.0.0
"""

import sys

from PyQt6.QtWidgets import QApplication

from pages import MainWindow

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    # handle the system close button and exit commands
    app.aboutToQuit.connect(main_window.exit_app_action)
    sys.exit(app.exec())
