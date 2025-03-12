from flask import Flask, render_template, request
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

# Store chat history
chat_history = []

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
    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3)
    chain = load_qa_chain(model, chain_type="stuff")  # ✅ "stuff" requires 'input_documents'
    return chain

# Route for Home Page
@app.route("/", methods=["GET", "POST"])
def index():
    global chat_history

    if request.method == "POST":
        # Handle file upload
        if "file" in request.files and request.files["file"].filename:
            pdf_file = request.files["file"]
            text = get_pdf_text(pdf_file)
            chunks = get_text_chunks(text)
            get_vector_store(chunks)
            return render_template("index.html", message="File uploaded and processed successfully!", chat_history=chat_history)

        # Handle chat input
        elif "message" in request.form:
            user_question = request.form["message"]

            try:
                # Load the FAISS vector store
                embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
                new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

                # Perform similarity search
                docs = new_db.similarity_search(user_question)

                # Load AI chain
                chain = get_chat_chain()

                # ✅ Use 'input_documents' instead of 'context'
                response = chain.invoke({"input_documents": docs, "question": user_question})

                # Store chat history
                chat_history.append(("You", user_question))
                chat_history.append(("AI", response["output_text"]))

            except Exception as e:
                chat_history.append(("AI", f"Error: {str(e)}"))

    # ✅ Ensure a valid return statement for GET requests
    return render_template("index.html", chat_history=chat_history)

if __name__ == "__main__":
    app.run(debug=True)
