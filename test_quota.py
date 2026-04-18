"""Test Gemini 2.0 Flash Quota"""

import sys
from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

api_key = os.getenv("GOOGLE_API_KEY")

print("Testing Gemini 2.0 Flash Exp quota...")
print(f"API Key: {api_key[:20]}...")

try:
    import google.generativeai as genai
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    print("\nSending test request...")
    response = model.generate_content("Say hello in Bengali")
    
    print(f"\nSUCCESS! Quota available.")
    print(f"Response: {response.text}")
    
except Exception as e:
    error_msg = str(e)
    if '429' in error_msg or 'quota' in error_msg.lower():
        print(f"\nQUOTA EXCEEDED for gemini-2.0-flash-exp")
        print("Need to wait or use different API key")
    else:
        print(f"\nERROR: {error_msg}")
