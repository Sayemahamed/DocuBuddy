"""This module contains the code for the RAG with Langchain."""

import os

import fastembed
from langchain_ollama.llms import OllamaLLM
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader  # @type: ignore
from langchain.text_splitter import RecursiveCharacterTextSplitter

# from langchain_community.chains import
# from langchain import PromptTemplate
# from langchain.chains import LLMChain

llm = OllamaLLM(model="phi3.5")
embedding_model = OllamaEmbeddings(model="phi3.5")


def generate_knowledge_from_csv():
    """Generate knowledge from a CSV file."""
    total_data = []
    directory = "./directory"
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            loader = CSVLoader(
                file_path=os.path.join(directory, filename),
                encoding="utf-8",
                csv_args={"delimiter": ","},
            )
            total_data.extend(loader.load())
    return total_data


if __name__ == "__main__":
    # Generate knowledge from a CSV file
    print("start")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=0, length_function=len
    )
    data = splitter.split_documents(generate_knowledge_from_csv())
    db = FAISS.from_documents(data, embedding_model)
    print("finish")

    db.save_local("./db", index_name="csv")
