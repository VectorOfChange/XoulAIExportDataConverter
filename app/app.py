import streamlit as st
import zipfile
import json
import time
from io import BytesIO
from docx import Document
from datetime import datetime

if "user_options_disabled" not in st.session_state:
    st.session_state.user_options_disabled = False

# Function to disable the user options
def disable_user_options():
    st.session_state.user_options_disabled = True

# Function to enable the user options
def enable_user_options():
    st.session_state.user_options_disabled = False

# Function to get current timestamp with milliseconds
def get_timestamp():
    now = datetime.now()
    return now.strftime("%H:%M:%S.%f")  # Format: HH:MM:SS.mmmmmm

# Initialize log message list
log_messages = []

# Function to log messages with timestamp
def log(msg: str):
    timestamp = get_timestamp()
    full_msg = f"[{timestamp}] {msg}"
    log_messages.append(full_msg)

st.set_page_config(page_title="Xoul AI Data Converter", layout="centered")

st.title("📄 Xoul AI Data Converter")

st.subheader("About")
st.markdown("This tool converts your Xoul AI exported data to other formats. This makes it easier to use your data on other platforms.")

st.subheader("Privacy")
st.markdown("Your data stays **100% private**: none of your content is stored or logged. No human or machine can review your content.")

st.header("Get Started!")

st.subheader("Step 1: Choose Options", divider=True)

include_markdown = st.checkbox("Include Markdown (.md) output", value=True, disabled=st.session_state.user_options_disabled)
include_word = st.checkbox("Include Word (.docx) output", value=True, disabled=st.session_state.user_options_disabled)

st.subheader("Step 2: Upload File", divider=True)
uploaded_file = st.file_uploader("Upload your Xoul AI Data Export Zip file", type=["zip"])

# Initialize log message list
log_messages = []

if uploaded_file is not None:
    st.success("✅ ZIP file uploaded!")

    st.subheader("Step 3: Start Processing", divider=True)
    st.markdown("To reset the form, click the Restart button")

    # Show process button
    func_button_col1, func_button_col2 = st.columns(2)
    
    with func_button_col1:
        process_button = st.button("🚀 Process File", on_click=disable_user_options, type="primary")
    
    if process_button:
        func_button_col2.button("⬅️ Restart (Clears Results)", on_click=enable_user_options)

        st.subheader("Step 4: Wait for Processing to Finish", divider=True)        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        st.subheader("Step 5: Download Results", divider=True)

        try:
            zip_bytes = BytesIO(uploaded_file.read())

            # Create a new in-memory zip to hold output files
            output_zip_buffer = BytesIO()

            with zipfile.ZipFile(zip_bytes, "r") as zip_file:
                file_list = [name for name in zip_file.namelist() if name.endswith(".json") and not name.endswith("/")]
                total_files = len(file_list)

                if total_files == 0:
                    st.warning("No JSON files found in the ZIP.")
                else:
                    st.subheader("📁 Contents of ZIP:")
                    for name in zip_file.namelist():
                        st.text(name)

                    # Open output ZIP
                    with zipfile.ZipFile(output_zip_buffer, "w", zipfile.ZIP_DEFLATED) as output_zip:
                        for idx, name in enumerate(file_list, start=1):
                            try:
                                with zip_file.open(name) as file:
                                    data = json.load(file)
                                    log(f"Loaded: {name}")

                                    st.markdown(f"### 📄 File: `{name}`")

                                    # Generate Markdown
                                    if include_markdown:
                                        markdown_output = json.dumps(data, indent=2)
                                        md_filename = name.replace(".json", ".md")
                                        output_zip.writestr(md_filename, markdown_output)
                                        log(f"Markdown added to ZIP: {md_filename}")

                                    # Generate Word
                                    if include_word:
                                        doc = Document()
                                        doc.add_heading("Generated Document", 0)
                                        doc.add_paragraph(json.dumps(data, indent=2))
                                        doc_buffer = BytesIO()
                                        doc.save(doc_buffer)
                                        doc_filename = name.replace(".json", ".docx")
                                        output_zip.writestr(doc_filename, doc_buffer.getvalue())
                                        log(f"Word doc added to ZIP: {doc_filename}")

                            except Exception as e:
                                error_msg = f"Error processing {name}: {e}"
                                log(error_msg)

                            # Update progress bar
                            progress = idx / total_files
                            progress_bar.progress(progress)
                            status_text.text(f"Processed {idx} of {total_files} files...")

                # Finish writing to ZIP
                output_zip_buffer.seek(0)

                # Show final download
                st.download_button("📦 Download All Output Files (ZIP)", output_zip_buffer.getvalue(), file_name="xoul_outputs.zip")
                log("Final ZIP download ready.")

            # Done message
            status_text.success("🎉 All files processed!")
            log(f"All files processed.")

        except Exception as e:
            st.error(f"❌ Failed to open ZIP: {e}")
            log(f"Failed to open ZIP: {e}")

        # Activity log section
        st.subheader("📜 Debug Log", divider=True)
        st.markdown("Send this to Vector if you run into problems. **DOWNLOAD YOUR FILE FIRST**, clicking the 📥 Download Log button will reset the form and you'll lose the results!")

        # Prepare log string
        log_str = "\n".join(log_messages)

        # Display the download button to save the log
        log_download_timestamp = get_timestamp()
        st.download_button("📥 Download Log", log_str, file_name=f"{log_download_timestamp}_xoul_convert_log.txt") # TODO: hold results in memory so this doesn't happen

        # Show log output with timestamps in a scrollable code block
        st.code(log_str, language="bash")

        enable_user_options()

