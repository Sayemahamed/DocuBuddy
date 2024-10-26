
# DocuBuddy

DocuBuddy is a cutting-edge assistant built for seamless interaction with documents and general question-answering, designed to leverage advanced language processing and search technologies. With tools like LangChain, Ollama, phi3.5, FastEmbed, and FAISS, DocuBuddy provides quick and accurate responses from your uploaded documents or for broader general inquiries.

## Table of Contents
- [Key Features](#key-features)
- [How DocuBuddy Can Help You](#how-docubuddy-can-help-you)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Troubleshooting and FAQs](#troubleshooting-and-faqs)
- [License](#license)
- [Contact](#contact)

## Key Features

- **Document Intelligence Powered by LangChain**: Using LangChain as its backbone, DocuBuddy links various models and workflows, allowing smooth interaction with documents of various formats and content types.

- **Efficient Semantic Search with FAISS**: Powered by FAISS (Facebook AI Similarity Search), DocuBuddy can quickly locate relevant information within documents, enabling high-speed retrieval and accurate answers.

- **High-Quality Embeddings with FastEmbed**: FastEmbed enhances DocuBuddy's understanding of text by generating precise embeddings, which enable accurate question-answering and deep insights within your documents.

- **Sophisticated Model Support via Ollama and phi3.5**: With models like Ollama and phi3.5, DocuBuddy goes beyond document-based answers to handle general inquiries, providing versatile and high-quality responses tailored to your needs.

- **User-Friendly Interface**: Upload your documents, ask questions, and let DocuBuddy take care of the rest. Its intuitive interface enables anyone to harness its powerful tools without needing technical expertise.

## How DocuBuddy Can Help You

DocuBuddy is perfect for:

- **Researchers** who need instant insights from numerous documents
- **Professionals** looking to streamline document searches and retrieve critical information efficiently
- **Students** aiming to dive deeper into new subjects and access detailed answers quickly

DocuBuddy combines these advanced tools to help you focus on what matters by handling information retrieval seamlessly and effectively.

Here’s the updated **Getting Started** section with the correct command:

```markdown
## Getting Started

1. **Clone the Repository**: Clone this repository to your local machine using:
   ```bash
   git clone https://github.com/Sayemahamed/DocuBuddy.git
   ```

2. **Create a Virtual Environment**: It's recommended to use a virtual environment to manage dependencies.
   - For Python 3, create a virtual environment by running:
     ```bash
     python3 -m venv docubuddy_env
     ```
   - Activate the virtual environment:
     - On macOS/Linux:
       ```bash
       source docubuddy_env/bin/activate
       ```
     - On Windows:
       ```bash
       docubuddy_env\Scripts\activate
       ```

3. **Install Requirements**: With the virtual environment activated, install all necessary dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**: Start the Streamlit app with:
   ```bash
   streamlit run .\DocuBuddy.py
   ```

5. **Usage**: Upload documents via the interface, ask questions, and explore DocuBuddy's powerful search and question-answering features.
```

This change aligns the command with the file name `DocuBuddy.py` in the root directory.

4. **Usage**: Upload documents via the interface, ask questions, and explore DocuBuddy's powerful search and question-answering features.

## Configuration

DocuBuddy may require certain configurations for optimal use:

- **API Keys**: Ensure you have access keys for any models, such as Ollama, used in the application.
- **Environment Variables**: Set up environment variables for sensitive information, such as keys or database URLs.

Example:
```bash
export OLLAMA_API_KEY=your_api_key
export FAISS_INDEX_PATH=path_to_index
```

## Usage Examples

Once you've uploaded a document, try some of these sample questions:

- "Summarize the contents of the uploaded document."
- "What are the main findings in section 2 of the document?"
- "Explain the key takeaways from the data in this document."

DocuBuddy will analyze and respond based on the content of the uploaded documents, giving you quick insights.

## Roadmap

Planned features for future releases include:
- **Expanded Model Integration**: Adding support for additional NLP models for more diverse language handling.
- **Multi-Document Search**: Enable querying across multiple documents simultaneously.
- **Enhanced PDF Parsing**: Improved handling of complex document layouts.
- **User Management and Security**: Optional authentication for document access control.

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add your feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

Make sure to adhere to the [Code of Conduct](CODE_OF_CONDUCT.md) and write detailed commit messages for any changes.

## Troubleshooting and FAQs

- **Q**: I get an error when trying to load a PDF.  
  **A**: Make sure the PDF format is supported. Large PDFs may require more memory.

- **Q**: How do I add custom embeddings?  
  **A**: Update the embedding module in `fastembed.py` and restart the app.

## License

DocuBuddy is licensed under the Mozilla Public License 2.0 (MPL 2.0). You may use, distribute, and modify the software under the terms of this license. For more details, please refer to the [LICENSE](LICENSE) file.

The MPL 2.0 allows for both open-source and proprietary use but requires any modifications to the licensed files to be disclosed under MPL 2.0 when distributed.

## Contact

For questions or further assistance, please reach out to the author at:
- **Email**: sayemahamed183@gmail.com

---

[GitHub Repository](https://github.com/Sayemahamed/DocuBuddy)
```

This README provides a comprehensive guide with a clear structure, making it easy for users to understand, configure, and contribute to DocuBuddy.
