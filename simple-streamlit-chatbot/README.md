Here's a sample README file that you can use to outline the steps to execute the Streamlit chatbot example code. This README will provide instructions on how to set up, configure, and run the application using an Ollama backend.

---

# Simple Streamlit Chatbot with Ollama

This repository contains a simple chatbot application built using [Streamlit](https://streamlit.io/) for the frontend UI and an [Ollama](https://ollama.ai/) model backend for generating responses. The application takes user inputs via a text box and sends them to the Ollama backend to generate responses using a specified model.

## Features

- **Interactive Chatbot Interface**: Built with Streamlit to provide a simple UI for interactions.
- **Ollama Backend Integration**: Connects to the Ollama backend server for LLM-based responses.
- **Environment Configuration**: Easily configure the Ollama backend server IP using an environment variable.

## Prerequisites

Before running the application, make sure you have the following:

1. **Python 3.7+** installed on your system.
2. An **Ollama Backend** server running and accessible. Replace the model and IP details according to your setup.
3. **Streamlit** and **Requests** libraries installed. You can install these with:

    ```bash
    pip install streamlit requests
    ```

## Getting Started

### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/denvrdata/examples.git
cd examples/simple-streamlit-chatbot
```

### Step 2: Set Up Environment Variables

Configure the Ollama server IP address using an environment variable. This ensures that the application knows where to send the requests.

**For Linux / Mac:**

```bash
export OLLAMA_IP=<your_ollama_ip>
```

**For Windows (Command Prompt):**

```cmd
set OLLAMA_IP=<your_ollama_ip>
```

**For Windows (PowerShell):**

```powershell
$env:OLLAMA_IP = "<your_ollama_ip>"
```

Replace `<your_ollama_ip>` with the actual IP address where your Ollama server is running, for example:

```bash
export OLLAMA_IP="<your_ollama_ip>"
```

### Step 3: Run the Streamlit App

Once the environment is set up, run the Streamlit app using the following command:

```bash
streamlit run Chatbot.py
```

### Step 4: Open the Application in Your Browser

After starting the app, Streamlit will output a local URL, usually something like:

```
Local URL: http://localhost:8501
```

Open this URL in your browser to access the chatbot UI.

### Step 5: Start Chatting

You can now enter your messages in the text box, and the bot will respond using the model specified in the backend.

## Code Overview

The main components of the code are:

1. **`get_ollama_response()`**: Sends user messages to the Ollama server using the `/api/chat` endpoint and retrieves the response.
2. **Environment Configuration**: Uses the `OLLAMA_IP` environment variable to dynamically construct the Ollama backend URL.
3. **Streamlit UI**: A simple interface for user inputs and displaying the chat history.

### Example Configuration

If the Ollama backend is running locally, you can set:

```bash
export OLLAMA_IP=localhost
```

If the backend is running on a remote server with IP `130.250.171.37`, use:

```bash
export OLLAMA_IP=130.250.171.37
```

## Troubleshooting

- **Environment Variable Not Set**: If the application is not connecting to the Ollama backend, ensure that the `OLLAMA_IP` variable is set correctly and that the server is reachable.
- **CORS Issues**: If running the backend on a different machine, make sure CORS settings allow connections from the Streamlit frontend.
- **Port Issues**: Ensure that port `11434` (or the port you specified) is open and accessible.


## Contributing

If you would like to contribute, please fork the repository and submit a pull request with your changes.

