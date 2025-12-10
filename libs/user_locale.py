# -*- coding: utf-8 -*-
import ctypes
from ctypes import wintypes

kernel32 = ctypes.windll.LoadLibrary("kernel32")

def get_user_locale_name():
    lcid = wintypes.LCID(kernel32.GetUserDefaultUILanguage())
    buffer_len = kernel32.LCIDToLocaleName(lcid, None, 0, 0)
    wstr = ctypes.create_unicode_buffer(buffer_len)
    ret = kernel32.LCIDToLocaleName(lcid, wstr, buffer_len, 0)
    return wstr.value