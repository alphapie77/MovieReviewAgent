"""
About Page - Complete Rewrite
Clean, bug-free, properly styled
"""

import streamlit as st
from pathlib import Path
import sys

# Import shared theme
sys.path.insert(0, str(Path(__file__).parent.parent))
from shared_theme import SHARED_CSS

# Page config
st.set_page_config(page_title="About", page_icon="📚", layout="wide")

# Apply shared theme
st.markdown(SHARED_CSS, unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-gradient">
    <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">📚 About This System</h1>
    <p style="font-size: 1.2rem; opacity: 0.9;">Bengali Movie Review Multi-Agent System</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Overview
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%); border: 2px solid #3b82f6; border-radius: 15px; padding: 2rem; margin: 1.5rem 0; box-shadow: 0 8px 32px rgba(59, 130, 246, 0.2);">
    <h2 style="color: #60a5fa; font-size: 2rem; margin-top: 0; margin-bottom: 1rem;">🎯 Project Overview</h2>
    <h3 style="color: #5b8dc9; font-size: 1.5rem; margin-bottom: 1rem; font-weight: 600;">Neuro-Symbolic Multi-Agent Framework with Weak Supervision and RAG</h3>
    <p style="color: #1f2937; font-size: 1.1rem; line-height: 1.8; margin-bottom: 1rem;">
        This system generates <strong style="color: #111827;">persona-specific Bengali movie reviews</strong> using a sophisticated multi-agent architecture that combines neural networks with symbolic reasoning.
    </p>
    <p style="color: #1f2937; font-size: 1.05rem; margin: 0;">
        <strong style="color: #111827;">Research Domain:</strong> NLP, Multi-Agent Systems, Low-Resource Languages, Neuro-Symbolic AI
    </p>
</div>
""", unsafe_allow_html=True)

# Key Features
st.markdown("""
<div style="margin: 2rem 0;">
    <h2 style="color: #60a5fa; font-size: 2rem;">✨ Key Features</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🤖 Multi-Agent System
    - **4 Specialized Agents**: Researcher, Writer, Critic, Reflector
    - **LangGraph Orchestration**: State-based workflow
    - **Self-Correction**: Automatic retry with feedback
    - **100% Persona Accuracy**: Validated output
    
    ### 🧠 Neural Components
    - **BanglaBERT**: Fine-tuned classifier (87.49% accuracy)
    - **LaBSE**: Multilingual embeddings (768-dim)
    - **Google Gemini**: Text generation LLM
    - **ChromaDB**: Vector database for RAG
    """)

with col2:
    st.markdown("""
    ### 🔬 Hybrid Validation
    - **60% Neural**: BanglaBERT classification
    - **40% Symbolic**: Linguistic rule scoring
    - **Persona Thresholds**: Adaptive validation
    - **First-Try Success**: Average 1.0 attempts
    
    ### 📊 Training Data
    - **6,114 Reviews**: Clean Bengali movie reviews
    - **3 Personas**: Clustered using K-means
    - **95% Retention**: High-quality data
    - **Real Examples**: Authentic Bengali text
    """)

st.markdown("---")

# System Architecture
st.markdown("""
<div style="margin: 2rem 0;">
    <h2 style="color: #60a5fa; font-size: 2rem;">🏗️ System Architecture</h2>
</div>
""", unsafe_allow_html=True)

st.code("""
User Input (Movie Plot)
        ↓
┌─────────────────────┐
│  Researcher Agent   │ → RAG Retrieval (10 examples from 6,114 reviews)
└─────────────────────┘
        ↓
┌─────────────────────┐
│   Writer Agent      │ → Gemini Generation (persona-specific prompts)
└─────────────────────┘
        ↓
┌─────────────────────┐
│   Critic Agent      │ → Hybrid Validation (60% BanglaBERT + 40% Linguistic)
└─────────────────────┘
        ↓
    [Pass?]
     ↙   ↘
   Yes    No
    ↓      ↓
  END   ┌─────────────────────┐
        │ Reflector Agent     │ → Feedback Generation
        └─────────────────────┘
                ↓
           [Retry Writer] (max 3 attempts)
""", language="text")

st.markdown("---")

# Personas
st.markdown("""
<div style="margin: 2rem 0;">
    <h2 style="color: #60a5fa; font-size: 2rem;">🎭 Persona Details</h2>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🔥 Die-hard Fan", "😊 Enthusiastic Casual", "😐 Indifferent Casual"])

with tab1:
    st.markdown("""
    ### Die-hard Fan (অতি উৎসাহী)
    
    **Characteristics:**
    - Extremely enthusiastic and emotional
    - Uses superlatives and exclamations
    - High engagement with detailed opinions
    - Focuses on positive aspects
    
    **Validation Threshold:** 0.70
    
    **Style Markers:**
    - অসাধারণ, দারুণ, মন ছুঁয়ে গেল
    - অভূতপূর্ব, অনবদ্য, একেবারে মুগ্ধ
    - অসম্ভব সুন্দর, জীবনের সেরা
    
    **Example:**
    """)
    
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); border-left: 4px solid #ff6b6b; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
        <p style="color: rgba(255,255,255,0.95); font-size: 1.1rem; line-height: 1.8; font-family: 'Noto Sans Bengali', sans-serif; margin: 0;">
            ওহ মাই গড! এই সিনেমাটা কী ছিল! একেবারে মন ছুঁয়ে গেল! নীলপুরের সেই শান্ত, নিরিবিলি শহরটা যে এমন এক ভয়াবহ রহস্যের চাদরে ঢেকে যাবে, কে জানত! প্রতিটি দৃশ্য এত নিখুঁতভাবে তৈরি যে চোখ ফেরানো যায় না!
        </p>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
    ### Enthusiastic Casual (ভালো লাগা)
    
    **Characteristics:**
    - Balanced perspective
    - Positive with minor criticism
    - Moderate engagement
    - Measured tone
    
    **Validation Threshold:** 0.45
    
    **Style Markers:**
    - ভালো লাগলো, বেশ ভালো, মন্দ না
    - ভালো ছিল, তবে, কিন্তু
    - একটু, মোটামুটি
    
    **Example:**
    """)
    
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); border-left: 4px solid #ffd93d; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
        <p style="color: rgba(255,255,255,0.95); font-size: 1.1rem; line-height: 1.8; font-family: 'Noto Sans Bengali', sans-serif; margin: 0;">
            নীলপুরের এই নতুন ছবিটা বেশ ভালো লাগল। তবে, কিছু কিছু জায়গায় একটু ধীরগতি মনে হয়েছে। গল্পটা ভালো ছিল, কিন্তু শেষটা আরেকটু ভালো হতে পারত। সব মিলিয়ে মোটামুটি ভালো একটা অভিজ্ঞতা।
        </p>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("""
    ### Indifferent Casual (উদাসীন)
    
    **Characteristics:**
    - Brief and critical
    - Low engagement
    - Focuses on negatives
    - Short sentences
    
    **Validation Threshold:** 0.60
    
    **Style Markers:**
    - সাধারণ, তেমন কিছু না, বিরক্তিকর
    - সময় নষ্ট, খারাপ, দুর্বল
    - হতাশ
    
    **Example:**
    """)
    
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); border-left: 4px solid #6bcfff; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
        <p style="color: rgba(255,255,255,0.95); font-size: 1.1rem; line-height: 1.8; font-family: 'Noto Sans Bengali', sans-serif; margin: 0;">
            শহরের ঘটনাগুলো কেমন যেন! সাধারণ। তেমন কিছু মনে রাখার মতো নেই। গল্পটা দুর্বল, অভিনয়ও তেমন না। সময় নষ্ট মনে হলো।
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Performance
st.markdown("""
<div style="margin: 2rem 0;">
    <h2 style="color: #60a5fa; font-size: 2rem;">📊 Performance Metrics</h2>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Dataset Size", "6,114 reviews")
    st.metric("Model Accuracy", "87.49%")

with col2:
    st.metric("Persona Accuracy", "100%")
    st.metric("Success Rate", "100%")

with col3:
    st.metric("Avg Attempts", "1.0")
    st.metric("Avg Time", "~30s")

st.markdown("---")

# Tech Stack
st.markdown("""
<div style="margin: 2rem 0;">
    <h2 style="color: #60a5fa; font-size: 2rem;">🛠️ Technology Stack</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Core Technologies
    - **Orchestration**: LangGraph
    - **LLM**: Google Gemini (gemini-2.5-flash-lite)
    - **Classification**: BanglaBERT (sagorsarker/bangla-bert-base)
    - **Vector DB**: ChromaDB
    """)

with col2:
    st.markdown("""
    ### Supporting Tools
    - **Embeddings**: LaBSE (sentence-transformers/LaBSE)
    - **State Management**: Pydantic
    - **Web Interface**: Streamlit
    - **Language**: Python 3.8+
    """)

st.markdown("---")

# Research Contributions - Using simple markdown instead of HTML
st.markdown("""
<div style="margin: 2rem 0;">
    <h2 style="color: #60a5fa; font-size: 2rem;">🎓 Research Contributions</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background: rgba(59, 130, 246, 0.1); border: 2px solid #3b82f6; border-radius: 15px; padding: 2rem; margin: 1.5rem 0;">
    <h3 style="color: #60a5fa; font-size: 1.8rem; margin-top: 0;">Novel Contributions</h3>
</div>
""", unsafe_allow_html=True)

st.markdown("""
### 1️⃣ First Neuro-Symbolic Multi-Agent System for Bengali
- Combines neural (BanglaBERT) and symbolic (linguistic rules) validation
- Achieves 100% persona accuracy

### 2️⃣ Hybrid Validation Framework
- **60% Neural**: BanglaBERT classification
- **40% Symbolic**: Linguistic feature scoring
- **Persona-specific adaptive thresholds**

### 3️⃣ RAG for Low-Resource Languages
- **ChromaDB** vector database
- **LaBSE** multilingual embeddings
- **Context-aware** generation

### 4️⃣ Persona-Constrained Generation
- **3 validated personas** from real data
- **Self-correction** with feedback loops
- **Average 1.0 attempts** (first-try success)
""")

st.markdown("---")

# Citation
st.markdown("""
<div style="margin: 2rem 0;">
    <h2 style="color: #60a5fa; font-size: 2rem;">📝 Citation</h2>
</div>
""", unsafe_allow_html=True)

st.code("""
@mastersthesis{bengali_multiagent_2026,
  title={A Neuro-Symbolic Multi-Agent Framework with Weak Supervision and RAG 
         for Pre-Release Audience Simulation in Low-Resource Language (Bangla)},
  author={[Your Name]},
  year={2026},
  school={[Your University]}
}
""", language="bibtex")

st.markdown("---")

# Contact
st.markdown("""
<div style="margin: 2rem 0;">
    <h2 style="color: #60a5fa; font-size: 2rem;">📧 Contact</h2>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **GitHub**  
    [github.com/yourusername/MovieReviewAgent](https://github.com)
    """)

with col2:
    st.markdown("""
    **Email**  
    your.email@university.edu
    """)

with col3:
    st.markdown("""
    **University**  
    [Your University Name]
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.6); padding: 1rem 0;">
    <p style="margin: 0.5rem 0;"><strong style="color: rgba(255,255,255,0.8);">Bengali Movie Review Multi-Agent System</strong></p>
    <p style="margin: 0.5rem 0;">Phase 3 Complete | Master's Thesis 2026</p>
    <p style="margin: 0.5rem 0;">© 2026 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
