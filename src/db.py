from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import Chroma
from wikipedia_extractor import get_contents
import os
import shutil

CHROMA_PATH = "chroma"

def main():
    generate_data_store()

def generate_data_store():
    page_titles = [
        "Olympic_Games",
        "Summer_Olympic_Games"
    ]
    documents = load_documents(page_titles)
    chunks = split_text(documents)
    save_to_chroma(chunks)

def load_documents(page_titles):
    documents = get_contents(page_titles)
    return documents

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    return chunks

def save_to_chroma(chunks: list[Document]):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Load the SentenceTransformer model
    sentence_transformer_model = SentenceTransformer('all-MiniLM-L6-v2')

    # Create a wrapper class for the embedding function
    class EmbeddingFunction:
        def embed_documents(self, texts):
            return sentence_transformer_model.encode(texts, convert_to_tensor=True).tolist()

    embedding_function = EmbeddingFunction()

    # Create a new DB from the documents using the embedding function
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_function,  # Use the instance of the embedding class
        persist_directory=CHROMA_PATH
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    main()
