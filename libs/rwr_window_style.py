# -*- coding: utf-8 -*-
import os
import enum
import ctypes
import winsound
import win32api, win32gui, win32con, win32process, win32timezone
from ctypes import wintypes
from PySide6.QtGui import QScreen
from PySide6.QtCore import QCoreApplication

dwmapi = ctypes.windll.LoadLibrary("dwmapi")
DWMWA_USE_IMMERSIVE_DARK_MODE = 20

class RWRWindowStyleManager:
    class Mode(enum.Enum):
        BORDERLESS_FULLSCREEN = 0x01
        BETTER_WINDOW = 0x02
    
    TARGET_WINDOW_STYLE = {
        Mode.BORDERLESS_FULLSCREEN: 0xffffffff & (
            win32con.WS_POPUP |
            win32con.WS_VISIBLE |
            win32con.WS_CLIPSIBLINGS |
            win32con.WS_CLIPCHILDREN |
            win32con.WS_GROUP |
            win32con.WS_MINIMIZEBOX
        ),
        Mode.BETTER_WINDOW: 0xffffffff & (
            win32con.WS_CAPTION |
            win32con.WS_VISIBLE |
            win32con.WS_CLIPSIBLINGS |
            win32con.WS_CLIPCHILDREN |
            win32con.WS_SYSMENU |
            win32con.WS_OVERLAPPED |
            win32con.WS_MINIMIZEBOX
        )
    }
    TARGET_WINDOW_EXSTYLE = {
        Mode.BORDERLESS_FULLSCREEN: 0xffffffff & (
            win32con.WS_EX_LEFT |
            win32con.WS_EX_LTRREADING |
            win32con.WS_EX_RIGHTSCROLLBAR |
            win32con.WS_EX_STATICEDGE |
            win32con.WS_EX_COMPOSITED
        ),
        Mode.BETTER_WINDOW: 0xffffffff & (
            win32con.WS_EX_LEFT |
            win32con.WS_EX_LTRREADING |
            win32con.WS_EX_RIGHTSCROLLBAR |
            win32con.WS_EX_WINDOWEDGE
        )
    }
    IGNORE_WINDOW_STYLE = {
        Mode.BORDERLESS_FULLSCREEN: 0xffffffff & (win32con.WS_MINIMIZE | win32con.WS_MAXIMIZE),
        Mode.BETTER_WINDOW: 0xffffffff & win32con.WS_MINIMIZE
    }
    IGNORE_WINDOW_EXSTYLE = {
        Mode.BORDERLESS_FULLSCREEN: 0x00000000,
        Mode.BETTER_WINDOW: 0x00000000
    }
        
    def __init__(self, mode:Mode, enable:bool, screen:QScreen, print_funticon):
        self.set_mode(mode)
        self.set_enable(enable)
        self.set_screen(screen)
        self.set_print_function(print_funticon)
        self.rwr_window = []
    
    def set_mode(self, mode:Mode):
        if mode not in self.Mode:
            raise ValueError("Invalid mode")
        self.mode = mode
        #print(f"RWRWindowStyleManager mode set to {self.mode.name}")
    
    def set_enable(self, enable:bool):
        if not isinstance(enable, bool):
            raise ValueError("Enable must be a boolean value")
        self.enable = enable
        #print(f"RWRWindowStyleManager enable set to {self.enable}")
    
    def set_screen(self, screen):
        if not isinstance(screen, QScreen):
            raise ValueError("Screen must be a QScreen instance")
        self.screen = screen
        #print(f"RWRWindowStyleManager screen set to {self.screen.name()}")
    
    def set_print_function(self, print_function):
        if not callable(print_function):
            raise ValueError("Print function must be callable")
        self.print_function = print_function
        #print("RWRWindowStyleManager print function set")
    
    def modify_rwr_window(self):
        new_rwr_window = []
        win32gui.EnumWindows(self.enum_windows_find_rwr, new_rwr_window)
        for new_window in new_rwr_window[:]:
            modify_flag = False
            for last_window in self.rwr_window:
                if new_window["hwnd"] == last_window["hwnd"]:
                    if new_window["process_creation_time"] != last_window["process_creation_time"]:
                        modify_flag = True
                    break
            else:
                modify_flag = True
            if modify_flag:
                modify_successful_flag = False
                if self.enable:
                    if self.mode == self.Mode.BORDERLESS_FULLSCREEN:
                        if self.set_borderless_window(new_window["hwnd"]):
                            if self.maximize_window(new_window["hwnd"]):
                                modify_successful_flag = True
                                winsound.MessageBeep(0)
                    elif self.mode == self.Mode.BETTER_WINDOW:
                        if self.set_better_window(new_window["hwnd"]):
                            self.set_dark_mode(new_window["hwnd"])
                            modify_successful_flag = True
                            winsound.MessageBeep(0)
                if not modify_successful_flag:
                    new_rwr_window.remove(new_window)
        self.rwr_window = new_rwr_window
    
    def enum_windows_find_rwr(self, hwnd, extra):
        window_text = win32gui.GetWindowText(hwnd)
        if "RUNNING WITH RIFLES" in window_text and "RUNNING WITH RIFLES Config" not in window_text:
            tid, pid = win32process.GetWindowThreadProcessId(hwnd)
            process_handle = win32api.OpenProcess( win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid)
            process_exe_path = win32process.GetModuleFileNameEx(process_handle, 0)
            process_times = win32process.GetProcessTimes(process_handle)
            win32api.CloseHandle(process_handle)
            if os.path.basename(process_exe_path) == "rwr_game.exe":
                extra.append({
                    "hwnd": hwnd,
                    "process_creation_time": process_times["CreationTime"].timestamp()
                })

    def set_borderless_window(self, hwnd):
        window_style = win32api.GetWindowLong(hwnd, win32con.GWL_STYLE)
        window_exstyle = win32api.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        if (window_style & ~self.IGNORE_WINDOW_STYLE[self.Mode.BORDERLESS_FULLSCREEN]) != self.TARGET_WINDOW_STYLE[self.Mode.BORDERLESS_FULLSCREEN] or\
            (window_exstyle & ~self.IGNORE_WINDOW_EXSTYLE[self.Mode.BORDERLESS_FULLSCREEN]) != self.TARGET_WINDOW_EXSTYLE[self.Mode.BORDERLESS_FULLSCREEN]:
            self.print_function(
                QCoreApplication.translate("ToolWindow", "Game HWND: {0} Current Style: {1} Current ExStyle: {2}", None).format(
                    hex(hwnd).replace("0x", "").upper().zfill(8),
                    hex(window_style).replace("0x", "").upper().zfill(8),
                    hex(window_exstyle).replace("0x", "").upper().zfill(8)
                )
            )
            self.print_function(
                QCoreApplication.translate("ToolWindow", "Set HWND {0} borderless window", None).format(hex(hwnd).replace("0x", "").upper().zfill(8))
            )
            win32api.SetWindowLong(hwnd, win32con.GWL_STYLE, self.TARGET_WINDOW_STYLE[self.Mode.BORDERLESS_FULLSCREEN])
            win32api.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, self.TARGET_WINDOW_EXSTYLE[self.Mode.BORDERLESS_FULLSCREEN])
            return True
        else:
            return False

    def maximize_window(self, hwnd):
        window_placement = win32gui.GetWindowPlacement(hwnd)
        if window_placement[1] != win32con.SW_SHOWMAXIMIZED:
            screen_resolution = self.screen.size() * self.screen.devicePixelRatio()
            self.print_function(
                QCoreApplication.translate("ToolWindow", "Set HWND {0} maximize on {1} ({2}x{3})", None).format(
                    hex(hwnd).replace("0x", "").upper().zfill(8),
                    self.screen.name(),
                    screen_resolution.width(),
                    screen_resolution.height()
                )
            )
            screen_rect = self.screen.geometry()
            device_pixel_ratio = self.screen.devicePixelRatio()
            win32gui.MoveWindow(
                hwnd,
                int(screen_rect.x() * device_pixel_ratio),
                int(screen_rect.y() * device_pixel_ratio),
                int(screen_rect.width() * device_pixel_ratio),
                int(screen_rect.height() * device_pixel_ratio),
                True
            )
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            return True
        else:
            return False

    def set_better_window(self, hwnd):
        window_style = win32api.GetWindowLong(hwnd, win32con.GWL_STYLE)
        window_exstyle = win32api.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        if (window_style & ~self.IGNORE_WINDOW_STYLE[self.Mode.BETTER_WINDOW]) != self.TARGET_WINDOW_STYLE[self.Mode.BETTER_WINDOW] or\
            (window_exstyle & ~self.IGNORE_WINDOW_EXSTYLE[self.Mode.BETTER_WINDOW]) != self.TARGET_WINDOW_EXSTYLE[self.Mode.BETTER_WINDOW]:
            self.print_function(
                QCoreApplication.translate("ToolWindow", "Game HWND: {0} Current Style: {1} Current ExStyle: {2}", None).format(
                    hex(hwnd).replace("0x", "").upper().zfill(8),
                    hex(window_style).replace("0x", "").upper().zfill(8),
                    hex(window_exstyle).replace("0x", "").upper().zfill(8)
                )
            )
            self.print_function(
                QCoreApplication.translate("ToolWindow", "Set HWND {0} better window", None).format(hex(hwnd).replace("0x", "").upper().zfill(8))
            )
            win32api.SetWindowLong(hwnd, win32con.GWL_STYLE, self.TARGET_WINDOW_STYLE[self.Mode.BETTER_WINDOW])
            win32api.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, self.TARGET_WINDOW_EXSTYLE[self.Mode.BETTER_WINDOW])
            win32gui.SetWindowPos(hwnd, None, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED)
            return True
        else:
            return False

    def set_dark_mode(self, hwnd):
        self.print_function(
            QCoreApplication.translate("ToolWindow", "Set HWND {0} dark mode", None).format(hex(hwnd).replace("0x", "").upper().zfill(8))
        )
        use_dark_mode = wintypes.BOOL(True)
        hresult = dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(use_dark_mode), ctypes.sizeof(use_dark_mode))
        if hresult != 0:
            raise Exception("HRESULT: 0x{}".format(hex(0xffffffff & hresult).replace("0x", "").upper().zfill(8)))
