# globals/globals.py
# CONSTANTS
from enums.bug_type import BugType

APP_VERSION = "0.0.5"
APP_VERSION_TAG = "" # put ALPHA, BETA, TESTBUILD or whatever else here
NO_DATA_DESCRIPTION = "None/Empty"
KNOWN_BUGS = [
    {"type": BugType.APP, "description": "If you click a button, the page might jump down to the very bottom"},
    {"type": BugType.APP, "description": "The file upload may not work on mobile Chrome (or Chrome based browsers like Brave). Workaround: use the 'view desktop page' option of your mobile browser"},
    {"type": BugType.DATA, "description": "Objectives (including meters) are malformed or missing. Particularly impacts group chats."},
]
IMAGES_FOLDER_PATH = "images/"