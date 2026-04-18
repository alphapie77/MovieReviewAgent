"""
Comprehensive Test - All Persona Cases
"""

import sys
from pathlib import Path

# Add backend
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from phase3_integration import generate_review, generate_all_personas

# Test plot
test_plot = "একটি রোমান্টিক মুভি যেখানে দুই প্রেমিক বাধা পেরিয়ে মিলিত হয়। তাদের ভালোবাসা সমাজের সব বাধা ভেঙে দেয়।"

print("=" * 80)
print("COMPREHENSIVE TEST - ALL CASES")
print("=" * 80)

# Test Case 1: Die-hard Fan
print("\n[TEST 1] Die-hard Fan")
print("-" * 80)
result1 = generate_review(test_plot, "Die-hard Fan", max_retries=3)
if result1.get('success'):
    print(f"✓ Success")
    print(f"  Attempts: {result1.get('total_attempts')}")
    print(f"  Score: {result1.get('validation_score'):.3f}")
    print(f"  Predicted: {result1.get('predicted_persona')}")
    print(f"  Review Length: {len(result1.get('final_review', ''))} chars")
    print(f"  Review Preview: {result1.get('final_review', '')[:100]}...")
else:
    print(f"✗ Failed: {result1.get('error')}")

# Test Case 2: Enthusiastic Casual
print("\n[TEST 2] Enthusiastic Casual")
print("-" * 80)
result2 = generate_review(test_plot, "Enthusiastic Casual", max_retries=3)
if result2.get('success'):
    print(f"✓ Success")
    print(f"  Attempts: {result2.get('total_attempts')}")
    print(f"  Score: {result2.get('validation_score'):.3f}")
    print(f"  Predicted: {result2.get('predicted_persona')}")
    print(f"  Review Length: {len(result2.get('final_review', ''))} chars")
    print(f"  Review Preview: {result2.get('final_review', '')[:100]}...")
else:
    print(f"✗ Failed: {result2.get('error')}")

# Test Case 3: Indifferent Casual
print("\n[TEST 3] Indifferent Casual")
print("-" * 80)
result3 = generate_review(test_plot, "Indifferent Casual", max_retries=3)
if result3.get('success'):
    print(f"✓ Success")
    print(f"  Attempts: {result3.get('total_attempts')}")
    print(f"  Score: {result3.get('validation_score'):.3f}")
    print(f"  Predicted: {result3.get('predicted_persona')}")
    print(f"  Review Length: {len(result3.get('final_review', ''))} chars")
    print(f"  Review Preview: {result3.get('final_review', '')[:100]}...")
else:
    print(f"✗ Failed: {result3.get('error')}")

# Test Case 4: All 3 Personas
print("\n[TEST 4] All 3 Personas")
print("-" * 80)
result_all = generate_all_personas(test_plot, max_retries=3)
if result_all.get('success'):
    print(f"✓ Success - All personas generated")
    print(f"\nResults:")
    for persona, result in result_all.get('results', {}).items():
        if result.get('success'):
            print(f"\n  {persona}:")
            print(f"    Attempts: {result.get('total_attempts')}")
            print(f"    Score: {result.get('validation_score'):.3f}")
            print(f"    Predicted: {result.get('predicted_persona')}")
            print(f"    Review Length: {len(result.get('final_review', ''))} chars")
            print(f"    Review Preview: {result.get('final_review', '')[:80]}...")
        else:
            print(f"\n  {persona}: ✗ Failed - {result.get('error')}")
else:
    print(f"✗ Failed: {result_all.get('error')}")

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

test_results = [
    ("Die-hard Fan", result1.get('success')),
    ("Enthusiastic Casual", result2.get('success')),
    ("Indifferent Casual", result3.get('success')),
    ("All 3 Personas", result_all.get('success'))
]

passed = sum(1 for _, success in test_results if success)
total = len(test_results)

for name, success in test_results:
    status = "✓ PASS" if success else "✗ FAIL"
    print(f"{status} - {name}")

print(f"\nTotal: {passed}/{total} tests passed")

if passed == total:
    print("\n🎉 ALL TESTS PASSED!")
else:
    print(f"\n⚠️ {total - passed} test(s) failed")
