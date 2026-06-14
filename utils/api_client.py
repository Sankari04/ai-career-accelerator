import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("WARNING: GEMINI_API_KEY is not set in the .env file.")

def generate_response(prompt, model_name="gemini-2.5-flash"):
    """
    Sends a prompt to the Gemini API and returns the generated text response.
    """
    try:
        if not API_KEY:
            return "Error: Gemini API Key is missing. Please add it to your .env file."
        
        # We use gemini-2.5-flash for fast text generation
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        
        return response.text
    except Exception as e:
        return f"An error occurred while calling the Gemini API: {e}"
