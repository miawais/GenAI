from flask import Flask, render_template, request, jsonify
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Google AI API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to extract text from PDF
def get_pdf_text(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = "".join([page.extract_text() or "" for page in pdf_reader.pages])
    return text

# Function to split text into chunks
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return text_splitter.split_text(text)

# Function to store text chunks in FAISS vector store
def get_vector_store(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(texts=chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

# Function to define AI Conversational Chain
def get_chat_chain():
    prompt_template = """You are an AI assistant. Use the provided document context to generate relevant answers.

    Context:
    {context}

    User Question:
    {question}

    Response:
    """
    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3)
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt_template)
    return chain

# Route for Home Page
@app.route("/")
def index():
    return render_template("index.html")

# Route to Upload and Process PDF
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    pdf_file = request.files["file"]
    text = get_pdf_text(pdf_file)
    chunks = get_text_chunks(text)
    get_vector_store(chunks)

    return jsonify({"message": "File uploaded and processed successfully"}), 200

# Route to Handle AI Chat
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_question = data.get("message")

    if not user_question:
        return jsonify({"error": "Empty question"}), 400

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    docs = new_db.similarity_search(user_question)
    chain = get_chat_chain()

    response = chain.invoke({
        "input_documents": docs,
        "question": user_question
    })

    return jsonify({"response": response.get("output_text", "No answer found.")})

if __name__ == "__main__":
    app.run(debug=True)
