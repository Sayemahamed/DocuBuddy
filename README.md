# DocuBuddy 🤖

An intelligent document interaction tool with advanced RAG (Retrieval Augmented Generation) capabilities.

## 🌟 Features

- 📄 Multi-format Document Support (PDF, TXT, DOCX)
- 🔍 Semantic Search with Advanced RAG
- 💬 Conversational Memory
- 📚 Dynamic Knowledge Base Management
- 📝 Source Document Tracking
- 🎯 Precise Document Retrieval

## 🛠️ Technical Stack

### AI Models
- Default: llama3.2
- Alternatives: mistral, llama2, codellama
- Embeddings: nomic-embed-text via langchain-ollama

### Core Dependencies
- Python 3.9+
- Streamlit
- LangChain (latest version)
- langchain-community
- langchain-ollama
- FAISS
- Ollama (local server)

## 🚀 Getting Started

1. **Environment Setup**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Install Ollama**
   - Download and install from [Ollama's website](https://ollama.ai/)
   - Ensure the Ollama server is running locally

3. **Run DocuBuddy**
   ```bash
   streamlit run DocuBuddy.py
   ```

## 📁 Project Structure

- `DocuBuddy.py`: Main Streamlit application
- `Agent.py`: Core RAG implementation
- `pages/`:
  - `1_File_Management.py`: Document upload and processing
  - `2_Knowledge_Base_Management.py`: KB creation and management
- `uploads/`: Temporary file storage
- `knowledge_bases/`: Persistent KB storage

## 🔧 Configuration

The system is configurable through the UI:
- AI Model Selection
- Temperature Settings
- Knowledge Base Management
- Document Processing Options

## 🔒 Security Features

- Local-only Processing
- Safe File Handling
- Input Validation
- Secure Document Management

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 Notes

- Requires a running Ollama server
- Supports multiple document formats
- Uses local processing for security
- Maintains conversation context
- Provides source attribution

## 📄 License

MIT License - See LICENSE file for details
