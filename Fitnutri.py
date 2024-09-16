import cohere
import streamlit as st

# Initialize the Cohere client
COHERE_API_KEY = 'ZHaOY2n1fbGF342yisQKgq3coGFZvGMIcL8DBjPy'  # Replace with your Cohere API key
co = cohere.Client(COHERE_API_KEY)

# Function to generate a response from Cohere based on the user's input
def generate_fitness_response(user_input):
    prompt = f"User: {user_input}\nFitNutriBot: Provide a detailed response related to fitness, workouts, nutrition, diet, exercise, physical activities, and gym exercises."

    # Call Cohere API to get the response
    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=1100,  # Adjust based on your needs
        temperature=0.5,  # Adjust if needed
    )

    # Return the generated text
    return response.generations[0].text.strip()

# Function to filter out off-topic responses
def filter_response(response_text):
    # Keywords related to fitness and nutrition topics
    keywords = ["fitness", "workouts", "nutrition", "diet", "exercise", "physical activities", "gym exercises"]

    # Check if any keyword is in the response
    if any(keyword in response_text.lower() for keyword in keywords):
        return response_text
    else:
        return "I can only provide information related to fitness, workouts, nutrition, diet, exercise, physical activities, and gym exercises. Please ask something related to these topics."

# Streamlit app layout
st.title("FitNutriBot")

# Initialize chat history
if 'history' not in st.session_state:
    st.session_state.history = []

# Display chat history
for entry in st.session_state.history:
    st.write(f"**User:** {entry['user']}")
    st.write(f"**FitNutriBot:** {entry['bot']}")

# User input
user_input = st.text_area("Ask me anything about fitness, workouts, nutrition, diet, or exercise:", height=150)

# Button to send the user input
if st.button("Send"):
    if user_input.strip():  # Ensure that user input is not empty
        # Generate response from the chatbot
        response = generate_fitness_response(user_input)

        # Filter the response to ensure it's on-topic
        filtered_response = filter_response(response)

        # Update chat history
        st.session_state.history.append({"user": user_input, "bot": filtered_response})

        # Display the chatbot's response
        st.write(f"**FitNutri:** {filtered_response}")
    else:
        st.write("Please enter a question.")