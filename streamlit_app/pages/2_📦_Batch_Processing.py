"""
Batch Processing Page - Complete Rewrite
Clean, bug-free, properly styled
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import json
from datetime import datetime
import io

# Add backend
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "backend"))

# Import shared theme
sys.path.insert(0, str(Path(__file__).parent.parent))
from shared_theme import SHARED_CSS

# Page config
st.set_page_config(page_title="Batch Processing", page_icon="📦", layout="wide")

# Apply shared theme
st.markdown(SHARED_CSS, unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-gradient">
    <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">📦 Batch Processing</h1>
    <p style="font-size: 1.2rem; opacity: 0.9;">Process multiple movie plots efficiently with CSV upload</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Instructions Section
st.markdown("""
<div style="background: rgba(255,255,255,0.05); padding: 2rem; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 2rem;">
    <h2 style="margin-top: 0; color: #3b82f6; font-size: 2rem; margin-bottom: 1.5rem; font-weight: 700;">📋 How to Use Batch Processing</h2>
</div>
""", unsafe_allow_html=True)

# CSV Format Requirements
st.markdown("""
<div style="background: rgba(102, 126, 234, 0.15); padding: 1.5rem; border-radius: 15px; border-left: 4px solid #667eea; margin-bottom: 1.5rem;">
    <h3 style="color: #4f5fd6; margin-top: 0; font-size: 1.4rem; margin-bottom: 1rem; font-weight: 700;">📄 CSV Format Requirements</h3>
    <p style="color: #1f2937; line-height: 1.8; margin-bottom: 1rem; font-size: 1.05rem;">Your CSV file must contain exactly <strong style="color: #111827;">2 columns</strong> with these names:</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background: rgba(0,0,0,0.2); padding: 1.5rem; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1);">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📝</div>
        <strong style="color: #3b82f6; font-size: 1.2rem; font-weight: 700;">Column 1: plot</strong>
        <p style="color: #1f2937; margin: 0.5rem 0 0 0; font-size: 1rem;">Movie plot text in Bengali or Banglish</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: rgba(0,0,0,0.2); padding: 1.5rem; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1);">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">👤</div>
        <strong style="color: #8b5cf6; font-size: 1.2rem; font-weight: 700;">Column 2: persona</strong>
        <p style="color: #1f2937; margin: 0.5rem 0 0 0; font-size: 1rem;">Target persona type</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Valid Persona Values
st.markdown("""
<div style="background: rgba(67, 233, 123, 0.15); padding: 1.5rem; border-radius: 15px; border-left: 4px solid #43e97b; margin-bottom: 1.5rem;">
    <h3 style="color: #059669; margin-top: 0; font-size: 1.4rem; margin-bottom: 1rem; font-weight: 700;">✅ Valid Persona Values</h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: rgba(255, 107, 107, 0.2); padding: 1.5rem; border-radius: 10px; text-align: center; border: 1px solid rgba(255, 107, 107, 0.3);">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔥</div>
        <strong style="color: #dc2626; font-size: 1.1rem; font-weight: 700;">Die-hard Fan</strong>
        <p style="color: #1f2937; font-size: 0.9rem; margin: 0.5rem 0 0 0;">Extremely enthusiastic</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: rgba(255, 217, 61, 0.2); padding: 1.5rem; border-radius: 10px; text-align: center; border: 1px solid rgba(255, 217, 61, 0.3);">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">😊</div>
        <strong style="color: #ca8a04; font-size: 1.1rem; font-weight: 700;">Enthusiastic Casual</strong>
        <p style="color: #1f2937; font-size: 0.9rem; margin: 0.5rem 0 0 0;">Balanced & positive</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: rgba(107, 207, 255, 0.2); padding: 1.5rem; border-radius: 10px; text-align: center; border: 1px solid rgba(107, 207, 255, 0.3);">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">😐</div>
        <strong style="color: #0284c7; font-size: 1.1rem; font-weight: 700;">Indifferent Casual</strong>
        <p style="color: #1f2937; font-size: 0.9rem; margin: 0.5rem 0 0 0;">Brief & critical</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Example CSV Format
st.markdown("""
<div style="background: rgba(245, 87, 108, 0.15); padding: 1.5rem; border-radius: 15px; border-left: 4px solid #f5576c; margin-bottom: 2rem;">
    <h3 style="color: #dc2626; margin-top: 0; font-size: 1.4rem; margin-bottom: 1rem; font-weight: 700;">📝 Example CSV Format</h3>
    <div style="background: rgba(0,0,0,0.3); padding: 1.5rem; border-radius: 10px; font-family: 'Courier New', monospace; border: 1px solid rgba(255,255,255,0.1);">
        <div style="color: #059669; margin-bottom: 0.5rem; font-size: 1rem; font-weight: 700;">plot,persona</div>
        <div style="color: #1f2937; margin-bottom: 0.3rem; font-size: 0.95rem;">একটি রোমান্টিক মুভি যেখানে দুই প্রেমিক মিলিত হয়,Die-hard Fan</div>
        <div style="color: #1f2937; margin-bottom: 0.3rem; font-size: 0.95rem;">একটি থ্রিলার মুভি যেখানে রহস্য উদঘাটন হয়,Enthusiastic Casual</div>
        <div style="color: #1f2937; font-size: 0.95rem;">ekta action movie jekhane hero lorai kore,Indifferent Casual</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Download Template Section
st.markdown("""
<div style="background: rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 2rem;">
    <h2 style="margin-top: 0; color: #8b5cf6; font-size: 1.8rem; margin-bottom: 0.5rem; font-weight: 700;">📥 Download CSV Template</h2>
    <p style="color: #1f2937; margin-bottom: 1rem;">Download a pre-filled template to get started quickly!</p>
</div>
""", unsafe_allow_html=True)

template_data = {
    'plot': [
        'একটি রোমান্টিক মুভি যেখানে দুই প্রেমিক মিলিত হয়',
        'একটি থ্রিলার মুভি যেখানে রহস্য উদঘাটন হয়',
        'একটি অ্যাকশন মুভি যেখানে নায়ক লড়াই করে'
    ],
    'persona': [
        'Die-hard Fan',
        'Enthusiastic Casual',
        'Indifferent Casual'
    ]
}

template_df = pd.DataFrame(template_data)
template_csv = template_df.to_csv(index=False, encoding='utf-8-sig')

st.download_button(
    "📥 Download CSV Template",
    template_csv,
    "batch_template.csv",
    "text/csv",
    use_container_width=True
)

st.markdown("<br>", unsafe_allow_html=True)

# Upload CSV Section
st.markdown("""
<div style="background: rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 1.5rem;">
    <h2 style="margin-top: 0; color: #10b981; font-size: 1.8rem; margin-bottom: 0.5rem; font-weight: 700;">📤 Upload Your CSV File</h2>
    <p style="color: #1f2937; margin-bottom: 0;">Select your CSV file with movie plots and personas</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose CSV file",
    type=['csv'],
    help="Upload CSV file with 'plot' and 'persona' columns"
)

if uploaded_file:
    try:
        # Read CSV
        df = pd.read_csv(uploaded_file, encoding='utf-8')
        
        # Validate columns
        if 'plot' not in df.columns or 'persona' not in df.columns:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); padding: 1rem 1.5rem; border-radius: 10px; margin: 1rem 0;">
                <strong style="color: #fff; font-size: 1.1rem;">❌ Error: CSV must have 'plot' and 'persona' columns</strong>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Show preview
            st.markdown("""
            <div style="margin: 1.5rem 0;">
                <h3 style="font-size: 1.6rem; color: #3b82f6; margin-bottom: 1rem; font-weight: 700;">👀 File Preview</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.dataframe(df.head(10), use_container_width=True)
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 1rem 1.5rem; border-radius: 10px; margin: 1rem 0;">
                <strong style="color: #fff; font-size: 1.1rem;">✅ Successfully loaded {len(df)} rows from CSV file!</strong>
            </div>
            """, unsafe_allow_html=True)
            
            # Settings
            st.markdown("""
            <div style="background: rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1); margin: 1.5rem 0;">
                <h3 style="margin-top: 0; color: #f59e0b; font-size: 1.6rem; margin-bottom: 0.5rem; font-weight: 700;">⚙️ Batch Settings</h3>
                <p style="color: #1f2937; margin-bottom: 0;">Configure processing parameters</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                max_retries = st.slider("Max Retries", 1, 5, 3)
            
            with col2:
                batch_size = st.number_input("Batch Size", 1, len(df), min(10, len(df)))
            
            st.markdown(f"""
            <div style="background: rgba(255, 193, 7, 0.15); padding: 1rem 1.5rem; border-radius: 10px; border-left: 4px solid #ffc107; margin: 1rem 0;">
                <strong style="color: #ffc107;">⚠️ Processing Information</strong><br>
                <span style="color: rgba(255,255,255,0.8);">• Processing <strong>{batch_size}</strong> plots from your CSV</span><br>
                <span style="color: rgba(255,255,255,0.8);">• Google Gemini Free Tier: <strong>20 requests/day</strong></span><br>
                <span style="color: rgba(255,255,255,0.8);">• Estimated time: <strong>~{batch_size * 30} seconds</strong></span>
            </div>
            """, unsafe_allow_html=True)
            
            # Process button
            if st.button("🚀 Start Batch Processing", type="primary", use_container_width=True):
                
                from phase3_integration import generate_review
                
                results = []
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Metrics
                col1, col2, col3 = st.columns(3)
                success_metric = col1.empty()
                failed_metric = col2.empty()
                progress_metric = col3.empty()
                
                success_count = 0
                failed_count = 0
                
                for idx, row in df.head(batch_size).iterrows():
                    try:
                        # Validate plot length
                        plot_word_count = len(str(row['plot']).split())
                        if plot_word_count < 200:
                            failed_count += 1
                            results.append({
                                'index': idx,
                                'plot': row['plot'],
                                'persona': row['persona'],
                                'success': False,
                                'review': '',
                                'score': 0,
                                'attempts': 0,
                                'error': f'Plot too short: {plot_word_count} words. Minimum 200 words required.'
                            })
                            failed_metric.metric("❌ Failed", failed_count)
                            continue
                        
                        # Update status
                        status_text.markdown(f"**Processing {idx+1}/{batch_size}:** {row['plot'][:50]}...")
                        progress_bar.progress((idx + 1) / batch_size)
                        
                        # Generate
                        result = generate_review(
                            row['plot'],
                            row['persona'],
                            max_retries
                        )
                        
                        # Track
                        if result.get('success'):
                            success_count += 1
                        else:
                            failed_count += 1
                        
                        # Update metrics
                        success_metric.metric("✅ Success", success_count)
                        failed_metric.metric("❌ Failed", failed_count)
                        progress_metric.metric("📊 Progress", f"{idx+1}/{batch_size}")
                        
                        # Store
                        results.append({
                            'index': idx,
                            'plot': row['plot'],
                            'persona': row['persona'],
                            'success': result.get('success', False),
                            'review': result.get('final_review', ''),
                            'score': result.get('validation_score', 0),
                            'attempts': result.get('total_attempts', 0),
                            'error': result.get('error', '')
                        })
                        
                    except Exception as e:
                        failed_count += 1
                        results.append({
                            'index': idx,
                            'plot': row['plot'],
                            'persona': row['persona'],
                            'success': False,
                            'review': '',
                            'score': 0,
                            'attempts': 0,
                            'error': str(e)
                        })
                        
                        # Check for quota error
                        if '429' in str(e) or 'quota' in str(e).lower():
                            st.markdown("""
                            <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); padding: 1rem 1.5rem; border-radius: 10px; margin: 1rem 0;">
                                <strong style="color: #fff;">❌ API Quota Exceeded. Stopping batch processing.</strong>
                            </div>
                            """, unsafe_allow_html=True)
                            break
                
                # Complete
                progress_bar.empty()
                status_text.empty()
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 1.5rem; border-radius: 15px; margin: 1.5rem 0; text-align: center;">
                    <h3 style="color: #fff; margin: 0; font-size: 1.5rem;">✅ Batch Processing Complete!</h3>
                    <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1.1rem;">
                        Success: <strong>{success_count}</strong> | Failed: <strong>{failed_count}</strong> | Total: <strong>{success_count + failed_count}</strong>
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Results
                st.markdown("""
                <div style="margin: 2rem 0;">
                    <h2 style="font-size: 2rem; margin-bottom: 1rem; color: #10b981; font-weight: 700;">📊 Processing Results</h2>
                    <p style="color: #1f2937; margin-bottom: 1rem;">Detailed results for all processed plots</p>
                </div>
                """, unsafe_allow_html=True)
                
                results_df = pd.DataFrame(results)
                st.dataframe(results_df, use_container_width=True)
                
                # Download
                st.markdown("""
                <div style="margin: 2rem 0;">
                    <h2 style="font-size: 2rem; margin-bottom: 1rem; color: #8b5cf6; font-weight: 700;">💾 Download Results</h2>
                    <p style="color: #1f2937; margin-bottom: 1rem;">Export your results in multiple formats</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # JSON
                    json_data = json.dumps(results, ensure_ascii=False, indent=2)
                    st.download_button(
                        "📥 Download JSON",
                        json_data,
                        f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        "application/json",
                        use_container_width=True
                    )
                
                with col2:
                    # CSV
                    csv_data = results_df.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        "📥 Download CSV",
                        csv_data,
                        f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        "text/csv",
                        use_container_width=True
                    )
                
                with col3:
                    # Excel
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        results_df.to_excel(writer, index=False, sheet_name='Results')
                    
                    st.download_button(
                        "📥 Download Excel",
                        buffer.getvalue(),
                        f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
    
    except Exception as e:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); padding: 1rem 1.5rem; border-radius: 10px; margin: 1rem 0;">
            <strong style="color: #fff;">❌ Error reading CSV: {str(e)}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("🔍 Error Details"):
            import traceback
            st.code(traceback.format_exc())

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.6); padding: 1rem 0;">
    <p>💡 Tip: Start with small batches to avoid API quota limits</p>
</div>
""", unsafe_allow_html=True)
