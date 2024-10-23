import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from llm_models import HuggingFaceModel, OpenAIModel


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


def answer_question(query_text):
    # Load environment variables from .env file
    load_dotenv()

    # Access the API token
    huggingface_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

    # Prepare the DB
    embedding_function = SentenceTransformerEmbedding('all-MiniLM-L6-v2')
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < 0.4:
        return "Unable to find matching results."

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    hf_model = HuggingFaceModel(
        repo_id="gpt2",
        huggingfacehub_api_token=huggingface_token,
        temperature=1.0
    )
    hf_response = hf_model.generate_text(prompt)

    formatted_response = f"Response: {hf_response}\n"  # Access the generated text
    
    return formatted_response
