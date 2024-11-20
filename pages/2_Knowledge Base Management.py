"""This page contains the knowledge base management functionality."""

import os
import streamlit as st
from RAG import Augmented_model
from pathlib import Path
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Folder containing knowledge bases
KNOWLEDGE_BASES_FOLDER = "knowledge_bases"

# Create the knowledge_bases folder if it doesn't exist
if not os.path.exists(KNOWLEDGE_BASES_FOLDER):
    os.makedirs(name=KNOWLEDGE_BASES_FOLDER)

st.set_page_config(
    page_title="Knowledge Base Management - DocuBuddy",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
    <style>
        .kb-section {
            background-color: #f8f9fa;
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .kb-card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            border: 1px solid #e9ecef;
            transition: transform 0.2s;
        }
        .kb-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .metric-card {
            background-color: white;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            border: 1px solid #e9ecef;
        }
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            color: #4CAF50;
        }
        .metric-label {
            color: #6c757d;
            font-size: 0.9rem;
        }
    </style>
""", unsafe_allow_html=True)

def knowledge_base_ui():
    st.title("🧠 Knowledge Base Management")
    st.caption("Manage and organize your document knowledge bases")
    
    # Create tabs for different KB operations
    tab1, tab2, tab3 = st.tabs(["Active KB", "Saved KBs", "Settings"])
    
    with tab1:
        st.markdown('<div class="kb-section">', unsafe_allow_html=True)
        st.header("Active Knowledge Base")
        
        # Active KB Stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">128</div>
                    <div class="metric-label">Documents</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">1.2K</div>
                    <div class="metric-label">Chunks</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">24MB</div>
                    <div class="metric-label">Size</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">99%</div>
                    <div class="metric-label">Health</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Active Documents List
        st.subheader("📄 Active Documents")
        with st.container():
            for i in range(3):  # Replace with actual document list
                st.markdown(f"""
                    <div class="kb-card">
                        <h3>Document {i+1}</h3>
                        <p>Added: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
                        <p>Size: 1.2MB | Chunks: 45 | Status: Active</p>
                    </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.header("💾 Saved Knowledge Bases")
        
        # KB Search and Filter
        col1, col2 = st.columns([3, 1])
        with col1:
            st.text_input("🔍 Search Knowledge Bases", placeholder="Search by name or description...")
        with col2:
            st.selectbox("Filter By", ["All", "Recent", "Largest", "Smallest"])
        
        # Saved KBs Grid
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div class="kb-card">
                    <h3>Project Documentation KB</h3>
                    <p>Created: 2024-02-10</p>
                    <p>Documents: 45 | Size: 12MB</p>
                    <p>Description: Contains project documentation and technical specs.</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="kb-card">
                    <h3>Research Papers KB</h3>
                    <p>Created: 2024-02-09</p>
                    <p>Documents: 23 | Size: 8MB</p>
                    <p>Description: Collection of research papers and academic documents.</p>
                </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.header("⚙️ Knowledge Base Settings")
        
        with st.expander("Chunking Settings"):
            st.slider("Chunk Size", 100, 2000, 500)
            st.slider("Chunk Overlap", 0, 200, 50)
            st.checkbox("Auto-detect optimal chunk size")
        
        with st.expander("Vector Store Settings"):
            st.selectbox("Vector Store Type", ["FAISS", "Chroma", "Pinecone"])
            st.number_input("Number of Vectors", min_value=1, value=3)
            st.checkbox("Enable caching")
        
        with st.expander("Maintenance"):
            st.button("Optimize Knowledge Base")
            st.button("Rebuild Index")
            st.button("Clean Temporary Files")

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

if __name__ == "__main__":
    knowledge_base_ui()
