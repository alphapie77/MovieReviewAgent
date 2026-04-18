"""Test gemini-3.1-flash-live-preview"""

import sys
from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

api_key = os.getenv("GOOGLE_API_KEY")

print("Testing gemini-3.1-flash-lite-preview...")
print(f"API Key: {api_key[:20]}...\n")

try:
    import google.generativeai as genai
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3.1-flash-lite-preview')
    
    print("Sending test request...")
    response = model.generate_content("Say hello in Bengali")
    
    print(f"\nSUCCESS! Model works!")
    print(f"Response: {response.text}")
    
except Exception as e:
    error_msg = str(e)
    if '404' in error_msg:
        print(f"\nMODEL NOT FOUND: gemini-3.1-flash-live-preview does not exist")
    elif '429' in error_msg or 'quota' in error_msg.lower():
        print(f"\nQUOTA EXCEEDED")
    else:
        print(f"\nERROR: {error_msg[:200]}")
