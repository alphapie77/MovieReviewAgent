"""
Download BanglaBERT model on first run
"""
import os
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def download_model():
    """Download trained BanglaBERT model from HuggingFace Hub"""
    model_path = Path(__file__).parent / "models" / "best_advanced_model"
    
    if not model_path.exists():
        print("Downloading trained BanglaBERT model from HuggingFace Hub...")
        model_path.mkdir(parents=True, exist_ok=True)
        
        # Download trained model from HuggingFace Hub
        model_name = "shksabbir7/bengali-movie-review-classifier"
        
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=3
        )
        
        # Save locally
        tokenizer.save_pretrained(model_path)
        model.save_pretrained(model_path)
        
        print("Model downloaded successfully!")
    else:
        print("Model already exists")

if __name__ == "__main__":
    download_model()
