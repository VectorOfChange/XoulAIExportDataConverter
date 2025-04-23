# generate_docs/generate_word_doc.py

from io import BytesIO
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml.ns import qn
from docx.oxml import OxmlElement 
from models.all_data import AllData

def generate_word_docs(all_data: AllData) -> BytesIO:
    doc = Document()

    # Title Page
    title = doc.add_paragraph("Converted Xoul AI Data", style='Title')
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    subtitle = doc.add_paragraph("Xouls - Beta Test", style='Subtitle')
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.add_run().add_break(WD_BREAK.PAGE)
    
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
    doc.add_heading("Test Heading 1", 1)
    doc.add_paragraph("Heading 1 Level")
    doc.add_heading("Test Heading 2", 2)
    doc.add_paragraph("Heading 2 Level")
    doc.add_heading("Test Heading 2", 2)
    doc.add_paragraph("Heading 2 Level")
    doc.add_heading("Test Heading 3", 3)
    doc.add_paragraph("Heading 3 Level")
    doc.add_heading("Test Heading 4", 4)
    doc.add_paragraph("Heading 4 Level")

    # doc.add_paragraph(json.dumps(data, indent=2))
    
    # Save document to buffer
    doc_buffer = BytesIO()
    doc.save(doc_buffer)
    
    return doc_buffer

    # doc_filename = name.replace(".json", ".docx")
    # output_zip.writestr(doc_filename, doc_buffer.getvalue())
    # log(f"Word doc added to ZIP: {doc_filename}")