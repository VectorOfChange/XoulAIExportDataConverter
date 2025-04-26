# doc_generation/format_specific_doc_orchestrators/word_doc_generation_orchestrator.py
from io import BytesIO
from app.doc_generation.type_group_generators.word_doc_chat_generator import generate_chat_word_docs
from doc_generation.type_group_generators.word_doc_nonchat_generator import generate_nonchat_word_docs
from dtos.file_buffer import FileBuffer
from models.all_data import AllData
from dtos.user_options import UserOptions

def generate_word_docs(all_data: AllData, user_options: UserOptions) -> list[FileBuffer]:
    doc_buffers: list[FileBuffer] = []

    # Extract selected content
    selected = user_options.selected_content

    # Check for chat-related content
    has_chat = "chats_single" in selected or "chats_group" in selected
    has_non_chat = any(opt not in ("chats_single", "chats_group") for opt in selected)

    if has_chat:
        doc_buffers.extend(generate_chat_word_docs(all_data, user_options))
    if has_non_chat:
        doc_buffers.extend(generate_nonchat_word_docs(all_data, user_options))

    return doc_buffers
