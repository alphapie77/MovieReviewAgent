"""
Phase 3 Backend Integration
Clean wrapper for Streamlit app
"""

import sys
from pathlib import Path
import os
from dotenv import load_dotenv

# Load .env from Phase 4 first, then Phase 3 as fallback
PHASE4_ROOT = Path(__file__).parent.parent
PHASE3_ROOT = PHASE4_ROOT.parent / "03_Phase3_MultiAgent"

# Try Phase 4 .env first
phase4_env = PHASE4_ROOT / ".env"
if phase4_env.exists():
    load_dotenv(phase4_env)
else:
    # Fallback to Phase 3 .env
    phase3_env = PHASE3_ROOT / ".env"
    if phase3_env.exists():
        load_dotenv(phase3_env)

# Add backend paths
BACKEND_ROOT = Path(__file__).parent
sys.path.insert(0, str(BACKEND_ROOT / "agents"))
sys.path.insert(0, str(BACKEND_ROOT / "config"))
sys.path.insert(0, str(BACKEND_ROOT / "tools"))

from workflow import run_workflow


def generate_review(movie_plot: str, target_persona: str, max_retries: int = 3) -> dict:
    """
    Generate review using Phase 3 system
    
    Args:
        movie_plot: Movie plot text
        target_persona: Target persona name
        max_retries: Maximum retry attempts
    
    Returns:
        Result dictionary with review and metrics
    """
    try:
        result = run_workflow(
            movie_plot=movie_plot,
            target_persona=target_persona,
            max_retries=max_retries
        )
        return result
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "movie_plot": movie_plot,
            "target_persona": target_persona
        }


def generate_all_personas(movie_plot: str, max_retries: int = 3) -> dict:
    """
    Generate reviews for all 3 personas
    
    Args:
        movie_plot: Movie plot text
        max_retries: Maximum retry attempts
    
    Returns:
        Dictionary with results for each persona
    """
    personas = ["Die-hard Fan", "Enthusiastic Casual", "Indifferent Casual"]
    results = {}
    all_success = True
    
    for persona in personas:
        result = generate_review(movie_plot, persona, max_retries)
        results[persona] = result
        if not result.get('success'):
            all_success = False
    
    return {
        'success': all_success,
        'results': results,
        'movie_plot': movie_plot
    }
