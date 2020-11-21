import sys
from cx_Freeze import setup, Executable
from mkings.constants import VERSION

build_exe_options = {
    "packages": ["pygame", "random", "sys"],
    "include_files": ["icon.ico", "fonts/", "images/", "sounds/"],
    "excludes": ["tkinter"]
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Memory Kings",
    version=f"v{VERSION[0]} ({VERSION[1]})",
    author="G. Scary T.",
    description="Memory Kings in Python 3",
    options={"build_exe": build_exe_options},
    executables=[Executable("memorykings.py", base=base, icon="icon.ico")],
)
