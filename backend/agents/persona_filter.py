"""
Post-Processing Filter for Persona Refinement
Removes overly enthusiastic markers from Enthusiastic Casual reviews
"""

import re

# Die-hard Fan markers that should NOT appear in Enthusiastic Casual
DIE_HARD_MARKERS = [
    "অসাধারণ", "দারুণ", "অনবদ্য", "অভূতপূর্ব", "মন ছুঁয়ে গেল", 
    "মন ছুঁয়ে যায়", "একদম", "ভীষণ", "অবিশ্বাস্য", "চমৎকার"
]

# Enthusiastic Casual replacements
REPLACEMENTS = {
    "অসাধারণ": "ভালো",
    "দারুণ": "বেশ ভালো",
    "অনবদ্য": "সুন্দর",
    "অভূতপূর্ব": "ভালো",
    "মন ছুঁয়ে গেল": "ভালো লাগলো",
    "মন ছুঁয়ে যায়": "ভালো লাগে",
    "একদম": "",
    "ভীষণ": "বেশ",
    "অবিশ্বাস্য": "ভালো",
    "চমৎকার": "সুন্দর"
}

def filter_enthusiastic_casual(review_text: str) -> str:
    """
    Remove Die-hard Fan markers from Enthusiastic Casual reviews
    """
    filtered = review_text
    
    # Replace Die-hard Fan markers
    for marker, replacement in REPLACEMENTS.items():
        filtered = filtered.replace(marker, replacement)
    
    # Remove excessive exclamations (keep max 1 per sentence)
    filtered = re.sub(r'!+', '!', filtered)
    filtered = re.sub(r'([^!]{50,}?)!', r'\1।', filtered)  # Replace some ! with ।
    
    # Clean up double spaces
    filtered = re.sub(r'\s+', ' ', filtered)
    
    return filtered.strip()


if __name__ == "__main__":
    # Test
    test_review = "অসাধারণ একটা সিনেমা! দারুণ লেগেছে! মন ছুঁয়ে গেল!"
    print("Before:", test_review)
    print("After:", filter_enthusiastic_casual(test_review))
