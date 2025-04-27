# doc_generation/type_group_generators/nonchat_word_doc_generator.py
from io import BytesIO
from os import path
from typing import Any, Callable, Optional
from docx import Document
from doc_generation.doc_generators.word.word_xoulai_chat_multi import word_xoulai_generate_chat_multi_docs
from doc_generation.doc_generators.word.word_xoulai_chat_single import word_xoulai_generate_chat_single_docs
from models.platform_xoulai.all_data_xoulai import AllDataXoulAI
from models.platform_xoulai.chat_single_xoulai import ChatSingleXoulAI
from utils.custom_logger import log
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
        "chats_single": word_xoulai_generate_chat_single_docs,
        "chats_multi": word_xoulai_generate_chat_multi_docs,
    },
    # Platform.ANOTHER: {
    #     "xouls": word_another_add_all_characters_to_doc,
    # }
}

# def generate_chat_single_word_docs(all_data: AllData, on_progress=None):
#     CONTENT_TYPE = "chats_single"

#     doc_buffers: list[FileBuffer] = []

#     for platform_data in all_data.get_all_platform_data():
#         content_fn = PLATFORM_CONTENT_GENERATORS[platform_data.platform].get(CONTENT_TYPE)
#         if content_fn:
#             doc_buffers = content_fn(platform_data, on_progress)
        
#     return doc_buffers

# def generate_chat_multi_word_docs(all_data: AllData, on_progress=None):
#     CONTENT_TYPE = "chats_multi"

#     doc_buffers: list[FileBuffer] = []

#     for platform_data in all_data.get_all_platform_data():
#         content_fn = PLATFORM_CONTENT_GENERATORS[platform_data.platform].get(CONTENT_TYPE)
#         if content_fn:
#             doc_buffers = content_fn(platform_data, on_progress)
        
#     return doc_buffers

# # chat generators dispatch dictionary
# CHAT_GENERATORS = {
#     "chats_single": generate_chat_single_word_docs,
#     "chats_multi": generate_chat_multi_word_docs,
# }

# # Generate Doc
# def generate_chat_word_docs(all_data: AllData, user_options: UserOptions, on_progress=None) -> list[FileBuffer]:
#     doc_buffers: list[FileBuffer] = []
    
#     for content_type in user_options.selected_content:
#         generate_docs_fn = CHAT_GENERATORS.get(content_type)
#         if generate_docs_fn:
#             doc_buffers.extend(generate_docs_fn(all_data, on_progress))
#         else:
#             log(f"Warning: No generator found for content type: '{content_type}'") # TODO: fix log message

#     return doc_buffers

# TODO: put on_progress type hint everywhere
def generate_chat_word_docs(all_data: AllData, user_options: UserOptions, on_progress: Optional[Callable] = None) -> list[FileBuffer]:
    """
    Generates Word documents for selected chat-related content across platforms.

    This function iterates through the selected content types (e.g., "chats_single", "chats_multi")
    and the available platforms (e.g., Xoulai, Another), calling the appropriate
    platform-specific generator function for each combination.

    Args:
        all_data: An AllData object containing data for all platforms.
        user_options: A UserOptions object specifying which content types to generate.
        on_progress: An optional callback function to report progress.

    Returns:
        A list of FileBuffer objects, each containing a generated Word document.
    """
    doc_buffers: List[FileBuffer] = []

    for platform_data in all_data.get_all_platform_data():
        platform_generators = PLATFORM_CONTENT_GENERATORS.get(platform_data.platform)
        if platform_generators:
            for content_type in user_options.selected_content:
                generate_docs_fn = platform_generators.get(content_type)
                if generate_docs_fn:
                    doc_buffers.extend(generate_docs_fn(platform_data, on_progress))
                else:
                    log(f"Warning: No generator found for content type '{content_type}' on platform '{platform_data.platform.value}'")
        else:
            log(f"Warning: No generator found for platform '{platform_data.platform.value}'")

    return doc_buffers