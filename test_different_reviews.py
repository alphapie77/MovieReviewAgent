"""
Debug Test - Check if reviews are different
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from phase3_integration import generate_review

test_plot = "একটি রোমান্টিক মুভি যেখানে দুই প্রেমিক বাধা পেরিয়ে মিলিত হয়।"

print("="*80)
print("TESTING IF REVIEWS ARE DIFFERENT")
print("="*80)

# Generate 3 reviews
print("\n[1] Generating Die-hard Fan review...")
result1 = generate_review(test_plot, "Die-hard Fan", 3)

print("\n[2] Generating Enthusiastic Casual review...")
result2 = generate_review(test_plot, "Enthusiastic Casual", 3)

print("\n[3] Generating Indifferent Casual review...")
result3 = generate_review(test_plot, "Indifferent Casual", 3)

# Compare
print("\n" + "="*80)
print("RESULTS")
print("="*80)

if result1.get('success'):
    review1 = result1.get('final_review', '')
    print(f"\nDie-hard Fan ({len(review1)} chars):")
    print(review1[:150] + "...")
else:
    print(f"\nDie-hard Fan: FAILED - {result1.get('error')}")
    review1 = ""

if result2.get('success'):
    review2 = result2.get('final_review', '')
    print(f"\nEnthusiastic Casual ({len(review2)} chars):")
    print(review2[:150] + "...")
else:
    print(f"\nEnthusiastic Casual: FAILED - {result2.get('error')}")
    review2 = ""

if result3.get('success'):
    review3 = result3.get('final_review', '')
    print(f"\nIndifferent Casual ({len(review3)} chars):")
    print(review3[:150] + "...")
else:
    print(f"\nIndifferent Casual: FAILED - {result3.get('error')}")
    review3 = ""

# Check if different
print("\n" + "="*80)
print("COMPARISON")
print("="*80)

if review1 and review2 and review3:
    if review1 == review2 == review3:
        print("\nWARNING: All reviews are IDENTICAL!")
        print("This should NOT happen!")
    elif review1 == review2:
        print("\nWARNING: Die-hard Fan and Enthusiastic Casual are SAME!")
    elif review2 == review3:
        print("\nWARNING: Enthusiastic Casual and Indifferent Casual are SAME!")
    elif review1 == review3:
        print("\nWARNING: Die-hard Fan and Indifferent Casual are SAME!")
    else:
        print("\nSUCCESS: All 3 reviews are DIFFERENT!")
        print(f"  Review 1 length: {len(review1)}")
        print(f"  Review 2 length: {len(review2)}")
        print(f"  Review 3 length: {len(review3)}")
else:
    print("\nCannot compare - some reviews failed to generate")
