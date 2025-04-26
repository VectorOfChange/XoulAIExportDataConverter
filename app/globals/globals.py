# globals/globals.py
# CONSTANTS
from app.enums.bug_type import BugType

APP_VERSION = "0.0.4"
NO_DATA_DESCRIPTION = "None/Empty"
KNOWN_BUGS = {
    "type": BugType.APP, "description": "If you click a button, the page might jump down to the very bottom",
    "type": BugType.APP, "description": "The file upload may not work on mobile Chrome (or Chrome based browsers like Brave). Workaround: use the 'view desktop page' option of your mobile browser",
}