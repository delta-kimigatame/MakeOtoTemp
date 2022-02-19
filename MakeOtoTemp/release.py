import datetime
import shutil
import os.path

BUILD_DIR = os.path.join("..", "release", "build")
PROJECTNAME = "MakeOtoTemp"
RELEASE_FILE = os.path.join("..", "release", PROJECTNAME + "-" + datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d"))
EXE_DIR = os.path.join("..", "MakeOtoTempExe", "bin", "Release", "net6.0-windows")
EXE_DIR_EXTENSIONS = [".exe",".dll",".runtimeconfig.json"]
SOURCE_FILES = ['MakeOtoTemp.py',
                'Oto.py', 
                'Preset.py',
                'settings.py']
README=os.path.join("..","README.md")
LICENSE=os.path.join("..","LICENSE")

exe_dir_files = os.listdir(EXE_DIR)
for file in exe_dir_files:
    for extensions in EXE_DIR_EXTENSIONS:
        if file.endswith(extensions):
            shutil.copy(os.path.join(EXE_DIR, file),os.path.join(BUILD_DIR, file))
            break
            
for file in os.listdir():
    if file in SOURCE_FILES:
        shutil.copy(file, os.path.join(BUILD_DIR, "src", file))

shutil.copy(LICENSE, os.path.join(BUILD_DIR, "license.txt"))
shutil.copy(README, os.path.join(BUILD_DIR, "readme.txt"))

shutil.make_archive(RELEASE_FILE, format="zip", root_dir=BUILD_DIR)