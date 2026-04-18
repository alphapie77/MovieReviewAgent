"""
LangGraph Workflow - Multi-Agent Orchestration
Coordinates Researcher, Writer, Critic, and Reflector agents
"""

import sys
from pathlib import Path
from typing import Dict, Any, Literal

# Add paths
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent.parent / "config"))

from langgraph.graph import StateGraph, END
from agent_state import AgentState
from agent_nodes import researcher_node, writer_node, critic_node, reflector_node
from logging_config import setup_logger

# Initialize logger
logger = setup_logger("Workflow")


def create_workflow() -> StateGraph:
    """
    Create LangGraph workflow with conditional routing
    
    Workflow:
    START → Researcher → Writer → Critic → [Decision]
                           ↑                    ↓
                           └─── Reflector ←─────┘
                                (if failed)
    """
    logger.info("Creating LangGraph workflow...")
    
    # Create state graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("critic", critic_node)
    workflow.add_node("reflector", reflector_node)
    
    # Set entry point
    workflow.set_entry_point("researcher")
    
    # Add edges
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", "critic")
    
    # Conditional edge from critic
    def should_continue(state: Dict[str, Any]) -> Literal["reflector", "end"]:
        """
        Decide whether to continue to reflector or end
        """
        # Handle both dict and Pydantic object
        validation_passed = state['validation_passed'] if isinstance(state, dict) else state.validation_passed
        generation_attempt = state['generation_attempt'] if isinstance(state, dict) else state.generation_attempt
        max_retries = state['max_retries'] if isinstance(state, dict) else state.max_retries
        error_message = state.get('error_message', '') if isinstance(state, dict) else getattr(state, 'error_message', '')
        
        # End if validation passed
        if validation_passed:
            logger.info("[ROUTING] Validation passed → END")
            return "end"
        
        # End if max retries reached
        if generation_attempt >= max_retries:
            logger.info("[ROUTING] Max retries reached → END")
            return "end"
        
        # End if error occurred
        if error_message:
            logger.info("[ROUTING] Error occurred → END")
            return "end"
        
        # Continue to reflector
        logger.info("[ROUTING] Validation failed → REFLECTOR")
        return "reflector"
    
    workflow.add_conditional_edges(
        "critic",
        should_continue,
        {
            "reflector": "reflector",
            "end": END
        }
    )
    
    # Conditional edge from reflector
    def should_retry(state: Dict[str, Any]) -> Literal["writer", "end"]:
        """
        Decide whether to retry writing or end
        """
        # Handle both dict and Pydantic object
        should_retry_flag = state.get('should_retry', False) if isinstance(state, dict) else getattr(state, 'should_retry', False)
        
        if should_retry_flag:
            logger.info("[ROUTING] Retrying → WRITER")
            return "writer"
        else:
            logger.info("[ROUTING] No retry → END")
            return "end"
    
    workflow.add_conditional_edges(
        "reflector",
        should_retry,
        {
            "writer": "writer",
            "end": END
        }
    )
    
    logger.info("Workflow created successfully")
    return workflow


def run_workflow(movie_plot: str, target_persona: str, max_retries: int = 3) -> Dict[str, Any]:
    """
    Run the complete workflow
    
    Args:
        movie_plot: Movie plot/synopsis
        target_persona: Target persona (Die-hard Fan, Enthusiastic Casual, Indifferent Casual)
        max_retries: Maximum retry attempts
    
    Returns:
        Workflow results with final review and metrics
    """
    logger.info("="*70)
    logger.info(f"Starting workflow for persona: {target_persona}")
    logger.info("="*70)
    
    # Create initial state
    initial_state = AgentState(
        movie_plot=movie_plot,
        target_persona=target_persona,
        max_retries=max_retries
    )
    
    # Create and compile workflow
    workflow = create_workflow()
    app = workflow.compile()
    
    # Run workflow
    try:
        final_state = app.invoke(initial_state.dict())
        
        logger.info("="*70)
        logger.info("Workflow completed")
        logger.info("="*70)
        
        # Prepare results
        results = {
            "success": final_state.get("validation_passed", False),
            "movie_plot": final_state["movie_plot"],
            "target_persona": final_state["target_persona"],
            "final_review": final_state.get("generated_review", ""),
            "validation_score": final_state.get("validation_score", 0.0),
            "predicted_persona": final_state.get("predicted_persona", ""),
            "total_attempts": final_state.get("generation_attempt", 0),
            "iteration_history": final_state.get("iteration_history", []),
            "error": final_state.get("error_message", None)
        }
        
        return results
    
    except Exception as e:
        logger.error(f"Workflow failed: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "movie_plot": movie_plot,
            "target_persona": target_persona
        }


if __name__ == "__main__":
    print("="*70)
    print("Testing LangGraph Workflow")
    print("="*70)
    
    # Test workflow
    test_plot = "একটি রোমান্টিক মুভি যেখানে দুই প্রেমিক মিলিত হয়"
    test_persona = "Die-hard Fan"
    
    print(f"\nPlot: {test_plot}")
    print(f"Persona: {test_persona}")
    print("\nRunning workflow...\n")
    
    results = run_workflow(test_plot, test_persona, max_retries=2)
    
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    print(f"Success: {results['success']}")
    print(f"Total Attempts: {results['total_attempts']}")
    print(f"Validation Score: {results['validation_score']:.3f}")
    print(f"Predicted Persona: {results['predicted_persona']}")
    print(f"\nFinal Review:\n{results['final_review']}")
    
    if results.get('error'):
        print(f"\nError: {results['error']}")
    
    print("\n" + "="*70)
