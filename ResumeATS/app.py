from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import io
from PIL import Image
import pdf2image 
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(ipnut, pdf_content, prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input, pdf_content[0],prompt])
    return response.text

def input_pdf_setup(upload_file):
    if upload_file is not None:
        images=pdf2image.convert_from_bytes(upload_file.read())

        first_page=images[0]

        img_byte_arr=io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getValue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("No File uploaded")
    
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description:", key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
#submit2 = st.button("How can I Improvise my skills")
submit3 = st.button("Percentage match")

input_prompt1= """You are an experienced Techincal Human Resource Manager in Data Science, Full stack, Web development, Big Data Engineer, Devops, Data Analyst, your task is to reviow the provided resume against the job description for these proofiles.
Please share your professional evaluation on whether the candidates profile aligns with the role Highlight strengths and weakness of the applicant in relation to the specified job requirements"""

input_prompt3="""
You are an skilled ATS scanner with a deep understanding of  Data Science, Full stack, Web development, Big Data Engineer, Devops, Data Analyst
against the provided job description. give me the percentage match if the resume matches, it should come as percentage and then keywords and last final thoughts
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please provide resume()PDF")

if submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please provide resume()PDF")




