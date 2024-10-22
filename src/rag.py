from sentence_transformers import SentenceTransformer
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import openai 
from dotenv import load_dotenv
import os
import shutil



# Function to ask questions using a retrieval-based approach
def ask_question(vector_store, question):  
    # Retrieve relevant documents from the vector store
    retrieved_docs = vector_store.similarity_search(question, k=3)  # Adjust k as needed

    # Prepare the context from retrieved documents
    context = "\n".join([doc.page_content for doc in retrieved_docs])

    # Set up a free language model for generation
    llm = HuggingFacePipeline.from_model_id(model_id="gpt2", task="text-generation")  # Replace with a more suitable model

    # Create the prompt with the context and the question
    prompt = f"Question: {question}\nAnswer:"
    
    # Truncate the input if it's too long
    if len(prompt.split()) > 512:  # Adjust this value as needed
        prompt = ' '.join(prompt.split()[:512])  # Truncate the prompt to 512 words
    
    # Generate the response
    response = llm.generate([prompt])
    
    return response
