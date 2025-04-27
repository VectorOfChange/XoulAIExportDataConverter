# image_fetching/discover_fetch_image_tasks.py
from typing import Any
import streamlit as st

from dtos.user_options import UserOptions
from image_fetching.fetch_image_task_register import FetchImageTaskRegister
from models.all_data import AllData
from models.platform_xoulai.all_data_xoulai import AllDataXoulAI
from models.platform_xoulai.chat_common_xoulai import ChatConversationXoulAI

def discover_fetch_image_tasks_in_xoulai_chat_conversation(conversation: ChatConversationXoulAI, fetch_image_task_register: FetchImageTaskRegister) -> None:
    if conversation.icon_url:
        description = f"Single_Chat_{conversation.name}"[:100]
        conversation.set_fetch_image_task(fetch_image_task_register.registerNewTask(conversation.icon_url, description))
    for xoul in conversation.xouls:
        if xoul.icon_url:
            description = f"Character_{xoul.name}_{xoul.slug}"[:100]
            xoul.set_fetch_image_task(fetch_image_task_register.registerNewTask(xoul.icon_url, description))
    for persona in conversation.personas:
        if persona.icon_url:
            description = f"Persona_{persona.name}"[:100]
            persona.set_fetch_image_task(fetch_image_task_register.registerNewTask(persona.icon_url, description))
    if conversation.scenario:
        scenario = conversation.scenario
        if scenario.icon_url:
            description = f"Scenario_{scenario.name}"[:100]
            scenario.set_fetch_image_task(fetch_image_task_register.registerNewTask(scenario.icon_url, description))
    if conversation.lorebook:
        lorebook = conversation.lorebook
        if lorebook.icon_url:
            description = f"Lorebook_{lorebook.name}"[:100]
            lorebook.set_fetch_image_task(fetch_image_task_register.registerNewTask(lorebook.icon_url, description))

def discover_fetch_image_tasks(all_data: AllData, user_options: UserOptions) -> None:
    all_xoul_data: AllDataXoulAI = all_data.get_xoulai_platform_data()
    fetch_image_task_register: FetchImageTaskRegister = st.session_state.fetch_image_task_register

    if user_options.is_content_characters_selected():
        for item in all_xoul_data.characters:
            if item.icon_url:
                description = f"Character_{item.name}_{item.slug}"[:100]
                item.set_fetch_image_task(fetch_image_task_register.registerNewTask(item.icon_url, description))

    if user_options.is_content_personas_selected():
        for item in all_xoul_data.personas:
            if item.icon_url:
                description = f"Persona_{item.name}"[:100]
                item.set_fetch_image_task(fetch_image_task_register.registerNewTask(item.icon_url, description))

    if user_options.is_content_scenarios_selected():
        for item in all_xoul_data.scenarios:
            if item.icon_url:
                description = f"Scenario_{item.name}"[:100]
                item.set_fetch_image_task(fetch_image_task_register.registerNewTask(item.icon_url, description))

    if user_options.is_content_lorebooks_selected():
        for item in all_xoul_data.lorebooks:
            if item.icon_url:
                description = f"Lorebook_{item.name}"[:100]
                item.set_fetch_image_task(fetch_image_task_register.registerNewTask(item.icon_url, description))

# ********************
# TODO: Change the access methods during doc creation to use item.get_public_fields()!
# ********************

    if user_options.is_content_chats_single_selected():
        for item in all_xoul_data.chats_single:
            conversation = item.conversation
            if conversation:
                discover_fetch_image_tasks_in_xoulai_chat_conversation(conversation, fetch_image_task_register)

    if user_options.is_content_chats_multi_selected():
        for item in all_xoul_data.chats_multi:
            conversation = item.conversation
            if conversation:
                discover_fetch_image_tasks_in_xoulai_chat_conversation(conversation, fetch_image_task_register)