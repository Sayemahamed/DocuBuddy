"""This module contains the code for the RAG with Langchain."""

import os

# import fastembed
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.document_loaders import CSVLoader  # @type: ignore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from regex import P

# embedding_model = fastembed.Embed(model_name="all-mpnet-base-v2")
# from langchain_community.chains import
# from langchain import PromptTemplate
# from langchain.chains import LLMChain
# for model in fastembed.TextEmbedding().list_supported_models():
#     print(model["model"])

embeddings = FastEmbedEmbeddings()


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
            for dat in loader.load():
                print(dat)
            total_data.extend(loader.load())

    print(total_data)
    return total_data


if __name__ == "__main__":
    # Generate knowledge from a CSV file
    print("start")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000, chunk_overlap=0, length_function=len
    )
    data = splitter.split_documents(generate_knowledge_from_csv())
    data.__len__()

    db = FAISS.from_documents(data, embeddings)
    db.similarity_search(
        "which school highest Trailing 2 Weeks Teacher Weighted School Engagement Score"
    )
    db.save_local("./db", index_name="csv")
