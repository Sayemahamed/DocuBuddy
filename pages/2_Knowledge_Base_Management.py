import streamlit as st
import os
from pathlib import Path
import shutil
from RAG import rag_instance

# Constants
KB_DIR = "knowledge_bases"
UPLOADS_DIR = "uploads"

def ensure_directories():
    """Ensure required directories exist."""
    for directory in [KB_DIR, UPLOADS_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)

def get_kb_size(kb_path: str) -> str:
    """Get the size of a knowledge base directory in human-readable format."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(kb_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    
    # Convert to human-readable format
    for unit in ['B', 'KB', 'MB', 'GB']:
        if total_size < 1024:
            return f"{total_size:.1f} {unit}"
        total_size /= 1024
    return f"{total_size:.1f} TB"

def kb_management_ui():
    """Display the knowledge base management interface."""
    st.title("📚 Knowledge Base Management")
    
    # Ensure directories exist
    ensure_directories()
    
    # Sidebar for KB creation and settings
    with st.sidebar:
        st.header("Create Knowledge Base")
        
        # KB name input
        kb_name = st.text_input(
            "Knowledge Base Name",
            help="Enter a name for the new knowledge base"
        ).strip()
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Upload Documents",
            type=["pdf", "txt", "docx"],
            accept_multiple_files=True,
            help="Select documents to add to the knowledge base"
        )
        
        # Create KB button
        if kb_name and uploaded_files:
            if st.button("Create Knowledge Base", type="primary"):
                try:
                    # Create KB directory
                    kb_path = os.path.join(KB_DIR, kb_name)
                    os.makedirs(kb_path, exist_ok=True)
                    
                    # Save uploaded files
                    file_paths = []
                    for file in uploaded_files:
                        file_path = os.path.join(UPLOADS_DIR, file.name)
                        with open(file_path, "wb") as f:
                            f.write(file.getvalue())
                        file_paths.append(file_path)
                    
                    # Process documents
                    with st.spinner("Processing documents..."):
                        rag_instance.process_documents(file_paths)
                        rag_instance.save_knowledge_base(kb_path)
                    
                    # Clean up uploaded files
                    for file_path in file_paths:
                        os.remove(file_path)
                    
                    st.success("Knowledge base created successfully!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error creating knowledge base: {str(e)}")
    
    # Main content area
    st.header("Available Knowledge Bases")
    
    # Get list of knowledge bases
    kbs = []
    if os.path.exists(KB_DIR):
        kbs = [d for d in os.listdir(KB_DIR) if os.path.isdir(os.path.join(KB_DIR, d))]
    
    if not kbs:
        st.info("No knowledge bases found. Create one using the sidebar.")
    else:
        # Display knowledge bases in a grid
        cols = st.columns(3)
        for idx, kb_name in enumerate(kbs):
            kb_path = os.path.join(KB_DIR, kb_name)
            with cols[idx % 3]:
                with st.expander(f"📚 {kb_name}", expanded=True):
                    st.metric("Size", get_kb_size(kb_path))
                    
                    # KB actions
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Load", key=f"load_{kb_name}"):
                            try:
                                with st.spinner("Loading knowledge base..."):
                                    rag_instance.load_knowledge_base(kb_path)
                                    st.session_state.current_kb = kb_name
                                    st.session_state.kb_loaded = True
                                st.success("Knowledge base loaded!")
                            except Exception as e:
                                st.error(f"Error loading knowledge base: {str(e)}")
                    
                    with col2:
                        if st.button("Delete", key=f"delete_{kb_name}"):
                            try:
                                shutil.rmtree(kb_path)
                                st.success("Knowledge base deleted!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error deleting knowledge base: {str(e)}")

if __name__ == "__main__":
    kb_management_ui()
