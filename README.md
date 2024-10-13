# PDF Text Extractor

## Overview
This application reads all PDF files located in the `inputs` folder and exports the unformatted text to the `output` folder. It's designed for users who need to quickly extract text from PDFs for further processing or analysis.

## Setup

### Prerequisites
Ensure you have Python 3.x installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Installation
To install the required libraries, run the following command in your terminal:

```bash
pip install -r requirements.txt
```

## Usage
1. Add PDF Files: Place the PDF files you want to process into the `inputs` folder.

2. Run the Application: Execute the following command in your console:

```bash
python main.py
```
3. Check Results: The extracted data will be saved in the `output` folder. This text can be copied and pasted into an Excel sheet.

## Debug Mode
Intead of generating a `.txt` file with tab-separated values, you can run in debug mode to view
- the direct PDF to text output
- the key-value pairs of the extracted data.

You can enable debug mode by running:

```bash
python main.py --debug
```

The debug outputs will be saved in the `output/debug` folder.

## Notes
- Only PDF files will be processed from the `inputs` folder. Other file types will be ignored.