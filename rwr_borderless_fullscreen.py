# -*- coding: utf-8 -*-
# @Author  : FastClock
# @Project : https://github.com/yzb2288/RWR_Borderless_Fullscreen_Extension

import time
import winsound
import win32api, win32gui, win32con

def enum_windows_find_rwr(hwnd, extra):
    window_text = win32gui.GetWindowText(hwnd)
    if "RUNNING WITH RIFLES" in window_text and "RUNNING WITH RIFLES Config" not in window_text: # 过滤掉rwr_config.exe
        class_name = win32gui.GetClassName(hwnd)
        if class_name != "SDL_app": # SDL_app是steam启动游戏确认窗口的类名
            extra.append({
                "hwnd": hwnd,
                "window_text": window_text,
                "class_name": class_name
            })

def set_borderless_window(hwnd):
    window_style = win32api.GetWindowLong(hwnd, win32con.GWL_STYLE)
    if window_style & (win32con.WS_BORDER | win32con.WS_DLGFRAME | win32con.WS_SYSMENU | win32con.WS_THICKFRAME | win32con.WS_MINIMIZEBOX):
        print("游戏窗口{}默认样式: {}".format(hex(hwnd).replace("0x", "").upper().zfill(8), hex(window_style).replace("0x", "").upper().zfill(8)))
        print("设置窗口{}为无边框样式".format(hex(hwnd).replace("0x", "").upper().zfill(8)))
        window_style &= ~(win32con.WS_BORDER | win32con.WS_DLGFRAME | win32con.WS_SYSMENU | win32con.WS_THICKFRAME | win32con.WS_MINIMIZEBOX)
        win32api.SetWindowLong(hwnd, win32con.GWL_STYLE, window_style)
        return True
    else:
        #print("窗口{}已经是无边框样式, 不修改".format(hex(hwnd).replace("0x", "").upper().zfill(8)))
        return False

def maximize_window(hwnd):
    window_placement = win32gui.GetWindowPlacement(hwnd)
    if window_placement[1] != win32con.SW_SHOWMAXIMIZED:
        print("设置窗口{}最大化".format(hex(hwnd).replace("0x", "").upper().zfill(8)))
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        return True
    else:
        #print("窗口{}已经是最大化, 不修改".format(hex(hwnd).replace("0x", "").upper().zfill(8)))
        return False

if __name__ == "__main__":
    print("欢迎使用RWR无边框全屏设置脚本, 使用前请在rwr_config.exe中设置RWR为跟屏幕分辨率一致的分辨率, 并将FULL SCREEN设置为《NO》")
    print("\033[1;33m请先打开此脚本, 再运行游戏\033[0m, 否则游戏可能会出现UI错位, 如果已经遇到了这个问题, 请退出当前地图重新进入来解决, \033[1;33m无需\033[0m重启游戏")
    print("开始循环检测游戏窗口, 检测到游戏窗口后将自动进行修改...")
    while True:
        rwr_windows = []
        win32gui.EnumWindows(enum_windows_find_rwr, rwr_windows)
        for window in rwr_windows:
            if set_borderless_window(window["hwnd"]):
                if maximize_window(window["hwnd"]):
                    winsound.MessageBeep(0)
        time.sleep(3)
    
    