# doc_generation/docs_generation_manager.py
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


def generate_all_docs(all_data: AllData, user_options: UserOptions) -> list[FileBuffer]:
    doc_buffers: list[FileBuffer] = []
    
    for fmt in user_options.selected_formats:
        generate_docs_fn = FORMAT_GENERATORS.get(fmt)
        if generate_docs_fn:
            doc_buffers.extend(generate_docs_fn(all_data, user_options))
        else:
            log(f"Warning: No generator found for format '{fmt}'") # TODO: fix log message

    return doc_buffers