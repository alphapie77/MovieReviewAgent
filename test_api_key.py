"""Quick API Key Test"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Fix Windows encoding
sys.stdout.reconfigure(encoding='utf-8')

# Load .env
env_path = Path(__file__).parent / ".env"
if not env_path.exists():
    env_path = Path(__file__).parent.parent / "03_Phase3_MultiAgent" / ".env"

load_dotenv(env_path)
print(f"Loading from: {env_path}")

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key or api_key == "your_google_api_key_here":
    print("❌ API key not found or not set")
    exit(1)

print(f"✓ API key found: {api_key[:20]}...")

# Test with Gemini
try:
    import google.generativeai as genai
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    
    print("\n🔄 Testing API connection...")
    response = model.generate_content("Say 'Hello' in Bengali")
    
    print(f"✓ API is working!")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"❌ API test failed: {e}")
    exit(1)

print("\n✅ API key is valid and working!")
