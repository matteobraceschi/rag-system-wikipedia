from retriever import answer_question

def main():
    # Prompt the user for a question
    question = input("\n--- Please enter your question:\n\n")

    # Call the answer_question function directly
    response = answer_question(question)

    # Display the response
    print("\n--- Response from the model:\n")
    print(response)

if __name__ == "__main__":
    main()


"""

Which city hosted the first modern Summer Olympic Games? In what year?

questions = [
    "Which city hosted the first modern Summer Olympic Games? In what year?",
    "How many times have the Summer Olympic Games been hosted in France?",
    "How long has it been since Paris last hosted the Summer Olympics?",
    "Did the first edition of the Winter Olympic Games take place before the first edition of the Summer Olympic Games?",
    "Sport climbing is not an Olympic sport: true or false?",
    "What is the average number of Olympic gold medals per edition for Italy?",
    "Who is the most recent winner of the 100-meter sprint? With what time?"
]"""
