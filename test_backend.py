"""
Test Phase 3 Backend Integration
Quick validation before running Streamlit
"""

import sys
import os
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    os.system('chcp 65001 > nul 2>&1')
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from phase3_integration import generate_review

print("=" * 70)
print("Testing Phase 3 Backend Integration")
print("=" * 70)

# Test plot
test_plot = "একটি রোমান্টিক মুভি যেখানে দুই প্রেমিক মিলিত হয়"
test_persona = "Die-hard Fan"

print(f"\nPlot: {test_plot}")
print(f"Persona: {test_persona}")
print("\nGenerating review...\n")

try:
    result = generate_review(test_plot, test_persona, max_retries=1)
    
    print("=" * 70)
    print("RESULT")
    print("=" * 70)
    print(f"Success: {result.get('success', False)}")
    print(f"Score: {result.get('validation_score', 0):.3f}")
    print(f"Review: {result.get('final_review', 'N/A')[:100]}...")
    
    if result.get('error'):
        print(f"\nError: {result['error']}")
    
    print("\n✅ Backend integration working!")
    
except Exception as e:
    print(f"\n❌ Backend integration failed: {e}")
    import traceback
    traceback.print_exc()
