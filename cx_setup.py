import sys
from cx_Freeze import setup, Executable
from mkings.constants import VERSION

build_exe_options = {
    "packages": ["pygame", "random", "sys"],
    "excludes": ["tkinter"]
}

bdist_mac_options = {
    "include_resources": [
        ("icon.ico", "icon.ico"),
        ("fonts", "fonts"),
        ("images", "images"),
        ("sounds", "sounds"),
    ],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Memory Kings",
    version=f"{VERSION}",
    author="G. Scary T.",
    description="Memory Kings in Python 3",
    options={
        "build_exe": build_exe_options,
        "bdist_mac": bdist_mac_options,
    },
    executables=[Executable("memorykings.py", base=base, icon="icon.ico")],
)
