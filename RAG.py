"""This is the Retrieval-Augmented Generator class."""

import json
import os

import pandas as pd
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.documents.base import Document

embedding_model = FastEmbedEmbeddings(
    # To utilize full CPU power
    threads=os.cpu_count(),
    # Used base mode large model was too heavy and Small model was not getting the job done 
      model_name="BAAI/bge-base-en-v1.5"
)
temp: list[Document] = [
    Document(
        page_content="placeholder data", metadata={"data_type": "placeholder data"}
    )
]
db: FAISS = FAISS.from_documents(temp, embedding_model)


# Utilities Functions
def handle_txt(file_path):
    print(f"Handling TXT file: {file_path}")


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


def handle_pdf(file_path):
    print(f"Handling PDF file: {file_path}")


# db: FAISS = FAISS.from_embeddings(embeddings=embedding_model.embed_documents(),)
class RAG:
    """This is the Retrieval-Augmented Generator class."""

    def __init__(self, vector_store: FAISS = db) -> None:
        """Initialize the RAG class."""
        self.vector_store = vector_store
        self.file_handlers = {
            "txt": handle_txt,
            "csv": handle_csv,
            "pdf": handle_pdf,
        }

    def generate_new_knowledge_base(self) -> None:
        """Generate a new knowledge base."""
        self.vector_store: FAISS = FAISS.from_documents(
            documents=self.get_data_from_all_files(),
            embedding=embedding_model,
        )

    def add_to_knowledge_base(self, path: str) -> None:
        """adds data to the knowledge base
        Args:
            path (str): the path to the file
        """
        self.vector_store.add_documents(self.file_handlers[path.split(".")[-1]](path))

    def get_data_from_all_files(self) -> list[Document]:
        """Get data from all files."""
        data_storage: list[Document] = []
        for file in os.listdir(path="./directory"):
            if os.path.isfile(os.path.join("./directory", file)):
                data_storage += self.file_handlers[file.split(".")[-1]](
                    os.path.join("./directory", file)
                )
        return data_storage


rag = RAG()
rag.generate_new_knowledge_base()

rag.vector_store.similarity_search_with_relevance_scores(
    "Which School has highest Trailing 2 Weeks Teacher Weighted School Engagement Score",
    k=10,
    fetch_k=100,
)
