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

class DocuBuddyUI:
    def __init__(self):
        self.rag = None
        self.initialize_page()
        
    def initialize_page(self):
        # Set page configuration
        st.set_page_config(
            page_title="DocuBuddy AI Assistant",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Apply custom CSS
        st.markdown("""
            <style>
                .main {
                    padding: 2rem;
                    max-width: 1200px;
                }
                .stButton>button {
                    width: 100%;
                    border-radius: 5px;
                    height: 3em;
                    background-color: #4CAF50;
                    color: white;
                }
                .chat-message {
                    padding: 1.5rem;
                    border-radius: 10px;
                    margin-bottom: 1rem;
                    display: flex;
                    align-items: flex-start;
                }
                .chat-message.user {
                    background-color: #E8F5E9;
                }
                .chat-message.assistant {
                    background-color: #F5F5F5;
                }
                .chat-message .avatar {
                    width: 40px;
                    height: 40px;
                    margin-right: 1rem;
                    border-radius: 50%;
                }
                .chat-message .message {
                    flex-grow: 1;
                }
                .sidebar .sidebar-content {
                    padding: 1rem;
                }
                div[data-testid="stSidebarNav"] {
                    background-color: #f8f9fa;
                    padding-top: 2rem;
                }
                .stAlert {
                    border-radius: 10px;
                }
            </style>
        """, unsafe_allow_html=True)

    def render_chat_message(self, content, is_user=False):
        avatar = "👤" if is_user else "🤖"
        message_type = "user" if is_user else "assistant"
        
        st.markdown(f"""
            <div class="chat-message {message_type}">
                <div class="avatar">{avatar}</div>
                <div class="message">{content}</div>
            </div>
        """, unsafe_allow_html=True)

    def main(self):
        st.title("💬 DocuBuddy AI Assistant")
        
        with st.sidebar:
            st.header("Configuration")
            model = st.selectbox(
                "Select Model",
                ["llama2", "mistral", "codellama"],
                help="Choose the AI model to use"
            )
            
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Controls randomness in responses"
            )
            
            st.divider()
            
            st.header("Active Documents")
            if 'active_docs' in st.session_state and st.session_state.active_docs:
                for doc in st.session_state.active_docs:
                    st.info(f"📄 {doc}")
            else:
                st.warning("No documents loaded")
            
            st.divider()
            
            with st.expander("⚙️ Advanced Settings"):
                chunk_size = st.number_input(
                    "Chunk Size",
                    min_value=100,
                    max_value=2000,
                    value=500,
                    step=100
                )
                chunk_overlap = st.number_input(
                    "Chunk Overlap",
                    min_value=0,
                    max_value=500,
                    value=50,
                    step=10
                )

        # Main chat interface
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages
        for message in st.session_state.messages:
            self.render_chat_message(
                message["content"],
                is_user=message["role"] == "user"
            )

        # Chat input
        with st.container():
            if prompt := st.chat_input("Ask me anything about your documents..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                self.render_chat_message(prompt, is_user=True)
                
                with st.spinner("Thinking..."):
                    if self.rag:
                        response = self.rag.get_response(prompt)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        self.render_chat_message(response, is_user=False)
                    else:
                        st.error("Please load some documents first!")

        # Footer
        st.markdown("---")
        st.markdown(
            """
            <div style='text-align: center'>
                <p>Made with ❤️ by DocuBuddy Team</p>
            </div>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    app = DocuBuddyUI()
    app.main()
