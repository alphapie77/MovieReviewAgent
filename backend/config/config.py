"""
Configuration Management for Phase 3 Multi-Agent System
Handles API keys, file paths, and system settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project Root
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Phase 1 & 2 Artifacts
DATA_DIR = PROJECT_ROOT / "02_Phase1_DataEngineering" / "THESIS_PHASE1_BACKUP"
MODEL_DIR = PROJECT_ROOT / "03_Phase2_ModelTraining"

# Key Files
CSV_FILE = DATA_DIR / "step3_clustered_data.csv"
BANGLABERT_MODEL = MODEL_DIR / "THESIS_ADVANCED_MODEL_ONLY" / "best_advanced_model"

# Phase 3 Directories
PHASE3_ROOT = PROJECT_ROOT / "03_Phase3_MultiAgent"
LOGS_DIR = PHASE3_ROOT / "logs"
TOOLS_DIR = PHASE3_ROOT / "tools"
CONFIG_DIR = PHASE3_ROOT / "config"
TESTS_DIR = PHASE3_ROOT / "tests"

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Model Configuration
GEMINI_MODEL = "gemini-3.1-flash-lite-preview"
BANGLABERT_TOKENIZER = "sagorsarker/bangla-bert-base"

# Agent Configuration
MAX_RETRIES = 3
VALIDATION_THRESHOLD = 0.7
TOP_K_EXAMPLES = 10  # Increased from 5 for better context

# Persona-specific thresholds (research-based adjustment)
PERSONA_THRESHOLDS = {
    "Die-hard Fan": 0.7,
    "Enthusiastic Casual": 0.45,  # Further lowered due to persistent issues
    "Indifferent Casual": 0.6
}

# Generation parameters
GENERATION_CONFIG = {
    "temperature": 0.9,  # Balanced: creative but controlled
    "top_p": 0.92,
    "top_k": 40
}

# Persona Types with enhanced prompting
PERSONAS = {
    "Die-hard Fan": {
        "cluster": 2,
        "sentiment_range": (3.5, 5.0),
        "characteristics": "High engagement, emotional, detailed",
        "style_markers": [
            "অসাধারণ", "দারুণ", "মন ছুঁয়ে গেল", "অভূতপূর্ব", "অনবদ্য",
            "একেবারে মুগ্ধ", "অসম্ভব সুন্দর", "জীবনের সেরা"
        ],
        "tone": "Extremely enthusiastic, uses many exclamations, superlatives, emotional expressions"
    },
    "Enthusiastic Casual": {
        "cluster": 1,
        "sentiment_range": (2.5, 3.5),
        "characteristics": "Moderate engagement, balanced",
        "style_markers": [
            "ভালো লাগলো", "বেশ ভালো", "মন্দ না", "ভালো ছিল",
            "তবে", "কিন্তু", "একটু", "মোটামুটি"
        ],
        "tone": "Positive but measured, mentions both strengths and minor weaknesses, balanced perspective"
    },
    "Indifferent Casual": {
        "cluster": 0,
        "sentiment_range": (1.0, 3.0),
        "characteristics": "Low engagement, brief, critical",
        "style_markers": [
            "সাধারণ", "তেমন কিছু না", "বিরক্তিকর", "সময় নষ্ট",
            "খারাপ", "দুর্বল", "হতাশ"
        ],
        "tone": "Brief, critical, focuses on negatives, minimal enthusiasm, short sentences"
    }
}


def validate_setup() -> bool:
    """Validate that all required files and configurations exist"""
    checks = {
        "CSV File": CSV_FILE.exists(),
        "BanglaBERT Model": BANGLABERT_MODEL.exists(),
        "Google API Key": bool(GOOGLE_API_KEY),
        "Logs Directory": LOGS_DIR.exists(),
    }
    
    print("🔍 Configuration Validation:")
    all_valid = True
    for name, status in checks.items():
        symbol = "✅" if status else "❌"
        print(f"  {symbol} {name}")
        if not status:
            all_valid = False
    
    return all_valid


if __name__ == "__main__":
    print("📋 Phase 3 Configuration:")
    print(f"  Project Root: {PROJECT_ROOT}")
    print(f"  CSV File: {CSV_FILE}")
    print(f"  Model Path: {BANGLABERT_MODEL}")
    print(f"  API Key Set: {'Yes' if GOOGLE_API_KEY else 'No'}")
    print()
    validate_setup()
