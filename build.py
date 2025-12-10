import os
import sys
import shutil
root_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
os.chdir(root_path)

if __name__ == "__main__":
    project_name = "rwr_window_tool"
    with open("VERSION", "r", encoding="utf-8") as f:
        version = f.read().strip()
    nuitka_output_dir = "nuitka_build"
    folder_name = project_name
    exe_name = f"{project_name}_v{version}.exe"
    ico_path = "assets/hud_laptop_gps_with_emoji.ico"
    
    if os.path.exists(nuitka_output_dir):
        shutil.rmtree(nuitka_output_dir)
    
    nuitka_command = [
        "python -m nuitka --standalone --onefile --remove-output --windows-console-mode=disable --enable-plugin=pyside6",
        f"--output-dir=\"{nuitka_output_dir}\"",
        f"--output-folder-name=\"{folder_name}\"",
        f"--output-filename=\"{exe_name}\"",
        f"--windows-icon-from-ico=\"{ico_path}\"",
        "main.py"
    ]
    nuitka_command = " ".join(nuitka_command)
    os.system(nuitka_command)

    for filepath, dirnames, filenames in os.walk("locales"):
        for filename in filenames:
            if os.path.splitext(filename)[1] == ".qm":
                source_file_path = os.path.join(filepath, filename)
                target_folder_path = os.path.join(nuitka_output_dir, filepath)
                target_file_path = os.path.join(target_folder_path, filename)
                if not os.path.exists(target_folder_path):
                    os.makedirs(target_folder_path)
                shutil.copyfile(source_file_path, target_file_path)