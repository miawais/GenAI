import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#function to extract Text form PDF
def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text+=page.extract_text()

            return text



#function to divide Text into Chunks
def get_text_chunks(text):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks=text_splitter.split_text(text)
    return chunks

#function to store text chunks in vector store
def get_vector_store(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store=FAISS.from_texts(texts=chunks,embedding=embeddings)
    vector_store.save_local("faiss_index")
    return vector_store


#function to define Conversational Chain
def get_chat_chain(vector_store):
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
    # Initialize the model
    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3)
    prompt=PromptTemplate(template=prompt_template,input_variables=["context","question"])
    chain=load_qa_chain(model,chain_type="stuff",prompt=prompt)
    return chain



#funtion to get user input
def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db=FAISS.load_local("faiss_index",embeddings)
    docs=new_db.similarity_search(user_question)

    chain= get_chat_chain(new_db)
    response = chain({"question": user_question, "context": docs}, return_only_outputs=True)
    print(docs)

    st.write("Reply : ",response["Answer"])




#main Function

def main():
    st.set_page_config(page_title="InkChat",page_icon=":books:")
    st.title("InkChat")

    user_question=st.text_input("Ask a question about your document:")
    if st.button("Ask"):
        user_input(user_question)


    with st.sidebar:
        st.title("Menu")
        pdf_docs=st.file_uploader("Upload Your PDF",type=["pdf"])
        if st.button("Submit & Process"):
            raw_text=get_pdf_text(pdf_docs)
            text_chunks=get_text_chunks(raw_text)
            vector_store=get_vector_store(text_chunks)
            st.success("Your Document has been processed successfully")
            st.balloons()




if __name__=="__main__":
    main()








