# doc_generation/type_group_generators/nonchat_word_doc_generator.py
from io import BytesIO
from os import path
from docx import Document
from doc_generation.doc_generators.word.word_xoulai_character import word_xoulai_add_all_characters_to_doc
from doc_generation.doc_generators.word.word_xoulai_lorebook import word_xoulai_add_all_lorebooks_to_doc
from doc_generation.doc_generators.word.word_xoulai_persona import word_xoulai_add_all_personas_to_doc
from doc_generation.doc_generators.word.word_xoulai_scenerio import word_xoulai_add_all_scenarios_to_doc
from doc_generation.doc_generators.word.word_common import word_add_info_section_to_doc, word_add_known_bugs_section_to_doc, word_add_title_page_to_doc, word_add_toc_to_doc
from dtos.file_buffer import FileBuffer
from dtos.user_options import UserOptions
from enums.platform import Platform
from enums.type_group import TypeGroup
from models.all_data import AllData

PLATFORM_CONTENT_GENERATORS = {
    Platform.XOULAI: {
        "characters": word_xoulai_add_all_characters_to_doc,
        "scenarios": word_xoulai_add_all_scenarios_to_doc,
        "personas": word_xoulai_add_all_personas_to_doc,
        "lorebooks": word_xoulai_add_all_lorebooks_to_doc,
    },
    # Platform.ANOTHER: {
    #     "xouls": word_another_add_all_characters_to_doc,
    # }
}

# Generate Doc
def generate_nonchat_word_docs(all_data: AllData, user_options: UserOptions) -> list[FileBuffer]:
    doc_buffers: list[FileBuffer] = []

    for platform_data in all_data.get_all_platform_data():
        doc = Document(path.join('app', 'assets', 'numbered_heading_template.docx'))

        # Content
        word_add_title_page_to_doc(doc, platform_data.platform, TypeGroup.NONCHAT)
        word_add_toc_to_doc(doc)
        word_add_info_section_to_doc(doc, platform_data.platform)
        word_add_known_bugs_section_to_doc(doc)
        
        for content_type in user_options.selected_content:
            content_fn = PLATFORM_CONTENT_GENERATORS[platform_data.platform].get(content_type)
            if content_fn:
                content_fn(doc, getattr(platform_data, content_type))

        # Save document to buffer
        doc_buffer = BytesIO()
        doc.save(doc_buffer)

        # get filename
        filename = f"XoulAI_NonChat_Data_For_{platform_data.platform}.docx"
        
        doc_buffers.append(FileBuffer(doc_buffer, filename))

    return doc_buffers

        # doc_filename = name.replace(".json", ".docx")
        # output_zip.writestr(doc_filename, doc_buffer.getvalue())
        # log(f"Word doc added to ZIP: {doc_filename}")