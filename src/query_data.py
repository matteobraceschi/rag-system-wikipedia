import argparse
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from langchain_chroma import Chroma


CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Shortly answer the following question based on the provided context:

{context}

---

Question: {question}

Answer:"""

class SentenceTransformerEmbedding:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)

    def embed_query(self, query):
        return self.model.encode(query).tolist()  # Ensure it returns a list

    def embed_documents(self, documents):
        return self.model.encode(documents).tolist()  # Ensure it returns a list

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Access the API token
    huggingface_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

    # Create CLI
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    # Prepare the DB
    embedding_function = SentenceTransformerEmbedding('all-MiniLM-L6-v2')
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < 0.4:
        print("Unable to find matching results.")
        print(results[0][1])
        return
    print(results[0][1])

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)
    
    # Initialize the model with explicit parameters
    model = HuggingFaceEndpoint(
        repo_id="distilgpt2",
        huggingfacehub_api_token=huggingface_token,
        temperature=1
    )
    
    # Pass the prompt as a list
    response_text = model.generate([prompt])

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text.generations[0][0]}\nSources: {sources}"  # Access the first generated text
    print(formatted_response)

if __name__ == "__main__":
    main()
