import os
from dotenv import load_dotenv
import streamlit as st
from langchain_community.llms import ollama
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# Load environment variables from .env file
load_dotenv()

# Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")

# Define the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful Assistant. Please respond to the question asked."),
        ("user", "Question: {question}")
    ]
)

# Streamlit Framework
st.title("Simple Langchain App Powered by LLAMA2")

# Take input from the user
input_text = st.text_input("What is your question?")

# Initialize the Ollama model with Llama2
llm = ollama.Ollama(model="llama2")

# Create the LLM chain with prompt and LLM
chain = LLMChain(
    prompt=prompt,
    llm=llm
)

# Check if there is any input from the user
if input_text:
    # Generate the response and display it
    response = chain.run({"question": input_text})
    st.write(response)
