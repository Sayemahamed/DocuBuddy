import streamlit as st
import os
from pathlib import Path
import logging
import shutil
from datetime import datetime
from RAG import rag_instance

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
UPLOADS_DIR = "uploads"
KB_DIR = "knowledge_bases"
SUPPORTED_FORMATS = {
    "pdf": "Adobe PDF Documents",
    "txt": "Text Files",
    "docx": "Microsoft Word Documents"
}

def initialize_session_state():
    """Initialize session state variables."""
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = {}

def ensure_directories():
    """Ensure required directories exist."""
    for directory in [UPLOADS_DIR, KB_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)

def get_file_info(file) -> dict:
    """Get formatted file information."""
    size_kb = file.size / 1024
    size_text = f"{size_kb:.1f} KB" if size_kb < 1024 else f"{(size_kb/1024):.1f} MB"
    
    return {
        "name": file.name,
        "size": size_text,
        "type": file.type if hasattr(file, 'type') else Path(file.name).suffix[1:].upper(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "kb_name": None,
        "processed": False
    }

def save_uploaded_file(uploaded_file) -> str:
    """Save uploaded file and return the path."""
    file_path = os.path.join(UPLOADS_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    return file_path

def process_file(file, kb_name=None):
    """Process a single file and add it to the knowledge base."""
    try:
        # Generate KB name if not provided
        if not kb_name:
            kb_name = f"kb_{Path(file.name).stem}"
        
        kb_path = os.path.join(KB_DIR, kb_name)
        file_path = save_uploaded_file(file)
        
        try:
            # Process document
            rag_instance.process_documents([file_path])
            
            # Save knowledge base
            os.makedirs(kb_path, exist_ok=True)
            rag_instance.save_knowledge_base(kb_path)
            
            # Update file info
            st.session_state.uploaded_files[file.name]["kb_name"] = kb_name
            st.session_state.uploaded_files[file.name]["processed"] = True
            
            return True, kb_name
            
        finally:
            # Clean up temporary file
            if os.path.exists(file_path):
                os.remove(file_path)
                
    except Exception as e:
        logger.error(f"Error processing file {file.name}: {e}")
        return False, str(e)

def file_management_ui():
    """Display the file management interface."""
    st.title(" File Management")
    
    # Initialize session state and ensure directories exist
    initialize_session_state()
    ensure_directories()
    
    # Sidebar with upload functionality
    with st.sidebar:
        st.header("Upload Files")
        
        # Show supported formats
        st.info("Supported Formats")
        for ext, desc in SUPPORTED_FORMATS.items():
            st.write(f"• .{ext} - {desc}")
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Drop your files here",
            type=list(SUPPORTED_FORMATS.keys()),
            accept_multiple_files=True,
            help="Select one or more files to upload"
        )
        
        # Process new uploads
        if uploaded_files:
            for file in uploaded_files:
                if file.name not in st.session_state.uploaded_files:
                    st.session_state.uploaded_files[file.name] = get_file_info(file)
    
    # Main content area
    if st.session_state.uploaded_files:
        # File statistics
        stats_col1, stats_col2, stats_col3 = st.columns(3)
        
        total_files = len(st.session_state.uploaded_files)
        processed_files = sum(1 for info in st.session_state.uploaded_files.values() if info["processed"])
        
        with stats_col1:
            st.metric("Total Files", total_files)
        with stats_col2:
            st.metric("Processed", processed_files)
        with stats_col3:
            st.metric("Pending", total_files - processed_files)
        
        # Batch actions
        st.divider()
        action_col1, action_col2, action_col3 = st.columns(3)
        
        with action_col1:
            if st.button("Process All", type="primary", 
                        disabled=len(st.session_state.uploaded_files) == 0):
                try:
                    with st.spinner("Processing files..."):
                        for file in uploaded_files:
                            if not st.session_state.uploaded_files[file.name]["processed"]:
                                success, result = process_file(file)
                                if success:
                                    st.success(f"Processed {file.name} into knowledge base: {result}")
                                else:
                                    st.error(f"Failed to process {file.name}: {result}")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error processing files: {str(e)}")
        
        with action_col2:
            if st.button("Clear Processed", type="secondary",
                       disabled=not any(info["processed"] for info in st.session_state.uploaded_files.values())):
                # Remove processed files from session state
                st.session_state.uploaded_files = {
                    name: info for name, info in st.session_state.uploaded_files.items() 
                    if not info["processed"]
                }
                st.rerun()
        
        with action_col3:
            if st.button("Clear All", type="secondary",
                       disabled=len(st.session_state.uploaded_files) == 0):
                st.session_state.uploaded_files.clear()
                st.rerun()
        
        # File list
        st.divider()
        st.subheader("Uploaded Files")
        
        for filename, info in st.session_state.uploaded_files.items():
            with st.expander(f" {filename}", expanded=True):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**Type:** {info['type']}")
                    st.write(f"**Added:** {info['timestamp']}")
                    if info["processed"]:
                        st.write(f"**KB:** {info['kb_name']}")
                
                with col2:
                    st.metric("Size", info['size'])
                
                with col3:
                    if info["processed"]:
                        st.success("Processed")
                    else:
                        if st.button("Process", key=f"process_{filename}"):
                            try:
                                with st.spinner("Processing file..."):
                                    # Get the corresponding uploaded file
                                    file = next(f for f in uploaded_files if f.name == filename)
                                    success, result = process_file(file)
                                    
                                    if success:
                                        st.success(f"Processed into knowledge base: {result}")
                                    else:
                                        st.error(f"Processing failed: {result}")
                                    
                                    st.rerun()
                            except Exception as e:
                                st.error(f"Error processing file: {str(e)}")
                    
                    if st.button("Remove", key=f"remove_{filename}"):
                        del st.session_state.uploaded_files[filename]
                        st.rerun()
    else:
        st.info("No files uploaded. Use the sidebar to upload files.")

if __name__ == "__main__":
    file_management_ui()
