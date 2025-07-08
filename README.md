# CodeFlow

Turn flowcharts into clean Python code. Get on-the-fly generation, explanation, and running of logic—all bundled in one web app.

## Overview

CodeFlow is a web-based tool that translates flowcharts to executable Python code. It is designed for visual thinkers who prefer closing the gap between diagramming and writing code. Import a `.drawio` flowchart, convert it to code, understand the logic in plain English, and even run the code right inside the browser.

## Features

- Import `.drawio` or `.xml` flowcharts from Draw.io
- Automatically convert flowcharts to Python code
- Show flowchart logic in natural language
- Show custom Python code step-by-step
- Run Python code inside the app using embedded execution
- Sanitize dark-themed interface built with custom CSS

## Best Use Cases

- Newcomers to programming through learning via flowcharts
- Intermediate learners who need explanation of code and logic
- Advanced developers looking to speed up prototyping using flowcharts

## Tech Stack

- Frontend: Streamlit
- Backend: Python, DeepSeek API
- Parsing Flowchart: Custom XML parser for Draw.io files
- Execution: Python `exec()` with input mocking, Trinket embed
- Styling: Custom CSS injected into Streamlit

## How to Run the App

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/codeflow.git
cd codeflow
```
###2. Install Dependencies in python:
pip install streamlit requests

### 3.Get an Api Key for the model = "deepseek/deepseek-r1-0528:free"
On Openrouter

###4.replace the api_key Variables in app.py and drawio_to_code.py

###5. Run "streamlit run app.py" in the terminal.

###6.Then open your browser to http://localhost:8501

## Credits
Font: Rubik by Hubert & Fischer, Meir Sadan, and Cyreal — licensed under the Open Font License.
