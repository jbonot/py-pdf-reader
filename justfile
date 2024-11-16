# Windows
set shell := ["cmd.exe", "/c"]

build:
    just check
    pyinstaller main.spec

run:
    python main.py

check:
    ruff check --fix

test:
    pytest