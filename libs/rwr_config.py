import os
import lxml.etree as ET

class RWRConfigManager:
    def __init__(self, rwr_appdata_folder_path):
        self.rwr_appdata_folder_path = rwr_appdata_folder_path
        self.tree = None
    
    def read_rwr_config(self):
        self.tree = ET.parse(os.path.join(self.rwr_appdata_folder_path, "config.xml"), ET.XMLParser(strip_cdata=False))
        return self.tree
    
    def write_rwr_config(self):
        self.tree.write(os.path.join(self.rwr_appdata_folder_path, "config.xml"), encoding="utf-8")
    
    def get_fullscreen(self):
        if self.tree == None:
            self.read_rwr_config()
        self.fullscreen = self.tree.find("./fullscreen").get("value")
        return self.fullscreen
    
    def get_resolution(self):
        if self.tree == None:
            self.read_rwr_config()
        self.video_mode = self.tree.find("./videomode").text.strip().split()
        self.resolution_width = int(self.video_mode[0])
        self.resolution_height = int(self.video_mode[2])
        return self.resolution_width, self.resolution_height
    
    def set_fullscreen(self, enable:bool):
        if self.tree == None:
            self.read_rwr_config()
        if enable:
            self.fullscreen = "1"
            self.tree.find("./fullscreen").set("value", "1")
        else:
            self.fullscreen = "0"
            self.tree.find("./fullscreen").set("value", "0")
        self.write_rwr_config()
    
    def set_resolution(self, width:int, height:int):
        if self.tree == None:
            self.read_rwr_config()
        self.resolution_width = width
        self.resolution_height = height
        self.video_mode[0] = str(int(width))
        self.video_mode[2] = str(int(height))
        self.tree.find("./videomode").text = ET.CDATA(" ".join(self.video_mode))
        self.write_rwr_config()