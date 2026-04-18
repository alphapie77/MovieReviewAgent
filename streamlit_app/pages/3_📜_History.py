"""
History Page
View and manage generation history from database
"""

import streamlit as st
import json
from datetime import datetime
import pandas as pd
from pathlib import Path
import sys

# Import shared theme
sys.path.insert(0, str(Path(__file__).parent.parent))
from shared_theme import SHARED_CSS

# Import database
sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))
from database import get_db

# Page config
st.set_page_config(page_title="History", page_icon="📜", layout="wide")

# Apply shared theme
st.markdown(SHARED_CSS, unsafe_allow_html=True)

# Initialize session
if 'user_id' not in st.session_state:
    import uuid
    st.session_state.user_id = str(uuid.uuid4())

# Initialize database
db = get_db()
db.create_user(st.session_state.user_id)

# Header
st.markdown("""
<div class="header-gradient">
    <h1>📜 Generation History</h1>
    <p>View and manage your review generation history (Persistent Database)</p>
</div>
""", unsafe_allow_html=True)

# Get statistics from database
stats = db.get_statistics(st.session_state.user_id)

# Stats
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Total Reviews", stats.get('total_reviews', 0))

with col2:
    st.metric("✅ Successful", stats.get('successful_reviews', 0))

with col3:
    avg_score = stats.get('avg_score', 0)
    st.metric("⭐ Avg Score", f"{avg_score:.3f}" if avg_score else "N/A")

with col4:
    avg_attempts = stats.get('avg_attempts', 0)
    st.metric("🔄 Avg Attempts", f"{avg_attempts:.1f}" if avg_attempts else "N/A")

st.markdown("---")

# Persona distribution
if stats.get('persona_distribution'):
    st.markdown("### 📊 Persona Distribution")
    
    persona_data = stats['persona_distribution']
    
    col1, col2, col3 = st.columns(3)
    
    for idx, (persona, count) in enumerate(persona_data.items()):
        with [col1, col2, col3][idx % 3]:
            st.markdown(f"""
            <div class="metric-box">
                <h3>{count}</h3>
                <p>{persona}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")

# Get history from database
history = db.get_user_history(st.session_state.user_id, limit=100)

# Check if empty
if not history:
    st.info("📭 No history yet. Generate some reviews to see them here!")
    
    if st.button("✍️ Generate First Review", use_container_width=True):
        st.switch_page("pages/1_✍️_Single_Review.py")

else:
    # Controls
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search", placeholder="Search in plots...")
    
    with col2:
        sort_by = st.selectbox("📊 Sort By", ["Latest First", "Oldest First", "Persona", "Score"])
    
    with col3:
        limit = st.selectbox("📄 Show", [10, 25, 50, 100], index=1)
    
    st.markdown("---")
    
    # Filter
    filtered_history = history[:limit]
    
    if search_query:
        filtered_history = [
            h for h in filtered_history 
            if search_query.lower() in h['movie_plot'].lower()
        ]
    
    # Sort
    if sort_by == "Latest First":
        filtered_history = sorted(filtered_history, key=lambda x: x['created_at'], reverse=True)
    elif sort_by == "Oldest First":
        filtered_history = sorted(filtered_history, key=lambda x: x['created_at'])
    elif sort_by == "Persona":
        filtered_history = sorted(filtered_history, key=lambda x: x['persona'])
    elif sort_by == "Score":
        filtered_history = sorted(filtered_history, key=lambda x: x['validation_score'], reverse=True)
    
    # Display history
    st.markdown(f"### 📋 History ({len(filtered_history)} items)")
    
    for idx, item in enumerate(filtered_history):
        # Parse timestamp
        created_at = datetime.fromisoformat(item['created_at'])
        
        # Create expander title
        plot_preview = item['movie_plot'][:60] + "..." if len(item['movie_plot']) > 60 else item['movie_plot']
        title = f"**{item['persona']}** - {plot_preview} ({created_at.strftime('%Y-%m-%d %H:%M')})"
        
        with st.expander(title):
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**🆔 Review ID:** `{item['review_id']}`")
                st.markdown(f"**📅 Created:** {created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                st.markdown(f"**🎭 Persona:** {item['persona']}")
                st.markdown(f"**⭐ Score:** {item['validation_score']:.3f}")
                st.markdown(f"**🔄 Attempts:** {item['total_attempts']}")
                st.markdown(f"**✅ Success:** {'Yes' if item['success'] else 'No'}")
                
                st.markdown("---")
                
                st.markdown("**📝 Movie Plot:**")
                st.info(item['movie_plot'])
                
                st.markdown("**💬 Generated Review:**")
                if item['success']:
                    st.success(item['generated_review'])
                else:
                    st.error("Review generation failed")
                
                if item['predicted_persona']:
                    match = "✅" if item['predicted_persona'] == item['persona'] else "❌"
                    st.markdown(f"**🎯 Predicted Persona:** {item['predicted_persona']} {match}")
            
            with col2:
                # Download
                review_data = {
                    'review_id': item['review_id'],
                    'created_at': item['created_at'],
                    'persona': item['persona'],
                    'movie_plot': item['movie_plot'],
                    'generated_review': item['generated_review'],
                    'validation_score': item['validation_score'],
                    'predicted_persona': item['predicted_persona'],
                    'total_attempts': item['total_attempts'],
                    'success': item['success']
                }
                
                json_data = json.dumps(review_data, ensure_ascii=False, indent=2)
                st.download_button(
                    "📥 JSON",
                    json_data,
                    f"review_{item['review_id']}.json",
                    "application/json",
                    key=f"download_{idx}",
                    use_container_width=True
                )
                
                txt_data = f"""Review ID: {item['review_id']}
Created: {item['created_at']}
Persona: {item['persona']}
Score: {item['validation_score']:.3f}

Movie Plot:
{item['movie_plot']}

Generated Review:
{item['generated_review']}
"""
                st.download_button(
                    "📥 TXT",
                    txt_data,
                    f"review_{item['review_id']}.txt",
                    "text/plain",
                    key=f"download_txt_{idx}",
                    use_container_width=True
                )
    
    # Bulk export
    st.markdown("---")
    st.markdown("### 💾 Bulk Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Export all as JSON
        export_data = []
        for item in filtered_history:
            export_data.append({
                'review_id': item['review_id'],
                'created_at': item['created_at'],
                'persona': item['persona'],
                'movie_plot': item['movie_plot'],
                'generated_review': item['generated_review'],
                'validation_score': item['validation_score'],
                'predicted_persona': item['predicted_persona'],
                'total_attempts': item['total_attempts'],
                'success': item['success']
            })
        
        all_json = json.dumps(export_data, ensure_ascii=False, indent=2)
        st.download_button(
            "📥 Export All (JSON)",
            all_json,
            f"history_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "application/json",
            use_container_width=True
        )
    
    with col2:
        # Export as CSV
        df = pd.DataFrame(filtered_history)
        csv_data = df.to_csv(index=False, encoding='utf-8-sig')
        
        st.download_button(
            "📥 Export All (CSV)",
            csv_data,
            f"history_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "text/csv",
            use_container_width=True
        )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>💾 History is stored in persistent database and will be available across sessions</p>
</div>
""", unsafe_allow_html=True)
