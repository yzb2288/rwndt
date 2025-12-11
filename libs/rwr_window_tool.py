# -*- coding: utf-8 -*-
import os
import subprocess
from PySide6.QtGui import QMoveEvent
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QCoreApplication, QSettings, QObject, QEvent, QTimer, QThread, Signal, Qt
from libs.steam_resources import SteamResources
from libs.ui_rwr_window_tool import Ui_ToolWindow
from libs.rwr_window_style import RWRWindowStyleManager
from libs.rwr_config import RWRConfigManager

class RWRWindowToolApp(QWidget, Ui_ToolWindow):
    def __init__(self, root_path):
        self.root_path = root_path
        super().__init__()
        self.setupUi(self)
        self.steam_resources = SteamResources()
        self.rwr_install_folder_path = self.steam_resources.get_game_path_from_app_id(270150)
        self.rwr_appdata_folder_path = os.path.join(os.getenv("APPDATA"), "Running with rifles")
        self.rwr_config_manager = RWRConfigManager(self.rwr_appdata_folder_path)
        self.fullscreen = None
        self.resolution_width = None
        self.resolution_height = None
        self.rwr_configure_subprocess = None
        self.rwr_window_style_manager = None
        self.reset_flag = True
        self.suitable_resolution_flag = True
        self.rwr_window = []
        self.last_screen = self.screen()
        self.settings = QSettings(
            os.path.join(self.root_path, "config/rwr_window_tool.ini"),
            QSettings.Format.IniFormat
        )
        self.load_settings()
        self.borderlessRadioButton.toggled.connect(self.settings_change_event)
        self.rwrConfigureButton.clicked.connect(self.start_rwr_configure)
        self.rwrStartButton.clicked.connect(self.start_rwr_game)
        self.fullscreenLabel.installEventFilter(self)
        self.resolutionLabel.installEventFilter(self)
        self.refresh_ui_timer = QTimer(self, singleShot=False, interval=3000)
        self.refresh_ui_timer.timeout.connect(self.refresh_ui)
        self.refresh_ui_timer.timeout.emit()
        self.refresh_ui_timer.start()
        self.show()
    
    def start_rwr_configure(self):
        if self.rwr_configure_subprocess == None:
            self.rwr_configure_subprocess = RWRConfigureSubprocess(self.rwr_install_folder_path)
            self.rwr_configure_subprocess.subprocess_close_signal.connect(self.settings_change_event)
        if self.rwr_configure_subprocess.subprocess_closed_flag:
            self.rwr_configure_subprocess.start()
    
    def start_rwr_game(self):
        os.startfile("steam://rungameid/270150/")
    
    def refresh_ui(self):
        self.get_rwr_config()
        self.check_suitable_resolution(self.resolution_width, self.resolution_height)
        self.update_fullscreen_label(self.fullscreen)
        self.update_resolution_label(self.resolution_width, self.resolution_height)
        if self.reset_flag:
            self.reset_text_browser()
            self.reset_flag = False
        self.update_rwr_window_style_manager()
    
    def update_rwr_window_style_manager(self):
        if self.rwr_window_style_manager == None:
            if self.borderlessRadioButton.isChecked():
                mode = RWRWindowStyleManager.Mode.BORDERLESS_FULLSCREEN
            elif self.windowRadioButton.isChecked():
                mode = RWRWindowStyleManager.Mode.BETTER_WINDOW
            if self.fullscreen == "0":
                enable = True
            else:
                enable = False
            self.rwr_window_style_manager = RWRWindowStyleManager(
                mode=mode,
                enable=enable,
                screen=self.screen(),
                print_funticon=self.text_browser_append
            )
            self.modify_rwr_window_timer = QTimer(self, singleShot=False, interval=3000)
            self.modify_rwr_window_timer.timeout.connect(self.rwr_window_style_manager.modify_rwr_window)
            self.modify_rwr_window_timer.timeout.emit()
            self.modify_rwr_window_timer.start()
        else:
            if self.borderlessRadioButton.isChecked():
                mode = RWRWindowStyleManager.Mode.BORDERLESS_FULLSCREEN
            elif self.windowRadioButton.isChecked():
                mode = RWRWindowStyleManager.Mode.BETTER_WINDOW
            if self.fullscreen == "0":
                enable = True
            else:
                enable = False
            self.rwr_window_style_manager.set_mode(mode)
            self.rwr_window_style_manager.set_enable(enable)
            self.rwr_window_style_manager.set_screen(self.screen())
    
    def load_settings(self):
        geometry = self.settings.value("geometry", None)
        if geometry:
            self.restoreGeometry(geometry)
        mode_selected = self.settings.value("mode_selected", RWRWindowStyleManager.Mode.BORDERLESS_FULLSCREEN.name)
        if mode_selected == RWRWindowStyleManager.Mode.BORDERLESS_FULLSCREEN.name:
            self.borderlessRadioButton.setChecked(True)
        elif mode_selected == RWRWindowStyleManager.Mode.BETTER_WINDOW.name:
            self.windowRadioButton.setChecked(True)
    
    def save_settings(self):
        self.settings.setValue("geometry", self.saveGeometry())
        if self.borderlessRadioButton.isChecked():
            self.settings.setValue("mode_selected", RWRWindowStyleManager.Mode.BORDERLESS_FULLSCREEN.name)
        elif self.windowRadioButton.isChecked():
            self.settings.setValue("mode_selected", RWRWindowStyleManager.Mode.BETTER_WINDOW.name)
    
    def settings_change_event(self):
        self.reset_flag = True
        self.refresh_ui()
        self.save_settings()
    
    def moveEvent(self, event:QMoveEvent):
        if self.screen() != self.last_screen:
            self.settings_change_event()
            self.last_screen = self.screen()
    
    def eventFilter(self, watched:QObject, event:QEvent):
        if watched == self.fullscreenLabel:
            if event.type() == QEvent.Type.HoverEnter:
                if self.fullscreen != None and self.fullscreen != "0":
                    self.fullscreenLabel.setStyleSheet("background-color: #343E48")
                else:
                    self.fullscreenLabel.setStyleSheet("background-color: none")
            elif event.type() == QEvent.Type.MouseButtonPress:
                if self.fullscreen != None and self.fullscreen != "0":
                    if event.button() == Qt.MouseButton.LeftButton:
                        self.fullscreenLabel.setStyleSheet("background-color: #141E28")
                else:
                    self.fullscreenLabel.setStyleSheet("background-color: none")
            elif event.type() == QEvent.Type.MouseButtonRelease:
                if self.fullscreen != None and self.fullscreen != "0":
                    if event.button() == Qt.MouseButton.LeftButton:
                        self.fullscreenLabel.setStyleSheet("background-color: #343E48")
                else:
                    self.fullscreenLabel.setStyleSheet("background-color: none")
            elif event.type() == QEvent.Type.MouseButtonDblClick:
                if self.fullscreen != None and self.fullscreen != "0":
                    if event.button() == Qt.MouseButton.LeftButton:
                        self.fullscreenLabel.setStyleSheet("background-color: #141E28")
                        self.rwr_config_manager.set_fullscreen(False)
                        self.settings_change_event()
                else:
                    self.fullscreenLabel.setStyleSheet("background-color: none")
            elif event.type() == QEvent.Type.HoverLeave:
                self.fullscreenLabel.setStyleSheet("background-color: none")
        elif watched == self.resolutionLabel:
            if event.type() == QEvent.Type.HoverEnter:
                if not self.suitable_resolution_flag:
                    self.resolutionLabel.setStyleSheet("background-color: #343E48")
                else:
                    self.resolutionLabel.setStyleSheet("background-color: none")
            elif event.type() == QEvent.Type.MouseButtonPress:
                if not self.suitable_resolution_flag:
                    if event.button() == Qt.MouseButton.LeftButton:
                        self.resolutionLabel.setStyleSheet("background-color: #141E28")
                else:
                    self.resolutionLabel.setStyleSheet("background-color: none")
            elif event.type() == QEvent.Type.MouseButtonRelease:
                if not self.suitable_resolution_flag:
                    if event.button() == Qt.MouseButton.LeftButton:
                        self.resolutionLabel.setStyleSheet("background-color: #343E48")
                else:
                    self.resolutionLabel.setStyleSheet("background-color: none")
            elif event.type() == QEvent.Type.MouseButtonDblClick:
                if not self.suitable_resolution_flag:
                    if event.button() == Qt.MouseButton.LeftButton:
                        screen_resolution = self.screen().size() * self.screen().devicePixelRatio()
                        self.rwr_config_manager.set_resolution(screen_resolution.width(), screen_resolution.height())
                        self.settings_change_event()
                else:
                    self.resolutionLabel.setStyleSheet("background-color: none")
            elif event.type() == QEvent.Type.HoverLeave:
                self.resolutionLabel.setStyleSheet("background-color: none")
        
        return super().eventFilter(watched, event)
    
    def closeEvent(self, event):
        self.save_settings()
        super().closeEvent(event)
    
    def reset_text_browser(self):
        self.textBrowser.clear()
        self.textBrowser.setTextColor(Qt.GlobalColor.white)
        self.text_browser_notice()
    
    def text_browser_notice(self):
        if self.fullscreen != "0":
            self.textBrowser.append(
                "<font color=#FF0000>" +
                QCoreApplication.translate(
                    "ToolWindow",
                    "This tool will not work when the fullscreen setting is enabled! Please adjust the fullscreen setting in RWR Configure, or try double clicking the fullscreen label to auto resolve.",
                    None
                ) +
                "</font>"
            )
        elif not self.suitable_resolution_flag:
            screen_resolution = self.screen().size() * self.screen().devicePixelRatio()
            self.textBrowser.append(
                "<font color=#FFFF00>" +
                QCoreApplication.translate(
                    "ToolWindow",
                    "The current resolution setting ({0}x{1}) does not match the resolution of the screen ({2}x{3}) where this widget is on! Please adjust in RWR Configure, or try double clicking the resolution label to auto resolve.",
                    None
                ).format(
                    self.resolution_width,
                    self.resolution_height,
                    screen_resolution.width(),
                    screen_resolution.height()
                ) +
                "</font>"
            )
        elif self.borderlessRadioButton.isChecked():
            self.textBrowser.append(
                QCoreApplication.translate(
                    "ToolWindow",
                    "Start detecting the game hwnd. Please move this tool's window to the screen where you want the game to run in fullscreen.",
                    None
                )
            )
        else:
            self.textBrowser.append(
                QCoreApplication.translate(
                    "ToolWindow",
                    "Start detecting the game hwnd. This tool will disable the maximize and resize functions of the game window and set the title bar to dark mode.",
                    None
                )
            )
    
    def text_browser_append(self, text):
        self.textBrowser.setTextColor(Qt.GlobalColor.white)
        self.textBrowser.append(text)
    
    def get_rwr_config(self):
        self.rwr_config_manager.read_rwr_config()
        self.fullscreen = self.rwr_config_manager.get_fullscreen()
        self.resolution_width, self.resolution_height = self.rwr_config_manager.get_resolution()
    
    def check_suitable_resolution(self, width, height):
        if self.borderlessRadioButton.isChecked():
            screen_resolution = self.screen().size() * self.screen().devicePixelRatio()
            if screen_resolution.width() != width or screen_resolution.height() != height:
                self.suitable_resolution_flag = False
                return
        self.suitable_resolution_flag = True
    
    def update_fullscreen_label(self, fullscreen):
        if fullscreen == "0":
            self.fullscreenLabel.setText(
                QCoreApplication.translate("ToolWindow", "Fullscreen: ", None) +
                "<font color=#FFFFFF>NO</font>"
            )
            self.fullscreenLabel.setToolTip("")
        else:
            self.fullscreenLabel.setText(
                QCoreApplication.translate("ToolWindow", "Fullscreen: ", None) +
                "<font color=#FF0000>YES</font>"
            )
            self.fullscreenLabel.setToolTip(
                QCoreApplication.translate("ToolWindow", "Double click to resolve.", None)
            )
    
    def update_resolution_label(self, width, height):
        if self.suitable_resolution_flag:
            self.resolutionLabel.setText(
                QCoreApplication.translate("ToolWindow", "Resolution: ", None) + f"{width}x{height}"
            )
            self.resolutionLabel.setToolTip("")
        else:
            self.resolutionLabel.setText(
                QCoreApplication.translate("ToolWindow", "Resolution: ", None) +
                f"<font color=#FFFF00>{width}x{height}</font>"
            )
            self.resolutionLabel.setToolTip(
                QCoreApplication.translate("ToolWindow", "Double click to resolve.", None)
            )

class RWRConfigureSubprocess(QThread):
    subprocess_close_signal = Signal()
    
    def __init__(self, rwr_install_folder_path):
        super().__init__()
        self.rwr_install_folder_path = rwr_install_folder_path
        self.subprocess_closed_flag = True

    def run(self):
        self.subprocess_closed_flag = False
        self.rwr_configure_subprocess = subprocess.Popen(
            os.path.join(self.rwr_install_folder_path, "rwr_config.exe"),
            cwd=self.rwr_install_folder_path
        )
        self.rwr_configure_subprocess.wait()
        self.subprocess_close_signal.emit()
        self.subprocess_closed_flag = True