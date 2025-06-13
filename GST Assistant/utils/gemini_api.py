import google.generativeai as genai
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def configure_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found in environment variables. "
            "Please create a .env file with your Gemini API key: GEMINI_API_KEY=your_api_key_here"
        )
    genai.configure(api_key=api_key)

def ask_gemini(prompt):
    try:
        configure_gemini()
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error calling Gemini API: {str(e)}")
        return None
