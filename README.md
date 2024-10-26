# DocuBuddy

DocuBuddy is an advanced assistant for seamless interaction with documents and question-answering. Utilizing technologies like LangChain, Ollama, phi3.5, FastEmbed, Streamlit and FAISS, DocuBuddy efficiently delivers quick and accurate responses from uploaded documents or general inquiries.
[Archetecture of DocuBuddy](https://app.eraser.io/workspace/6rhglH5bcLJdhtmP1qjM?origin=share)

## Table of Contents
- [Key Features](#key-features)
- [Use Cases](#use-cases)
- [Getting Started](#getting-started)
- [Usage Examples](#usage-examples)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Contact](#contact)

## Key Features

- **Document Interaction with LangChain**: LangChain supports document queries, enabling DocuBuddy to process documents of various formats and content types.
- **Efficient Search with FAISS**: FAISS quickly locates relevant content within documents through fast indexing and optimized retrieval.
- **Embeddings with FastEmbed**: FastEmbed enables high-quality embeddings, enhancing DocuBuddy's question-answering capabilities.
- **Advanced Model Support**: Integrating models like Ollama and phi3.5, DocuBuddy handles both document-based and general questions.
- **User-Friendly Interface**: Easily upload documents, ask questions, and explore document insights without technical expertise.

## Use Cases

DocuBuddy is ideal for:
- **Researchers** needing quick insights from multiple documents
- **Professionals** seeking efficient document searches
- **Students** looking to understand new topics quickly

DocuBuddy streamlines information retrieval, so you can focus on what matters.

## Getting Started

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Sayemahamed/DocuBuddy.git
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python3 -m venv docubuddy_env
   ```
   - Activate the environment:
     - macOS/Linux:
       ```bash
       source docubuddy_env/bin/activate
       ```
     - Windows:
       ```bash
       docubuddy_env\Scripts\activate
       ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   streamlit run .\DocuBuddy.py
   ```

## Usage Examples

After uploading a document, try the following sample questions:
- "Summarize the contents of the uploaded document."
- "What are the key findings in section 2 of the document?"

DocuBuddy will analyze and respond based on document content, providing quick insights.

## Roadmap

- **Expanded Model Integration**: Support for additional NLP models
- **Multi-Document Querying**: Search across multiple documents simultaneously
- **Enhanced PDF Parsing**: Better handling of complex document layouts
- **Security Features**: Optional authentication for secure access

## Contributing

To contribute:
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/YourFeature
   ```
3. Commit your changes:
   ```bash
   git commit -am 'Add your feature'
   ```
4. Push to the branch and open a Pull Request.

Please follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Troubleshooting

- **Error loading a PDF?** Check format compatibility; larger PDFs may need more memory.
- **Custom embeddings?** Update `fastembed.py` for custom embeddings and restart the app.

## License

DocuBuddy is licensed under the Mozilla Public License 2.0 (MPL 2.0), which permits both open-source and proprietary use. Modifications to licensed files must be disclosed when distributed. For more details, refer to the [LICENSE](LICENSE) file.

## Contact

For questions or support, contact:
- **Email**: sayemahamed183@gmail.com


[GitHub Repository](https://github.com/Sayemahamed/DocuBuddy)


