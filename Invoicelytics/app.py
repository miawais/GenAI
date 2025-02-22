from http.client import responses

from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from huggingface_hub import upload_file

load_dotenv()

#configuring API Key for Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Function to Load GeminiPro Vision
model = genai.GenerativeModel('gemini-pro-vision')


def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts  # Fixed indentation
    else:
        raise FileNotFoundError("File not found")


#Streamlit APP

st.set_page_config(page_title="Invoicelytics", page_icon=":moneybag:")
st.header("Invoicelytics")
input = st.text_input("Input Prompt ", key="input")
uploaded_file = st.file_uploader("choose and image", type=["jpg", "jpeg", "png"])
image=""

if upload_file is not None:
    image = Image.open(upload_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit = st.button("Explain The Invoice")

input_prompt= """
You are an expert in understandin invoices. We will upload a  image as invvoice and youwill have to answer any questions based on the uploaded invoice image."""

if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("Response")
    st.write(response)