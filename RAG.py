"""This module contains the RAG class."""

import os
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.documents.base import Document
from langchain_community.document_loaders.csv_loader import CSVLoader

embedding_model = FastEmbedEmbeddings(threads=os.cpu_count())
temp: list[Document] = [
    Document(
        page_content="placeholder data", metadata={"data_type": "placeholder data"}
    )
]
db: FAISS = FAISS.from_documents(temp, embedding_model)


# Utilities Functions
def handle_txt(file_path):
    print(f"Handling TXT file: {file_path}")


def handle_csv(
    path: str, encoding: str = "utf-8", csv_args: dict = {"delimiter": ","}
) -> list[Document]:
    """Returns ths data from the CSV file in a list of Documents

    Args:
        path (str): _description_
        encoding (str, optional): _description_. Defaults to "utf-8".
        csv_args (_type_, optional): _description_. Defaults to {"delimiter": ","}.

    Returns:
        list[Document]: _description_
    """
    loader = CSVLoader(
        file_path=path,
        encoding=encoding,
        csv_args=csv_args,
    )
    return loader.load()


def handle_pdf(file_path):
    print(f"Handling PDF file: {file_path}")


# db: FAISS = FAISS.from_embeddings(embeddings=embedding_model.embed_documents(),)
class RAG:
    """This is the Retrieval-Augmented Generator class."""

    def __init__(self, vector_store: FAISS = db) -> None:
        """Initialize the RAG class."""
        self.vector_store = vector_store
        self.file_handlers = {
            ".txt": handle_txt,
            ".csv": handle_csv,
            ".pdf": handle_pdf,
        }

    def generate_new_knowledge_base(self) -> None:
        """Generate a new knowledge base."""
        self.vector_store: FAISS = FAISS.from_documents(
            documents=self.get_data_from_all_files(),
            embedding=embedding_model,
        )

    def get_data_from_all_files(self) -> list[Document]:
        """Get data from all files."""
        data_storage: list[Document] = []
        for file in os.listdir(path="./directory"):
            if os.path.isfile(os.path.join("./directory", file)):
                data_storage.append(
                    self.file_handlers[file.split(".")[-1]](
                        os.path.join("./directory", file)
                    )
                )
        return data_storage
