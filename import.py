"""Import von unstrukturierten Daten mittels unstructured.io"""
import pickle
import os
from llama_index import download_loader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", default="")
assert OPENAI_API_KEY, "OPENAI_API_KEY environment variable is missing from .env"

def import_docs():
    """Lese alle Dokumente im Verzeichnis data und wandle zu Vektoren"""
    directory_reader = download_loader("SimpleDirectoryReader")
    loader = directory_reader('./data', recursive=True)
    raw_documents = loader.load_data()
    langchain_documents = [d.to_langchain_format() for d in raw_documents]
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    documents = text_splitter.split_documents(langchain_documents)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectorstore = FAISS.from_documents(documents, embeddings)

    # Save vectorstore
    with open("embedded_docs.pkl", "wb") as file:
        pickle.dump(vectorstore, file)


if __name__ == "__main__":
    import_docs()
