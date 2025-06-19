# Web-based Multi PDF RAG Chatbot with LangChain & Groq

---
## Problem Statement
Organizations frequently manage large repositories of unstructured PDF documents such as technical manuals, compliance reports, internal policies, and product documentation. Manually retrieving relevant information from these files is time-consuming and inefficient.
Traditional search mechanisms often lack semantic understanding and fail to provide context-aware answers, resulting in increased workload, delayed decision-making, and reduced productivity.

---
## Objective:
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
2.	Generative Model:
o	After retrieving the relevant data, the generative model (such as a GPT-based model) is tasked with crafting a human-like response using the context provided by the retrieved documents.
3.	Chatbot Pipeline:
o	Step 1: User submits a query (e.g., "What are the top features of Product X?").
o	Step 2: The retrieval component searches for relevant documents or product details related to Product X from the knowledge base.
o	Step 3: The retrieved information is passed to the generative model, which formulates a coherent, context-aware response.
o	Step 4: The response is delivered to the user in a conversational manner.

## Architecture:

![image](https://github.com/user-attachments/assets/86f014a1-548f-4ad6-8de5-8e75511e9969)
