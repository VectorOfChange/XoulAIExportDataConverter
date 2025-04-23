# generate_docs/generate_word_doc.py

from io import BytesIO
from docx import Document
from docx.document import Document as DocxDocument
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml.ns import qn
from docx.oxml import OxmlElement 
from models.all_data import AllData
from models.character import Character

def add_character_to_doc(doc: DocxDocument, character: Character):
    # Add Heading 1 with the character's name
    doc.add_heading(character.name or "Unnamed Character", level=1)

    # Iterate over the character fields dynamically
    for field_name, value in vars(character).items():
        if field_name == "name":
            continue  # already used in Heading 1

        # Format the field name nicely (e.g., backstory_spec -> Backstory Spec)
        formatted_name = field_name.replace('_', ' ').title()
        doc.add_heading(formatted_name, level=2)

        # Handle the field content
        if value:
            if isinstance(value, list):
                doc.add_paragraph(", ".join(str(item) for item in value))
            else:
                doc.add_paragraph(str(value))
        else:
            doc.add_paragraph("None/Empty")


def add_all_characters_to_doc(doc: DocxDocument, characters):
    for index, character in enumerate(characters):
        add_character_to_doc(doc, character)
        if index < len(characters) - 1:
            doc.add_page_break()
    

def generate_word_docs(all_data: AllData) -> BytesIO:
    doc = Document()

    # Title Page
    title = doc.add_paragraph("Converted Xoul AI Data", style='Title')
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    subtitle = doc.add_paragraph("Xouls - Beta Test", style='Subtitle')
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_page_break()
    
    # TOC
    doc.add_heading("Table of Contents", 0)
    toc_paragraph = doc.add_paragraph()
    toc_run = toc_paragraph.add_run()
    fldChar = OxmlElement('w:fldChar')  # creates a new element
    fldChar.set(qn('w:fldCharType'), 'begin')  # sets attribute on element
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')  # sets attribute on element
    instrText.text = 'TOC \\o "1-3" \\h \\z \\u'   # change 1-3 depending on heading levels you need

    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:t')
    fldChar3.text = "Right-click on this text, then click Update Field to show the  Table of Contents."
    fldChar2.append(fldChar3)

    fldChar4 = OxmlElement('w:fldChar')
    fldChar4.set(qn('w:fldCharType'), 'end')

    r_element = toc_run._r
    r_element.append(fldChar)
    r_element.append(instrText)
    r_element.append(fldChar2)
    r_element.append(fldChar4)

    toc_run.add_break(WD_BREAK.PAGE)
    
    # Content
    add_all_characters_to_doc(doc, all_data.characters)

    # Save document to buffer
    doc_buffer = BytesIO()
    doc.save(doc_buffer)
    
    return doc_buffer

    # doc_filename = name.replace(".json", ".docx")
    # output_zip.writestr(doc_filename, doc_buffer.getvalue())
    # log(f"Word doc added to ZIP: {doc_filename}")