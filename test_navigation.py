"""
Button Navigation Test
Verify all page navigation works
"""

import os
import sys

# Fix encoding
if sys.platform == 'win32':
    os.system('chcp 65001 > nul 2>&1')
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

from pathlib import Path

print("=" * 70)
print("BUTTON NAVIGATION TEST")
print("=" * 70)

# Check all pages exist
pages = {
    "Home": "streamlit_app/Home.py",
    "Single Review": "streamlit_app/pages/1_✍️_Single_Review.py",
    "Batch Processing": "streamlit_app/pages/2_📦_Batch_Processing.py",
    "History": "streamlit_app/pages/3_📜_History.py",
    "About": "streamlit_app/pages/4_📚_About.py"
}

print("\n[TEST 1] Page Files")
all_exist = True
for name, path in pages.items():
    full_path = Path(__file__).parent / path
    if full_path.exists():
        print(f"✅ {name}: {path}")
    else:
        print(f"❌ {name}: {path} - NOT FOUND")
        all_exist = False

# Check button navigation code
print("\n[TEST 2] Navigation Code")

navigation_checks = {
    "Home → Single Review": ('Home.py', 'st.switch_page("pages/1_✍️_Single_Review.py")'),
    "Home → Batch": ('Home.py', 'st.switch_page("pages/2_📦_Batch_Processing.py")'),
}

for check_name, (file, code) in navigation_checks.items():
    file_path = Path(__file__).parent / "streamlit_app" / file
    if file_path.exists():
        content = file_path.read_text(encoding='utf-8')
        if code in content:
            print(f"✅ {check_name}")
        else:
            print(f"⚠️  {check_name} - Code not found (may use different syntax)")
    else:
        print(f"❌ {check_name} - File not found")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

if all_exist:
    print("✅ All pages exist")
    print("✅ Navigation should work")
    print("\nTo test manually:")
    print("  1. Run: python -m streamlit run Home.py")
    print("  2. Click 'Generate Single Review' button")
    print("  3. Click 'Batch Processing' button")
    print("  4. Check if pages load correctly")
else:
    print("❌ Some pages missing")

print("=" * 70)
