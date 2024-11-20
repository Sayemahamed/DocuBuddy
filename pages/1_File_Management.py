import streamlit as st
import os
from pathlib import Path
import logging
import shutil
from datetime import datetime
from Agent import rag_instance

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="File Management - DocuBuddy",
    page_icon="📁",
    layout="wide"
)

def create_kb_directory(kb_name: str) -> Path:
    """Create a new knowledge base directory with a unique name."""
    kb_dir = Path("knowledge_bases") / kb_name
    kb_dir.mkdir(parents=True, exist_ok=True)
    return kb_dir

def save_uploaded_file(uploaded_file, upload_dir: Path) -> Path:
    """Save an uploaded file to the specified directory."""
    file_path = upload_dir / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    return file_path

def process_files(files, kb_name: str):
    """Process uploaded files and create a knowledge base."""
    try:
        # Create directories
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        kb_dir = create_kb_directory(kb_name)
        
        # Save and process files
        file_paths = []
        for file in files:
            file_path = save_uploaded_file(file, upload_dir)
            file_paths.append(file_path)
        
        # Create knowledge base
        rag_instance.process_documents(
            file_paths,
            kb_name=kb_name
        )
        
        # Save knowledge base
        rag_instance.save_knowledge_base(str(kb_dir))
        
        # Clean up uploaded files
        for file_path in file_paths:
            file_path.unlink()
        
        return True, "Knowledge base created successfully!"
    except Exception as e:
        logger.error(f"Error processing files: {e}", exc_info=True)
        return False, f"Error: {str(e)}"

def display_file_management():
    """Display the file management interface."""
    st.title("📁 File Management")
    
    with st.sidebar:
        st.header("Upload Settings")
        kb_name = st.text_input(
            "Knowledge Base Name",
            value=f"kb_{datetime.now().strftime('%y%m%d_%H%M%S')}",
            help="Enter a name for the new knowledge base"
        )

    # File upload section
    st.header("Upload Documents")
    
    uploaded_files = st.file_uploader(
        "Choose documents to process",
        type=["pdf", "txt", "docx"],
        accept_multiple_files=True,
        help="Select one or more documents to process"
    )
    
    if uploaded_files:
        st.text(f"Selected {len(uploaded_files)} files:")
        for file in uploaded_files:
            st.text(f"• {file.name} ({file.type})")
        
        if st.button("Process Documents", type="primary"):
            with st.spinner("Processing documents..."):
                success, message = process_files(uploaded_files, kb_name)
                if success:
                    st.success(message)
                    # Update session state
                    st.session_state.current_kb = kb_name
                    st.session_state.kb_loaded = True
                else:
                    st.error(message)
    
    # Display current status
    st.sidebar.divider()
    st.sidebar.header("Current Status")
    if st.session_state.get("kb_loaded"):
        st.sidebar.success(f"📚 Active KB: {st.session_state.get('current_kb')}")
    else:
        st.sidebar.info("No knowledge base loaded")

if __name__ == "__main__":
    display_file_management()
