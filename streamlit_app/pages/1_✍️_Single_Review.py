"""
Single Review Generation Page
Modern UI with complete error handling
"""

import streamlit as st
import sys
from pathlib import Path
import json
from datetime import datetime

# Add backend
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "backend"))

# Import shared theme
sys.path.insert(0, str(Path(__file__).parent.parent))
from shared_theme import SHARED_CSS

# Import database
sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))
from database import get_db

# Page config
st.set_page_config(page_title="Single Review", page_icon="✍️", layout="wide")

# Apply shared theme
st.markdown(SHARED_CSS, unsafe_allow_html=True)

# Initialize session
if 'history' not in st.session_state:
    st.session_state.history = []
if 'total_generated' not in st.session_state:
    st.session_state.total_generated = 0
if 'user_id' not in st.session_state:
    import uuid
    st.session_state.user_id = str(uuid.uuid4())

# Initialize database
db = get_db()
db.create_user(st.session_state.user_id)

# Header
st.markdown("""
<div class="header-gradient">
    <h1>✍️ Single Review Generation</h1>
    <p>Generate persona-specific Bengali movie review</p>
</div>
""", unsafe_allow_html=True)

# Input Section
st.markdown("## 📝 Input")

# Example plots dictionary (200+ words each)
examples = {
    "Romantic": """কলকাতার একটি পুরনো পাড়ায় থাকে অর্ণব আর তানিয়া। দুজনেই শৈশব থেকে একসাথে বড় হয়েছে। তাদের বাড়ি পাশাপাশি, স্কুল একই, এমনকি প্রিয় খাবারও একই। অর্ণব একজন সংগীতশিল্পী, স্বপ্ন দেখে বড় মঞ্চে গান গাওয়ার। প্রতিদিন সন্ধ্যায় সে ছাদে বসে গিটার বাজায়। তানিয়া একজন চিত্রশিল্পী, তার ছবিতে ফুটে ওঠে জীবনের রঙ। সে প্রায়ই অর্ণবের গান শুনতে শুনতে ছবি আঁকে। দুজনের মধ্যে ভালোবাসা জন্মায় কিন্তু কেউ কাউকে বলতে পারে না। তারা ভয় পায় যে এই স্বীকারোক্তি তাদের বন্ধুত্ব নষ্ট করে দেবে। একদিন অর্ণবের বাবা তাকে বিদেশে পাঠাতে চান উচ্চশিক্ষার জন্য। লন্ডনের একটি বিখ্যাত মিউজিক একাডেমিতে তার ভর্তির সুযোগ এসেছে। অর্ণব দ্বিধায় পড়ে যায়। সে তানিয়াকে ছেড়ে যেতে চায় না কিন্তু বাবার স্বপ্নও ভাঙতে চায় না। সে রাতের পর রাত ঘুমাতে পারে না। তানিয়া যখন এই খবর শুনে, সে অর্ণবকে উৎসাহ দেয় যেতে। সে বলে, "তোমার স্বপ্ন পূরণ করো, আমি অপেক্ষা করব। তুমি ফিরে এলে আমরা আবার একসাথে থাকব।" অর্ণব কাঁদতে কাঁদতে বিদেশে চলে যায়। তিন বছর পর সে ফিরে আসে একজন সফল সংগীতশিল্পী হয়ে। তার গান এখন সবাই শোনে। কিন্তু ফিরে এসে সে শুনে তানিয়ার বিয়ে ঠিক হয়ে গেছে পরিবারের চাপে। তানিয়ার বাবা-মা চান তাদের মেয়ে একজন ডাক্তার বা ইঞ্জিনিয়ারকে বিয়ে করুক। অর্ণব সম্পূর্ণ ভেঙে পড়ে। তার সব সাফল্য মনে হয় অর্থহীন। সে তানিয়ার সাথে দেখা করে এবং প্রথমবারের মতো তার মনের কথা বলে। সে বলে, "আমি তোমাকে ভালোবাসি, সবসময় ভালোবেসেছি।" তানিয়াও কাঁদতে কাঁদতে স্বীকার করে যে সে এখনও অর্ণবকে ভালোবাসে। সে বলে, "আমি শুধু তোমার জন্যই অপেক্ষা করেছি।" দুজনে মিলে পরিবারকে বোঝায়। প্রথমে পরিবার রাজি হয় না। অনেক তর্ক-বিতর্ক হয়। কিন্তু অর্ণব তার সংগীত দিয়ে, তানিয়া তার শিল্প দিয়ে প্রমাণ করে যে তারা একসাথে থাকলে আরও ভালো কিছু সৃষ্টি করতে পারবে। অনেক বাধা পেরিয়ে অবশেষে তাদের ভালোবাসা জয়ী হয়। শেষে দুজনে একসাথে নতুন জীবন শুরু করে, যেখানে আছে সংগীত, শিল্প আর অসীম ভালোবাসা। তারা একটি ছোট্ট স্টুডিও খোলে যেখানে অর্ণব গান শেখায় আর তানিয়া ছবি আঁকা শেখায়।""",
    
    "Thriller": """শহরটার নাম নীলপুর। একটি শান্ত, নিরিবিলি শহর যেখানে সবাই সবাইকে চেনে। মানুষজন সরল, জীবনযাত্রা সহজ। কিন্তু হঠাৎ করেই শহরে অদ্ভুত কিছু ঘটনা ঘটতে শুরু করে। রাতের বেলা মানুষজন অচেতন হয়ে পড়ে যাচ্ছে। সকালে উঠে তারা কিছুই মনে করতে পারছে না। প্রথমে একজন, তারপর দুজন, এভাবে প্রতিদিন আক্রান্তের সংখ্যা বাড়ছে। শহরের মানুষ আতঙ্কিত। কেউ রাতে ঘুমাতে সাহস পাচ্ছে না। শহরের একজন তরুণ সাংবাদিক রাহুল এই রহস্যের সমাধান খুঁজতে শুরু করে। সে প্রতিটি আক্রান্ত ব্যক্তির সাথে কথা বলে। সে লক্ষ্য করে যে সবাই একই এলাকায় থাকে। সে আবিষ্কার করে যে শহরের পুরনো একটি বাড়িতে কিছু অদ্ভুত শব্দ শোনা যায়। রাহুল যখন সেই বাড়িতে যায়, সে দেখে একটি পুরনো ডায়েরি। ডায়েরিটি ধুলোয় ঢাকা, পাতাগুলো হলুদ হয়ে গেছে। ডায়েরিতে লেখা আছে যে ৫০ বছর আগে এই শহরে একই ঘটনা ঘটেছিল। তখন একজন বিজ্ঞানী ডক্টর সেনগুপ্ত একটি পরীক্ষা করছিলেন যা ভুল হয়ে গিয়েছিল। তিনি মানুষের মস্তিষ্কের তরঙ্গ নিয়ে গবেষণা করছিলেন। রাহুল বুঝতে পারে যে সেই পরীক্ষার প্রভাব এখনও রয়ে গেছে। সে শহরের একজন পুরনো অধ্যাপকের সাথে দেখা করে যিনি সেই বিজ্ঞানীর ছাত্র ছিলেন। অধ্যাপক তাকে বলেন যে সেই পরীক্ষাটি ছিল মানুষের মস্তিষ্কের তরঙ্গ নিয়ে। একটি যন্ত্র তৈরি করা হয়েছিল যা মস্তিষ্কের তরঙ্গকে প্রভাবিত করতে পারে। কিন্তু পরীক্ষা ব্যর্থ হয় এবং ডক্টর সেনগুপ্ত সেই যন্ত্র লুকিয়ে রাখেন। রাহুল এবং অধ্যাপক মিলে সেই পুরনো ল্যাবরেটরি খুঁজে বের করেন। সেখানে গিয়ে তারা দেখেন একটি যন্ত্র এখনও চালু আছে। যন্ত্রটি থেকে একটি অদৃশ্য তরঙ্গ বের হচ্ছে। তারা সাবধানে সেই যন্ত্র বন্ধ করে দেন। এরপর থেকে শহরে আর কোনো অদ্ভুত ঘটনা ঘটে না। রাহুল তার রিপোর্ট প্রকাশ করে এবং পুরো দেশে সাড়া পড়ে যায়। নীলপুর আবার শান্ত শহরে পরিণত হয়। মানুষ আবার নিশ্চিন্তে ঘুমাতে পারে।""",
    
    "Action": """রাজু একজন সাধারণ ট্যাক্সি ড্রাইভার যে কলকাতার রাস্তায় গাড়ি চালায়। তার একটি ছোট্ট পরিবার আছে - স্ত্রী মীনা এবং একটি আট বছরের মেয়ে পিয়া। রাজু প্রতিদিন সকাল থেকে রাত পর্যন্ত কাজ করে তার পরিবারের জন্য। সে একজন সৎ এবং পরিশ্রমী মানুষ। একদিন রাজু তার ট্যাক্সিতে একজন যাত্রী তুলে নেয়। সেই যাত্রী আসলে একজন সাক্ষী যে একটি বড় অপরাধ দেখে ফেলেছে। সে দেখেছে কিভাবে একটি বড় মাফিয়া চক্র একজন সৎ পুলিশ অফিসারকে হত্যা করেছে। হঠাৎ করে কিছু সশস্ত্র লোক রাজুর গাড়ি আক্রমণ করে। তারা সেই সাক্ষীকে মেরে ফেলতে চায়। রাজু তার ড্রাইভিং দক্ষতা দিয়ে তাদের থেকে পালাতে সক্ষম হয়। সে সরু গলি দিয়ে, ভিড়ের মধ্যে দিয়ে গাড়ি চালিয়ে পালায়। কিন্তু এরপর থেকে সেই অপরাধী চক্র রাজুর পরিবারকে টার্গেট করে। তারা রাজুকে হুমকি দেয় যে সে যদি পুলিশে যায় তাহলে তার পরিবারকে মেরে ফেলবে। একদিন তারা রাজুর মেয়ে পিয়াকে স্কুল থেকে অপহরণ করে নেয়। রাজু পাগলের মতো হয়ে যায়। সে পুলিশের কাছে যায় কিন্তু পুলিশও সেই অপরাধী চক্রের ভয়ে কিছু করতে পারে না। সেই মাফিয়া চক্রের নেতা হলো শংকর, যে পুরো শহরে ত্রাসের রাজত্ব চালায়। রাজু তখন নিজেই সিদ্ধান্ত নেয় তার মেয়েকে উদ্ধার করার। সে তার পুরনো বন্ধুদের সাহায্য নেয় যারা সেনাবাহিনীতে ছিল। তারা জানায় যে রাজু নিজেও আগে সেনাবাহিনীতে ছিল কিন্তু পরিবারের জন্য চাকরি ছেড়ে দিয়েছিল। তারা একসাথে একটি পরিকল্পনা করে। রাজু সেই অপরাধীদের আড্ডায় ঢুকে পড়ে। সেখানে তীব্র লড়াই হয়। রাজু তার সামরিক প্রশিক্ষণ ব্যবহার করে। সে তার সাহস এবং বুদ্ধি দিয়ে একে একে সব অপরাধীকে পরাজিত করে। শেষ লড়াইটা হয় শংকরের সাথে। দীর্ঘ লড়াইয়ের পর রাজু শংকরকে পরাজিত করে। অবশেষে সে তার মেয়েকে উদ্ধার করে। পুলিশ এসে সব অপরাধীকে গ্রেফতার করে। রাজু আবার তার সাধারণ জীবনে ফিরে যায় কিন্তু এবার সে একজন হিরো হিসেবে সবার কাছে পরিচিত। শহরের মানুষ তাকে সম্মান করে।"""
}

# Example buttons - Show examples as info boxes instead
with st.expander("📋 Example Plots - Copy and Paste"):
    st.info("**📖 Romantic:**\n" + examples["Romantic"])
    st.info("**🔍 Thriller:**\n" + examples["Thriller"])
    st.info("**💥 Action:**\n" + examples["Action"])

# Movie plot input - simple text area without value binding
movie_plot = st.text_area(
    "Movie Plot (Bengali/Banglish)",
    height=150,
    placeholder="উদাহরণ: একটি রোমান্টিক মুভি যেখানে দুই প্রেমিক মিলিত হয়...\n\nঅথবা: ekta romantic movie jekhane duijon premik mile jay...\n\nTip: Copy example from above and paste here!",
    help="Enter movie plot in Bengali or Banglish. Minimum 20 characters required.",
    key="movie_plot_input"
)

col1, col2 = st.columns(2)

with col1:
    persona = st.selectbox(
        "Select Persona",
        ["All 3 Personas", "Die-hard Fan", "Enthusiastic Casual", "Indifferent Casual"],
        help="Choose the target persona for review generation"
    )

with col2:
    max_retries = st.slider(
        "Max Retries",
        min_value=1,
        max_value=5,
        value=3,
        help="Maximum retry attempts if validation fails"
    )

# Advanced options
with st.expander("⚙️ Advanced Options"):
    show_logs = st.checkbox("Show detailed logs", value=False)
    save_to_history = st.checkbox("Save to history", value=True)

st.markdown("---")

# Generate button
if st.button("🚀 Generate Review", type="primary", use_container_width=True):
    
    # Validation - minimum 200 words
    if not movie_plot or len(movie_plot.strip()) < 20:
        st.markdown("""
        <div class="error-box">
            <strong>❌ Error:</strong> Movie plot is too short. Please enter at least 20 characters.
        </div>
        """, unsafe_allow_html=True)
    else:
        # Count words
        word_count = len(movie_plot.split())
        if word_count < 200:
            st.markdown(f"""
            <div class="error-box">
                <strong>❌ Plot Too Short:</strong> Your plot has only {word_count} words.<br>
                <strong>Minimum required: 200 words</strong> for professional review generation.<br><br>
                💡 <strong>Why?</strong> Short plots lead to generic reviews with hallucinated details. 
                A detailed plot (200+ words) ensures the AI generates accurate, plot-specific reviews.
            </div>
            """, unsafe_allow_html=True)
        else:
            # Progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Initialize
                status_text.markdown("**Step 1/4:** Initializing agents...")
                progress_bar.progress(25)
                
                from phase3_integration import generate_review, generate_all_personas
                
                # Step 2: Generate
                if persona == "All 3 Personas":
                    status_text.markdown(f"**Step 2/4:** Generating reviews for **all 3 personas**...")
                    progress_bar.progress(50)
                    
                    result = generate_all_personas(movie_plot, max_retries)
                    
                    # Step 3: Validate
                    status_text.markdown("**Step 3/4:** Validating outputs...")
                    progress_bar.progress(75)
                    
                    # Step 4: Complete
                    status_text.markdown("**Step 4/4:** Finalizing...")
                    progress_bar.progress(100)
                    
                    # Clear progress
                    progress_bar.empty()
                    status_text.empty()
                    
                    # Check result
                    if result.get('success'):
                        # Success
                        st.markdown("""
                        <div class="success-box">
                            <strong>✅ Success!</strong> All 3 persona reviews generated successfully.
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Overall Metrics
                        st.markdown("## 📊 Overall Metrics")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            total_attempts = sum(r.get('total_attempts', 0) for r in result.get('results', {}).values())
                            st.markdown(f"""
                            <div class="metric-box">
                                <h3>{total_attempts}</h3>
                                <p>Total Attempts</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            avg_score = sum(r.get('validation_score', 0) for r in result.get('results', {}).values()) / 3
                            st.markdown(f"""
                            <div class="metric-box">
                                <h3>{avg_score:.3f}</h3>
                                <p>Avg Score</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col3:
                            success_count = sum(1 for r in result.get('results', {}).values() if r.get('success'))
                            st.markdown(f"""
                            <div class="metric-box">
                                <h3>{success_count}/3</h3>
                                <p>Success</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col4:
                            total_chars = sum(len(r.get('final_review', '')) for r in result.get('results', {}).values())
                            st.markdown(f"""
                            <div class="metric-box">
                                <h3>{total_chars}</h3>
                                <p>Total Chars</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Individual Reviews
                        st.markdown("## 📝 Generated Reviews")
                        
                        for persona_name, persona_result in result.get('results', {}).items():
                            if persona_result.get('success'):
                                score = persona_result.get('validation_score', 0)
                                review = persona_result.get('final_review', '')
                                attempts = persona_result.get('total_attempts', 0)
                                
                                st.markdown(f"""
                                <div class="result-card">
                                    <h3>{persona_name}</h3>
                                    <p><strong>Score:</strong> {score:.3f} | <strong>Attempts:</strong> {attempts}</p>
                                    <p style="font-size: 1.1rem; line-height: 1.8; margin-top: 1rem;">{review}</p>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        # Download
                        st.markdown("## 💾 Download")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            json_data = json.dumps(result, ensure_ascii=False, indent=2)
                            st.download_button(
                                "📥 Download JSON",
                                json_data,
                                f"all_reviews_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                "application/json",
                                use_container_width=True
                            )
                        
                        with col2:
                            txt_data = "\n\n".join([
                                f"{p}: {r.get('final_review', '')}" 
                                for p, r in result.get('results', {}).items()
                            ])
                            st.download_button(
                                "📥 Download TXT",
                                txt_data,
                                f"all_reviews_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                "text/plain",
                                use_container_width=True
                            )
                        
                        # Save to history
                        if save_to_history:
                            st.session_state.history.append({
                                'timestamp': datetime.now().isoformat(),
                                'plot': movie_plot[:100] + "...",
                                'persona': 'All 3 Personas',
                                'result': result
                            })
                            st.session_state.total_generated += 3
                            
                            # Save to database
                            batch_id = db.save_batch_review(
                                st.session_state.user_id,
                                movie_plot,
                                result
                            )
                            if batch_id:
                                st.success(f"✅ Saved to database (ID: {batch_id[:12]}...)")
                    
                    else:
                        # Failed
                        error_msg = result.get('error', 'Unknown error')
                        
                        st.markdown(f"""
                        <div class="error-box">
                            <strong>❌ Generation Failed</strong><br>
                            {error_msg}
                        </div>
                        """, unsafe_allow_html=True)
                
                else:
                    # Single persona
                    status_text.markdown(f"**Step 2/4:** Generating review for **{persona}**...")
                    progress_bar.progress(50)
                    
                    result = generate_review(movie_plot, persona, max_retries)
                    
                    # Step 3: Validate
                    status_text.markdown("**Step 3/4:** Validating output...")
                    progress_bar.progress(75)
                    
                    # Step 4: Complete
                    status_text.markdown("**Step 4/4:** Finalizing...")
                    progress_bar.progress(100)
                    
                    # Clear progress
                    progress_bar.empty()
                    status_text.empty()
                    
                    # Check result
                    if result.get('success'):
                        # Success
                        st.markdown("""
                        <div class="success-box">
                            <strong>✅ Success!</strong> Review generated and validated successfully.
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Metrics
                        st.markdown("## 📊 Metrics")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.markdown(f"""
                            <div class="metric-box">
                                <h3>{result.get('total_attempts', 0)}</h3>
                                <p>Attempts</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            score = result.get('validation_score', 0)
                            st.markdown(f"""
                            <div class="metric-box">
                                <h3>{score:.3f}</h3>
                                <p>Score</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col3:
                            predicted = result.get('predicted_persona', 'N/A')
                            match = "✓" if predicted == persona else "✗"
                            st.markdown(f"""
                            <div class="metric-box">
                                <h3>{match}</h3>
                                <p>Match</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col4:
                            review_len = len(result.get('final_review', ''))
                            st.markdown(f"""
                            <div class="metric-box">
                                <h3>{review_len}</h3>
                                <p>Characters</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Review
                        st.markdown("## 📝 Generated Review")
                        
                        st.markdown(f"""
                        <div class="result-card">
                            <h3>{persona}</h3>
                            <p style="font-size: 1.1rem; line-height: 1.8;">{result.get('final_review', '')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Download
                        st.markdown("## 💾 Download")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            json_data = json.dumps(result, ensure_ascii=False, indent=2)
                            st.download_button(
                                "📥 Download JSON",
                                json_data,
                                f"review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                "application/json",
                                use_container_width=True
                            )
                        
                        with col2:
                            txt_data = f"Persona: {persona}\nScore: {score:.3f}\n\nReview:\n{result.get('final_review', '')}"
                            st.download_button(
                                "📥 Download TXT",
                                txt_data,
                                f"review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                "text/plain",
                                use_container_width=True
                            )
                        
                        # Save to history
                        if save_to_history:
                            st.session_state.history.append({
                                'timestamp': datetime.now().isoformat(),
                                'plot': movie_plot[:100] + "...",
                                'persona': persona,
                                'result': result
                            })
                            st.session_state.total_generated += 1
                            
                            # Save to database
                            review_id = db.save_review(
                                st.session_state.user_id,
                                movie_plot,
                                persona,
                                result
                            )
                            if review_id:
                                st.success(f"✅ Saved to database (ID: {review_id[:12]}...)")
                        
                    else:
                        # Failed
                        error_msg = result.get('error', 'Unknown error')
                        
                        st.markdown(f"""
                        <div class="error-box">
                            <strong>❌ Generation Failed</strong><br>
                            {error_msg}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Check for quota error
                        if 'quota' in error_msg.lower() or '429' in error_msg:
                            st.markdown("""
                            <div class="warning-box">
                                <strong>⚠️ API Quota Exceeded</strong><br>
                                Google Gemini free tier limit reached (20 requests/day).<br>
                                Please try again tomorrow or upgrade your API plan.
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Show partial result if available
                        if result.get('final_review'):
                            st.markdown("### 📝 Generated Review (Not Validated)")
                            st.info(result.get('final_review', ''))
                    
                    # Show logs
                    if show_logs and result.get('iteration_history'):
                        with st.expander("📋 Detailed Logs"):
                            for i, iteration in enumerate(result['iteration_history'], 1):
                                st.write(f"**Attempt {i}:**")
                                st.write(f"- Score: {iteration.get('score', 0):.3f}")
                                st.write(f"- Passed: {iteration.get('passed', False)}")
                                if iteration.get('feedback'):
                                    st.write(f"- Feedback: {iteration['feedback'][:200]}...")
                                st.write("---")
            
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                
                st.markdown(f"""
                <div class="error-box">
                    <strong>❌ System Error</strong><br>
                    {str(e)}
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("🔍 Error Details"):
                    import traceback
                    st.code(traceback.format_exc())

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>💡 Tip: Use clear and descriptive movie plots for best results</p>
</div>
""", unsafe_allow_html=True)
