# DocuBuddy 

An intelligent document interaction and analysis tool powered by advanced RAG (Retrieval Augmented Generation) capabilities.

## Features

- **Multi-Document Processing**: Support for PDF, TXT, and DOCX files
- **Intelligent Q&A**: Advanced RAG-based document querying
- **Multiple AI Models**: Support for various Ollama models
  - llama3.2 (Default, recommended)
  - mistral
  - llama2
  - codellama
- **Dynamic Knowledge Base**: Efficient document storage and retrieval
- **User-Friendly Interface**: Built with Streamlit for ease of use
- **Source Attribution**: Track which documents provided answers
- **Conversation Memory**: Maintain context in discussions
- **Temperature Control**: Adjust AI response creativity

## Quick Start

1. **Prerequisites**
   ```bash
   # Install Ollama (required)
   # Windows: Follow instructions at https://ollama.ai/download
   
   # Install Python 3.9+
   python --version
   
   # Create virtual environment
   python -m venv .venv
   .venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   streamlit run DocuBuddy.py
   ```

3. **Access the Interface**
   - Open your browser to `http://localhost:8501`
   - Use the sidebar to configure AI model settings
   - Upload documents in the File Management page
   - Start asking questions!

## Project Structure

```
DocuBuddy/
├── DocuBuddy.py          # Main application
├── Agent.py              # AI agent implementation
├── pages/
│   ├── 1_File_Management.py        # File upload and processing
│   └── 2_Knowledge_Base_Management.py  # KB management
├── knowledge_bases/      # Stored knowledge bases
├── uploads/             # Temporary file storage
└── requirements.txt     # Python dependencies
```

## Configuration

### Environment Setup
- Knowledge bases stored in `knowledge_bases/`
- Temporary uploads in `uploads/`
- Default model: `llama3.2`
- Default embedding: `nomic-embed-text`

### Supported File Types
- PDF Documents (*.pdf)
- Text Files (*.txt)
- Word Documents (*.docx)

## Understanding DocuBuddy's Data Flow

### Chat UI

The main application, `DocuBuddy.py`, serves as the interface for chatting with the AI. Users can:
- Query documents and retrieve intelligent answers
- Select AI models (llama3.2, mistral, llama2, codellama)
- Adjust response temperature
- View source documents for answers
- Maintain conversation context

### File Upload & Processing

`1_File_Management.py` manages the file upload process:
- Handles PDF, TXT, and DOCX formats
- Tracks uploaded files until processing is complete
- Stores files temporarily in `uploads/` directory
- Generates knowledge bases (KB) stored in `knowledge_bases/`
- Provides progress tracking and error handling

### Knowledge Base Management

`2_Knowledge_Base_Management.py` handles KB tracking and management:
- Allows loading specific KBs into current conversation
- Enables deletion of unwanted KBs
- Manages KB metadata and status
- Provides KB size and content information

### AI Agent Implementation

The heart of the intelligent Q&A system resides in `Agent.py`:
- Implements Retrieval-Augmented Generation (RAG) capabilities
- Uses FAISS for efficient vector storage
- Integrates with Ollama for AI models
- Manages conversation memory and context
- Provides source attribution for answers
- Handles safe local file operations

This modular flow ensures seamless transitions from file uploading to knowledge generation, management, and conversational AI. The system maintains security through local-only processing and secure file handling while providing an intuitive interface for document interaction.

## Usage Tips

1. **File Management**
   - Upload documents in the File Management page
   - Process files individually or in batch
   - Monitor processing status and KB assignment

2. **Knowledge Base Management**
   - Create and manage knowledge bases
   - View KB sizes and contents
   - Delete or archive old KBs

3. **Chat Interface**
   - Select AI model from sidebar
   - Adjust temperature for response creativity
   - View source documents for answers
   - Clear conversation when needed

## Security Notes

- Only processes local files
- Safe deserialization for knowledge bases
- Secure document handling
- No external API dependencies

## Limitations

- Requires local Ollama installation
- Limited to supported document formats
- Memory constraints for large documents
- Local processing only

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [LangChain](https://python.langchain.com/)
- Uses [Ollama](https://ollama.ai/) for AI models
- Embeddings by [Nomic](https://nomic.ai/)
