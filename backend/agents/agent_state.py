"""
Agent State Definition for Multi-Agent Workflow
Defines the shared state that flows through all agents
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class AgentState(BaseModel):
    """
    Shared state for multi-agent workflow
    Each agent reads from and writes to this state
    """
    
    # Input
    movie_plot: str = Field(description="Movie plot/synopsis")
    target_persona: str = Field(description="Target persona: Die-hard Fan, Enthusiastic Casual, or Indifferent Casual")
    
    # Researcher Agent Output
    rag_examples: List[Dict[str, Any]] = Field(default_factory=list, description="Retrieved example reviews")
    rag_context: str = Field(default="", description="Formatted context for LLM")
    
    # Writer Agent Output
    generated_review: str = Field(default="", description="Generated Bengali review")
    generation_attempt: int = Field(default=0, description="Number of generation attempts")
    
    # Critic Agent Output
    validation_score: float = Field(default=0.0, description="Validation score (0-1)")
    validation_passed: bool = Field(default=False, description="Whether validation passed")
    predicted_persona: str = Field(default="", description="Predicted persona by validator")
    confidence_scores: Dict[str, float] = Field(default_factory=dict, description="All persona confidence scores")
    
    # Reflector Agent Output
    reflection_feedback: str = Field(default="", description="Feedback for improvement")
    should_retry: bool = Field(default=False, description="Whether to retry generation")
    
    # Workflow Metadata
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    workflow_complete: bool = Field(default=False, description="Whether workflow is complete")
    error_message: str = Field(default="", description="Error message if any")
    
    # Performance Tracking
    iteration_history: List[Dict[str, Any]] = Field(default_factory=list, description="History of all iterations")
    
    class Config:
        arbitrary_types_allowed = True


if __name__ == "__main__":
    print("Testing AgentState...")
    
    state = AgentState(
        movie_plot="একটি রোমান্টিক মুভি",
        target_persona="Die-hard Fan"
    )
    
    print(f"Plot: {state.movie_plot}")
    print(f"Persona: {state.target_persona}")
    print("✅ AgentState working!")
