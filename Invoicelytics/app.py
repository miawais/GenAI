from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

load_dotenv()

# Configuring API Key for Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini 1.5 Pro model (Switching from deprecated gemini-pro-vision)
model = genai.GenerativeModel('gemini-1.5-pro')  # Change model name here

def get_gemini_response(input_text, image, prompt):
    response = model.generate_content([input_text, image[0], prompt])
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
        return image_parts
    else:
        raise FileNotFoundError("File not found")


# Streamlit APP
st.set_page_config(page_title="Invoicelytics", page_icon=":moneybag:")
st.header("Invoicelytics")

input_text = st.text_input("Input Prompt", key="input")
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Explain The Invoice")

input_prompt = """
You are an expert in understanding invoices. We will upload an invoice image, and you will have to answer any questions based on the uploaded invoice image.
"""

if submit and uploaded_file is not None:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input_text)
    st.subheader("Response")
    st.write(response)
