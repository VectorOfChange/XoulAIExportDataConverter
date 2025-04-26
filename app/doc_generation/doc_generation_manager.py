# doc_generation/docs_generation_manager.py
import streamlit as st

from io import BytesIO
from doc_generation.format_specific_doc_orchestrators.word_doc_generation_orchestrator import generate_word_docs
from dtos.file_buffer import FileBuffer
from dtos.user_options import UserOptions
from doc_generation.type_group_generators.word_doc_nonchat_generator import generate_nonchat_word_docs
from utils.custom_logger import log
from models.all_data import AllData

# formats dispatch dictionary
FORMAT_GENERATORS = {
    "word": generate_word_docs,
    #"txt": generate_txt,
    #"md": generate_md,
    #"json": generate_json,
}


def generate_all_docs(all_data: AllData, user_options: UserOptions, on_progress=None) -> list[FileBuffer]:
    doc_buffers: list[FileBuffer] = []
    
    # calculate total documents
    # AllData:
    #   1 Doc for Chars, Scenarios, Personas and Lorebooks combined
    #   1 Doc per Chat
    # TODO: Will need to be adjusted for platform specific JSON somehow... 

    all_platform_data = all_data.get_all_platform_data()

    total_docs = 0

    # if any nonchat content is selected, add one doc per platform
    if any(item in user_options.selected_content for item in ("characters", "personas", "scenarios", "lorebooks")):
        total_docs += len(all_platform_data)
    
    # each chat transcript gets its own document
    for platform_data in all_platform_data:
        if "chats_single" in user_options.selected_content:
            total_docs += len(platform_data.chats_single)
        
        if "chats_multi" in user_options.selected_content:
            total_docs += len(platform_data.chats_multi)

    st.session_state.total_doc_files = total_docs

    for fmt in user_options.selected_formats:
        generate_docs_fn = FORMAT_GENERATORS.get(fmt)
        if generate_docs_fn:
            doc_buffers.extend(generate_docs_fn(all_data, user_options, on_progress))
        else:
            log(f"Warning: No generator found for format '{fmt}'") # TODO: fix log message

    return doc_buffers