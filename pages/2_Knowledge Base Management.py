"""This page contains the knowledge base management functionality."""

import os

import streamlit as st

from RAG import Augmented_model

# Folder containing knowledge bases
KNOWLEDGE_BASES_FOLDER = "knowledge_bases"

# Create the knowledge_bases folder if it doesn't exist
if not os.path.exists(KNOWLEDGE_BASES_FOLDER):
    os.makedirs(name=KNOWLEDGE_BASES_FOLDER)

# Title and description
st.title(body="Knowledge Base Manager")
st.write("View, load, and save knowledge bases within the `knowledge_bases` folder.")

# Input field for knowledge base name
kb_name: str = st.text_input(label="Enter Knowledge Base Name")

# Buttons for loading and saving the knowledge base
col1, col2 = st.columns([1, 1])
with col1:
    load_button: bool = st.button(label="Load Knowledge Base")
with col2:
    save_button: bool = st.button(label="Save Current Knowledge Base")

# Handle Load Knowledge Base action
if load_button:
    knowledge_bases = [
        d
        for d in os.listdir(path=KNOWLEDGE_BASES_FOLDER)
        if os.path.isdir(s=os.path.join(KNOWLEDGE_BASES_FOLDER, d))
    ]
    if kb_name in knowledge_bases:
        Augmented_model.load_knowledge_base(name=kb_name)
        st.success(body=f"Knowledge base '{kb_name}' loaded successfully.")
    else:
        st.error(body=f"Knowledge base '{kb_name}' does not exist.")

# Handle Save Knowledge Base action
if save_button:
    kb_path: str = os.path.join(KNOWLEDGE_BASES_FOLDER, kb_name)
    if not os.path.exists(kb_path):
        os.makedirs(name=kb_path)
        Augmented_model.save_knowledge_base(name=kb_name)
        st.success(body=f"Knowledge base '{kb_name}' has been created and saved.")
    else:
        st.warning(
            body=f"Knowledge base '{kb_name}' already exists. Saving current data."
        )

# List all subdirectories in the knowledge_bases folder
st.write("### Available Knowledge Bases:")
knowledge_bases: list[str] = [
    d
    for d in os.listdir(path=KNOWLEDGE_BASES_FOLDER)
    if os.path.isdir(os.path.join(KNOWLEDGE_BASES_FOLDER, d))
]

if knowledge_bases:
    for kb in knowledge_bases:
        st.write(f"- {kb}")
else:
    st.write("No knowledge bases found in the `knowledge_bases` folder.")
