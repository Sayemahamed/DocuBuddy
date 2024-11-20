# DocuBuddy 🤖

An intelligent document assistant with advanced RAG (Retrieval Augmented Generation) capabilities, robust error handling, and comprehensive document processing features.

## 🌟 Key Features

- 🤖 **Advanced AI Integration**
  - Multiple AI model support (llama3.2, mistral, llama2, codellama)
  - Configurable temperature settings
  - Local inference using Ollama

- 📚 **Robust Document Processing**
  - Enhanced error handling
  - Multi-encoding support
  - Advanced document chunking
  - Comprehensive format support (PDF, TXT, DOCX, and more)

- 🔍 **Smart RAG System**
  - Advanced Retrieval Augmented Generation
  - Source document tracking
  - Conversation memory management
  - Semantic search capabilities

- 💾 **Knowledge Base Management**
  - Create and manage multiple knowledge bases
  - Easy switching between bases
  - Persistent storage
  - Efficient vector indexing

- ⚙️ **Advanced Configuration**
  - Flexible model selection
  - Temperature control
  - Memory management
  - Source attribution settings

## 🛠️ Technical Stack

### Core Technologies
- **Framework**: Streamlit
- **AI Backend**: LangChain + Ollama
- **Vector Store**: FAISS
- **Document Processing**: 
  - Unstructured
  - PyPDF2
  - python-docx
  - Various text encodings support

### AI Models
- **Default**: llama3.2
- **Alternatives**: 
  - mistral (fast, efficient)
  - llama2 (reliable)
  - codellama (code-specialized)
- **Embeddings**: nomic-embed-text via langchain-ollama

## 💻 System Requirements

- Python 3.9+
- 8GB+ RAM recommended
- SSD storage recommended
- Ollama (local installation)
- Windows/Linux/MacOS support

## 🚀 Getting Started

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Sayemahamed/DocuBuddy.git
   cd DocuBuddy
   ```

2. **Environment Setup**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On Unix/MacOS:
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Install Ollama**
   - Download from [Ollama's website](https://ollama.ai/)
   - Install and ensure the Ollama server is running

4. **Run DocuBuddy**
   ```bash
   streamlit run DocuBuddy.py
   ```

## 📁 Project Structure

```
DocuBuddy/
├── DocuBuddy.py        # Main application
├── Agent.py            # RAG implementation
├── pages/
│   ├── 1_File_Management.py           # Document upload and management
│   ├── 2_Knowledge_Base_Management.py # KB configuration
│   └── 3_About.py                     # About page
├── knowledge_bases/    # Storage for knowledge bases
└── requirements.txt    # Project dependencies
```

## 🔧 Configuration

- **Model Settings**: Select AI models and adjust temperature in the sidebar
- **Knowledge Base**: Create and manage knowledge bases in the File Management page
- **Document Processing**: Automatic format detection and processing
- **Error Handling**: Comprehensive error management and recovery

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the Mozilla Public License 2.0 (MPL 2.0).

## 👤 Author

**MD Iftaker Ahamed Sayem**
- GitHub: [@Sayemahamed](https://github.com/Sayemahamed)
- Email: sayemahamed183@gmail.com

---
Made with ❤️ using Python, Streamlit, and the power of Local AI models
