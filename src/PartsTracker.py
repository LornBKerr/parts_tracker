"""
Run the 'Parts Tracker' Application

File:       PartsTracker.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file License 
"""

import sys

from PyQt6.QtWidgets import QApplication

from pages import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow(app)
    sys.exit(app.exec())
