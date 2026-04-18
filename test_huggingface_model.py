"""
Test HuggingFace Model Integration
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "backend"))

from backend.phase3_integration import generate_review

# Test with proper plot
test_plot = """
শহরটার নাম নীলপুর। শান্ত, নিরিবিলি—সবাই সবাইকে চেনে। 
কিন্তু হঠাৎ করেই শহরে অদ্ভুত কিছু ঘটনা ঘটতে শুরু করে। 
রাতের বেলা মানুষজন অচেতন হয়ে পড়ে, আর সকালে উঠে দেখে তাদের স্মৃতি হারিয়ে গেছে।
কেউ মনে করতে পারে না গতকাল কী হয়েছিল। 

এই রহস্যের পেছনে কে? কী তাদের উদ্দেশ্য? 
শহরের একজন তরুণ সাংবাদিক রিয়া এই রহস্য উদঘাটনে নামে।
সে আবিষ্কার করে যে এই ঘটনার সাথে জড়িত আছে একটি পুরনো গবেষণাগার।
যেখানে একসময় মানুষের মস্তিষ্ক নিয়ে পরীক্ষা চলত।

রিয়া যত গভীরে যায়, তত বিপদ বাড়ে। 
কিন্তু সে থামে না। কারণ এই শহরের মানুষদের বাঁচাতে হবে।
শেষ পর্যন্ত সে জানতে পারে যে এই সবকিছুর পেছনে আছে একজন পাগল বিজ্ঞানী।
যে চায় মানুষের স্মৃতি মুছে দিয়ে একটি নতুন সমাজ তৈরি করতে।

রিয়া কি পারবে তাকে থামাতে? নাকি পুরো শহর হারিয়ে যাবে অন্ধকারে?
"""

print("=" * 70)
print("Testing HuggingFace Model Integration")
print("=" * 70)

print("\n" + "=" * 70)
print("Generating review for: Die-hard Fan")
print("=" * 70)

result = generate_review(
    movie_plot=test_plot,
    target_persona="Die-hard Fan"
)

print("\n" + "=" * 70)
print("RESULT")
print("=" * 70)
print(f"Success: {result['success']}")
print(f"Score: {result['validation_score']:.3f}")
print(f"Attempts: {result['attempts']}")
print(f"\nReview generated successfully!")

if not result['success']:
    print(f"\nError: {result.get('error', 'Unknown error')}")

print("\n" + "=" * 70)
print("Test Complete!")
print("=" * 70)
