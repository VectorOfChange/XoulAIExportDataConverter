# utils/custom_logger.py

import streamlit as st
from utils.custom_timestamp import get_timestamp


# Function to log messages with timestamp
def log(msg: str):
    timestamp = get_timestamp()
    full_msg = f"[{timestamp}] {msg}"
    st.session_state.log_messages.append(full_msg)