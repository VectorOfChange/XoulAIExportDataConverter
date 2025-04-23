# generate_docs/docs_generator.py

from app.generate_docs.generate_word_docs import generate_word_docs
from utils.custom_logger import log
from models.all_data import AllData

# formats dispatch dictionary
format_generators = {
    "word": generate_word_docs,
    #"txt": generate_txt,
    #"md": generate_md,
}


def generate_docs(all_data: AllData, selected_formats) -> list:
    doc_buffers = []
    
    for fmt in selected_formats:
        generate_docs_fn = format_generators.get(fmt)
        if generate_docs_fn:
            doc_buffers.append(generate_docs_fn(all_data))
        else:
            log(f"Warning: No generator found for format '{fmt}'") # TODO: fix log message

    return doc_buffers