import streamlit as st
import os
from pathlib import Path
from typing import List, Dict
import logging
from Agent import rag_instance

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
        "type": "chat",
    },
    "mistral": {
        "name": "mistral",
        "description": "Fast and efficient general-purpose model",
        "type": "chat",
    },
    "llama2": {
        "name": "llama2",
        "description": "Reliable general-purpose model",
        "type": "chat",
    },
    "codellama": {
        "name": "codellama",
        "description": "Specialized for code understanding and generation",
        "type": "code",
    },
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
        if "current_temperature" not in st.session_state:
            st.session_state.current_temperature = 0.7

    def _setup_page(self):
        """Configure the page layout and sidebar."""
        st.set_page_config(page_title="DocuBuddy", page_icon="📚", layout="wide")

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
                help="Choose the AI model for document analysis",
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
                value=st.session_state.current_temperature,
                step=0.1,
                help="Higher values make responses more creative but less focused",
            )

            if temperature != st.session_state.current_temperature:
                st.session_state.current_temperature = temperature
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
        """
        Main chat interface for document interaction.
        Allows users to:
        - Query documents and get intelligent answers
        - Select AI models
        - Adjust response temperature
        - View source documents
        - Maintain conversation context
        """
        st.title("DocuBuddy Chat")

        # Sidebar for model configuration
        with st.sidebar:
            st.header("Model Settings")
            model = st.selectbox(
                "Select AI Model",
                ["llama3.2", "mistral", "llama2", "codellama"],
                index=0,
            )
            temperature = st.slider(
                "Response Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Higher values make responses more creative",
            )

            # Update model if changed
            if (
                "current_model" not in st.session_state
                or st.session_state.current_model != model
            ):
                st.session_state.current_model = model
                rag_instance.update_model(model)

            # Update temperature if changed
            if (
                "current_temperature" not in st.session_state
                or st.session_state.current_temperature != temperature
            ):
                st.session_state.current_temperature = temperature
                rag_instance.update_temperature(temperature)

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "sources" in message:
                    st.info("Sources: " + message["sources"])

        # Chat input
        if prompt := st.chat_input("Ask about your documents..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            try:
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = rag_instance.query(prompt)
                        sources = response.get("sources", [])

                        # Format source documents
                        if sources:
                            source_text = ", ".join(
                                [
                                    f"{s.get('metadata', {}).get('source', 'Unknown')}"
                                    for s in sources
                                ]
                            )
                        else:
                            source_text = "No specific sources"

                        st.markdown(response["answer"])
                        st.info(f"Sources: {source_text}")

                        # Save message with sources
                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": response["answer"],
                                "sources": source_text,
                            }
                        )
            except Exception as e:
                st.error(f"Error: {str(e)}")
                logger.error(f"Error in chat interface: {e}", exc_info=True)

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
