import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["pygame", "random", "sys"],
    "include_files": ["icon.ico", "fonts/", "images/"],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Memory Kings",
    version="0.6",
    author="G. Scary T.",
    description="Memory Kings in Python",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, icon="icon.ico")],
)
