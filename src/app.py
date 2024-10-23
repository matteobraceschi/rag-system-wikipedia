import streamlit as st
from retriever import answer_question  # Ensure these functions are defined in your retriever module
from evaluation import evaluate_response  # Ensure these functions are defined in your evaluation module
from create_db import generate_data_store  # Import the function from database.py

# Predefined questions and correct responses
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
    st.title("Olympic Trivia Chatbot")
    st.write("Ask a question about the Olympics, and I will provide you with an answer!")

    # Create a container for the button
    button_container = st.container()

    # Add CSS for the button styling
    st.markdown("""
        <style>
            .small-button {
                position: absolute;
                top: 10px;
                right: 10px;
                padding: 5px 10px;
                font-size: 12px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .small-button:hover {
                background-color: #0056b3;
            }
        </style>
    """, unsafe_allow_html=True)

    # Button to create the database
    button_clicked = button_container.button("Create Database", key="create_db")

    if button_clicked:
        with st.spinner("Creating database..."):
            try:
                generate_data_store()  # Call the function from database.py
                st.success("Database created successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

    # Input field for user questions
    user_question = st.text_input("Type your question here:")
    st.write(f"**Question:**\n {user_question}")

    if user_question:
        # Check if the question is in the predefined list
        if user_question in questions:
            # Get the corresponding answer
            index = questions.index(user_question)
            response = answer_question(user_question)
            st.write(f"**Response from the model:**\n {response}")

            # Evaluate the response
            evaluation_result = evaluate_response(response, correct_responses[index])
            st.write(f"**Evaluation:**\n {evaluation_result}")
        else:
            response = answer_question(user_question)
            st.write(f"**Response from the model:**\n {response}")
    

if __name__ == "__main__":
    main()
