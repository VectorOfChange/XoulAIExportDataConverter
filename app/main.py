# main.py
import re
import streamlit as st
import zipfile
from io import BytesIO

from dtos.user_options import UserOptions
from globals.globals import APP_VERSION, KNOWN_BUGS
from doc_generation.doc_generation_manager import generate_all_docs
from extract.json_extractor import extract_data
from utils.custom_logger import log
from utils.custom_timestamp import get_timestamp

# Constants
# moved to globals module

# Session state for user options
if "user_options_disabled" not in st.session_state:
    st.session_state.user_options_disabled = False

# Session state for holding output
# if you add something here, remember to reset it in the reset button action
if "processed" not in st.session_state:
    st.session_state.processed = False
if "output_zip" not in st.session_state:
    st.session_state.output_zip = None
if "log_output" not in st.session_state:
    st.session_state.log_output = ""
if "log_messages" not in st.session_state:
    st.session_state.log_messages = []
if "total_raw_files" not in st.session_state:
    st.session_state.total_raw_files = 0
if "total_doc_files" not in st.session_state:
    st.session_state.total_doc_files = 0
if "completed_doc_files" not in st.session_state:
    st.session_state.completed_doc_files = 0
if "completed_tasks" not in st.session_state:
    st.session_state.completed_tasks = 0

# flags
reset_button_visible = False

def sanitize_filename(filename: str) -> str:
    # Remove unsafe characters and trim length
    filename = re.sub(r'[^a-zA-Z0-9_\-\. ]', '_', filename)
    return filename[:200]  # Limit to 200 characters

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
    st.session_state.total_raw_files = 0
    st.session_state.total_doc_files = 0
    st.session_state.completed_doc_files = 0
    st.session_state.completed_tasks = 0

# Function to show reset button
def show_reset_button():
    global reset_button_visible
    
    if not reset_button_visible:
        reset_button_visible = True
        with func_button_col2:
            st.button("⬅️ Restart (Clears Results)", on_click=reset_app)

# Function to show process button
def show_process_button(user_option_content_choices: list, user_option_platform_choices: list, user_option_format_choices: list):
    user_choices_invalid = (
        not any(user_option_content_choices)
        or not any(user_option_platform_choices)
        or not any(user_option_format_choices)
    )
    
    process_button_disabled = ( 
        st.session_state.user_options_disabled
        or user_choices_invalid
    )

    with func_button_col1:
        process_button_internal = st.button("🚀 Process File", on_click=disable_user_options, type="primary", disabled=process_button_disabled)
    
    if user_choices_invalid:
        st.error("Invalid choices. Review Step 1. Make sure there's at least one box checked in each group of choices.")

    return process_button_internal

# Function to update progress for JSON extraction
def update_extraction_progress(completed_files: int) -> None:
    """
    Update the extraction progress bar and status text with the number of completed files.

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
    progress = completed_files / st.session_state.total_raw_files
    extraction_progress_bar.progress(progress)
    status_message = f"Extracted data from {completed_files} of {st.session_state.total_raw_files} JSON files..."
    
    if progress == 1:
        extraction_status_text.success("🎉 " + status_message)
    else:
        extraction_status_text.text(status_message)
    
    log(status_message)

# Function to update progress for JSON extraction
def increment_doc_generation_progress() -> None:
    """
    Increment the document generation progress bar and status text with the number of completed files.
    """
    st.session_state.completed_doc_files += 1

    progress = st.session_state.completed_doc_files / st.session_state.total_doc_files
    doc_generation_progress_bar.progress(progress)
    status_message = f"Generated {st.session_state.completed_doc_files} of {st.session_state.total_doc_files} Documents..."
    
    if progress == 1:
        doc_generation_status_text.success("🎉 " + status_message)
    else:
        doc_generation_status_text.text(status_message)

    log(status_message)

def increment_data_manipulation_progress() -> None:
    """
    Increment the document generation progress bar and status text with the number of completed files.

    NOTE: THIS JUST SETS IT TO COMPLETE. WRITE FOR REAL ONCE DATA MANIP IS ADDED
    """
    manipulation_progress_bar.progress(1.0)
    manipulation_status_text.success("Skipped...Data Manipulation Feature Not Available Yet")

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
                    | Personas | ```beta``` | 
                    | Scenarios | ```beta``` | 
                    | Lorebooks | ```beta``` |
                    | Single Chats | ```beta``` |
                    | Group Chats | ```beta``` |
                    | Images/Avatars | ```in progress``` |
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

    with st.expander("Contact/Technical Issues"):
        st.markdown("The best way to contact me is to send me a discord DM: @vectorofchange (join the [Xoul Discord](https://discord.gg/xoul) to get access to DM me)")
        st.markdown("You can also tag me (@VectorOfChange) in the #alts channel in the Xoul Discord.")
        st.markdown("If you don't use Discord, you can start an Issue on Github on the source code. **Note:** Anything you put here will be public.")
        st.header(":red[Technical Issue or Bug?]")
        st.subheader(":red[**Save the log**] so you can send it to me!")
        st.markdown("You can do this by using the button just above the log (at the bottom of the page) or copy/pasting it")
    
    st.subheader("Known Bugs")
    with st.expander("Known Bugs"):
        if KNOWN_BUGS:
            for bug in KNOWN_BUGS:
                st.markdown("- " + f"({bug['type'].value}): {bug['description']}")
        else:
            st.markdown("- No known bugs")


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
st.markdown("The file upload may not work on mobile Chrome (or Chrome based browsers like Brave). Workaround: use the ```view desktop page``` option of your mobile browser")

st.header("Get Started!")

st.subheader("Step 1: Choose Options", divider=True)

with st.expander("Xoul Data to Process", expanded=True):
    st.markdown("Choose the types of Xoul data you want to process.")
    
    user_option_content_col1, user_option_content_col2 = st.columns(2)

    user_option_content_choices = []

    with user_option_content_col1:
        user_option_content_choices.append(st.checkbox("Xouls", value=True, disabled=st.session_state.user_options_disabled, key="app_content_characters"))
        user_option_content_choices.append(st.checkbox("Personas", value=True, disabled=st.session_state.user_options_disabled, key="app_content_personas"))
        user_option_content_choices.append(st.checkbox("Scenarios", value=True, disabled=st.session_state.user_options_disabled, key="app_content_scenarios"))
    
    with user_option_content_col2:
        user_option_content_choices.append(st.checkbox("Lorebooks", value=True, disabled=st.session_state.user_options_disabled, key="app_content_lorebooks"))
        user_option_content_choices.append(st.checkbox("Individual Chats", value=True, disabled=st.session_state.user_options_disabled, key="app_content_chats_single"))
        user_option_content_choices.append(st.checkbox("Group Chats", value=True, disabled=st.session_state.user_options_disabled, key="app_content_chats_multi"))

    if not any(user_option_content_choices):
        st.error("You must choose at least one type of Xoul data to process.")

with st.expander("Platform Specific Adjustment", expanded=True):
    st.markdown("Choose the platforms you want to generate data for. Each selection will generate a set of files optimized for use with the platform.")
    
    user_option_platform_col1, user_option_platform_col2 = st.columns(2)

    user_option_platform_choices = []

    with user_option_platform_col1:
        user_option_platform_choices.append(st.checkbox("Unmodified (Original Xoul AI Data)", value=True, disabled=st.session_state.user_options_disabled, key="app_platform_xoulai"))
        # user_option_platform_choices.append(st.checkbox("MyAI", value=False, disabled=st.session_state.user_options_disabled, key="app_platform_myai"))
    
    # with user_option_platform_col2:
    #     user_option_platform_choices.append(st.checkbox("Wyvern", value=False, disabled=st.session_state.user_options_disabled, key="app_platform_wyvern"))
    #     user_option_platform_choices.append(st.checkbox("CharSnap", value=False, disabled=st.session_state.user_options_disabled, key="app_platform_charsnap"))
    #     user_option_platform_choices.append(st.checkbox("Sakura", value=False, disabled=st.session_state.user_options_disabled, key="app_platform_sakura"))
    
    # st.markdown("* Tavern Card v2 JSON is a type of JSON that is accepted at many sites. Make sure you choose JSON output in the ```File Output Types```` section below.") # TODO: create Tavern Card v2 FAQ
    
    if not any(user_option_platform_choices):
        st.error("You must choose at least one platform to generate data for.")

with st.expander("File Output Types", expanded=True):
    st.markdown("Choose the types of files you want to generate.")
    
    user_option_format_col1, user_option_format_col2 = st.columns(2)

    user_option_format_choices = []

    with user_option_format_col1:
        user_option_format_choices.append(st.checkbox("Word (.docx)", value=True, disabled=st.session_state.user_options_disabled, key="app_format_word"))
    #     user_option_format_choices.append(st.checkbox("Text (.txt)", value=False, disabled=st.session_state.user_options_disabled, key="app_format_txt"))
    
    # with user_option_format_col2:
    #     user_option_format_choices.append(st.checkbox("Markdown (.md)", value=False, disabled=st.session_state.user_options_disabled, key="app_format_md"))
    #     user_option_format_choices.append(st.checkbox("Platform Specific JSON (.json)", value=False, disabled=st.session_state.user_options_disabled, key="app_format_json"))
    
    # st.markdown("* Platform Specific JSON files are used by specific platforms and not interchangeable with other platforms. This will only be generated for platforms that support JSON importing.") # TODO: Create JSON file FAQ

    if not any(user_option_format_choices):
        st.error("You must choose at least one file output type to generate.")

# TODO: For chat transcripts, documents are only Xoul AI platform, other platforms are only JSON. Enforce options if needed, add note about this, code exceptions in backend
# TODO: JSON output shouldn't do Xoul AI platform

st.subheader("Step 2: Upload File", divider=True)
uploaded_file = st.file_uploader("Upload your Xoul AI Data Export Zip file", type=["zip"])

if uploaded_file is not None:
    st.success("✅ ZIP file uploaded!")

    st.subheader("Step 3: Start Processing", divider=True)
    

    # Show process button
    func_button_col1, func_button_col2 = st.columns(2)
    
    process_button = show_process_button(user_option_content_choices, user_option_platform_choices, user_option_format_choices)

    if process_button and not st.session_state.processed:
        
        show_reset_button()

        # get user options

        user_options = UserOptions.from_session_state()

        st.subheader("Step 4: Wait for Processing to Finish", divider=True)        
        
        progress_col1, progress_col2, progress_col3 = st.columns(3)
        
        with progress_col1:
            # Data Extraction Progress bar
            st.markdown("Data Extraction Progress")
            extraction_progress_bar = st.progress(0)
            extraction_status_text = st.empty()
        
        with progress_col2:
            # Data Manipulation Progress bar
            st.markdown("Data Manipulation Progress")
            manipulation_progress_bar = st.progress(0)
            manipulation_status_text = st.empty()
        
        with progress_col3:
            # Document Creation Progress bar
            st.markdown("Document Creation Progress")
            doc_generation_progress_bar = st.progress(0)
            doc_generation_status_text = st.empty()

        try:
            zip_bytes = BytesIO(uploaded_file.read())

            with zipfile.ZipFile(zip_bytes, "r") as zip_file:
                try:
                    with progress_col2, st.spinner("Extraing Data..."):
                        all_data = extract_data(zip_file, on_progress=update_extraction_progress)

                except ValueError as extract_error:
                    error_msg = f"Error during JSON Extraction: {extract_error}"
                    log(error_msg)
                    st.error(error_msg)
                    # TODO: properly handle this error, stop processing, show reset button, disable download button

                # TODO: add success and error files count


        except Exception as unzip_e:
            st.error(f"❌ Failed to open ZIP: {unzip_e}")
            log(f"Failed to open ZIP: {unzip_e}")

        # Manipulate Data
        increment_data_manipulation_progress()

        # GENERATE AND SAVE DOCUMENTS
        # TODO: split into two sections to get better logging and error reporting
        try:
            with progress_col3, st.spinner("Generating Docs..."):
                generated_doc_buffers = generate_all_docs(all_data, user_options, on_progress=increment_doc_generation_progress)

            # Open output ZIP
            # Create a new in-memory zip to hold output files
            output_zip_buffer = BytesIO()

            with zipfile.ZipFile(output_zip_buffer, "w", zipfile.ZIP_DEFLATED) as output_zip: 
                for doc_buffer in generated_doc_buffers:
                    doc_filename = sanitize_filename(doc_buffer.filename)
                    output_zip.writestr(doc_filename, doc_buffer.buffer.getvalue())
                    log(f"Document added to ZIP: {doc_filename}")

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
        show_reset_button()

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

st.subheader("Changelog")
st.markdown("""
            * Version ```0.0.1```:
                * FEATURE: Initial Version
                * FEATURE: Process Xouls into Word Document
            * Version ```0.0.2```:
                * FEATURE: Add processing Personas, Scenarios, and Lorebooks
                * GUI: Significant updates including sidebar
            * Version ```0.0.3```:
                * FEATURE: Make options use selectable
                * Refactor backend to prepare for expansion
            * Version ```0.0.4```:
                * FEATURE: Generate individual chats
                * FEATURE: Generate group chats
                * GUI: Enforce valid user choices
                * GUI: Fix and enhance progress bar
                * FIX: Only include bugs that impact data in the documents
            """)

st.subheader("Page suddenly scrolled to the bottom? It's a bug. Sorry about that! Scroll up ⬆️ to find your files again.", divider=False)

# TODO: Add JSON explainer
# TODO: Add jump to links and jump back to to top links