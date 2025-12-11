# -*- coding: utf-8 -*-
import os
import sys
import qdarkstyle
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication, QTranslator
from libs.rwr_window_tool import RWRWindowToolApp
from libs.win32_singleton import Win32SingletonManager
from libs.user_locale import get_user_locale_name

script_folder_path = os.path.split(os.path.realpath(sys.argv[0]))[0]

if __name__ == "__main__":
        app = QApplication([])
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
        locale_name = get_user_locale_name()
        translator = QTranslator()
        if os.path.exists(os.path.join(script_folder_path, f"locales/{locale_name}/{locale_name}.qm")):
            if translator.load(f"{locale_name}.qm", directory=os.path.join(script_folder_path, f"locales/{locale_name}")):
                QApplication.installTranslator(translator)
        singleton = Win32SingletonManager(QCoreApplication.translate("ToolWindow", "RWR Window Tool", None))
        if singleton.run_flag:
            rwr_window_tool = RWRWindowToolApp(script_folder_path)
            app.exec()
        else:
            app.exit(1)
        singleton.close_mutex()