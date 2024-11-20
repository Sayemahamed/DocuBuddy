"""
DocuBuddy RAG (Retrieval Augmented Generation) Implementation.
This module provides the core RAG functionality for document processing and Q&A.
"""

import os
from typing import List, Dict, Any
import logging
from pathlib import Path
import pickle
import tempfile

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    UnstructuredFileLoader,
)
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_core.memory import BaseMemory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGSystem:
    def __init__(
        self, model_name: str = "llama3.2", embed_model: str = "nomic-embed-text"
    ):
        """Initialize the RAG system with specified models."""
        self.model_name = model_name
        self.embed_model = embed_model
        self.vector_store = None
        self.conversation_chain = None
        self.temperature = 0.0

        # Initialize chat history and memory
        self.chat_history = ChatMessageHistory()
        self.memory = ConversationBufferMemory(
            chat_memory=self.chat_history,
            memory_key="chat_history",
            output_key="answer",
            return_messages=True,
        )

        # Initialize embeddings
        self.embeddings = OllamaEmbeddings(model=self.embed_model)

        # Initialize LLM
        self._initialize_llm()

        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, length_function=len
        )

    def _initialize_llm(self):
        """Initialize or reinitialize the LLM with current settings."""
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        self.llm = ChatOllama(
            model=self.model_name,
            callback_manager=callback_manager,
            temperature=self.temperature,
        )

        # Reinitialize conversation chain if it exists
        if self.vector_store is not None:
            self._initialize_conversation_chain()

    def _initialize_conversation_chain(self):
        """Initialize or reinitialize the conversation chain."""
        self.conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
            memory=self.memory,
            return_source_documents=True,
            return_generated_question=False,
        )

    def update_model(self, model_name: str):
        """Update the model and reinitialize components."""
        self.model_name = model_name
        self._initialize_llm()
        logger.info(f"Updated model to {model_name}")

    def update_temperature(self, temperature: float):
        """Update the temperature setting."""
        self.temperature = temperature
        self._initialize_llm()
        logger.info(f"Updated temperature to {temperature}")

    def load_document(self, file_path: str) -> List[str]:
        """Load and split a document into chunks."""
        try:
            # Verify file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            # Select appropriate loader based on file extension
            ext = Path(file_path).suffix.lower()
            try:
                if ext == ".pdf":
                    loader = PyPDFLoader(file_path)
                elif ext == ".txt":
                    loader = TextLoader(file_path, encoding='utf-8')
                elif ext == ".docx":
                    loader = Docx2txtLoader(file_path)
                else:
                    loader = UnstructuredFileLoader(file_path)

                # Load and split the document
                documents = loader.load()
                if not documents:
                    raise ValueError(f"No content found in file: {file_path}")

                chunks = self.text_splitter.split_documents(documents)
                if not chunks:
                    raise ValueError(f"Document was split but no chunks were created: {file_path}")

                logger.info(f"Successfully loaded and split document: {file_path}")
                return chunks

            except UnicodeDecodeError:
                # Try different encodings if UTF-8 fails
                encodings = ['latin-1', 'cp1252', 'iso-8859-1']
                for encoding in encodings:
                    try:
                        loader = TextLoader(file_path, encoding=encoding)
                        documents = loader.load()
                        if documents:
                            chunks = self.text_splitter.split_documents(documents)
                            logger.info(f"Successfully loaded document with {encoding} encoding: {file_path}")
                            return chunks
                    except UnicodeDecodeError:
                        continue

                raise ValueError(f"Could not decode file with any supported encoding: {file_path}")

        except Exception as e:
            logger.error(f"Error loading document {file_path}: {str(e)}")
            raise

    def process_documents(self, file_paths: List[str], kb_name: str = None) -> None:
        """Process multiple documents and create/update vector store."""
        if not file_paths:
            raise ValueError("No files provided for processing")

        try:
            all_chunks = []
            failed_files = []

            for file_path in file_paths:
                try:
                    chunks = self.load_document(file_path)
                    if chunks:
                        all_chunks.extend(chunks)
                        logger.info(f"Successfully processed: {file_path}")
                    else:
                        failed_files.append((file_path, "No content extracted"))
                except Exception as e:
                    failed_files.append((file_path, str(e)))
                    logger.error(f"Failed to process {file_path}: {str(e)}")

            if not all_chunks:
                raise ValueError("No valid content extracted from any of the provided files")

            # Create or update vector store
            if self.vector_store is None:
                self.vector_store = FAISS.from_documents(
                    documents=all_chunks, embedding=self.embeddings
                )
            else:
                self.vector_store.add_documents(all_chunks)

            # Initialize conversation chain
            self._initialize_conversation_chain()

            # Log results
            success_count = len(file_paths) - len(failed_files)
            logger.info(f"Successfully processed {success_count} out of {len(file_paths)} documents")
            
            if failed_files:
                error_msg = "\n".join([f"- {path}: {error}" for path, error in failed_files])
                logger.warning(f"Failed to process the following files:\n{error_msg}")

        except Exception as e:
            logger.error(f"Error in document processing: {str(e)}")
            raise

    def save_knowledge_base(self, save_path: str) -> None:
        """Save the vector store to disk."""
        try:
            if self.vector_store is not None:
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(save_path), exist_ok=True)

                # Save the vector store
                self.vector_store.save_local(save_path)
                logger.info(f"Successfully saved knowledge base to {save_path}")
            else:
                logger.warning("No vector store to save")

        except Exception as e:
            logger.error(f"Error saving knowledge base: {str(e)}")
            raise

    def load_knowledge_base(self, load_path: str) -> None:
        """Load a vector store from disk."""
        try:
            if os.path.exists(load_path):
                self.vector_store = FAISS.load_local(
                    load_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True,  # Only for local files we created
                )

                # Initialize conversation chain
                self._initialize_conversation_chain()

                logger.info(f"Successfully loaded knowledge base from {load_path}")
            else:
                logger.warning(f"Knowledge base not found at {load_path}")

        except Exception as e:
            logger.error(f"Error loading knowledge base: {str(e)}")
            raise

    def query(self, question: str) -> Dict[str, Any]:
        """Query the knowledge base."""
        try:
            if self.conversation_chain is None:
                raise ValueError(
                    "No knowledge base loaded. Please process documents first."
                )

            # Get response from conversation chain
            response = self.conversation_chain.invoke({"question": question})

            # Extract answer and source documents
            answer = response["answer"]
            source_docs = response["source_documents"]

            # Format source documents
            sources = []
            for doc in source_docs:
                source_info = {"content": doc.page_content, "metadata": doc.metadata}
                sources.append(source_info)

            return {"answer": answer, "sources": sources}

        except Exception as e:
            logger.error(f"Error querying knowledge base: {str(e)}")
            raise

    def clear_memory(self):
        """Clear conversation memory."""
        self.memory.clear()
        logger.info("Cleared conversation memory")


# Create a global instance with default configuration
rag_instance = RAGSystem()
