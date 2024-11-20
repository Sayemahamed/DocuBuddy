"""
DocuBuddy - An AI-powered document assistant.
This module provides the Streamlit web interface for the DocuBuddy application.
"""

import asyncio
import logging
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

import streamlit as st
from streamlit_chat import message
from RAG import RAG, RAGConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="DocuBuddy - Your AI Document Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e6f3ff;
        border-left: 5px solid #2196F3;
    }
    .assistant-message {
        background-color: #f8f9fa;
        border-left: 5px solid #4CAF50;
    }
    .sidebar .element-container {
        margin-bottom: 1rem;
    }
    .upload-section {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

class DocuBuddyApp:
    """Main application class for DocuBuddy."""
    
    def __init__(self):
        """Initialize the DocuBuddy application."""
        self.initialize_session_state()
        self.rag = RAG(RAGConfig())
        
    @staticmethod
    def initialize_session_state() -> None:
        """Initialize session state variables."""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "uploaded_files" not in st.session_state:
            st.session_state.uploaded_files = set()
        if "knowledge_bases" not in st.session_state:
            st.session_state.knowledge_bases = []
            
    def render_sidebar(self) -> None:
        """Render the sidebar with file upload and knowledge base management."""
        with st.sidebar:
            st.title("📚 Document Management")
            
            # File Upload Section
            st.header("Upload Documents")
            uploaded_files = st.file_uploader(
                "Choose your documents",
                type=["pdf", "txt", "csv"],
                accept_multiple_files=True,
                help="Supported formats: PDF, TXT, CSV"
            )
            
            if uploaded_files:
                for file in uploaded_files:
                    if file.name not in st.session_state.uploaded_files:
                        self.process_uploaded_file(file)
                        
            # Knowledge Base Management
            st.header("Knowledge Base")
            kb_name = st.text_input("Knowledge Base Name")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Save KB", help="Save current knowledge base"):
                    self.save_knowledge_base(kb_name)
                    
            with col2:
                if st.button("Load KB", help="Load saved knowledge base"):
                    self.load_knowledge_base(kb_name)
                    
            # Links and Info
            st.markdown("---")
            st.markdown("[View Source Code](https://github.com/Sayemahamed/DocuBuddy)")
            st.markdown("[System Architecture](https://raw.githubusercontent.com/Sayemahamed/DocuBuddy/refs/heads/main/System_Diagram.png)")
            
    async def process_uploaded_file(self, file: Any) -> None:
        """
        Process an uploaded file and add it to the knowledge base.
        
        Args:
            file: The uploaded file object from Streamlit
        """
        try:
            # Save uploaded file temporarily
            temp_path = Path("temp") / file.name
            temp_path.parent.mkdir(exist_ok=True)
            
            with open(temp_path, "wb") as f:
                f.write(file.getvalue())
                
            # Process the file
            await self.rag.add_document(temp_path)
            st.session_state.uploaded_files.add(file.name)
            
            # Cleanup
            temp_path.unlink()
            st.success(f"Successfully processed {file.name}")
            
        except Exception as e:
            logger.error(f"Error processing file {file.name}: {e}")
            st.error(f"Error processing {file.name}: {str(e)}")
            
    async def save_knowledge_base(self, name: str) -> None:
        """
        Save the current knowledge base.
        
        Args:
            name: Name of the knowledge base
        """
        if not name:
            st.warning("Please provide a name for the knowledge base")
            return
            
        try:
            kb_path = Path("knowledge_bases") / name
            await self.rag.save_knowledge_base(kb_path)
            st.success(f"Knowledge base '{name}' saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving knowledge base: {e}")
            st.error(f"Error saving knowledge base: {str(e)}")
            
    async def load_knowledge_base(self, name: str) -> None:
        """
        Load a saved knowledge base.
        
        Args:
            name: Name of the knowledge base to load
        """
        if not name:
            st.warning("Please provide the name of the knowledge base to load")
            return
            
        try:
            kb_path = Path("knowledge_bases") / name
            await self.rag.load_knowledge_base(kb_path)
            st.success(f"Knowledge base '{name}' loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading knowledge base: {e}")
            st.error(f"Error loading knowledge base: {str(e)}")
            
    def render_chat_interface(self) -> None:
        """Render the chat interface."""
        st.title("📄 DocuBuddy")
        st.caption("Your AI assistant for instant document insights!")
        
        # Display chat history
        for msg in st.session_state.messages:
            message_class = "user-message" if msg["role"] == "user" else "assistant-message"
            with st.container():
                st.markdown(f"""
                <div class="chat-message {message_class}">
                    <div>{msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
                
        # Chat input
        if prompt := st.chat_input("Ask me anything about your documents..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            try:
                answer = asyncio.run(self.rag.query(prompt))
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                logger.error(f"Error processing query: {e}")
                st.error("I encountered an error processing your query. Please try again.")
                
    def run(self) -> None:
        """Run the DocuBuddy application."""
        try:
            self.render_sidebar()
            self.render_chat_interface()
            
        except Exception as e:
            logger.error(f"Application error: {e}")
            st.error("An unexpected error occurred. Please refresh the page and try again.")

def main() -> None:
    """Main entry point for the DocuBuddy application."""
    app = DocuBuddyApp()
    app.run()

if __name__ == "__main__":
    main()
