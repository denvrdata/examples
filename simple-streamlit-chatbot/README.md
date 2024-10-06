
# Simple Streamlit Chatbot with Ollama

This repository contains a simple chatbot application built using [Streamlit](https://streamlit.io/) for the frontend UI and an [Ollama](https://ollama.ai/) model backend for generating responses. The application takes user inputs via a text box and sends them to the Ollama backend to generate responses using a specified model.

## Features

- **Interactive Chatbot Interface**: Built with Streamlit to provide a simple UI for interactions.
- **Ollama Backend Integration**: Connects to the Ollama backend server for LLM-based responses.
- **Environment Configuration**: Easily configure the Ollama backend server IP using an environment variable.


## Getting Started

### Step 1: Denvr Cloud Account

Setup your account to launch your GPU of choice ( A100-40G, A100-80G, H100, Gaudi2 )

https://console.cloud.denvrdata.com/account/login

### Step 2: Launch the VM

### Step 3: Install/Update packages

```
sudo apt update -y
sudo apt install python3-pip
```

### Step 4: Set Up Environment Variables

Setup Virtual env ( if required )

```
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
git clone https://github.com/denvrdata/examples.git
cd simple-streamlit-chatbot
pip3 install -r requirements.txt
```

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

### Step 5: Run the Streamlit App

Once the environment is set up, run the Streamlit app using the following command:

```bash
streamlit run Chatbot.py
```

### Step 5: Open the Application in Your Browser

After starting the app, Streamlit will output a local URL, usually something like:

```
Local URL: http://localhost:8501
```

Open this URL in your browser to access the chatbot UI.

### Step 7: Start Chatting

You can now enter your messages in the text box, and the bot will respond using the model specified in the backend.


## Troubleshooting

- **Environment Variable Not Set**: If the application is not connecting to the Ollama backend, ensure that the `OLLAMA_IP` variable is set correctly and that the server is reachable.
- **CORS Issues**: If running the backend on a different machine, make sure CORS settings allow connections from the Streamlit frontend.
- **Port Issues**: Ensure that port `11434` (or the port you specified) is open and accessible.


## Contributing

If you would like to contribute, please fork the repository and submit a pull request with your changes.

