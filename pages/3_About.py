import streamlit as st

st.set_page_config(
    page_title="About DocuBuddy",
    page_icon="ℹ️",
    layout="wide"
)

st.markdown("""
    <style>
        .about-section {
            background-color: #f8f9fa;
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .feature-card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            border: 1px solid #e9ecef;
            transition: transform 0.2s;
        }
        .feature-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .tech-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            margin: 0.25rem;
            border-radius: 15px;
            background-color: #e9ecef;
            color: #495057;
            font-size: 0.9rem;
        }
        .team-card {
            text-align: center;
            padding: 1.5rem;
            background-color: white;
            border-radius: 10px;
            margin: 1rem;
            border: 1px solid #e9ecef;
        }
        .avatar {
            width: 120px;
            height: 120px;
            border-radius: 60px;
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

def about_page():
    # Header Section
    st.title("About DocuBuddy")
    st.caption("Your AI-powered document assistant")
    
    # Project Overview
    st.markdown('<div class="about-section">', unsafe_allow_html=True)
    st.header("🎯 Project Overview")
    st.write("""
    DocuBuddy is an innovative AI-powered document assistant that helps you interact with your documents
    in a natural and intuitive way. Using advanced language models and document processing techniques,
    DocuBuddy makes it easy to extract insights, answer questions, and manage your document knowledge base.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Key Features
    st.header("✨ Key Features")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <h3>🤖 AI-Powered Analysis</h3>
                <p>Advanced language models understand your documents and provide intelligent responses to your queries.</p>
            </div>
            
            <div class="feature-card">
                <h3>📚 Knowledge Base Management</h3>
                <p>Organize and manage your documents efficiently with our powerful knowledge base system.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card">
                <h3>🔍 Smart Search</h3>
                <p>Find exactly what you're looking for with our context-aware document search capabilities.</p>
            </div>
            
            <div class="feature-card">
                <h3>📊 Document Analytics</h3>
                <p>Get insights into your document collection with comprehensive analytics and visualizations.</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Technology Stack
    st.header("🛠️ Technology Stack")
    st.markdown('<div class="about-section">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Frontend")
        st.markdown("""
            <span class="tech-badge">Streamlit</span>
            <span class="tech-badge">HTML/CSS</span>
            <span class="tech-badge">JavaScript</span>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Backend")
        st.markdown("""
            <span class="tech-badge">Python</span>
            <span class="tech-badge">FastAPI</span>
            <span class="tech-badge">LangChain</span>
        """, unsafe_allow_html=True)
    
    with col3:
        st.subheader("AI/ML")
        st.markdown("""
            <span class="tech-badge">Ollama</span>
            <span class="tech-badge">FAISS</span>
            <span class="tech-badge">PyMuPDF</span>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # System Architecture
    st.header("🏗️ System Architecture")
    st.image("https://raw.githubusercontent.com/Sayemahamed/DocuBuddy/refs/heads/main/System_Diagram.png", 
             caption="DocuBuddy System Architecture",
             use_column_width=True)
    
    # Getting Started
    st.header("🚀 Getting Started")
    with st.expander("Installation"):
        st.code("""
        # Clone the repository
        git clone https://github.com/Sayemahamed/DocuBuddy.git
        
        # Install dependencies
        pip install -r requirements.txt
        
        # Run the application
        streamlit run DocuBuddy.py
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>Made with ❤️ by DocuBuddy Team</p>
            <p>
                <a href='https://github.com/Sayemahamed/DocuBuddy' target='_blank'>GitHub</a> |
                <a href='https://github.com/Sayemahamed/DocuBuddy/issues' target='_blank'>Report Issues</a> |
                <a href='https://github.com/Sayemahamed/DocuBuddy/wiki' target='_blank'>Documentation</a>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    about_page()
