# main.py
import streamlit as st
import zipfile
from io import BytesIO

from globals.globals import APP_VERSION
from generate_docs.docs_generator import generate_docs
from extract.json_extractor import extract_data
from utils.custom_logger import log
from utils.custom_timestamp import get_timestamp

# Constants
# moved to globals module

# Session state for user options
if "user_options_disabled" not in st.session_state:
    st.session_state.user_options_disabled = False

# Session state for holding output
if "processed" not in st.session_state:
    st.session_state.processed = False
if "output_zip" not in st.session_state:
    st.session_state.output_zip = None
if "log_output" not in st.session_state:
    st.session_state.log_output = ""
if "log_messages" not in st.session_state:
    st.session_state.log_messages = []
if "total_files" not in st.session_state:
    st.session_state.total_files = 0

# flags
reset_button_visible = False
process_button_visible = False

# Function to disable the user options
def disable_user_options():
    st.session_state.user_options_disabled = True

# Function to enable the user options
def enable_user_options():
    st.session_state.user_options_disabled = False

# reset everything
def reset_app():
    enable_user_options()
    st.session_state.processed = False
    st.session_state.output_zip = None
    st.session_state.log_output = ""
    st.session_state.log_messages = []
    st.session_state.total_files = 0

# Function to show reset button
def show_reset_button():
    global reset_button_visible
    
    if not reset_button_visible:
        reset_button_visible = True
        func_button_col2.button("⬅️ Restart (Clears Results)", on_click=reset_app)

# Function to show process button
def show_process_button():
    global process_button_visible
    
    if not process_button_visible:
        process_button_visible = True
        with func_button_col1:
            process_button_internal = st.button("🚀 Process File", on_click=disable_user_options, type="primary", disabled=st.session_state.user_options_disabled)
        
        return process_button_internal

# Function to update progress for JSON extraction
def update_extraction_progress(completed_files: int) -> None:
    """
    Update the progress bar and status text with the number of completed files.

    Args:
        completed_files (int): The number of files that have been fully processed.
            NOTE: If this function is called from within a loop using enumerate,
            ensure you pass in (index + 1) since enumerate is zero-indexed and this
            function expects a 1-based count of completed files.

    Example:
        for i, file in enumerate(files):
            process(file)
            update_extraction_progress(i + 1)

    This function can also be called from non-loop contexts where an exact count of
    completed files is tracked separately.
    """
    progress = completed_files / st.session_state.total_files
    progress_bar.progress(progress)
    status_message = f"Extracted JSON from {completed_files} of {st.session_state.total_files} JSON files..."
    status_text.text(status_message)
    log(status_message)

st.set_page_config(page_title="Xoul AI Data Converter", layout="centered")

# SIDEBAR
with st.sidebar:
    st.title("About")

    st.subheader("Supported Features")

    with st.expander("Xoul AI Data Types"):
        st.markdown("Supported data types from the Xoul Data Export Zip File")
        st.markdown("""
                    | Data Type | Status |
                    |----|----|
                    | Xouls | ```beta``` | 
                    | Personas | ```in progress``` | 
                    | Scenarios | ```in progress``` | 
                    | Lorebooks | ```in progress``` |
                    | Single Chats | ```planned``` |
                    | Multi Chats | ```planned``` |
                    """)
        
    with st.expander("Output File Types"):
        st.markdown("""
                    | File Type | Extension | Status |
                    |----|----|----|
                    | Word | .docx | ```beta``` | 
                    | Markdown | .md | ```planned``` | 
                    | Text | .txt | ```planned``` | 
                    | JSON (for supported platforms) | ```planned``` |
                    """)
        
    with st.expander("Data Conversion for Other Platforms"):
        st.markdown("This will adjust and/or convert the data from Xoul to make importing into other platforms easier.")
        st.markdown("JSON files for direct importing will be generated for  platforms that support it.")
        st.markdown("""
                    | Platform | Status | Supports JSON |
                    |----|----|----|
                    | Tavern Card (v2) | ```planned``` | ```yes``` | 
                    | MyAI | ```planned``` | ```unknown``` | 
                    | Wyvern | ```planned``` |  ```unknown``` |
                    | CharSnap | ```planned``` |  ```unknown``` |
                    | Sakura | ```planned``` | ```unknown``` |
                    """)
        st.markdown("Want other platforms? Tell me by contacting me! Details below ⬇️")
        
    with st.expander("Legend"):
        st.markdown("""
                    | Status | Meaning |
                    |----|----|
                    | ```released``` | Available |
                    | ```beta``` | Available (in testing). *May be broken* |  
                    | ```in progress``` | Being coded now |  
                    | ```planned``` | To be added soon |
                    | ```future``` | To be added...eventually (if people want it) |  
                    | ```Rejected``` | Will not be added |  
                    """)

    st.subheader("Code and Contact")
    with st.expander("Source Code"):
        st.markdown("[Github Source Code Repo](https://github.com/VectorOfChange/XoulAIExportDataConverter)")

    with st.expander("Contact/Bugs"):
        st.markdown("The best way to contact me is to send me a discord DM: @vectorofchange (join the [Xoul Discord](https://discord.gg/xoul) to get access to DM me)")
        st.markdown("You can also tag me (@VectorOfChange) in the #alts channel in the Xoul Discord.")
        st.markdown("If you don't use Discord, you can start an Issue on Github on the source code. **Note:** Anything you put here will be public.")
        st.header(":red[Technical Issue or Bug?]")
        st.subheader(":red[**Save the log**] so you can send it to me!")
        st.markdown("You can do this by using the button just above the log (at the bottom of the page) or copy/pasting it")
    
    st.subheader("More Info")

    with st.expander("Privacy Info"):
        st.markdown("Everything is 100% private. All data is kept in memory on the server, nothing is ever written to disk.")
        st.markdown("All of your data is permanently deleted from the server memory as soon as you close or refresh the webpage.")
        st.markdown("No human or machine can ever access or review your data.")

    with st.expander("App Version"):
        st.markdown(f"Version: ```{APP_VERSION}```") # TODO: Add app version to log

# MAIN PAGE
st.title("📄 Xoul AI Data Converter")

st.subheader("About")
st.markdown("This tool converts your Xoul AI exported data to other formats. This makes it easier to use your data on other platforms.")

st.subheader("🔒 Privacy")
st.markdown("Your data stays **100% private**: none of your content is stored or logged. No human or machine can review your content.")

st.subheader("⬅️ More Info is in the Sidebar")
st.markdown("It contains information on current and future features, contact details, source code link, and more.")
st.markdown("If you can't see the sidebar, click the ```>``` button at the top left of the page. This buttons changes to ```<``` when the sidebar is visible, and you can click it to hide the sidebar.")
st.markdown("""
            :red[Bugs? Errors? Technical issues?]  
            :red[Missing Data? Weird computer code in the generated documents?]  
            Report it and I'll fix it! See the ```Contact/Bugs``` section in the sidebar for details.
            """)

st.subheader("📱 Running on Phones")
st.markdown("This isn't tested on phones, but is should work properly. Please tell me if you run into problems.")

st.header("Get Started!")

st.subheader("Step 1: Choose Options", divider=True)

# include_markdown = st.checkbox("Include Markdown (.md) output", value=True, disabled=st.session_state.user_options_disabled)
include_word = st.checkbox("Include Word (.docx) output", value=True, disabled=st.session_state.user_options_disabled, key="format_word")

st.subheader("Step 2: Upload File", divider=True)
uploaded_file = st.file_uploader("Upload your Xoul AI Data Export Zip file", type=["zip"])

if uploaded_file is not None:
    st.success("✅ ZIP file uploaded!")

    st.subheader("Step 3: Start Processing", divider=True)
    st.markdown("To reset the form, click the Restart button")

    # Show process button
    func_button_col1, func_button_col2 = st.columns(2)
    
    process_button = show_process_button()

    if process_button and not st.session_state.processed:
        
        show_reset_button();

        # get user options
        selected_formats = [
            key.replace("format_", "")                  # expression
            for key, value in st.session_state.items()  # iterable
            if key.startswith("format_") and value      # condition
        ]

        st.subheader("Step 4: Wait for Processing to Finish", divider=True)        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            zip_bytes = BytesIO(uploaded_file.read())

            with zipfile.ZipFile(zip_bytes, "r") as zip_file:
                try:
                    all_data = extract_data(zip_file, on_progress=update_extraction_progress)

                except ValueError as extract_error:
                    error_msg = f"Error during JSON Extraction: {extract_error}"
                    log(error_msg)
                    st.error(error_msg)
                    # TODO: properly handle this error, stop processing, show reset button, disable download button
                
                # Done message
                # TODO: add success and error files count
                status_text.success(f"🎉 {st.session_state.total_files}/{st.session_state.total_files} files processed!")
                log(f"{st.session_state.total_files}/{st.session_state.total_files} files processed.")

                # # save results
                # st.session_state.output_zip = output_zip_buffer.getvalue()
                # st.session_state.processed = True
                # st.session_state.log_output = "\n".join(st.session_state.log_messages)

        except Exception as unzip_e:
            st.error(f"❌ Failed to open ZIP: {unzip_e}")
            log(f"Failed to open ZIP: {unzip_e}")

        # GENERATE AND SAVE DOCUMENTS
        # TODO: split into two sections to get better logging and error reporting
        try:
            generated_doc_buffers = generate_docs(all_data, selected_formats)

            # Open output ZIP
            # Create a new in-memory zip to hold output files
            output_zip_buffer = BytesIO()

            with zipfile.ZipFile(output_zip_buffer, "w", zipfile.ZIP_DEFLATED) as output_zip: 
                for doc_buffer in generated_doc_buffers:
                    doc_filename = "XoulAIBasicData_BetaTest.docx"
                    output_zip.writestr(doc_filename, doc_buffer.getvalue())
                    log(f"Word doc added to ZIP: {doc_filename}")

            # Finish writing to ZIP
            output_zip_buffer.seek(0)

            # save results
            st.session_state.output_zip = output_zip_buffer.getvalue()
            st.session_state.processed = True

        except Exception as generate_docs_e:
            st.error(f"❌ Failed to generate or save documents: {generate_docs_e}")
            log(f"Failed to generate or save documents: {generate_docs_e}")

        # Generate log output
        st.session_state.log_output = "\n".join(st.session_state.log_messages)

        # TODO: fix status bar, make it accurate, make it accommodate session_state.processed properly 

    if st.session_state.processed:            
        show_reset_button();

        st.subheader("Step 5: Download Results", divider=True)
        
        # Show final download
        output_download_timestamp = get_timestamp()
        st.download_button("📦 Download All Output Files (ZIP)", st.session_state.output_zip, file_name=f"{output_download_timestamp}_ConvertedXoulAIData.zip")
        log("Final ZIP download ready.")

        # Activity log section
        st.subheader("📜 Debug Log", divider=True)
        st.markdown("Send this to Vector if you run into problems.")

        # Display the download button to save the log
        log_download_timestamp = get_timestamp()
        st.download_button("📥 Download Log", st.session_state.log_output, file_name=f"{log_download_timestamp}_xoul_convert_log.txt") 

        # Show log output with timestamps in a scrollable code block
        st.code(st.session_state.log_output, language="bash")

        st.subheader("Page suddenly scrolled to the bottom? It's a bug. Sorry about that! Scroll up ⬆️ to find your files again.", divider=False)