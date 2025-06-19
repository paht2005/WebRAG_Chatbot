# Web-based Multi PDF RAG Chatbot with LangChain & Groq


---
## Table of Contents
- [Problem Statement](#problem-statement)
- [Objective](#objective)
- [System Workflow](#system-workflow)
  - [1. Document Ingestion](#1-document-ingestion)
  - [2. Embedding & Indexing](#2-embedding--indexing)
  - [3. Query Execution (RAG Pipeline)](#3-query-execution-rag-pipeline)
  - [4. Conversational Memory](#4-conversational-memory)
- [Key Components](#key-components)
- [Repository Structure](#repository-structure)
- [System Architecture](#system-architecture)
- [Use Cases](#use-cases)
- [Installation](#installation)
- [License](#license)
- [Contributing](#contributing)

---
## Problem Statement
- Organizations frequently manage large repositories of unstructured PDF documents such as technical manuals, compliance reports, internal policies, and product documentation. Manually retrieving relevant information from these files is time-consuming and inefficient.
- Traditional search mechanisms often lack semantic understanding and fail to provide context-aware answers, resulting in increased workload, delayed decision-making, and reduced productivity.

---
## Context & Motivation
Leveraging machine learning, natural language processing, and Generative AI, this project automates traditionally manual processes like document review, insurance claim triage, or customer support through a PDF-based intelligent assistant.
- **AI-enhanced understanding** of unstructured content for faster analysis.
- **Predictive insights** to support proactive decision-making.
- **Streamlined information flow** across internal teams or external users.
- Based on real-world use cases like product queries, support FAQs, legal document analysis, etc.
---
## Objective
This project aims to develop a **Retrieval-Augmented Generation (RAG)** based conversational agent that enables users to interact with a corpus of PDF documents through a natural language interface. The system is designed to:
- Automate information retrieval from enterprise documents.
- Provide real-time, contextually relevant responses to user queries.
- Maintain conversational memory for multi-turn interactions.
- Enhance user productivity and decision-making through intelligent document Q&A.

---
## System Workflow

### 1.	Document Ingestion
- All PDF files placed under the ``static/`` directory are loaded using ``PyPDFLoader``.
- Documents are segmented into semantically meaningful chunks using ``RecursiveCharacterTextSplitter``.
### 2.	Embedding & Indexing
- Each chunk is transformed into a vector representation using HuggingFaceEmbeddings (``all-MiniLM-L6-v2``).
- Vectors are stored in a **FAISS** index for fast and scalable similarity search.
### 3.	Query Execution (RAG Pipeline)
- A user submits a natural language query via the chat UI.
- Retriever selects top relevant chunks from the FAISS index.
- These chunks are passed to a **Groq-hosted large language model** (``mixtral-8x7b-32768``) to generate an informed response.
### 4. Conversational Memory
- A session-based ``ChatMessageHistory`` maintains prior user inputs and bot replies.
- ``RunnableWithMessageHistory`` wraps the chain to handle contextual understanding across turns.

---
## Key Components
| Module                | Technology Used                                     |
| --------------------- | --------------------------------------------------- |
| Web Interface         | Flask + Jinja2 Templates (`chat.html`)              |
| Document Loader       | `PyPDFLoader` from `langchain_community`            |
| Text Chunking         | `RecursiveCharacterTextSplitter`                    |
| Embedding Model       | `HuggingFaceEmbeddings` (MiniLM-L6-v2)              |
| Vector Store          | FAISS                                               |
| Language Model        | `ChatGroq` (`mixtral-8x7b-32768`)                   |
| Conversational Memory | `ChatMessageHistory` + `RunnableWithMessageHistory` |

--- 
## Repository Structure
```
WebRAG_Chatbot/
├── pycache/ # Compiled Python cache
├── faiss/ # FAISS vector index
├── imgs/ # Image assets 
├── static/ # Source PDF documents (knowledge base)
├── templates/ # HTML templates for Flask frontend
├── .env # API keys and environment variables
├── Final Report.pdf # Final report for documentation or submission
├── README.md # Project documentation
├── app.py # Main application code (Flask + LangChain)
├── gitignore # Git ignore rules
├── prompts.py # Custom system prompts for RAG chain
├── requirements.txt                # Python dependencies
├── LICENSE

```
---
## System Architecture

![image](https://github.com/user-attachments/assets/86f014a1-548f-4ad6-8de5-8e75511e9969)

---
## Use Cases
- Customer support based on internal knowledge base PDFs.
- Legal or compliance document Q&A.
- Employee onboarding or policy clarification assistant.
- Technical manuals or product documentation assistant.

--- 
## Installation
Follow the steps below to set up and run the Multi-PDF RAG Chatbot locally:

### 1.  Clone the repository
```bash
git clone https://github.com/paht2005/WebRAG_Chatbot.git
cd WebRAG_Chatbot
```

### 2. (Optional but recommended) Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate       # On Linux/macOS
venv\Scripts\activate          # On Windows
```
### 3. Install dependencies

```bash
pip install -r requirements.txt
```
### 4. Create a .env file
Create a file named ``.env`` in the root directory and add your API key:

```bash
GROQ_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxx

```
**Do not share this file publicly. Use my ``.env`` for reference in the repo.**

### 5. Add your PDFs
Place all your ``.pdf`` documents inside the ``static/`` folder. These will be parsed and indexed automatically when the app starts.

### 6. Run the Flask app

```bash
python app.py

```
- Then open your browser and navigate to:
```bash
(http://127.0.0.1:5000)
```
- **You can now start chatting with your documents in real time**

--- 

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.


---
## Contributing
I welcome contributions to improve this project!
Feel free to fork, pull request, or open issues. Ideas welcome!
