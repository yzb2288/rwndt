# -*- coding: utf-8 -*-
import os
import vdf
import win32api
import win32con

class SteamResources:
    def __init__(self):
        self.steam_path = self.get_steam_path()
        with open(os.path.join(self.steam_path, "steamapps\\libraryfolders.vdf"), "r", encoding="utf-8") as f:
            self.steam_library_folders = vdf.loads(f.read())
    
    def get_steam_path(self):
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, "Software\\Valve\\Steam", 0, win32con.KEY_READ)
        steam_path = win32api.RegQueryValueEx(key, "SteamPath")[0]
        key.Close()
        return steam_path
    
    def get_game_path_from_app_id(self, game_app_id):
        for library_folders_id in self.steam_library_folders["libraryfolders"].keys():
            for app_id in self.steam_library_folders["libraryfolders"][library_folders_id]["apps"].keys():
                if app_id == str(game_app_id):
                    game_library_folder_path = self.steam_library_folders["libraryfolders"][library_folders_id]["path"]
                    game_steamapps_folder_path = os.path.join(game_library_folder_path, "steamapps")
                    for file in os.listdir(game_steamapps_folder_path):
                        file_path = os.path.join(game_steamapps_folder_path, file)
                        if os.path.isfile(file_path) and file == f"appmanifest_{game_app_id}.acf":
                            with open(file_path, "r", encoding="utf-8") as f:
                                game_appmanifest = vdf.loads(f.read())
                            return os.path.join(game_steamapps_folder_path, "common\\" + game_appmanifest["AppState"]["installdir"])
                    break

if __name__ == "__main__":
    sr = SteamResources()
    rwr_install_folder_path = sr.get_game_path_from_app_id(270150)
    rwr_appdata_folder_path = os.path.join(os.getenv("APPDATA"), "Running with rifles")
    print(rwr_install_folder_path)
    print(rwr_appdata_folder_path)