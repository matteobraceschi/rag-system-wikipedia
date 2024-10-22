import chromadb
from sentence_transformers import SentenceTransformer

# Inizializzare il modello di Sentence Transformers
model = SentenceTransformer('all-MiniLM-L6-v2')

# Inizializzare ChromaDB
client = chromadb.Client()

# Creare un nuovo database Chroma
collection = client.create_collection("sentence_embeddings")

# Frasi da trasformare in embedding
texts = [
    "Ciao, come stai?",
    "Oggi è una bella giornata.",
    "Il machine learning è interessante.",
    "Chroma è un database per embedding."
]

# Creare gli embedding delle frasi
embeddings = model.encode(texts)

# Aggiungere le frasi e i loro embedding al database Chroma
for text, embedding in zip(texts, embeddings):
    collection.add(
        documents=[text],
        embeddings=[embedding.tolist()]  # Convertire l'embedding in lista
    )

# Esempio di ricerca: trovare l'embedding più vicino a una nuova frase
query = "Qual è il tuo stato d'animo oggi?"
query_embedding = model.encode([query])

# Eseguire la ricerca nel database Chroma
results = collection.query(
    query_embeddings=query_embedding.tolist(),
    n_results=2  # Numero di risultati da restituire
)

# Stampare i risultati
print("Risultati della ricerca:")
for document, score in zip(results['documents'][0], results['distances'][0]):
    print(f"Testo: {document}, Distanza: {score}")
