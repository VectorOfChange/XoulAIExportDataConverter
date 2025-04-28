# utils/version.py

# Function to get the version string
from globals.globals import APP_VERSION, APP_VERSION_TAG

def get_app_version() -> str:
    version = f"{APP_VERSION}{'.' + APP_VERSION_TAG if APP_VERSION_TAG else ''}"
    
    return version