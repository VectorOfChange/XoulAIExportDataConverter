# XoulAIExportDataConverter
A tool to convert Xoul AI exported data for easier use with other platforms

## Run Online
This tool can be run online at:
* [Hugging Face Spaces](https://huggingface.co/spaces/VectorOfChange/XoulAIExportDataConverter)

Note: these are free servers, so there's limits. If you get a timeout or error, try again later or download the tool and run it locally.

## Run Locally
You need to have Python installed. If you don't, install Python 3.

*Note: These directions were tested on Windows 10 with VSCode terminal. Minor modifications may be required for your system configuration.*

1. Clone the repo
2. Go to the repo directory
3. Setup a virtual environment:
        
        python -m venv venv
4. Activate the virtual environment:
        
        venv\Scripts\activate

    Your terminal should now show ```(venv)``` before the prompt.
6. Install dependencies:

        pip install -r app/requirements.txt
7. Run the app:

        streamlit run app/main.py
8. Your browser should automatically open a new tab and load the application. If it doesn't, browse to the address shown in the terminal. 