from rag import ask_question, embedder
from wikipedia_extractor import get_contents


def main():


    # Define example questions
    questions = [
        "Quale città ospitò i primi Giochi Olimpici estivi dell’età moderna? In che anno?",
        "Quante volte i Giochi Olimpici estivi sono stati ospitati in Francia?",
        "Quanto tempo è passato dall’ultima volta che Parigi ha ospitato le olimpiadi estive?",
        "La prima edizione dei Giochi Olimpici invernali è avvenuta prima della prima edizione dei Giochi Olimpici estivi?",
        "L’arrampicata sportiva non è uno sport olimpico: vero o falso?",
        "Quale è il numero medio di ori olimpici per edizione per l’Italia?",
        "Chi è l’ultima vincitrice dei 100 metri piani? Con quale tempo?"
    ]

    # Get content from Wikipedia
    documents = get_contents(page_titles)
    # Create a vector store from the extracted documents
    vector_store = embedder(documents)

    # Iterate through questions and get answers
    for question in questions:
        answer = ask_question(vector_store, question)
        print(f"Q: {question}\nA: {answer}\n")

if __name__ == "__main__":
    main()