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
    page_title="Knowledge Base Management - DocuBuddy",
    page_icon="📚",
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

def get_kb_size(kb_path: Path) -> str:
    """Calculate the total size of a knowledge base directory."""
    total_size = sum(f.stat().st_size for f in kb_path.rglob('*') if f.is_file())
    if total_size < 1024:
        return f"{total_size} B"
    elif total_size < 1024 * 1024:
        return f"{total_size/1024:.1f} KB"
    else:
        return f"{total_size/(1024*1024):.1f} MB"

def process_files(files, kb_name: str):
    """Process uploaded files and create/update a knowledge base."""
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
        
        # Create/update knowledge base
        rag_instance.process_documents(
            file_paths,
            kb_name=kb_name
        )
        
        # Save knowledge base
        rag_instance.save_knowledge_base(str(kb_dir))
        
        # Clean up uploaded files
        for file_path in file_paths:
            file_path.unlink()
        
        return True, "Knowledge base updated successfully!"
    except Exception as e:
        logger.error(f"Error processing files: {e}", exc_info=True)
        return False, f"Error: {str(e)}"

def load_knowledge_base(kb_name: str):
    """Load a knowledge base."""
    try:
        kb_dir = Path("knowledge_bases") / kb_name
        if kb_dir.exists():
            rag_instance.load_knowledge_base(str(kb_dir))
            st.session_state.current_kb = kb_name
            st.session_state.kb_loaded = True
            return True, f"Loaded knowledge base: {kb_name}"
        else:
            return False, f"Knowledge base not found: {kb_name}"
    except Exception as e:
        logger.error(f"Error loading knowledge base: {e}", exc_info=True)
        return False, f"Error: {str(e)}"

def delete_knowledge_base(kb_name: str):
    """Delete a knowledge base."""
    try:
        kb_dir = Path("knowledge_bases") / kb_name
        if kb_dir.exists():
            shutil.rmtree(kb_dir)
            
            # Update session state if the deleted KB was active
            if st.session_state.get("current_kb") == kb_name:
                st.session_state.current_kb = None
                st.session_state.kb_loaded = False
            
            return True, f"Deleted knowledge base: {kb_name}"
        else:
            return False, f"Knowledge base not found: {kb_name}"
    except Exception as e:
        logger.error(f"Error deleting knowledge base: {e}", exc_info=True)
        return False, f"Error: {str(e)}"

def display_kb_management():
    """Display the knowledge base management interface."""
    st.title("📚 Knowledge Base Management")
    
    # Get list of knowledge bases
    kb_dir = Path("knowledge_bases")
    kb_dir.mkdir(exist_ok=True)
    knowledge_bases = [d.name for d in kb_dir.iterdir() if d.is_dir()]
    
    # Sidebar for KB selection and actions
    with st.sidebar:
        st.header("Knowledge Bases")
        
        if knowledge_bases:
            selected_kb = st.selectbox(
                "Select Knowledge Base",
                options=knowledge_bases,
                index=knowledge_bases.index(st.session_state.get("current_kb")) 
                if st.session_state.get("current_kb") in knowledge_bases 
                else 0
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Load KB", type="primary"):
                    success, message = load_knowledge_base(selected_kb)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
            
            with col2:
                if st.button("Delete KB", type="secondary"):
                    if st.session_state.get("current_kb") == selected_kb:
                        st.error("Cannot delete active knowledge base")
                    else:
                        success, message = delete_knowledge_base(selected_kb)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
        else:
            st.info("No knowledge bases found")
        
        # Display current status
        st.divider()
        st.header("Current Status")
        if st.session_state.get("kb_loaded"):
            st.success(f"📚 Active KB: {st.session_state.get('current_kb')}")
        else:
            st.info("No knowledge base loaded")
    
    # Main content area
    st.header("Add Documents")
    
    # File upload
    uploaded_files = st.file_uploader(
        "Upload documents to add to the knowledge base",
        type=["pdf", "txt", "docx"],
        accept_multiple_files=True,
        help="Select one or more documents to process"
    )
    
    if uploaded_files:
        st.text(f"Selected {len(uploaded_files)} files:")
        for file in uploaded_files:
            st.text(f"• {file.name} ({file.type})")
        
        # Only allow processing if a KB is selected
        if st.session_state.get("current_kb"):
            if st.button("Process Documents", type="primary"):
                with st.spinner("Processing documents..."):
                    success, message = process_files(
                        uploaded_files,
                        st.session_state.current_kb
                    )
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
        else:
            st.warning("Please load a knowledge base first")
    
    # Display KB information
    if knowledge_bases:
        st.divider()
        st.header("Knowledge Base Information")
        
        for kb_name in knowledge_bases:
            with st.expander(f"📚 {kb_name}", expanded=True):
                kb_path = kb_dir / kb_name
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Size", get_kb_size(kb_path))
                with col2:
                    st.metric(
                        "Status",
                        "Active" if st.session_state.get("current_kb") == kb_name else "Inactive"
                    )
                with col3:
                    st.metric(
                        "Last Modified",
                        datetime.fromtimestamp(kb_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                    )

if __name__ == "__main__":
    display_kb_management()
