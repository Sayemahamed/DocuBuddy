"""This is the Retrieval-Augmented Generator class."""

import json
import os
import re

import pandas as pd
from langchain_community.document_loaders.pdf import PyMuPDFLoader
from langchain_community.document_loaders.text import TextLoader
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.documents.base import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama.llms import OllamaLLM


class RAG:
    """This is the Retrieval-Augmented Generator class."""

    def __init__(self) -> None:
        """Initialize the RAG class."""
        self.embedding_model = FastEmbedEmbeddings(
            # To utilize full CPU power
            threads=os.cpu_count(),
            # Used base mode large model was too heavy and Small model was not getting the job done
            model_name="BAAI/bge-base-en-v1.5",
        )
        self.llm = OllamaLLM(model="phi3.5", temperature=0.7)
        self.vector_store = FAISS.from_documents(
            documents=[
                Document(
                    page_content="placeholder data",
                    metadata={"data_type": "placeholder data"},
                )
            ],
            embedding=self.embedding_model,
        )
        self.file_handlers = {
            "txt": handle_txt,
            "csv": handle_csv,
            "pdf": handle_pdf,
        }

    def generate_new_knowledge_base(self) -> None:
        """generates a new knowledge base from the files in the uploads"""
        self.vector_store: FAISS = FAISS.from_documents(
            documents=self.get_data_from_all_files(),
            embedding=self.embedding_model,
        )

    def add_to_knowledge_base(self, path: str) -> None:
        """adds data to the knowledge base
        Args:
            path (str): the path to the file
        """
        self.vector_store.add_documents(
            documents=self.file_handlers[path.split(".")[-1]](path)
        )

    def get_data_from_all_files(self) -> list[Document]:
        """
        Gets data from all files in the uploads
        Returns:
            list[Document]: list of documents
        """
        data_storage: list[Document] = []
        for file in os.listdir(path="./uploads"):
            if os.path.isfile(os.path.join("./uploads", file)):
                data_storage += self.file_handlers[file.split(".")[-1]](
                    os.path.join("./uploads", file)
                )
        return data_storage

    def vector_search(self, query: str, context_limit: int = 6000) -> list[str]:
        """
        Searches the vector store for the query
        Args:
            query (str): the user query
            data_limit (int, optional): the number of data to be returned. Defaults to 4000.
        Returns:
            list[Document]: the list of documents
        """
        relevant_documents: list[str] = []
        length_count: int = len(query)
        for (
            current_document
        ) in self.vector_store.similarity_search_with_relevance_scores(
            query=query, k=50
        ):
            length_count += len(str(object=current_document[0]))
            if length_count >= context_limit or current_document[1] <= 0.3:
                break
            relevant_documents.append(
                f"({current_document[0].page_content})=>{current_document[0].metadata}"
            )
        return relevant_documents

    def save_knowledge_base(self, name: str) -> None:
        """
        Saves the knowledge base
        Args:
            name (str): name the current knowledge base
        """
        path: str = os.path.join("./knowledge_bases", name)
        self.vector_store.save_local(folder_path=path)

    def load_knowledge_base(self, name: str) -> None:
        """
        Loads Saved knowledge base
        Args:
            name (str): name of the knowledge base to be loaded
        """
        path: str = os.path.join("./knowledge_bases", name)
        self.vector_store = FAISS.load_local(
            folder_path=path,
            embeddings=self.embedding_model,
            allow_dangerous_deserialization=True,
        )

    def ask(self, query: str) -> str:
        """
        Asks a question
        Args:
            query (str): the user query
        Returns:
            str: the answer
        """
        context: list[str] = self.vector_search(query=query, context_limit=3000)
        user_name: str = os.getlogin()
        Prompt_Template = """
        You are DocuBuddy, the AI assistant for {user_name}.
        For question types such as "Factual Lookup," "Summaries," "Comparative Analysis," "Extractive Questions," "Guidance/Procedure," "Interpretation," and "Document Retrieval," **respond** directly from the provided document with precision and clarity. Documents will be supplied in the format (data)=>{metadata}.
        For question types including "General Knowledge," "Creative/Hypothetical," "Opinion-Based," "Programming Help," "Translation/Grammar," "Math/Logic," and "Definitions," **refrain** from referencing document content unless absolutely necessary.
        **Ensure** responses are brief and focused. If the information is incomplete or uncertain, **reply** with "I'm not fully certain..." and **request** additional context or documents. For ambiguous questions, **seek** clarification succinctly without making assumptions. Be funny and engaging in your responses.

        Question:
        {query}

        Document:
        {context}
        """
        Prompt_Template: str = Prompt_Template.format(
            user_name=user_name,
            metadata="{metadata}",
            query=query if query else "No query provided.",
            context="\n\n".join(context)
            if context
            else "No document content provided.",
        )
        return self.llm.invoke(input=Prompt_Template)


# Utilities Functions
def handle_txt(path: str) -> list[Document]:
    """Returns ths data from the txt file in a list of Documents
    Args:
        path (str): path to the txt file
    Returns:
        list[Document]: list of Documents of the txt file
    """
    file_name: str = os.path.basename(p=path)
    cleaned_documents: list[Document] = []
    for document_data_frame in TextLoader(file_path=path, encoding="utf-8").load():
        if document_data_frame.page_content != "":
            document_data_frame.page_content = clean_string(
                text=document_data_frame.page_content
            )
            document_data_frame.metadata = {
                "file_name": file_name,
            }
            cleaned_documents.append(document_data_frame)
    return RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=20,
    ).split_documents(documents=cleaned_documents)


def handle_csv(path: str) -> list[Document]:
    """Returns ths data from the CSV file in a list of Documents
    Args:
        path (str): path to the csv file
    Returns:
        list[Document]: list of Documents of the csv file
    """
    data: list[Document] = []
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=path)
    file_name: str = os.path.basename(path)
    json_data = json.loads(df.to_json(orient="records"))
    for item in json_data:
        temp_data_holding: str = "{"
        for key, value in item.items():
            if (
                value is None
                or value == ""
                or value == " "
                or value == "null"
                or value == "NULL"
                or value == "None"
                or value == "none"
                or value == 0
                or value == "0"
            ):
                continue
            elif isinstance(value, str):
                temp_data_holding += f'"{key}": "{value}",'
            else:
                temp_data_holding += f'"{key}": {value},'
        temp_data_holding += "}"
        if len(data) > 0 and len(str(data[-1])) <= 250:
            data[-1].page_content += "," + temp_data_holding
        else:
            data.append(
                Document(
                    page_content=temp_data_holding, metadata={"File Name": file_name}
                )
            )
    return data


def handle_pdf(path: str) -> list[Document]:
    """
    Returns ths data from the PDF file in a list of Documents
    Args:
        path (str): path to the PDF file
    Returns:
        list[Document]: list of Documents of the PDF file
    """
    cleaned_documents: list[Document] = []
    for document_data_frame in PyMuPDFLoader(
        file_path=path, extract_images=False
    ).load():
        if document_data_frame.page_content != "":
            document_data_frame.page_content = clean_string(
                text=document_data_frame.page_content
            )
            document_data_frame.metadata = {
                "title": document_data_frame.metadata["title"],
                "page": document_data_frame.metadata["page"],
            }
            cleaned_documents.append(document_data_frame)
    return RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=20,
    ).split_documents(documents=cleaned_documents)


def clean_string(text: str) -> str:
    """
    Cleans the string by removing extra spaces
    Args:
        text (str): the string to be cleaned
    Returns:
        str: the cleaned string
    """
    return re.sub(pattern="\\s+", repl=" ", string=text).strip()


Augmented_model: RAG = RAG()
