# Windows
set shell := ["cmd.exe", "/c"]

build:
    pyinstaller app.spec

run mode="normal":
    python {{ if mode == "debug" {'main.py --debug'} else if mode == "test" {'main.py'} else {'app.py'} }}



