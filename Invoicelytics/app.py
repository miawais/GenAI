from dotenv import load_dotenv
import os
from PIL import Image
import google.generativeai as genai
from flask import Flask, request, render_template, jsonify

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro')


def get_gemini_response(input_text, image, prompt):
    response = model.generate_content([input_text, image[0], prompt])
    return response.text


def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.read()
        image_parts = [
            {
                "mime_type": uploaded_file.content_type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("File not found")


app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route('/')
def home():
    return render_template('index.html', response='')


@app.route('/explain_invoice', methods=['POST'])
def explain_invoice():
    input_prompt = request.form['inputPrompt']
    uploaded_file = request.files['imageUpload']

    if uploaded_file is not None:
        image_data = input_image_details(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, "")
        return jsonify({"response": response})
    else:
        return jsonify({"error": "No image provided"}), 400


if __name__ == '__main__':
    app.run(debug=True)