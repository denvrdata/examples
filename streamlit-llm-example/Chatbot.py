import streamlit as st
import requests
import os

# Set up Streamlit page
st.set_page_config(page_title="Simple Chatbot", page_icon="🤖")

# Define the Ollama backend URL
ollama_ip = os.getenv("OLLAMA_IP", "localhost")
OLLAMA_API_URL = f"http://{ollama_ip}:11434/api/chat"  # Replace with your actual Ollama endpoint

# Streamlit UI
st.title("💬 Simple Chatbot with Streamlit and Ollama")
st.write("This is a simple chatbot using Streamlit for UI and Ollama for backend.")

# Create a text input for user to type a message
user_message = st.text_input("You: ", "")

# Maintain chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to send message to Ollama backend and parse response
def get_ollama_response(message):
    # Define the payload in batch mode
    payload = {
        "model": "llama3.2",  # Replace with your specific model if needed
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ],
        "stream": False  # Use batch mode to get the full response at once
    }
    
    try:
        # Send POST request to the Ollama backend
        print("Firing request to ",OLLAMA_API_URL)
        response = requests.post(OLLAMA_API_URL, json=payload)
        
        if response.status_code == 200:
            # Extract the assistant's response from the JSON structure
            return response.json()["message"]["content"]
        else:
            return f"Error: {response.status_code}, {response.text}"
    except Exception as e:
        return f"Exception occurred: {str(e)}"

# Clear previous chat history when a new message is entered
if user_message:
    # Reset chat history for each new message
    st.session_state.chat_history = [{"role": "user", "content": user_message}]

    # Get response from Ollama
    bot_response = get_ollama_response(user_message)
    
    # Add bot response to chat history
    st.session_state.chat_history.append({"role": "bot", "content": bot_response})

# Display chat history
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"**You:** {chat['content']}")
    else:
        st.markdown(f"**Bot:** {chat['content']}")
