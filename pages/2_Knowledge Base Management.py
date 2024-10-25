import streamlit as st
import os
from RAG import Augmented_model

# Folder containing knowledge bases
KNOWLEDGE_BASES_FOLDER = "knowledge_bases"

# Create the knowledge_bases folder if it doesn't exist
if not os.path.exists(KNOWLEDGE_BASES_FOLDER):
    os.makedirs(KNOWLEDGE_BASES_FOLDER)

# Title and description
st.title("Knowledge Base Manager")
st.write("View, load, and save knowledge bases within the `knowledge_bases` folder.")

# Input field for knowledge base name
kb_name = st.text_input("Enter Knowledge Base Name")

# Buttons for loading and saving the knowledge base
col1, col2 = st.columns([1, 1])
with col1:
    load_button = st.button("Load Knowledge Base")
with col2:
    save_button = st.button("Save Current Knowledge Base")

# Handle Load Knowledge Base action
if load_button:
    knowledge_bases = [
        d
        for d in os.listdir(KNOWLEDGE_BASES_FOLDER)
        if os.path.isdir(os.path.join(KNOWLEDGE_BASES_FOLDER, d))
    ]
    if kb_name in knowledge_bases:
        Augmented_model.load_knowledge_base(name=kb_name)
        st.success(f"Knowledge base '{kb_name}' loaded successfully.")
        # Add code here to load the knowledge base data as needed
    else:
        st.error(f"Knowledge base '{kb_name}' does not exist.")

# Handle Save Knowledge Base action
if save_button:
    kb_path = os.path.join(KNOWLEDGE_BASES_FOLDER, kb_name)
    if not os.path.exists(kb_path):
        os.makedirs(kb_path)
        Augmented_model.save_knowledge_base(name=kb_name)
        st.success(f"Knowledge base '{kb_name}' has been created and saved.")
        # Add code here to save the current knowledge base data as needed
    else:
        st.warning(f"Knowledge base '{kb_name}' already exists. Saving current data.")
        # Add code here to update the existing knowledge base data

# List all subdirectories in the knowledge_bases folder
st.write("### Available Knowledge Bases:")
knowledge_bases = [
    d
    for d in os.listdir(KNOWLEDGE_BASES_FOLDER)
    if os.path.isdir(os.path.join(KNOWLEDGE_BASES_FOLDER, d))
]

if knowledge_bases:
    for kb in knowledge_bases:
        st.write(f"- {kb}")
else:
    st.write("No knowledge bases found in the `knowledge_bases` folder.")
