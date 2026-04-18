"""
Shared CSS Theme - Clean Modern Design (No Blur)
"""

SHARED_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Bengali:wght@400;600;700&family=Inter:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Inter', 'Noto Sans Bengali', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
    }
    
    .header-gradient {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(59, 130, 246, 0.3);
    }
    
    .header-gradient h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        color: white;
    }
    
    .header-gradient p {
        font-size: 1.2rem;
        margin: 0.8rem 0 0 0;
        color: rgba(255, 255, 255, 0.95);
    }
    
    .stat-card {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        padding: 2rem 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(59, 130, 246, 0.4);
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .stat-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 50px rgba(59, 130, 246, 0.6);
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 700;
        color: white;
        margin: 0;
    }
    
    .stat-label {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        padding: 2rem;
        border-radius: 15px;
        height: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 8px 30px rgba(139, 92, 246, 0.4);
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 50px rgba(139, 92, 246, 0.6);
    }
    
    .feature-card h3 {
        color: white;
        font-size: 1.6rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .feature-card p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        line-height: 1.7;
    }
    
    .persona-card {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 2rem;
        border-radius: 15px;
        height: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 8px 30px rgba(16, 185, 129, 0.4);
    }
    
    .persona-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 50px rgba(16, 185, 129, 0.6);
    }
    
    .persona-card h3 {
        color: white;
        font-size: 1.7rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .persona-card ul, .persona-card p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.05rem;
        line-height: 1.9;
    }
    
    .result-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 2px solid #3b82f6;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(59, 130, 246, 0.2);
        margin: 1rem 0;
        color: white;
    }
    
    .metric-box {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.3);
    }
    
    .metric-box h3 {
        color: white;
        font-size: 2rem;
        margin: 0;
        font-weight: 700;
    }
    
    .success-box {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
    }
    
    .error-box {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.3);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(245, 158, 11, 0.3);
    }
    
    .info-box {
        background: rgba(59, 130, 246, 0.1);
        border: 2px solid #3b82f6;
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        color: white;
    }
    
    .info-box h3 {
        color: #60a5fa;
        font-size: 1.8rem;
        margin-top: 0;
        margin-bottom: 1.5rem;
    }
    
    .info-box p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        line-height: 1.8;
        margin-bottom: 1rem;
    }
    
    .info-box ol {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        line-height: 1.8;
        padding-left: 1.5rem;
    }
    
    .info-box ol li {
        margin-bottom: 1.5rem;
    }
    
    .info-box ul {
        margin-top: 0.5rem;
        padding-left: 1.5rem;
    }
    
    .info-box ul li {
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 0.5rem;
    }
    
    .persona-example {
        background: rgba(0, 0, 0, 0.3);
        border-left: 4px solid #8b5cf6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .persona-example p {
        color: rgba(255, 255, 255, 0.95);
        font-family: 'Noto Sans Bengali', sans-serif;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.4);
        border: none;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(139, 92, 246, 0.6);
        background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%);
    }
    
    h2 {
        color: #60a5fa;
        font-size: 2rem;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        background: #ffffff !important;
        border: 2px solid #3b82f6 !important;
        color: #000000 !important;
        border-radius: 10px !important;
        font-size: 1.1rem !important;
        padding: 0.8rem !important;
    }
    
    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: #6b7280 !important;
    }
    
    .stTextInput label,
    .stTextArea label {
        color: #60a5fa !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e293b;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        border-radius: 10px;
    }
</style>
"""
