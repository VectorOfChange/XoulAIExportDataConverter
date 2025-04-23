# utils/custom_timestamp.py
from datetime import datetime

# Function to get current timestamp with milliseconds
def get_timestamp():
    now = datetime.now()
    return now.strftime("%H:%M:%S.%f")  # Format: HH:MM:SS.mmmmmm