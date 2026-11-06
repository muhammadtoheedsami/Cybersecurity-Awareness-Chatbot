# SecureBot | AI Cybersecurity Awareness Assistant

## Project Overview
SecureBot is an AI-powered cybersecurity awareness chatbot developed using Streamlit, Python, LangChain, FAISS, Hugging Face Embeddings, and the Groq API.

The purpose of SecureBot is to provide users with simple and educational information about cybersecurity topics. It uses a knowledge base of frequently asked questions and AI-generated responses to help users understand digital security concepts.

## Features
- AI-powered cybersecurity chatbot
- Beginner-friendly cybersecurity explanations
- Retrieval-Augmented Generation (RAG)
- Semantic search using Hugging Face embeddings
- FAISS vector database for knowledge retrieval
- Groq API integration for AI responses
- Interactive chat interface
- Suggested cybersecurity questions
- Retrieved knowledge and source display
- Sidebar with cybersecurity topics
- Clear Chat functionality
- Custom dark-themed Streamlit interface

## Cybersecurity Topics
SecureBot provides educational information about:

- Cybersecurity Basics
- Phishing
- Password Security
- Malware
- Ransomware
- Firewall
- Wi-Fi Security
- Social Engineering
- Two-Factor Authentication
- Secure Boot
- Network Security
- Encryption
- Ethical Hacking
- Information Security
- Operating System Security

## Technologies Used
- Python
- Streamlit
- LangChain
- Groq API
- Hugging Face Embeddings
- FAISS
- JSON
- python-dotenv

## Project Structure

```text
SecureBot/
│
├── index.py
├── Pipfile
├── README.md
├── .env
│
└── data/
    └── security_faq.json
```

**Note:** The `.env` file contains the API key and should not be shared or uploaded to a public repository.

## Installation and Setup

### 1. Install Python
Install Python on your computer and make sure it is available in your terminal.

### 2. Open the Project Folder
Open the terminal in your project directory:

```powershell
cd "D:\chatbot project"
```

### 3. Install Required Packages

If Pipenv is configured:

```powershell
pipenv install
```

Alternatively, install the dependencies using pip:

```powershell
python -m pip install streamlit python-dotenv langchain-core langchain-huggingface langchain-community langchain-groq faiss-cpu sentence-transformers
```

### 4. Configure the Groq API Key
Create a `.env` file in the project root directory and add your API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Replace `your_groq_api_key_here` with your valid Groq API key.

Do not publish your real API key.

### 5. Run the Application

```powershell
python -m streamlit run index.py
```

Streamlit will provide a local URL, usually:

```text
http://localhost:8501
```

Open this URL in your web browser to use SecureBot.

## Knowledge Base
SecureBot uses a JSON file located at:

```text
data/security_faq.json
```

The file contains cybersecurity questions and their answers. The application loads the JSON data, converts valid entries into documents, generates embeddings, and stores them in a FAISS vector database.

Example JSON entry:

```json
{
  "question": "What is cybersecurity?",
  "answer": "Cybersecurity is the practice of protecting systems, networks, and data from digital threats."
}
```

## System Workflow
1. The user opens the SecureBot application.
2. The application loads the Groq API key from the environment configuration.
3. The cybersecurity FAQ data is loaded from the JSON file.
4. Hugging Face embeddings are generated for the knowledge documents.
5. FAISS retrieves relevant knowledge based on the user's question.
6. The retrieved information is provided to the Groq language model.
7. The AI generates a beginner-friendly response.
8. The response and retrieved knowledge are displayed in the chat interface.

## Purpose of the Project
The main purpose of SecureBot is to improve cybersecurity awareness and help users understand common digital threats and security practices.

It is designed as an educational project and does not replace professional cybersecurity services or security assessments.

## Troubleshooting

### Groq API Key Error
Check that the `.env` file exists in the project directory and contains a valid `GROQ_API_KEY`.

### Knowledge Base File Not Found
Make sure the following file exists:

```text
data/security_faq.json
```

### Missing Python Packages
Install the required packages using pip or Pipenv.

### Streamlit Does Not Run
Use the following command:

```powershell
python -m streamlit run index.py
```

## Project Status
SecureBot is an educational cybersecurity awareness project.

## License
No license has been specified for this project.