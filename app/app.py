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

if uploaded_file is not None:
    st.success("ZIP file uploaded!")

    try:
        # Step 1: Read ZIP into memory
        zip_bytes = BytesIO(uploaded_file.read())

        # Step 2: Open as zip file
        with zipfile.ZipFile(zip_bytes, "r") as zip_file:
            # Optional: Show list of files
            st.subheader("📁 Contents of ZIP:")
            for name in zip_file.namelist():
                st.text(name)

            # Step 3: Process each file in memory
            for name in zip_file.namelist():
                if name.endswith(".json") and not name.endswith("/"):  # skip folders
                    with zip_file.open(name) as file:
                        try:
                            data = json.load(file)
                            st.success("JSON loaded successfully!")

                            # Show preview
                            st.subheader("🔍 Preview")
                            st.json(data)

                            # Generate Markdown
                            markdown_output = json.dumps(data, indent=2)
                            if include_markdown:
                                st.download_button("⬇ Download Markdown", markdown_output, file_name="output.md")

                            # Generate Word
                            if include_word:
                                doc = Document()
                                doc.add_heading("Generated Document", 0)
                                doc.add_paragraph(json.dumps(data, indent=2))

                                buffer = BytesIO()
                                doc.save(buffer)
                                st.download_button("⬇ Download Word (.docx)", buffer.getvalue(), file_name="output.docx")
                            # # Read and decode JSON
                            # json_data = file.read().decode("utf-8")
                            # st.markdown(f"### 📄 File: `{name}`")
                            # st.json(json_data)
                        except Exception as e:
                            st.warning(f"❌ Could not read {name}: {e}")

    except Exception as e:
        st.error(f"❌ Failed to parse JSON: {e}")