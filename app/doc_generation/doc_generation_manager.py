# doc_generation/docs_generation_manager.py
from doc_generation.type_group_generators.nonchat_word_doc_generator import generate_nonchat_word_docs
from utils.custom_logger import log
from models.all_json_data import AllJsonData

# formats dispatch dictionary
format_generators = {
    "word": generate_nonchat_word_docs,
    #"txt": generate_txt,
    #"md": generate_md,
}


def generate_all_docs(all_data: AllJsonData, selected_formats) -> list:
    doc_buffers = []
    
    for fmt in selected_formats:
        generate_docs_fn = format_generators.get(fmt)
        if generate_docs_fn:
            doc_buffers.append(generate_docs_fn(all_data))
        else:
            log(f"Warning: No generator found for format '{fmt}'") # TODO: fix log message

    return doc_buffers