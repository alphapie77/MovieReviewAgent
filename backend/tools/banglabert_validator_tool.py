"""
BanglaBERT Validator Tool - Quality Judge for Generated Reviews
Uses Phase 2 trained model to validate review quality and persona match
"""

import sys
from pathlib import Path
from typing import Dict, Any
import torch
from pydantic import BaseModel, Field

# Add paths
sys.path.append(str(Path(__file__).parent.parent / "config"))
from base_tool import BaseTool, ToolInput, ToolOutput
import config as cfg

# Transformers imports
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F


class ValidatorInput(ToolInput):
    """Input schema for BanglaBERT Validator"""
    review_text: str = Field(description="Generated Bengali review to validate")
    expected_persona: str = Field(description="Expected persona: Die-hard Fan, Enthusiastic Casual, or Indifferent Casual")


class BanglaBERTValidatorTool(BaseTool):
    """
    BanglaBERT Validator Tool
    Validates generated reviews using Phase 2 trained model
    Returns confidence score and persona prediction
    """
    
    def __init__(self):
        super().__init__(name="BanglaBERTValidator")
        
        # Device setup
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.logger.info(f"Using device: {self.device}")
        
        # Load tokenizer
        self.logger.info("Loading BanglaBERT tokenizer...")
        try:
            # Check if local model exists
            if isinstance(cfg.BANGLABERT_MODEL, Path) and cfg.BANGLABERT_MODEL.exists():
                self.tokenizer = AutoTokenizer.from_pretrained(
                    str(cfg.BANGLABERT_MODEL),
                    local_files_only=True
                )
            else:
                # Use base model tokenizer
                self.tokenizer = AutoTokenizer.from_pretrained(cfg.BANGLABERT_TOKENIZER)
        except Exception as e:
            self.logger.warning(f"Failed to load tokenizer from model path: {e}")
            # Fallback to base model
            self.tokenizer = AutoTokenizer.from_pretrained(cfg.BANGLABERT_TOKENIZER)
        
        # Load trained model
        self.logger.info(f"Loading trained model from {cfg.BANGLABERT_MODEL}")
        
        # Check if it's a local path or HuggingFace repo
        if isinstance(cfg.BANGLABERT_MODEL, Path) and cfg.BANGLABERT_MODEL.exists():
            # Local model
            self.model = AutoModelForSequenceClassification.from_pretrained(
                str(cfg.BANGLABERT_MODEL),
                num_labels=3,
                local_files_only=True
            )
        else:
            # HuggingFace model (string path)
            model_name = str(cfg.BANGLABERT_MODEL) if not isinstance(cfg.BANGLABERT_MODEL, str) else cfg.BANGLABERT_MODEL
            
            # If it looks like a file path, use base model instead
            if '/' in model_name and not model_name.count('/') == 1:
                self.logger.warning(f"Invalid model path: {model_name}, using base model")
                model_name = "sagorsarker/bangla-bert-base"
            
            self.model = AutoModelForSequenceClassification.from_pretrained(
                model_name,
                num_labels=3
            )
        self.model.to(self.device)
        self.model.eval()
        
        # Persona mapping
        self.id_to_persona = {
            0: "Indifferent Casual",
            1: "Enthusiastic Casual",
            2: "Die-hard Fan"
        }
        self.persona_to_id = {v: k for k, v in self.id_to_persona.items()}
        
        self.logger.info("BanglaBERT Validator initialized successfully")
    
    def _clean_text(self, text: str) -> str:
        """Clean and preprocess Bengali text"""
        # Remove extra whitespace
        text = " ".join(text.split())
        cleaned = text.strip()
        
        # Debug log
        if not cleaned:
            self.logger.error(f"Text became empty after cleaning. Original length: {len(text)}")
            self.logger.error(f"Original text preview: {text[:200]}")
        
        return cleaned
    
    def _execute(self, input_data: ValidatorInput) -> ToolOutput:
        """
        Validate review and return confidence score
        """
        try:
            # Clean text
            clean_text = self._clean_text(input_data.review_text)
            
            if not clean_text:
                return ToolOutput(
                    success=False,
                    data=None,
                    error="Empty review text after cleaning"
                )
            
            # Tokenize
            inputs = self.tokenizer(
                clean_text,
                max_length=512,
                padding='max_length',
                truncation=True,
                return_tensors='pt'
            )
            
            # Move to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Get predictions
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                
                # Get probabilities
                probs = F.softmax(logits, dim=-1)
                confidence_scores = probs[0].cpu().numpy()
                
                # Get prediction
                predicted_id = torch.argmax(logits, dim=-1).item()
                predicted_persona = self.id_to_persona[predicted_id]
                predicted_confidence = float(confidence_scores[predicted_id])
            
            # Check if matches expected persona
            expected_id = self.persona_to_id.get(input_data.expected_persona)
            persona_match = (predicted_id == expected_id)
            
            # Calculate validation score (0-1)
            if persona_match:
                validation_score = predicted_confidence
            else:
                # Penalize mismatch
                validation_score = predicted_confidence * 0.5
            
            # Pass/Fail decision
            passed = validation_score >= cfg.VALIDATION_THRESHOLD
            
            # Prepare detailed results
            all_scores = {
                self.id_to_persona[i]: float(confidence_scores[i])
                for i in range(len(confidence_scores))
            }
            
            return ToolOutput(
                success=True,
                data={
                    "validation_score": float(validation_score),
                    "passed": passed,
                    "predicted_persona": predicted_persona,
                    "predicted_confidence": float(predicted_confidence),
                    "expected_persona": input_data.expected_persona,
                    "persona_match": persona_match,
                    "all_scores": all_scores,
                    "threshold": cfg.VALIDATION_THRESHOLD
                },
                metadata={
                    "review_length": len(clean_text),
                    "device": str(self.device),
                    "model_path": str(cfg.BANGLABERT_MODEL)
                }
            )
        
        except Exception as e:
            self.logger.error(f"Validation failed: {e}", exc_info=True)
            return ToolOutput(
                success=False,
                data=None,
                error=str(e)
            )
    
    def get_feedback(self, validation_result: Dict[str, Any]) -> str:
        """
        Generate human-readable feedback from validation results
        """
        if not validation_result:
            return "No validation results available."
        
        score = validation_result.get('validation_score', 0)
        passed = validation_result.get('passed', False)
        predicted = validation_result.get('predicted_persona', 'Unknown')
        expected = validation_result.get('expected_persona', 'Unknown')
        match = validation_result.get('persona_match', False)
        
        feedback = []
        
        # Overall result
        if passed:
            feedback.append(f"✓ PASSED (Score: {score:.2f})")
        else:
            feedback.append(f"✗ FAILED (Score: {score:.2f}, Threshold: {cfg.VALIDATION_THRESHOLD})")
        
        # Persona match
        if match:
            feedback.append(f"✓ Persona Match: {predicted}")
        else:
            feedback.append(f"✗ Persona Mismatch: Expected '{expected}', Got '{predicted}'")
        
        # Confidence scores
        all_scores = validation_result.get('all_scores', {})
        feedback.append("\nConfidence Scores:")
        for persona, conf in all_scores.items():
            feedback.append(f"  - {persona}: {conf:.3f}")
        
        return "\n".join(feedback)


# Test the tool
if __name__ == "__main__":
    print("=" * 60)
    print("Testing BanglaBERT Validator Tool")
    print("=" * 60)
    
    # Initialize tool
    print("\nInitializing BanglaBERT Validator...")
    tool = BanglaBERTValidatorTool()
    
    # Test reviews (you can replace with actual Bengali reviews)
    test_cases = [
        {
            "review": "এই সিনেমাটি সত্যিই অসাধারণ! অভিনয়, গল্প, গান সব কিছুই পারফেক্ট। আমি এই সিনেমা দেখে মুগ্ধ হয়ে গেছি।",
            "expected": "Die-hard Fan"
        },
        {
            "review": "সিনেমাটা ভালো ছিল। কিছু জায়গায় একটু বোরিং লাগলেও overall enjoyable।",
            "expected": "Enthusiastic Casual"
        },
        {
            "review": "তেমন কিছু না। সময় নষ্ট।",
            "expected": "Indifferent Casual"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"Test Case {i}")
        print(f"{'='*60}")
        print(f"Review: {test['review']}")
        print(f"Expected Persona: {test['expected']}")
        
        # Create input
        test_input = ValidatorInput(
            review_text=test['review'],
            expected_persona=test['expected']
        )
        
        # Run validation
        print("\nValidating...")
        output = tool.run(test_input)
        
        # Display results
        if output.success:
            print("\n" + tool.get_feedback(output.data))
        else:
            print(f"\n[ERROR] {output.error}")
    
    print("\n" + "=" * 60)
    print("BanglaBERT Validator Test Complete")
    print("=" * 60)
