from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from sentence_transformers import SentenceTransformer
import weaviate
from wikipedia_extractor import get_contents
import os
import shutil

WEAVIATE_URL = "http://localhost:8080"  # Assicurati che Weaviate sia in esecuzione su questa porta
CLIENT = weaviate.Client(WEAVIATE_URL)

def main():
    generate_data_store()

def generate_data_store():
    # Define Wikipedia pages to extract content from
    page_titles = [
        "Giochi_olimpici",
        "Giochi_olimpici_estivi"
    ]
    documents = load_documents(page_titles)
    chunks = split_text(documents)
    save_to_weaviate(chunks)

def load_documents(page_titles):
    # Get content from Wikipedia
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
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    # Example output for debugging
    if chunks:
        document = chunks[10]  # Ensure there are enough chunks
        print(document.page_content)
        print(document.metadata)

    return chunks

def save_to_weaviate(chunks: list[Document]):
    # Clear out the previous class data (optional)
    try:
        CLIENT.schema.delete_class("Document")
    except Exception as e:
        print(f"Class 'Document' does not exist or could not be deleted: {e}")

    # Define schema for Weaviate
    class_obj = {
        "class": "Document",
        "properties": [
            {
                "name": "content",
                "dataType": ["text"],
            },
            {
                "name": "metadata",
                "dataType": ["string"],  # Puoi modificare in base alle tue necessità
            },
        ],
    }
    CLIENT.schema.create_class(class_obj)

    # Load the SentenceTransformer model
    sentence_transformer_model = SentenceTransformer('all-MiniLM-L6-v2')

    # Define the embedding function
    for chunk in chunks:
        embedding = sentence_transformer_model.encode(chunk.page_content, convert_to_tensor=True).tolist()
        # Add document to Weaviate
        CLIENT.data.creator.create(
            class_name="Document",
            properties={
                "content": chunk.page_content,
                "metadata": chunk.metadata,
                "_embedding": embedding,  # Aggiungi l'embedding come proprietà
            },
        )
    print(f"Saved {len(chunks)} chunks to Weaviate.")

if __name__ == "__main__":
    main()
