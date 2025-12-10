import os
import sys
import xml.etree.ElementTree as ET
script_folder_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
root_path = os.path.join(script_folder_path, "..")
python_root = os.path.split(os.path.realpath(sys.executable))[0]
os.chdir(root_path)
sys.path.append(root_path)
from libs.user_locale import get_user_locale_name

if __name__ == "__main__":
    locale_name = get_user_locale_name()
    
    if not os.path.exists("./locales"):
        os.makedirs("./locales")
    if not os.path.exists(f"./locales/{locale_name}"):
        os.makedirs(f"./locales/{locale_name}")
    os.system("pyside6-lupdate -recursive -extensions py,ui,qml libs/ -ts locales/lupdate.ts")
    os.system(f"pyside6-lupdate -recursive -extensions py,ui,qml libs/ -ts locales/{locale_name}/{locale_name}.ts")
    
    tree = ET.parse(f"./locales/{locale_name}/{locale_name}.ts")
    messages = tree.findall("./context/message")
    for message in messages:
        if message.find("./translation").get("type") != None:
            print("Translation is not finished, please go to {} to continue.".format(
                os.path.join(python_root, "Lib\site-packages\PySide6\linguist.exe")
            ))
            break
    else:
        os.system(f"pyside6-lrelease locales/{locale_name}/{locale_name}.ts -qm locales/{locale_name}/{locale_name}.qm")