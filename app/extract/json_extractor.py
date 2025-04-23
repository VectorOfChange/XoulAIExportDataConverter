import streamlit as st
import zipfile
import json

from app.models.character import Character
from app.models.all_data import AllData
from app.utils.custom_logger import log

# Parsers
def parse_character_jsons(json_list) -> List[Character]:
    return [Character(**item) for item in json_list]

def extract_data(zip_file: zipfile.ZipFile, on_progress=None) -> AllData:
    character_jsons = []
    # scenario_jsons = []
    # chats_multi_jsons = []
    # chats_single_jsons = []
    # persona_jsons = []
    # xoul_jsons = []
    # asset_jsons = []

    # A dictionary to map prefixes to their corresponding type lists and parsers
    type_parsers = {
        'c': character_jsons, # character folder
        # 's': scenario_jsons, # scenario folder
        # 'chats_m': chats_multi_jsons, # chats_multi folder
        # 'chats_s': chats_single_jsons, # chats_single folder
        # 'p': persona_jsons, # persona folder
        # 'x': xoul_jsons, # xoul folder
        # 'a': asset_jsons, # asset folder
    }

    file_list = [name for name in zip_file.namelist() if name.endswith(".json") and not name.endswith("/")]
    st.session_state.total_files = len(file_list)

    if st.session_state.total_files == 0:
        st.warning("No JSON files found in the ZIP.")
        # TODO: make sure this case is handled, add logging, etc
    else:
        # Iterate over the files and categorize them based on the name prefix
        for name in file_list:
            try:
                with zip_file.open(name) as file:
                    json_data = json.load(file)
                    
                    for prefix, type_list in type_parsers.items():
                        if file.name.startswith(prefix):
                            type_list.append(json_data)
                            break  # No need to check further once a match is found
            
            except Exception as e:
                error_msg = f"Error processing {name}: {e}"
                log(error_msg)
            
            # TODO: log the found and categorized folders

    # Parse each category's data and return the AllData instance
    return AllData(
        characters=parse_character_jsons(character_jsons),
        # scenarios=parse_scenario_jsons(scenario_jsons),
        # chats_multi=parse_chat_multi_jsons(chat_multi_jsons),
        # chats_single=parse_chat_single_jsons(chat_single_jsons),
        # personas=parse_persona_jsons(persona_jsons),
        # xouls=parse_xoul_jsons(xoul_jsons),
        # assets=parse_asset_jsons(asset_jsons)
    )


        # TODO: add progress bar back in
        # if on_progress:
        #     on_progress(i / 10)
