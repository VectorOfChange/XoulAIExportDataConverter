# extract/json_extractor.py
import streamlit as st
import zipfile
import json

from models.platform_xoulai.all_data_xoulai import AllDataXoulAI
from models.platform_xoulai.persona_xoulai import PersonaXoulAI
from models.platform_xoulai.scenario_xoulai import ScenarioXoulAI
from models.platform_xoulai.character_xoulai import CharacterXoulAI
from models.platform_xoulai.lorebook_xoulai import LorebookXoulAI
from models.all_data import AllData
from utils.custom_logger import log

# Parsers
def parse_character_jsons(json_list) -> list[CharacterXoulAI]:
    return [CharacterXoulAI.from_dict(item) for item in json_list]

def parse_scenario_jsons(json_list) -> list[ScenarioXoulAI]:
    return [ScenarioXoulAI.from_dict(item) for item in json_list]

def parse_persona_jsons(json_list) -> list[PersonaXoulAI]:
    return [PersonaXoulAI.from_dict(item) for item in json_list]

def parse_lorebook_jsons(json_list) -> list[LorebookXoulAI]:
    return [LorebookXoulAI.from_dict(item) for item in json_list]

def extract_data(zip_file: zipfile.ZipFile, on_progress=None) -> AllData:
    character_jsons = []
    scenario_jsons = []
    # chats_multi_jsons = []
    # chats_single_jsons = []
    persona_jsons = []
    lorebook_jsons = []

    # A dictionary to map prefixes to their corresponding type lists and parsers
    type_parsers = {
        'x': character_jsons, # character folder
        's': scenario_jsons, # scenario folder
        # 'chats_m': chats_multi_jsons, # chats_multi folder
        # 'chats_s': chats_single_jsons, # chats_single folder
        'p': persona_jsons, # persona folder
        'a': lorebook_jsons, # asset folder
    }

    file_list = [name for name in zip_file.namelist() if name.endswith(".json") and not name.endswith("/")]
    st.session_state.total_files = len(file_list)

    if st.session_state.total_files == 0:
        raise ValueError("No JSON files were found in the ZIP archive.")
    else:
        # Iterate over the files and categorize them based on the name prefix
        for idx, name in enumerate(file_list):
            try:
                with zip_file.open(name) as file:
                    json_data = json.load(file)
                    json_data["source_filename"] = name
                    
                    for prefix, type_list in type_parsers.items():
                        if file.name.startswith(prefix):
                            type_list.append(json_data)
                            break  # No need to check further once a match is found
            
            except Exception as e:
                error_msg = f"Error processing {name}: {e}"
                log(error_msg)
            
            if on_progress:
                on_progress(idx + 1) # expects number of completed files, so adjust for zero-indexed loop index
            
    # TODO: log the found and categorized folders

    xoulai_data = AllDataXoulAI(
        characters=parse_character_jsons(character_jsons),
        scenarios=parse_scenario_jsons(scenario_jsons),
        # chats_multi=parse_chat_multi_jsons(chat_multi_jsons),
        # chats_single=parse_chat_single_jsons(chat_single_jsons),
        personas=parse_persona_jsons(persona_jsons),
        lorebooks=parse_lorebook_jsons(lorebook_jsons))

    # Parse each category's data and return the AllData instance
    return AllData(xoulai_data)
