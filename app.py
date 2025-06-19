from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains import RetrievalQA
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from prompts import qa_system_prompt, contextualize_q_system_prompt

# Load .env file
load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
# Init Flask App
app = Flask(__name__)
chat_history = []
conversation_store = {}
FAISS_PATH = "faiss"

# Init LLM (Groq)
llm = ChatGroq(model="mixtral-8x7b-32768")

# Chat Session Store 
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in conversation_store:
        print(f"Creating store for session: {session_id}")
        conversation_store[session_id] = ChatMessageHistory()
    return conversation_store[session_id]

# PDF Document Loader 
def get_document_loader():
    loader = DirectoryLoader('static', glob="**/*.pdf", show_progress=True, loader_cls=PyPDFLoader)
    docs = loader.load()
    return docs

# Split into Chunks
def get_text_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
    chunks = text_splitter.split_documents(documents)
    return chunks

# Embedding & Vectorstore
def get_embeddings():
    path = os.path.join(os.getcwd(), FAISS_PATH)
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    if os.path.exists(path):
        print(f"FAISS index found. Loading from {path}")
        db = FAISS.load_local(path, embedding_model, allow_dangerous_deserialization=True)
    else:
        print(f"No FAISS index found. Creating at {path}")
        documents = get_document_loader()
        chunks = get_text_chunks(documents)
        db = FAISS.from_documents(chunks, embedding_model)
        db.save_local(path)
    
    return db

def get_retriever():
    db = get_embeddings()
    retriever = db.as_retriever()
    return retriever

#  Home Page 
@app.route('/')
def index():
    return render_template('home.html')

# Chat Interface 
@app.route('/chat', methods=['GET', 'POST'])
def document_display():
    if request.method == 'GET':
        return render_template('chat.html')
    
    question = request.form['question']
    retriever = get_retriever()

    # Prompt templates
    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])

    # Build chains
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer"
    )

    try:
        response = conversational_rag_chain.invoke(
            {"input": question},
            config={"configurable": {"session_id": "abc123"}}
        )
        chat_history.append(question)
        chat_history.append(response['answer'])

    except Exception as e:
        chat_history.append(f"🚫 Error: {str(e)}")

    return render_template('chat.html', chat_history=chat_history)

#  Run Server 
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
