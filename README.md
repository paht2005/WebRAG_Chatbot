# Web-based Multi PDF RAG Chatbot with LangChain & Groq

---
## Problem Statement
Organizations frequently manage large repositories of unstructured PDF documents such as technical manuals, compliance reports, internal policies, and product documentation. Manually retrieving relevant information from these files is time-consuming and inefficient.
Traditional search mechanisms often lack semantic understanding and fail to provide context-aware answers, resulting in increased workload, delayed decision-making, and reduced productivity.

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
- A user submits a natural language query via the web UI.
- The retriever identifies the top-k relevant chunks from the vector store.
- These chunks are passed to a **Groq-hosted large language model** (``mixtral-8x7b-32768``) to generate an informed response.
### 4. Conversational Memory
- The system maintains session-level chat history using LangChain's ``RunnableWithMessageHistory`` to support follow-up questions with contextual understanding.

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

## System Architecture

![image](https://github.com/user-attachments/assets/86f014a1-548f-4ad6-8de5-8e75511e9969)

---
## Use Cases
- Customer support based on internal knowledge base PDFs.
- Legal or compliance document Q&A.
- Employee onboarding or policy clarification assistant.
- Technical manuals or product documentation assistant.
