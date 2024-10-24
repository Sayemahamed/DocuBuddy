"""This is the Retrieval-Augmented Generator class."""

import json
import os
import re

import pandas as pd
from langchain_community.document_loaders.text import TextLoader
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.documents.base import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.pdf import PyMuPDFLoader


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
        """generates a new knowledge base from the files in the directory"""
        self.vector_store: FAISS = FAISS.from_documents(
            documents=self.get_data_from_all_files(),
            embedding=self.embedding_model,
        )

    def add_to_knowledge_base(self, path: str) -> None:
        """adds data to the knowledge base
        Args:
            path (str): the path to the file
        """
        self.vector_store.add_documents(self.file_handlers[path.split(".")[-1]](path))

    def get_data_from_all_files(self) -> list[Document]:
        """
        Gets data from all files in the directory
        Returns:
            list[Document]: list of documents
        """
        data_storage: list[Document] = []
        for file in os.listdir(path="./directory"):
            if os.path.isfile(os.path.join("./directory", file)):
                data_storage += self.file_handlers[file.split(".")[-1]](
                    os.path.join("./directory", file)
                )
        return data_storage


# Utilities Functions
def handle_txt(path: str) -> list[Document]:
    """Returns ths data from the txt file in a list of Documents
    Args:
        path (str): path to the txt file

    Returns:
        list[Document]: list of Documents of the txt file
    """
    cleaned_documents: list[Document] = []
    for document_data_frame in TextLoader(file_path=path, encoding="utf-8").load():
        if document_data_frame.page_content != "":
            document_data_frame.page_content = clean_string(
                text=document_data_frame.page_content
            )
            cleaned_documents.append(document_data_frame)
    return RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
    ).split_documents(cleaned_documents)


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
        data.append(
            Document(page_content=temp_data_holding, metadata={"File Name": file_name})
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
            cleaned_documents.append(document_data_frame)
    print(cleaned_documents)
    return RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
    ).split_documents(cleaned_documents)


def clean_string(text: str) -> str:
    """
    Cleans the string by removing extra spaces
    Args:
        text (str): the string to be cleaned
    Returns:
        str: the cleaned string
    """
    return re.sub("\\s+", " ", text).strip()


# Testing Area
rag = RAG()
rag.generate_new_knowledge_base()

# rag.vector_store.similarity_search_with_relevance_scores(
#     "Fastest computing device",
#     k=10,
#     fetch_k=100,
# )
