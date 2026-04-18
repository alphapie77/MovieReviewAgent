"""
Bengali Movie Review Generator - Home Page
Clean Modern Design
"""

import streamlit as st
import sys
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Bengali Movie Review Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import shared theme
sys.path.insert(0, str(Path(__file__).parent))
from shared_theme import SHARED_CSS

# Apply shared theme
st.markdown(SHARED_CSS, unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'total_generated' not in st.session_state:
    st.session_state.total_generated = 0

# Header
st.markdown("""
<div class="header-gradient">
    <h1>🎬 Bengali Movie Review Generator</h1>
    <p>Neuro-Symbolic Multi-Agent System with RAG & BanglaBERT</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Stats
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">6,114</div>
        <div class="stat-label">📚 Reviews</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">87.49%</div>
        <div class="stat-label">🎯 Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">100%</div>
        <div class="stat-label">✅ Success</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{st.session_state.total_generated}</div>
        <div class="stat-label">🚀 Generated</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Quick Start
st.markdown("## 🚀 Quick Start")

col1, col2 = st.columns(2)

with col1:
    if st.button("✍️ Generate Single Review", key="single"):
        st.switch_page("pages/1_✍️_Single_Review.py")

with col2:
    if st.button("📦 Batch Processing", key="batch"):
        st.switch_page("pages/2_📦_Batch_Processing.py")

st.markdown("<br>", unsafe_allow_html=True)

# System Architecture
st.markdown("## 🏗️ System Architecture")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🔍 Researcher Agent</h3>
        <p>Retrieves 10 similar reviews from 6,114 examples using RAG (ChromaDB + LaBSE embeddings)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>✍️ Writer Agent</h3>
        <p>Generates persona-specific Bengali review using Google Gemini LLM with contextual prompts</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>🎯 Critic Agent</h3>
        <p>Validates using Hybrid system: 60% BanglaBERT Neural + 40% Linguistic Rules</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>🔄 Reflector Agent</h3>
        <p>Provides detailed feedback and triggers retry if validation fails (max 3 attempts)</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Personas
st.markdown("## 🎭 Available Personas")

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="persona-card">
        <h3>🔥 Die-hard Fan</h3>
        <p><strong>Characteristics:</strong></p>
        <ul>
            <li>Extremely enthusiastic</li>
            <li>Emotional language</li>
            <li>Uses superlatives</li>
            <li>High engagement</li>
        </ul>
        <p><strong>Threshold:</strong> 0.70</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="persona-card">
        <h3>😊 Enthusiastic Casual</h3>
        <p><strong>Characteristics:</strong></p>
        <ul>
            <li>Balanced perspective</li>
            <li>Positive with minor criticism</li>
            <li>Moderate engagement</li>
            <li>Measured tone</li>
        </ul>
        <p><strong>Threshold:</strong> 0.45</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="persona-card">
        <h3>😐 Indifferent Casual</h3>
        <p><strong>Characteristics:</strong></p>
        <ul>
            <li>Brief and critical</li>
            <li>Low engagement</li>
            <li>Focuses on negatives</li>
            <li>Short sentences</li>
        </ul>
        <p><strong>Threshold:</strong> 0.60</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.8); padding: 1rem 0;">
    <p style="margin: 0; font-size: 1.1rem;"><strong>Bengali Movie Review Multi-Agent System</strong></p>
    <p style="margin: 0.5rem 0 0 0; font-size: 1rem;">Phase 3 Complete | Master's Thesis 2026</p>
</div>
""", unsafe_allow_html=True)
