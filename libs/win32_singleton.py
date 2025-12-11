import ctypes
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QCoreApplication

kernel32 = ctypes.windll.LoadLibrary("kernel32")
ERROR_ALREADY_EXISTS = 183

class Win32SingletonManager(QMessageBox):
    def __init__(self, program_name):
        self.program_name = program_name
        self.mutex_name = program_name + "_mutex"
        self.run_flag = self.create_mutex()
        if not self.run_flag:
            super().__init__()
            if self.last_error == ERROR_ALREADY_EXISTS:
                self.critical(
                    None,
                    QCoreApplication.translate("ToolWindow", "ERROR", None),
                    QCoreApplication.translate("ToolWindow", "{0} is already running!", None).format(self.program_name)
                )
            else:
                self.critical(
                    None,
                    QCoreApplication.translate("ToolWindow", "ERROR", None),
                    QCoreApplication.translate("ToolWindow", "CreateMutexW failed! GetLastError - {0}", None).format(self.last_error)
                )
    
    def create_mutex(self):
        self.mutex_handle = kernel32.CreateMutexW(None, 1, self.mutex_name)
        if self.mutex_handle:
            self.last_error = kernel32.GetLastError()
            if self.last_error == ERROR_ALREADY_EXISTS:
                kernel32.CloseHandle(self.mutex_handle)
                return False
            else:
                return True
        else:
            self.last_error = kernel32.GetLastError()
            return False
    
    def close_mutex(self):
        if self.mutex_handle and self.run_flag:
            kernel32.CloseHandle(self.mutex_handle)
            self.run_flag = False
            self.mutex_handle = None