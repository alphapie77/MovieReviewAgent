"""List Available Gemini Models"""

import sys
from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

api_key = os.getenv("GOOGLE_API_KEY")

print("Checking available Gemini models...")
print(f"API Key: {api_key[:20]}...\n")

try:
    import google.generativeai as genai
    
    genai.configure(api_key=api_key)
    
    print("Available models that support generateContent:\n")
    
    models = genai.list_models()
    found = False
    
    for m in models:
        if 'generateContent' in m.supported_generation_methods:
            print(f"  - {m.name}")
            found = True
    
    if not found:
        print("  No models found (API issue or quota)")
        
except Exception as e:
    print(f"ERROR: {e}")
