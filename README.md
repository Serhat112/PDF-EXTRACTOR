# PDF Page Extractor

This is a Python desktop app to extract specific pages from PDF files.

## Requirements

- Python 3.13+
- Packages: `customtkinter`, `tkinterdnd2`, `pypdf`, `python-dotenv`
- TCL/TK libraries (usually come with Python)

## Setup

1. Clone the repository
2. Create a virtual environment and install dependencies
python -m venv .venv
source .venv/Scripts/activate


3. Create a .env file in the project root with your local TCL/TK paths:
TCL_LIBRARY=C:\path\to\tcl\tcl8.6
TK_LIBRARY=C:\path\to\tcl\tk8.6

4. Run the app:
python app.py
