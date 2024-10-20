# Windows
set shell := ["cmd.exe", "/c"]

build:
    pyinstaller main.spec

run mode="normal":
    python main.py {{ if mode == "debug" {'--debug'} else {''} }}

