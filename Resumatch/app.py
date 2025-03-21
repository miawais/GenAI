import base64
import os
import io  # ✅ Added missing import
import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Function to get Gemini response
def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text


# Function to process uploaded PDF
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Open the PDF file using PyMuPDF (fitz)
        pdf_file = fitz.open(stream=uploaded_file.read(), filetype="pdf")

        # Convert the first page to an image
        page = pdf_file.load_page(0)  # 0 is the first page
        pix = page.get_pixmap()  # Render page to a pixmap (image)

        # Convert pixmap to PIL image
        image_byt_arr = io.BytesIO(pix.tobytes("png"))
        image = Image.open(image_byt_arr)

        # Convert image to base64 for Gemini API
        image_byt_arr = io.BytesIO()
        image.save(image_byt_arr, format='JPEG')
        image_byt_arr = image_byt_arr.getvalue()

        # Convert image to base64 for Gemini API
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(image_byt_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded.")


# Streamlit app setup
st.set_page_config(layout="wide", page_icon="📄", page_title="ATS Resume Analyzer")
st.header("📄 Resume Analyzer")

# Input Fields
input_text = st.text_area("Job Description", key="input")
uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    st.success("✅ PDF Resume Uploaded Successfully!")
else:
    st.warning("⚠ Please upload a PDF file.")

# Resume Analysis Options
submit_button_01 = st.button("📑 Tell me About the Resume")
submit_button_02 = st.button("📈 How Can I Improve My Skills?")
submit_button_03 = st.button("🔍 What Keywords are Missing?")
submit_button_04 = st.button("📊 Percentage Match with Job Description")

# Input Prompt Templates
input_prompt_01 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the given job description.
Provide a detailed evaluation, highlighting the candidate's strengths, weaknesses, and overall alignment with the job role.
"""

input_prompt_02 = """
Analyze the skills mentioned in this resume and suggest relevant skills the candidate should improve or acquire.
Base your recommendations on current industry trends and job market demands.
"""

input_prompt_03 = """
Compare the provided resume against industry-specific job descriptions. Identify missing or underrepresented keywords critical for
Applicant Tracking System (ATS) optimization. Highlight essential technical skills, soft skills, and role-specific terminology.
"""

input_prompt_04 = """
Analyze this resume against the provided job description and calculate a percentage match based on skills, experience, education, 
and relevant keywords. Provide a detailed breakdown of matching and missing elements.
"""

# Handling Button Clicks
if submit_button_01:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt_01)
        st.subheader("📑 Resume Analysis")
        st.write(response)
    else:
        st.error("⚠ No file uploaded. Please upload a PDF resume.")

elif submit_button_02:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt_02)
        st.subheader("📈 Skills Improvement Suggestions")
        st.write(response)
    else:
        st.error("⚠ No file uploaded. Please upload a PDF resume.")

elif submit_button_03:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt_03)
        st.subheader("🔍 Missing Keywords for ATS Optimization")
        st.write(response)
    else:
        st.error("⚠ No file uploaded. Please upload a PDF resume.")

elif submit_button_04:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt_04)
        st.subheader("📊 Resume Match Percentage")
        st.write(response)
    else:
        st.error("⚠ No file uploaded. Please upload a PDF resume.")
