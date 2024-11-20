import streamlit as st

st.set_page_config(page_title="About", page_icon="ℹ️", layout="wide")


def about_page():
    # Header
    st.title("About DocuBuddy")

    # Introduction
    st.info(
        "DocuBuddy is an intelligent document assistant that helps you interact with your documents "
        "using natural language. Built with modern AI technologies like LangChain and Ollama, "
        "DocuBuddy provides an intuitive interface for document analysis and question-answering "
        "with advanced error handling and robust document processing capabilities."
    )

    # Key Features
    st.header("Key Features")

    features = [
        {
            "icon": "🤖",
            "title": "Advanced AI Integration",
            "desc": "Multiple AI models (llama3.2, mistral, llama2, codellama) with configurable temperature settings",
        },
        {
            "icon": "📚",
            "title": "Robust Document Processing",
            "desc": "Enhanced error handling, multi-encoding support, and advanced document chunking",
        },
        {
            "icon": "🔍",
            "title": "Smart RAG System",
            "desc": "Advanced Retrieval Augmented Generation with source tracking and conversation memory",
        },
        {
            "icon": "📄",
            "title": "Comprehensive Format Support",
            "desc": "Support for PDF, TXT, DOCX, and various other document formats with robust error handling",
        },
        {
            "icon": "💾",
            "title": "Knowledge Base Management",
            "desc": "Create, manage, and switch between multiple knowledge bases with ease",
        },
        {
            "icon": "⚙️",
            "title": "Advanced Configuration",
            "desc": "Flexible model selection, temperature control, and memory management",
        },
    ]

    # Display features in columns
    cols = st.columns(2)
    for i, feature in enumerate(features):
        with cols[i % 2]:
            st.markdown(
                f"""
                ### {feature['icon']} {feature['title']}
                {feature['desc']}
                """
            )

    # Technical Details
    st.header("Technical Details")
    
    tech_cols = st.columns(2)
    
    with tech_cols[0]:
        st.subheader("🛠️ Core Technologies")
        st.markdown("""
        - **Framework**: Streamlit
        - **AI Backend**: LangChain + Ollama
        - **Vector Store**: FAISS
        - **Document Processing**: Unstructured, PyPDF2, python-docx
        """)
        
    with tech_cols[1]:
        st.subheader("🔧 Key Components")
        st.markdown("""
        - **RAG System**: Advanced document retrieval and generation
        - **Error Handling**: Comprehensive error management
        - **Memory Management**: Conversation context preservation
        - **Source Tracking**: Document source attribution
        """)

    # System Requirements
    st.header("System Requirements")
    st.markdown("""
    - Python 3.9+
    - Ollama (local installation)
    - 8GB+ RAM recommended
    - SSD storage recommended for better performance
    """)

    # Footer
    st.divider()
    st.markdown(
        "Made with ❤️ using Python, Streamlit, and the power of Local AI models"
    )


if __name__ == "__main__":
    about_page()
