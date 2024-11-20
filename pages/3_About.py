import streamlit as st

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide"
)

def about_page():
    # Header
    st.title("About DocuBuddy")
    
    # Introduction
    st.info(
        "DocuBuddy is an intelligent document assistant that helps you interact with your documents "
        "using natural language. Built with modern AI technologies like LangChain and Ollama, "
        "DocuBuddy provides an intuitive interface for document analysis and question-answering."
    )
    
    # Key Features
    st.header("Key Features")
    
    features = [
        {
            "icon": "🤖",
            "title": "AI-Powered Document Interaction",
            "desc": "Natural language interaction with documents using state-of-the-art language models"
        },
        {
            "icon": "📚",
            "title": "Knowledge Base Management",
            "desc": "Organize and manage multiple document collections efficiently"
        },
        {
            "icon": "🔍",
            "title": "Smart Search",
            "desc": "Find information quickly with semantic search capabilities"
        },
        {
            "icon": "📄",
            "title": "Multi-Format Support",
            "desc": "Support for PDF, TXT, and DOCX documents"
        },
        {
            "icon": "💻",
            "title": "User-Friendly Interface",
            "desc": "Clean, modern interface built with Streamlit for easy document management"
        }
    ]
    
    # Display features in columns
    cols = st.columns(2)
    for i, feature in enumerate(features):
        with cols[i % 2]:
            st.container()
            st.write(f"### {feature['icon']} {feature['title']}")
            st.write(feature['desc'])
            st.divider()
    
    # Technical Stack
    st.header("Technical Stack")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Frontend & Backend")
        st.write("- **Frontend**: Streamlit")
        st.write("- **Backend**: Python")
    
    with col2:
        st.subheader("AI & Machine Learning")
        st.write("- **Document Processing**: LangChain")
        st.write("- **Language Models**: Ollama")
        st.write("- **Vector Store**: FAISS")
        st.write("- **Storage**: Local File System")
    
    # Getting Started
    st.header("Getting Started")
    
    st.code("""
    # Install Dependencies
    pip install -r requirements.txt
    
    # Start Ollama Server (required)
    # Ensure Ollama is running locally
    
    # Run DocuBuddy
    streamlit run DocuBuddy.py
    """)
    
    # Contact Information
    st.divider()
    st.subheader("Contact")
    
    contact_col1, contact_col2 = st.columns(2)
    with contact_col1:
        st.write("**Author**: [MD Iftaker Ahamed Sayem](https://github.com/Sayemahamed)")
        st.write("**Email**: sayemahamed183@gmail.com")
    with contact_col2:
        st.write("**GitHub**: [DocuBuddy Repository](https://github.com/Sayemahamed/DocuBuddy)")
        st.write("**License**: Mozilla Public License 2.0 (MPL 2.0)")

if __name__ == "__main__":
    about_page()
