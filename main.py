# -*- coding: utf-8 -*-
import os
import sys
from PySide6.QtWidgets import QApplication
from libs.rwr_window_tool import RWRWindowToolApp

script_folder_path = os.path.split(os.path.realpath(sys.argv[0]))[0]

if __name__ == "__main__":
    app = QApplication([])
    rwr_window_tool = RWRWindowToolApp(script_folder_path)
    app.exec()