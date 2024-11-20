import streamlit as st
import os
from pathlib import Path
from typing import List, Dict
import logging
from RAG import rag_instance

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
KB_DIR = "knowledge_bases"
DEFAULT_KB = "default_kb"

# Available models configuration
MODELS = {
    "llama3.2": {
        "name": "llama3.2",
        "description": "Latest Llama model with improved performance",
        "type": "chat"
    },
    "mistral": {
        "name": "mistral",
        "description": "Fast and efficient general-purpose model",
        "type": "chat"
    },
    "llama2": {
        "name": "llama2",
        "description": "Reliable general-purpose model",
        "type": "chat"
    },
    "codellama": {
        "name": "codellama",
        "description": "Specialized for code understanding and generation",
        "type": "code"
    }
}

class DocuBuddy:
    def __init__(self):
        self._initialize_session_state()
        self._setup_page()
        
    def _initialize_session_state(self):
        """Initialize session state variables."""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "current_kb" not in st.session_state:
            st.session_state.current_kb = DEFAULT_KB
        if "kb_loaded" not in st.session_state:
            st.session_state.kb_loaded = False
        if "current_model" not in st.session_state:
            st.session_state.current_model = "llama3.2"

    def _setup_page(self):
        """Configure the page layout and sidebar."""
        st.set_page_config(
            page_title="DocuBuddy",
            page_icon="📚",
            layout="wide"
        )
        
        # Main title with styling
        st.title("📚 DocuBuddy")
        st.markdown("Your AI-powered document assistant")

    def _setup_sidebar(self):
        """Configure the sidebar with model settings."""
        with st.sidebar:
            st.header("⚙️ Configuration")
            
            # Model selection with descriptions
            model = st.selectbox(
                "Select AI Model",
                options=list(MODELS.keys()),
                index=list(MODELS.keys()).index(st.session_state.current_model),
                format_func=lambda x: f"{x} - {MODELS[x]['description']}",
                help="Choose the AI model for document analysis"
            )
            
            # Update model if changed
            if model != st.session_state.current_model:
                st.session_state.current_model = model
                rag_instance.update_model(model)
                st.success(f"Switched to {model} model")
            
            # Model info
            with st.expander("Model Information", expanded=False):
                st.info(
                    f"**Current Model**: {model}\n\n"
                    f"**Type**: {MODELS[model]['type'].title()}\n\n"
                    f"**Description**: {MODELS[model]['description']}"
                )
            
            # Temperature setting
            temperature = st.slider(
                "Response Creativity",
                min_value=0.0,
                max_value=1.0,
                value=0.0,
                step=0.1,
                help="Higher values make responses more creative but less focused"
            )
            
            if temperature != getattr(rag_instance, 'temperature', 0.0):
                rag_instance.update_temperature(temperature)
            
            # Knowledge Base selection
            st.divider()
            st.subheader("Knowledge Base")
            kb_path = os.path.join(KB_DIR, st.session_state.current_kb)
            if os.path.exists(kb_path):
                st.success("✅ Knowledge Base: Ready")
                if st.button("Clear Memory"):
                    rag_instance.clear_memory()
                    st.session_state.messages = []
                    st.success("Memory cleared!")
            else:
                st.warning("⚠️ No Knowledge Base loaded")

    def display_chat_interface(self):
        """Display the chat interface and handle interactions."""
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "sources" in message:
                    with st.expander("View Sources"):
                        for source in message["sources"]:
                            st.info(
                                f"📄 {source['source']} "
                                f"(Page {source['page']})\n\n"
                                f"{source['content']}"
                            )

        # Chat input
        if prompt := st.chat_input(f"Ask me about your documents using {st.session_state.current_model}..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate response
            with st.chat_message("assistant"):
                try:
                    with st.spinner(f"Thinking using {st.session_state.current_model}..."):
                        response = rag_instance.query(prompt)
                        
                        # Display response
                        st.markdown(response["answer"])
                        
                        # Add to message history with sources
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response["answer"],
                            "sources": response["sources"]
                        })
                        
                        # Display sources in expander
                        if response["sources"]:
                            with st.expander("View Sources"):
                                for source in response["sources"]:
                                    st.info(
                                        f"📄 {source['source']} "
                                        f"(Page {source['page']})\n\n"
                                        f"{source['content']}"
                                    )
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    logger.error(f"Query error: {str(e)}")

    def run(self):
        """Run the DocuBuddy application."""
        try:
            # Setup sidebar
            self._setup_sidebar()
            
            # Load knowledge base if needed
            if not st.session_state.kb_loaded:
                kb_path = os.path.join(KB_DIR, st.session_state.current_kb)
                if os.path.exists(kb_path):
                    rag_instance.load_knowledge_base(kb_path)
                    st.session_state.kb_loaded = True
            
            # Display chat interface
            self.display_chat_interface()
            
        except Exception as e:
            st.error(f"Application error: {str(e)}")
            logger.error(f"Application error: {str(e)}")

if __name__ == "__main__":
    app = DocuBuddy()
    app.run()
