import base64

from dotenv import load_dotenv
from transformers.models.pop2piano.convert_pop2piano_weights_to_hf import model

load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-pro')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:

        #converting PDF To Image
        images=pdf2image.convert_from_bytes(uploaded_file.read())
        first_page=images[0]

        #converting Image to Bytes
        image_byt_arr=io.BytesIO()
        first_page.save(image_byt_arr, format='JPEG')
        image_byt_arr=image_byt_arr.getvalue()

        pdf_parts=[
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(image_byt_arr).decode()

            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploded")


#streamlit app
st.set_page_config(layout="wide",page_icon="ATS Resume Analyzer")
st.header("Resume Analyzer")
input_text=st.text_area("Job Description ",key="input")
uploaded_file=st.file_uploader("Upload Your PDF",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Resume Uploaded Sucessfully")
else:
    st.write("File Not Uploaded")

#Resume Analysis Options or Features
submit_button_01=st.button("Tell me About the Resume")
submit_button_02=st.button("How Ca i Improvise my Skills")
submit_button_03=st.button("What are the keywords that are Missing")
submit_button_04=st.button("Percentage Match of the Resume")


#Input Prompt Templates for all features
input_prompt_01="""
You are an experience technical Human Resource manager,Your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with Highlight the strengths and weakness in relation to the spcified job role.
"""
input_prompt_02=







