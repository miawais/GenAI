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


# Function to generate summary and suggested questions
def generate_summary_and_questions(text):
    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3)
    prompt = f"""
    Given the following document text, generate a concise summary followed by 5 relevant questions a user might ask.

    Document:
    {text}

    Provide the response in the following format:
    Summary: <Your summary here>
    Questions:
    1. <Question 1>
    2. <Question 2>
    3. <Question 3>
    4. <Question 4>
    5. <Question 5>
    """

    response = model.invoke(prompt)
    response_text = response.content if hasattr(response, "content") else str(response)
    summary_part, *questions_part = response_text.split("Questions:")
    summary = summary_part.replace("Summary:", "").strip()
    questions = [q.strip() for q in questions_part[0].split("\n") if q.strip()] if questions_part else []

    return {"summary": summary, "questions": questions}


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
    docs = new_db.similarity_search(user_question)
    chain = get_chat_chain()
    response = chain.invoke({"input_documents": docs, "question": user_question})
    return response.get("output_text", "Sorry, I couldn't find an answer.")


# Main Streamlit Application
def main():
    st.set_page_config(page_title="InkChat", page_icon="📚")
    st.title("InkChat")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    with st.sidebar:
        st.title("📂 Upload & Process")
        pdf_docs = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)

        if st.button("Submit & Process"):
            if pdf_docs:
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)

                summary_response = generate_summary_and_questions(raw_text)

                st.session_state.summary = summary_response.get("summary", "Summary not available.")
                st.session_state.suggested_questions = summary_response.get("questions", [])
                st.success("Your document has been processed successfully!")
            else:
                st.warning("Please upload at least one PDF.")

    if "summary" in st.session_state:
        st.subheader("📜 Document Summary")
        st.write(st.session_state.summary)

    if "suggested_questions" in st.session_state:
        st.subheader("💡 Suggested Questions")
        for q in st.session_state.suggested_questions:
            if st.button(q):
                response = user_input(q)
                st.session_state.chat_history.append((q, response))

    st.subheader("💬 Chat with Your Document")
    user_question = st.chat_input("Ask something about your document...")
    if user_question:
        response = user_input(user_question)
        st.session_state.chat_history.append((user_question, response))

    for q, a in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(q)
        with st.chat_message("assistant"):
            st.write(a)


if __name__ == "__main__":
    main()
