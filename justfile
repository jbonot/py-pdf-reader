# Windows
set shell := ["cmd.exe", "/c"]

output_name := "parse_pdfs"
main := "main.py"

build:
    pyinstaller --onefile -w --name {{output_name}} {{main}}

run mode="normal":
    python {{main}} {{ if mode == "debug" {'--debug'} else {''} }}

