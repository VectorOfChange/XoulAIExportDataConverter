import streamlit as st
import zipfile
import json
from io import BytesIO
from docx import Document

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
                                log_messages.append(f"✅ Loaded: {name}")

                                st.markdown(f"### 📄 File: `{name}`")
                                st.json(data)

                                # Generate Markdown
                                if include_markdown:
                                    markdown_output = json.dumps(data, indent=2)
                                    st.download_button(f"⬇ Download Markdown ({name})", markdown_output, file_name=f"{name}.md")
                                    log_messages.append(f"📄 Markdown generated: {name}.md")

                                # Generate Word
                                if include_word:
                                    doc = Document()
                                    doc.add_heading("Generated Document", 0)
                                    doc.add_paragraph(json.dumps(data, indent=2))

                                    buffer = BytesIO()
                                    doc.save(buffer)
                                    st.download_button(f"⬇ Download Word (.docx) ({name})", buffer.getvalue(), file_name=f"{name}.docx")
                                    log_messages.append(f"📄 Word doc generated: {name}.docx")

                        except Exception as e:
                            error_msg = f"❌ Error processing {name}: {e}"
                            log_messages.append(error_msg)

                        # Update progress bar
                        progress = idx / total_files
                        progress_bar.progress(progress)
                        status_text.text(f"Processed {idx} of {total_files} files...")

        # Done message
        status_text.success("🎉 All files processed!")

    except Exception as e:
        st.error(f"❌ Failed to open ZIP: {e}")
        log_messages.append(f"❌ Failed to open ZIP: {e}")

    # Activity log
    st.subheader("📜 Activity Log")
    log_str = "\n".join(log_messages)
    st.code(log_str, language="bash")