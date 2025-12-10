# -*- coding: utf-8 -*-
import re

def replace_match(match):
    unicode_content = match.group(1)
    decoded_content = unicode_content.encode().decode("unicode_escape")
    return f'"{decoded_content}"'

def replace_file_unicode_strings(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    new_content = re.sub(r"u\"(.*?)\"", replace_match, content)
    new_content = re.sub(r"u\'(.*?)\'", replace_match, new_content)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    file_list = ["rwr_window_tool.py"]
    for file_path in file_list:
        replace_file_unicode_strings(file_path)