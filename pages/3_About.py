"""This page contains information about DocuBuddy."""

import streamlit as st

with st.sidebar:
    st.markdown(body="[View the source code](https://github.com/Sayemahamed/DocuBuddy)")
    st.markdown(
        body="[Internal Architecture](https://raw.githubusercontent.com/Sayemahamed/DocuBuddy/refs/heads/main/System_Diagram.png)"
    )

# Title for the About Page
st.title(body="About DocuBuddy")

# Description of DocuBuddy
st.markdown(
    body="""
**DocuBuddy** is a cutting-edge assistant built for seamless interaction with documents and answering general questions, designed to bring you the power of advanced language processing and search technologies. Leveraging tools like **LangChain**, **Ollama**, **phi3.5**, **FastEmbed**, and **FAISS**, DocuBuddy provides fast, accurate responses from your uploaded documents or for broader general inquiries.
"""
)

# Key Features Section
st.header(body="Key Features")

st.markdown(
    body="""
- **Document Intelligence Powered by LangChain**: Using LangChain as its backbone, DocuBuddy effectively links different models and workflows, allowing for a smooth interaction with documents of various formats and content types.

- **Efficient Semantic Search with FAISS**: With FAISS (Facebook AI Similarity Search), DocuBuddy quickly locates relevant information in your documents. Its advanced indexing enables fast and accurate answers by embedding content in a format optimized for speed.

- **High-Quality Embeddings with FastEmbed**: FastEmbed enhances DocuBuddy's understanding of text by generating precise embeddings, enabling accurate question-answering and deeper insights within your documents.

- **Sophisticated Model Support via Ollama and phi3.5**: By integrating models like Ollama and phi3.5, DocuBuddy not only provides answers from your documents but also handles general questions, providing versatility and high-quality responses tailored to your needs.

- **Easy-to-Use Interface**: Simply upload your documents, ask questions, and let DocuBuddy handle the rest. Its intuitive interface allows anyone to make the most of its powerful tools without needing technical expertise.
"""
)

# Benefits Section
st.header(body="How DocuBuddy Can Help You")

st.markdown(
    body="""
Whether you’re a researcher needing instant insights, a professional looking to streamline document searches, or a student tackling new subjects, DocuBuddy combines innovative tools to deliver quick, relevant information. It’s built to help you focus on what matters by taking care of information retrieval seamlessly and effectively.

Experience smarter, faster, and more accurate document interactions with **DocuBuddy**—your intelligent document and question-answering companion.
"""
)
