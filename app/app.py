import streamlit as st
import zipfile
import json
from io import BytesIO
from docx import Document
from datetime import datetime

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

uploaded_file = st.file_uploader("Upload your Xoul AI Data Export Zip file", type=["zip"])

include_markdown = st.checkbox("Include Markdown output", value=True)
include_word = st.checkbox("Include Word (.docx) output", value=True)

# Initialize log message list
log_messages = []

if uploaded_file is not None:
    st.success("✅ ZIP file uploaded!")

    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        zip_bytes = BytesIO(uploaded_file.read())

        with zipfile.ZipFile(zip_bytes, "r") as zip_file:
            file_list = [name for name in zip_file.namelist() if name.endswith(".json") and not name.endswith("/")]
            total_files = len(file_list)

            if total_files == 0:
                st.warning("No JSON files found in the ZIP.")
            else:
                st.subheader("📁 Contents of ZIP:")
                for name in zip_file.namelist():
                    st.text(name)

                with st.spinner("🔄 Processing files..."):
                    for idx, name in enumerate(file_list, start=1):
                        try:
                            with zip_file.open(name) as file:
                                data = json.load(file)
                                log(f"Loaded: {name}")

                                st.markdown(f"### 📄 File: `{name}`")
                                #st.json(data)

                                # Generate Markdown
                                if include_markdown:
                                    markdown_output = json.dumps(data, indent=2)
                                    st.download_button(f"⬇ Download Markdown ({name})", markdown_output, file_name=f"{name}.md")
                                    log(f"Markdown generated: {name}.md")

                                # Generate Word
                                if include_word:
                                    doc = Document()
                                    doc.add_heading("Generated Document", 0)
                                    doc.add_paragraph(json.dumps(data, indent=2))

                                    buffer = BytesIO()
                                    doc.save(buffer)
                                    st.download_button(f"⬇ Download Word (.docx) ({name})", buffer.getvalue(), file_name=f"{name}.docx")
                                    log(f"Word doc generated: {name}.docx")

                        except Exception as e:
                            error_msg = f"Error processing {name}: {e}"
                            log(error_msg)

                        # Update progress bar
                        progress = idx / total_files
                        progress_bar.progress(progress)
                        status_text.text(f"Processed {idx} of {total_files} files...")

        # Done message
        status_text.success("🎉 All files processed!")
        log(f"All files processed.")

    except Exception as e:
        st.error(f"❌ Failed to open ZIP: {e}")
        log(f"Failed to open ZIP: {e}")

    # Activity log section
    st.subheader("📜 Activity Log")

    # Prepare log string
    log_str = "\n".join(log_messages)

    # Display the download button to save the log
    st.download_button("📥 Download Log", log_str, file_name="xoul_log.txt")

    # Show log output with timestamps in a scrollable code block
    st.code(log_str, language="bash")