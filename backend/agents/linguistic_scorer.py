"""
Linguistic Feature Scorer for Hybrid Validation
Counts persona-specific style markers in Bengali reviews
"""

import re
from typing import Dict, Tuple

# Persona-specific style markers
PERSONA_MARKERS = {
    "Die-hard Fan": {
        "positive": [
            "অসাধারণ", "দারুণ", "অনবদ্য", "অভূতপূর্ব", "মন ছুঁয়ে গেল", 
            "মন ছুঁয়ে যায়", "একদম", "ভীষণ", "অবিশ্বাস্য", "চমৎকার",
            "অপূর্ব", "মুগ্ধ", "জীবনের সেরা", "হৃদয় ছুঁয়ে", "প্রাণ জুড়িয়ে"
        ],
        "weight": 1.0
    },
    "Enthusiastic Casual": {
        "positive": [
            "ভালো লাগলো", "বেশ ভালো", "ভালো", "সুন্দর", "মন্দ না", 
            "ভালো ছিল", "মিষ্টি", "চমৎকার ছিল", "দেখার মতো"
        ],
        "balanced": ["তবে", "কিন্তু", "একটু", "মোটামুটি", "যদিও"],
        "weight": 1.0
    },
    "Indifferent Casual": {
        "negative": [
            "সাধারণ", "তেমন কিছু না", "খারাপ", "বিরক্তিকর", "সময় নষ্ট",
            "দুর্বল", "হতাশ", "বাজে", "নিম্নমানের", "একঘেয়ে"
        ],
        "weight": 1.0
    }
}


def count_markers(text: str, markers: list) -> int:
    """Count occurrences of markers in text"""
    count = 0
    for marker in markers:
        count += len(re.findall(re.escape(marker), text))
    return count


def calculate_linguistic_score(review_text: str) -> Dict[str, float]:
    """
    Calculate linguistic feature scores for each persona
    
    Returns:
        Dict with persona names as keys and scores as values
    """
    scores = {}
    
    # Die-hard Fan score
    die_hard_positive = count_markers(review_text, PERSONA_MARKERS["Die-hard Fan"]["positive"])
    scores["Die-hard Fan"] = min(die_hard_positive / 3.0, 1.0)  # Normalize to 0-1
    
    # Enthusiastic Casual score
    enthusiastic_positive = count_markers(review_text, PERSONA_MARKERS["Enthusiastic Casual"]["positive"])
    enthusiastic_balanced = count_markers(review_text, PERSONA_MARKERS["Enthusiastic Casual"]["balanced"])
    
    # Enthusiastic Casual needs both positive AND balanced markers
    if enthusiastic_positive > 0 and enthusiastic_balanced > 0:
        scores["Enthusiastic Casual"] = min((enthusiastic_positive + enthusiastic_balanced) / 4.0, 1.0)
    else:
        scores["Enthusiastic Casual"] = min(enthusiastic_positive / 5.0, 0.5)  # Penalty if no balance
    
    # Indifferent Casual score
    indifferent_negative = count_markers(review_text, PERSONA_MARKERS["Indifferent Casual"]["negative"])
    scores["Indifferent Casual"] = min(indifferent_negative / 2.0, 1.0)
    
    return scores


def get_linguistic_prediction(review_text: str) -> Tuple[str, float, Dict[str, float]]:
    """
    Get persona prediction based on linguistic features
    
    Returns:
        Tuple of (predicted_persona, confidence, all_scores)
    """
    scores = calculate_linguistic_score(review_text)
    
    # Get prediction
    predicted_persona = max(scores, key=scores.get)
    confidence = scores[predicted_persona]
    
    return predicted_persona, confidence, scores


def hybrid_validation(
    review_text: str,
    banglabert_persona: str,
    banglabert_score: float,
    target_persona: str,
    neural_weight: float = 0.6,
    linguistic_weight: float = 0.4
) -> Dict[str, any]:
    """
    Combine BanglaBERT neural score with linguistic features
    
    Args:
        review_text: The generated review
        banglabert_persona: BanglaBERT's prediction
        banglabert_score: BanglaBERT's confidence
        target_persona: Expected persona
        neural_weight: Weight for neural score (default 0.6)
        linguistic_weight: Weight for linguistic score (default 0.4)
    
    Returns:
        Dict with hybrid prediction and scores
    """
    # Get linguistic scores
    ling_persona, ling_confidence, ling_scores = get_linguistic_prediction(review_text)
    
    # Calculate hybrid scores for each persona
    hybrid_scores = {}
    personas = ["Die-hard Fan", "Enthusiastic Casual", "Indifferent Casual"]
    
    for persona in personas:
        # BanglaBERT score for this persona (1.0 if predicted, else lower)
        neural_score = banglabert_score if banglabert_persona == persona else 0.3
        
        # Linguistic score for this persona
        linguistic_score = ling_scores.get(persona, 0.0)
        
        # Weighted combination
        hybrid_scores[persona] = (neural_weight * neural_score) + (linguistic_weight * linguistic_score)
    
    # Get final prediction
    final_persona = max(hybrid_scores, key=hybrid_scores.get)
    final_score = hybrid_scores[final_persona]
    
    # Check if matches target
    matches_target = (final_persona == target_persona)
    
    return {
        "predicted_persona": final_persona,
        "confidence": final_score,
        "matches_target": matches_target,
        "hybrid_scores": hybrid_scores,
        "banglabert_prediction": banglabert_persona,
        "banglabert_score": banglabert_score,
        "linguistic_prediction": ling_persona,
        "linguistic_confidence": ling_confidence,
        "linguistic_scores": ling_scores
    }


if __name__ == "__main__":
    # Test
    test_reviews = {
        "Die-hard Fan": "অসাধারণ! দারুণ! মন ছুঁয়ে গেল! একদম অনবদ্য!",
        "Enthusiastic Casual": "বেশ ভালো লাগলো। সুন্দর ছিল। তবে একটু ধীর।",
        "Indifferent Casual": "সাধারণ। তেমন কিছু না। খারাপ লাগলো।"
    }
    
    for persona, review in test_reviews.items():
        print(f"\n{persona}:")
        print(f"Review: {review}")
        pred, conf, scores = get_linguistic_prediction(review)
        print(f"Predicted: {pred} (confidence: {conf:.2f})")
        print(f"Scores: {scores}")
