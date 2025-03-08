import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to extract text from PDF
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
    return text

# Function to split text into chunks
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

# Function to store text chunks in FAISS vector store
def get_vector_store(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(texts=chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
    return vector_store

# Function to define Conversational Chain
def get_chat_chain():
    prompt_template = """
    You are an AI assistant designed to provide accurate and relevant answers based on multiple documents. 
    Use the provided document context to generate helpful responses. If the answer is not found in the documents, 
    let the user know and avoid making up information.

    Context:
    {context}

    User Question:
    {question}

    Response:
    """
    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

# Function to process user input
def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    # Perform the similarity search
    docs = new_db.similarity_search(user_question)

    # Get the QA chain
    chain = get_chat_chain()

    # Pass the documents in the required format
    response = chain.invoke({
        "input_documents": docs,
        "question": user_question
    })

    # Display the answer
    st.write("Reply:", response.get("output_text", "Sorry, I couldn't find an answer."))

# Main Streamlit Application
def main():
    st.set_page_config(page_title="InkChat", page_icon="📚")
    st.title("InkChat")

    user_question = st.text_input("Ask a question about your document:")
    if st.button("Ask"):
        if user_question.strip():
            user_input(user_question)
        else:
            st.warning("Please enter a question.")

    with st.sidebar:
        st.title("Menu")
        pdf_docs = st.file_uploader("Upload Your PDFs", type=["pdf"], accept_multiple_files=True)

        if st.button("Submit & Process"):
            if pdf_docs:
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Your document has been processed successfully!")
                st.balloons()
            else:
                st.warning("Please upload at least one PDF.")

if __name__ == "__main__":
    main()