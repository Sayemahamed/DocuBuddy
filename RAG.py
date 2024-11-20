"""
DocuBuddy RAG (Retrieval Augmented Generation) Implementation.
This module provides the core RAG functionality for document processing and Q&A.
"""

import asyncio
import json
import logging
import os
from pathlib import Path
from typing import List, Dict, Optional, Any, Union

import pandas as pd
from langchain_community.document_loaders.pdf import PyMuPDFLoader
from langchain_community.document_loaders.text import TextLoader
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.documents.base import Document
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import LLM
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama.llms import OllamaLLM
from pydantic import BaseModel, Field
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGConfig(BaseModel):
    """Configuration for RAG model."""
    
    llm_model: str = Field(default="llama3.2", description="Name of the LLM model to use")
    llm_temperature: float = Field(default=0.7, description="Temperature for LLM responses")
    chunk_size: int = Field(default=300, description="Size of text chunks for splitting")
    chunk_overlap: int = Field(default=20, description="Overlap between text chunks")
    context_limit: int = Field(default=6000, description="Maximum context length for queries")
    ollama_base_url: str = Field(default="http://localhost:11434", description="Ollama API base URL")
    
class DocumentProcessor:
    """Handles document loading and processing."""
    
    def __init__(self, chunk_size: int, chunk_overlap: int):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        
    async def process_text(self, path: Path) -> List[Document]:
        """Process text files."""
        try:
            docs = TextLoader(str(path), encoding="utf-8").load()
            return self.text_splitter.split_documents(self._clean_documents(docs, path))
        except Exception as e:
            logger.error(f"Error processing text file {path}: {e}")
            raise
            
    async def process_csv(self, path: Path) -> List[Document]:
        """Process CSV files."""
        try:
            df = pd.read_csv(path)
            records = json.loads(df.to_json(orient="records"))
            docs = []
            
            for record in records:
                content = self._format_record(record)
                if content:
                    docs.append(Document(
                        page_content=content,
                        metadata={"file_name": path.name, "type": "csv"}
                    ))
            return docs
        except Exception as e:
            logger.error(f"Error processing CSV file {path}: {e}")
            raise
            
    async def process_pdf(self, path: Path) -> List[Document]:
        """Process PDF files."""
        try:
            loader = PyMuPDFLoader(str(path))
            docs = loader.load()
            return self.text_splitter.split_documents(self._clean_documents(docs, path))
        except Exception as e:
            logger.error(f"Error processing PDF file {path}: {e}")
            raise
            
    def _clean_documents(self, docs: List[Document], path: Path) -> List[Document]:
        """Clean and prepare documents."""
        cleaned_docs = []
        for doc in docs:
            if doc.page_content.strip():
                doc.page_content = self._clean_text(doc.page_content)
                doc.metadata.update({"file_name": path.name})
                cleaned_docs.append(doc)
        return cleaned_docs
    
    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean text content."""
        import re
        return re.sub(r'\s+', ' ', text).strip()
        
    @staticmethod
    def _format_record(record: Dict[str, Any]) -> Optional[str]:
        """Format a CSV record into a string."""
        formatted = {}
        for key, value in record.items():
            if value and str(value).strip() and str(value).lower() not in ['none', 'null', '0']:
                formatted[key] = value
        return json.dumps(formatted) if formatted else None

class RAG:
    """Retrieval-Augmented Generation implementation."""
    
    def __init__(self, config: Optional[RAGConfig] = None):
        """Initialize RAG with optional configuration."""
        self.config = config or RAGConfig()
        self.logger = logging.getLogger(__name__)
        self._initialize_components()
        
    def _initialize_components(self) -> None:
        """Initialize LLM, embeddings, and vector store."""
        try:
            self.embedding_model: Embeddings = OllamaEmbeddings(
                model=self.config.llm_model,
                base_url=self.config.ollama_base_url
            )
            
            self.llm: LLM = OllamaLLM(
                model=self.config.llm_model,
                temperature=self.config.llm_temperature,
                base_url=self.config.ollama_base_url
            )
            
            # Initialize with placeholder document
            self.vector_store = FAISS.from_documents(
                documents=[Document(
                    page_content="placeholder",
                    metadata={"type": "placeholder"}
                )],
                embedding=self.embedding_model
            )
            
            self.doc_processor = DocumentProcessor(
                chunk_size=self.config.chunk_size,
                chunk_overlap=self.config.chunk_overlap
            )
            
        except Exception as e:
            self.logger.error(f"Failed to initialize RAG components: {e}")
            raise
            
    async def add_document(self, file_path: Union[str, Path]) -> None:
        """Add a document to the knowledge base."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
            
        processors = {
            ".txt": self.doc_processor.process_text,
            ".csv": self.doc_processor.process_csv,
            ".pdf": self.doc_processor.process_pdf
        }
        
        processor = processors.get(path.suffix.lower())
        if not processor:
            raise ValueError(f"Unsupported file type: {path.suffix}")
            
        try:
            docs = await processor(path)
            self.vector_store.add_documents(docs)
            self.logger.info(f"Successfully processed {path}")
        except Exception as e:
            self.logger.error(f"Error processing {path}: {e}")
            raise
            
    async def query(self, query: str) -> str:
        """Process a query and return a response."""
        if not query.strip():
            raise ValueError("Query cannot be empty")
            
        try:
            context = await self._get_context(query)
            return await self._generate_response(query, context)
        except Exception as e:
            self.logger.error(f"Error processing query: {e}")
            return "I encountered an error processing your query. Please try again."
            
    async def _get_context(self, query: str) -> List[str]:
        """Retrieve relevant context for the query."""
        relevant_docs = self.vector_store.similarity_search_with_relevance_scores(
            query=query,
            k=50
        )
        
        context = []
        length_count = len(query)
        
        for doc, score in relevant_docs:
            if score <= 0.2 or length_count >= self.config.context_limit:
                break
            content = f"({doc.page_content})=>{doc.metadata}"
            length_count += len(content)
            context.append(content)
            
        return context
        
    async def _generate_response(self, query: str, context: List[str]) -> str:
        """Generate a response using the LLM."""
        prompt = self._create_prompt(query, context)
        return self.llm.invoke(prompt)
        
    def _create_prompt(self, query: str, context: List[str]) -> str:
        """Create a prompt for the LLM."""
        return f"""
        You are DocuBuddy, the AI assistant for {os.getlogin()}.
        For document-based questions (Factual Lookup, Summaries, Analysis, etc.), use the provided context.
        For general knowledge questions, respond without referencing documents unless necessary.
        Be concise and precise. If uncertain, acknowledge it and request clarification.
        
        Question: {query}
        
        Context: {chr(10).join(context) if context else "No relevant context found."}
        """
        
    async def save_knowledge_base(self, path: Union[str, Path]) -> None:
        """Save the current knowledge base."""
        try:
            save_path = Path(path)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            self.vector_store.save_local(str(save_path))
            self.logger.info(f"Knowledge base saved to {save_path}")
        except Exception as e:
            self.logger.error(f"Error saving knowledge base: {e}")
            raise
            
    async def load_knowledge_base(self, path: Union[str, Path]) -> None:
        """Load a saved knowledge base."""
        try:
            load_path = Path(path)
            if not load_path.exists():
                raise FileNotFoundError(f"Knowledge base not found: {load_path}")
                
            self.vector_store = FAISS.load_local(
                str(load_path),
                self.embedding_model,
                allow_dangerous_deserialization=True
            )
            self.logger.info(f"Knowledge base loaded from {load_path}")
        except Exception as e:
            self.logger.error(f"Error loading knowledge base: {e}")
            raise

# Create a global instance with default configuration
rag_instance = RAG()
