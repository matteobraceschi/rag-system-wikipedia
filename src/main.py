from retriever import answer_question
from evaluation import evaluate_response

questions = [
    "Which city hosted the first modern Summer Olympic Games? In what year?",
    "How many times have the Summer Olympic Games been hosted in France?",
    "How long has it been since Paris last hosted the Summer Olympics?",
    "Did the first edition of the Winter Olympic Games take place before the first edition of the Summer Olympic Games?",
    "Sport climbing is not an Olympic sport: true or false?",
    "What is the average number of Olympic gold medals per edition for Italy?",
    "Who is the most recent winner of the 100-meter sprint? With what time?"
]


correct_responses = [
    "Athens hosted the first modern Summer Olympic Games in 1896.",
    "The Summer Olympic Games have been hosted in France three times: in 1900 (Paris), 1924 (Paris), and 2024 (Paris).",
    "It has been 96 years since Paris last hosted the Summer Olympics in 1924.",  
    "Yes, the first edition of the Winter Olympic Games took place in 1924, which was after the first modern Summer Olympic Games in 1896.",
    "False. Sport climbing was included as an Olympic sport in the 2020 Tokyo Olympics.",
    "Italy has won a total of 742 Olympic medals, of which 257 are gold. The average number of gold medals per edition is approximately 6.5.",
    "The most recent winner of the 100-meter sprint is Christian Coleman, who won the gold medal at the 2022 World Athletics Championships with a time of 9.86 seconds."  
]

def main():
    # Prompt the user for a question
    n_QA = 0
    question = questions[n_QA]
    # question = input("\n*** Please enter your question: ***\n\n")
    print("*"*50)
    print("\n*** Question: ***\n")
    print(question)    
    # Call the answer_question function directly
    response = answer_question(question)
    # Display the response
    print("\n*** Response from the model: ***\n")
    print(response)
    print("*"*50)
    evaluate_response(response, correct_responses[n_QA])
    print("*"*50)

if __name__ == "__main__":
    main()

