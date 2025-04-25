# Architecture and Design
Internal notes on structure. Designed as a mix of fast and proper form. Complete decoupling and OOP is not achieved, but relatively easy expansion is. 

## User Options
### Formats
* Word
* MD
* Text
* JSON (where compatible)

### Platforms
* Xoul
* Wyvern
* MyAI
* Sakura 

### Content Types (used for non-JSON output, JSON output is unique to the platform)
* Non-Chat
    * Personas
    * Xouls
    * Scenarios
* Chat
    * Single Chat
    * Group Chat

## Program Flow
* Unzip Files
* Extract JSON into original JSON holder
* If additional platforms are selected
    * Manipulate data for platform 
    * Add platform manipulated JSON to JSON holder
* Pass JSON holder to Doc Generation Orchestrator
* Doc Generation Manager
    * For each Format
        * Pass JSON holder to Format Specific Doc Generator
* Format Specific Doc Orchestrator
    * For Each Content Type Group
        * Pass JSON holder to Content Type Group generator
* Content Type Group Generator
    * Creates document
    * Uses imported platform specific doc generation functions for each platform specific entry in JSON Holder

## Datatype Architecture 
AllJSONData[ (One objected passed around)
    List PlatformJsonData[ (one object per platform, always has Platform, Lists are variable and match the platform specific document generation stuff)
        Enum Platform
        List Characters[
            Str Filename
            Data Fields
        ]
        List Scenarios[]
        List Chats[]
    ]
]
