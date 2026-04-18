"""
Shared CSS Theme - Professional Mobile-First Responsive Design
"""

SHARED_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Bengali:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');
    
    /* Base Styles - Mobile First */
    * {
        font-family: 'Inter', 'Noto Sans Bengali', sans-serif;
        box-sizing: border-box;
    }
    
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        padding: 0.5rem;
    }
    
    /* Header - Mobile First */
    .header-gradient {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        padding: 1rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    .header-gradient h1 {
        font-size: 1.25rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.3;
    }
    
    .header-gradient p {
        font-size: 0.8rem;
        margin: 0.4rem 0 0 0;
        opacity: 0.95;
    }
    
    /* Stat Cards - Mobile First */
    .stat-card {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        padding: 0.8rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        transition: transform 0.2s ease;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .stat-card:active {
        transform: scale(0.98);
    }
    
    .stat-number {
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        margin: 0;
    }
    
    .stat-label {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.75rem;
        margin-top: 0.25rem;
        font-weight: 500;
    }
    
    /* Feature Cards - Mobile First */
    .feature-card {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
        margin-bottom: 0.8rem;
        transition: transform 0.2s ease;
    }
    
    .feature-card:active {
        transform: scale(0.98);
    }
    
    .feature-card h3 {
        color: white;
        font-size: 1rem;
        margin: 0 0 0.6rem 0;
        font-weight: 600;
    }
    
    .feature-card p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.8rem;
        line-height: 1.5;
        margin: 0;
    }
    
    /* Persona Cards - Mobile First */
    .persona-card {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        margin-bottom: 0.8rem;
        transition: transform 0.2s ease;
    }
    
    .persona-card:active {
        transform: scale(0.98);
    }
    
    .persona-card h3 {
        color: white;
        font-size: 1rem;
        margin: 0 0 0.6rem 0;
        font-weight: 600;
    }
    
    .persona-card ul, .persona-card p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 0.8rem;
        line-height: 1.5;
        margin: 0;
    }
    
    .persona-card ul {
        padding-left: 1.2rem;
    }
    
    .persona-card li {
        margin-bottom: 0.3rem;
    }
    
    /* Result Cards - Mobile First */
    .result-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 2px solid #3b82f6;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
        margin: 0.8rem 0;
        color: white;
    }
    
    .result-card h3 {
        font-size: 1rem;
        margin: 0 0 0.6rem 0;
        color: #60a5fa;
    }
    
    .result-card p {
        font-size: 0.85rem;
        line-height: 1.6;
        margin: 0;
    }
    
    /* Metric Boxes - Mobile First */
    .metric-box {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        padding: 0.8rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        margin-bottom: 0.5rem;
    }
    
    .metric-box h3 {
        color: white;
        font-size: 1.3rem;
        margin: 0;
        font-weight: 700;
    }
    
    .metric-box p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.7rem;
        margin: 0.2rem 0 0 0;
    }
    
    /* Alert Boxes - Mobile First */
    .success-box, .error-box, .warning-box {
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        font-size: 0.85rem;
        line-height: 1.5;
    }
    
    .success-box {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    
    .error-box {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
    }
    
    /* Info Boxes - Mobile First */
    .info-box {
        background: rgba(59, 130, 246, 0.1);
        border: 2px solid #3b82f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.8rem 0;
        color: white;
    }
    
    .info-box h3 {
        color: #60a5fa;
        font-size: 1rem;
        margin: 0 0 0.6rem 0;
    }
    
    .info-box p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.85rem;
        line-height: 1.5;
        margin: 0 0 0.6rem 0;
    }
    
    .info-box ol, .info-box ul {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.85rem;
        line-height: 1.5;
        padding-left: 1.2rem;
        margin: 0;
    }
    
    .info-box li {
        margin-bottom: 0.5rem;
    }
    
    /* Persona Examples - Mobile First */
    .persona-example {
        background: rgba(0, 0, 0, 0.3);
        border-left: 3px solid #8b5cf6;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.6rem 0;
    }
    
    .persona-example p {
        color: rgba(255, 255, 255, 0.95);
        font-family: 'Noto Sans Bengali', sans-serif;
        font-size: 0.85rem;
        line-height: 1.6;
        margin: 0;
    }
    
    /* Buttons - Mobile First */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
        border: none;
    }
    
    .stButton>button:active {
        transform: scale(0.98);
    }
    
    /* Headings - Mobile First */
    h2 {
        color: #60a5fa;
        font-size: 1.1rem;
        font-weight: 700;
        margin: 1.2rem 0 0.6rem 0;
    }
    
    h3 {
        color: #60a5fa;
        font-size: 1rem;
        font-weight: 600;
        margin: 1rem 0 0.5rem 0;
    }
    
    /* Sidebar - Mobile First */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
        font-size: 0.85rem !important;
    }
    
    /* Form Inputs - Mobile First */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>div {
        background: #ffffff !important;
        border: 2px solid #3b82f6 !important;
        color: #000000 !important;
        border-radius: 8px !important;
        font-size: 0.85rem !important;
        padding: 0.6rem !important;
    }
    
    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: #6b7280 !important;
        font-size: 0.8rem !important;
    }
    
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label {
        color: #60a5fa !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }
    
    /* Expander - Mobile First */
    .streamlit-expanderHeader {
        font-size: 0.85rem !important;
        padding: 0.6rem !important;
    }
    
    /* Download Buttons - Mobile First */
    .stDownloadButton>button {
        font-size: 0.8rem !important;
        padding: 0.5rem 0.8rem !important;
    }
    
    /* Scrollbar - Mobile First */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e293b;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        border-radius: 6px;
    }
    
    /* Tablet Breakpoint (768px and up) */
    @media (min-width: 768px) {
        .main {
            padding: 1rem;
        }
        
        .header-gradient {
            padding: 1.5rem;
            border-radius: 15px;
            margin-bottom: 1.5rem;
        }
        
        .header-gradient h1 {
            font-size: 1.8rem;
        }
        
        .header-gradient p {
            font-size: 0.95rem;
        }
        
        .stat-card {
            padding: 1.2rem;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .stat-number {
            font-size: 1.8rem;
        }
        
        .stat-label {
            font-size: 0.85rem;
        }
        
        .feature-card, .persona-card {
            padding: 1.3rem;
        }
        
        .feature-card:hover, .persona-card:hover {
            transform: translateY(-5px);
        }
        
        .feature-card h3, .persona-card h3 {
            font-size: 1.1rem;
        }
        
        .feature-card p, .persona-card p {
            font-size: 0.85rem;
        }
        
        .result-card {
            padding: 1.3rem;
        }
        
        .result-card h3 {
            font-size: 1.1rem;
        }
        
        .result-card p {
            font-size: 0.9rem;
        }
        
        .metric-box {
            padding: 1rem;
        }
        
        .metric-box h3 {
            font-size: 1.5rem;
        }
        
        .metric-box p {
            font-size: 0.8rem;
        }
        
        h2 {
            font-size: 1.4rem;
        }
        
        h3 {
            font-size: 1.2rem;
        }
        
        .stButton>button {
            padding: 0.8rem 1.5rem;
            font-size: 0.95rem;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
        }
        
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
    }
    
    /* Desktop Breakpoint (1024px and up) */
    @media (min-width: 1024px) {
        .main {
            padding: 1.5rem;
        }
        
        .header-gradient {
            padding: 2rem;
            border-radius: 18px;
            margin-bottom: 2rem;
        }
        
        .header-gradient h1 {
            font-size: 2.2rem;
        }
        
        .header-gradient p {
            font-size: 1.05rem;
        }
        
        .stat-card {
            padding: 1.5rem;
        }
        
        .stat-number {
            font-size: 2rem;
        }
        
        .stat-label {
            font-size: 0.9rem;
        }
        
        .feature-card, .persona-card {
            padding: 1.5rem;
        }
        
        .feature-card h3, .persona-card h3 {
            font-size: 1.2rem;
        }
        
        .feature-card p, .persona-card p {
            font-size: 0.9rem;
        }
        
        .result-card {
            padding: 1.5rem;
        }
        
        .result-card h3 {
            font-size: 1.2rem;
        }
        
        .result-card p {
            font-size: 0.95rem;
        }
        
        .metric-box {
            padding: 1.2rem;
        }
        
        .metric-box h3 {
            font-size: 1.8rem;
        }
        
        .metric-box p {
            font-size: 0.85rem;
        }
        
        h2 {
            font-size: 1.6rem;
        }
        
        h3 {
            font-size: 1.3rem;
        }
        
        .stButton>button {
            padding: 0.9rem 2rem;
            font-size: 1rem;
        }
    }
    
    /* Large Desktop (1440px and up) */
    @media (min-width: 1440px) {
        .header-gradient h1 {
            font-size: 2.5rem;
        }
        
        .header-gradient p {
            font-size: 1.1rem;
        }
        
        .stat-number {
            font-size: 2.2rem;
        }
        
        h2 {
            font-size: 1.8rem;
        }
    }
</style>
"""
