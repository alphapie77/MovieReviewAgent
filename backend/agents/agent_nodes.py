"""
Agent Nodes for LangGraph Workflow
Each node represents an agent in the multi-agent system
"""

import sys
from pathlib import Path
from typing import Dict, Any

# Add paths
sys.path.append(str(Path(__file__).parent.parent / "tools"))
sys.path.append(str(Path(__file__).parent.parent / "config"))
sys.path.append(str(Path(__file__).parent))

from agent_state import AgentState
from rag_retriever_tool import RAGRetrieverTool, RAGRetrieverInput
from banglabert_validator_tool import BanglaBERTValidatorTool, ValidatorInput
from logging_config import setup_logger
from persona_filter import filter_enthusiastic_casual
from linguistic_scorer import hybrid_validation
import config as cfg

# Gemini imports
import google.generativeai as genai

# Initialize logger
logger = setup_logger("AgentNodes")

# Initialize tools (singleton pattern)
_rag_tool = None
_validator_tool = None
_llm = None


def get_rag_tool():
    """Get or create RAG tool instance"""
    global _rag_tool
    if _rag_tool is None:
        logger.info("Initializing RAG Retriever Tool...")
        _rag_tool = RAGRetrieverTool()
    return _rag_tool


def get_validator_tool():
    """Get or create Validator tool instance"""
    global _validator_tool
    if _validator_tool is None:
        logger.info("Initializing BanglaBERT Validator Tool...")
        _validator_tool = BanglaBERTValidatorTool()
    return _validator_tool


def get_llm():
    """Get or create LLM instance"""
    global _llm
    if _llm is None:
        logger.info(f"Initializing Gemini LLM ({cfg.GEMINI_MODEL})...")
        genai.configure(api_key=cfg.GOOGLE_API_KEY)
        _llm = genai.GenerativeModel(
            cfg.GEMINI_MODEL,
            generation_config=genai.GenerationConfig(
                temperature=cfg.GENERATION_CONFIG['temperature'],
                top_p=cfg.GENERATION_CONFIG['top_p'],
                top_k=cfg.GENERATION_CONFIG['top_k']
            )
        )
    return _llm


# ============================================================
# NODE 1: RESEARCHER AGENT
# ============================================================

def researcher_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Researcher Agent: Retrieves relevant examples using RAG
    """
    # Handle both dict and Pydantic object
    target_persona = state['target_persona'] if isinstance(state, dict) else state.target_persona
    movie_plot = state['movie_plot'] if isinstance(state, dict) else state.movie_plot
    
    logger.info(f"[RESEARCHER] Starting for persona: {target_persona}")
    
    try:
        rag_tool = get_rag_tool()
        
        # Create input
        rag_input = RAGRetrieverInput(
            query=movie_plot,
            persona=target_persona,
            top_k=cfg.TOP_K_EXAMPLES
        )
        
        # Retrieve examples
        output = rag_tool.run(rag_input)
        
        if output.success:
            logger.info(f"[RESEARCHER] Retrieved {output.data['count']} examples")
            
            # Debug: Log example details
            for i, ex in enumerate(output.data['examples'][:3], 1):  # Log first 3
                logger.info(f"[RESEARCHER] Example {i} - Similarity: {ex['similarity']:.3f}")
                logger.info(f"[RESEARCHER] Example {i} - Review preview: {ex['review'][:100]}...")
            
            return {
                "rag_examples": output.data['examples'],
                "rag_context": output.data['context']
            }
        else:
            logger.error(f"[RESEARCHER] Failed: {output.error}")
            return {
                "error_message": f"RAG retrieval failed: {output.error}"
            }
    
    except Exception as e:
        logger.error(f"[RESEARCHER] Exception: {e}", exc_info=True)
        return {
            "error_message": f"Researcher error: {str(e)}"
        }


# ============================================================
# NODE 2: WRITER AGENT
# ============================================================

def writer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Writer Agent: Generates review using Gemini LLM
    """
    # Handle both dict and Pydantic object
    generation_attempt = state['generation_attempt'] if isinstance(state, dict) else state.generation_attempt
    target_persona = state['target_persona'] if isinstance(state, dict) else state.target_persona
    movie_plot = state['movie_plot'] if isinstance(state, dict) else state.movie_plot
    rag_context = state.get('rag_context', '') if isinstance(state, dict) else getattr(state, 'rag_context', '')
    reflection_feedback = state.get('reflection_feedback', '') if isinstance(state, dict) else getattr(state, 'reflection_feedback', '')
    
    attempt = generation_attempt + 1
    logger.info(f"[WRITER] Starting attempt {attempt} for persona: {target_persona}")
    
    # Validate plot length (minimum 200 words)
    plot_word_count = len(movie_plot.split())
    if plot_word_count < 200:
        error_msg = f"Plot too short: {plot_word_count} words. Minimum 200 words required for professional review generation."
        logger.error(f"[WRITER] {error_msg}")
        return {
            "error_message": error_msg,
            "generation_attempt": attempt
        }
    
    try:
        llm = get_llm()
        
        # Get persona-specific guidance
        persona_info = cfg.PERSONAS.get(target_persona, {})
        
        # Build STRICT plot-based prompts
        
        if target_persona == "Enthusiastic Casual":
            full_prompt = f"""You are a professional Bengali movie reviewer. Write a review STRICTLY based on the plot provided.

**CRITICAL RULES:**
1. Write ONLY about information in the plot below
2. DO NOT add characters, scenes, or details not in the plot
3. DO NOT hallucinate or imagine extra story elements
4. If plot is brief, keep review proportionally brief
5. Length: 150-250 words maximum

**STYLE FOR 'Enthusiastic Casual':**
- Tone: Positive but balanced
- Language: MODERATE praise - ভালো লাগলো, বেশ ভালো, সুন্দর, মন্দ না
- Structure: 70% positives + 30% constructive criticism
- AVOID: অসাধারণ, দারুণ, অনবদ্য, মন ছুঁয়ে গেল (too enthusiastic)
- Include: তবে, একটু, কিন্তু (for balance)

**MOVIE PLOT (USE ONLY THIS):**
{movie_plot}

**EXAMPLE STYLE (for tone reference only, NOT content):**
{rag_context[:500]}

{reflection_feedback}

**Write a Bengali review discussing ONLY what's in the plot above. Be specific but don't invent details.**"""
        
        elif target_persona == "Die-hard Fan":
            full_prompt = f"""You are a professional Bengali movie reviewer. Write a review STRICTLY based on the plot provided.

**CRITICAL RULES:**
1. Write ONLY about information in the plot below
2. DO NOT add characters, scenes, or details not in the plot
3. DO NOT hallucinate or imagine extra story elements
4. If plot is brief, keep review proportionally brief
5. Length: 200-300 words maximum

**STYLE FOR 'Die-hard Fan':**
- Tone: Extremely enthusiastic and emotional
- Language: Superlatives - অসাধারণ, দারুণ, মন ছুঁয়ে গেল, অভূতপূর্ব
- Express deep emotional connection
- Use exclamations!

**MOVIE PLOT (USE ONLY THIS):**
{movie_plot}

**EXAMPLE STYLE (for tone reference only, NOT content):**
{rag_context[:500]}

{reflection_feedback}

**Write an enthusiastic Bengali review discussing ONLY what's in the plot above. Be specific but don't invent details.**"""
        
        else:  # Indifferent Casual
            full_prompt = f"""You are a professional Bengali movie reviewer. Write a review STRICTLY based on the plot provided.

**CRITICAL RULES:**
1. Write ONLY about information in the plot below
2. DO NOT add characters, scenes, or details not in the plot
3. DO NOT hallucinate or imagine extra story elements
4. Keep it VERY brief
5. Length: 80-120 words maximum

**STYLE FOR 'Indifferent Casual':**
- Tone: Brief, critical, unimpressed
- Language: Negative/neutral - সাধারণ, তেমন কিছু না, খারাপ
- Short sentences, minimal engagement

**MOVIE PLOT (USE ONLY THIS):**
{movie_plot}

**EXAMPLE STYLE (for tone reference only, NOT content):**
{rag_context[:500]}

{reflection_feedback}

**Write a brief, critical Bengali review discussing ONLY what's in the plot above. Don't invent details.**"""

        logger.info(f"[WRITER] Plot word count: {plot_word_count}")
        logger.info(f"[WRITER] Using {len(rag_context)} chars of RAG context")
        
        response = llm.generate_content(
            full_prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.7,  # Lower for more controlled output
                top_p=0.85,
                top_k=30
            )
        )
        generated_review = response.text.strip()
        
        logger.info(f"[WRITER] Raw output preview: {generated_review[:200]}...")
        
        # Apply post-processing filter for Enthusiastic Casual
        if target_persona == "Enthusiastic Casual":
            generated_review = filter_enthusiastic_casual(generated_review)
            logger.info(f"[WRITER] Applied Enthusiastic Casual filter")
        
        logger.info(f"[WRITER] Generated review ({len(generated_review)} chars)")
        
        return {
            "generated_review": generated_review,
            "generation_attempt": attempt
        }
    
    except Exception as e:
        logger.error(f"[WRITER] Exception: {e}", exc_info=True)
        return {
            "error_message": f"Writer error: {str(e)}",
            "generation_attempt": attempt
        }


# ============================================================
# NODE 3: CRITIC AGENT
# ============================================================

def critic_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Critic Agent: Validates review using BanglaBERT
    """
    # Handle both dict and Pydantic object
    generation_attempt = state['generation_attempt'] if isinstance(state, dict) else state.generation_attempt
    generated_review = state['generated_review'] if isinstance(state, dict) else state.generated_review
    target_persona = state['target_persona'] if isinstance(state, dict) else state.target_persona
    
    logger.info(f"[CRITIC] Validating review (attempt {generation_attempt})")
    
    try:
        validator_tool = get_validator_tool()
        
        # Create input
        val_input = ValidatorInput(
            review_text=generated_review,
            expected_persona=target_persona
        )
        
        # Validate
        output = validator_tool.run(val_input)
        
        if output.success:
            data = output.data
            
            # Get BanglaBERT prediction
            banglabert_persona = data['predicted_persona']
            banglabert_score = data['validation_score']
            
            # Apply Hybrid Validation (Neural + Linguistic)
            hybrid_result = hybrid_validation(
                review_text=generated_review,
                banglabert_persona=banglabert_persona,
                banglabert_score=banglabert_score,
                target_persona=target_persona
            )
            
            # Use hybrid prediction
            final_persona = hybrid_result['predicted_persona']
            final_score = hybrid_result['confidence']
            matches_target = hybrid_result['matches_target']
            
            # Use persona-specific threshold
            threshold = cfg.PERSONA_THRESHOLDS.get(target_persona, cfg.VALIDATION_THRESHOLD)
            passed = final_score >= threshold and matches_target
            
            logger.info(f"[CRITIC] BanglaBERT: {banglabert_persona} ({banglabert_score:.3f})")
            logger.info(f"[CRITIC] Linguistic: {hybrid_result['linguistic_prediction']} ({hybrid_result['linguistic_confidence']:.3f})")
            logger.info(f"[CRITIC] Hybrid Final: {final_persona} ({final_score:.3f}), Threshold: {threshold:.2f}, Passed: {passed}")
            
            return {
                "validation_score": final_score,
                "validation_passed": passed,
                "predicted_persona": final_persona,
                "confidence_scores": hybrid_result['hybrid_scores'],
                "banglabert_persona": banglabert_persona,
                "banglabert_score": banglabert_score,
                "linguistic_scores": hybrid_result['linguistic_scores']
            }
        else:
            logger.error(f"[CRITIC] Failed: {output.error}")
            return {
                "error_message": f"Validation failed: {output.error}"
            }
    
    except Exception as e:
        logger.error(f"[CRITIC] Exception: {e}", exc_info=True)
        return {
            "error_message": f"Critic error: {str(e)}"
        }


# ============================================================
# NODE 4: REFLECTOR AGENT
# ============================================================

def reflector_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Reflector Agent: Provides feedback for improvement
    """
    # Handle both dict and Pydantic object
    generation_attempt = state['generation_attempt'] if isinstance(state, dict) else state.generation_attempt
    validation_passed = state['validation_passed'] if isinstance(state, dict) else state.validation_passed
    max_retries = state['max_retries'] if isinstance(state, dict) else state.max_retries
    error_message = state.get('error_message', '') if isinstance(state, dict) else getattr(state, 'error_message', '')
    predicted_persona = state['predicted_persona'] if isinstance(state, dict) else state.predicted_persona
    target_persona = state['target_persona'] if isinstance(state, dict) else state.target_persona
    validation_score = state['validation_score'] if isinstance(state, dict) else state.validation_score
    generated_review = state['generated_review'] if isinstance(state, dict) else state.generated_review
    iteration_history = state.get('iteration_history', []) if isinstance(state, dict) else state.iteration_history
    
    logger.info(f"[REFLECTOR] Analyzing failure (attempt {generation_attempt})")
    
    try:
        # Check if should retry
        should_retry = (
            not validation_passed and 
            generation_attempt < max_retries and
            not error_message
        )
        
        if not should_retry:
            logger.info("[REFLECTOR] Max retries reached or error occurred")
            return {
                "should_retry": False,
                "workflow_complete": True
            }
        
        # Generate feedback
        feedback_parts = []
        
        # Persona mismatch
        if predicted_persona != target_persona:
            feedback_parts.append(
                f"⚠️ Persona Mismatch: Expected '{target_persona}' but got '{predicted_persona}'. "
                f"Adjust the tone and style to match '{target_persona}' characteristics."
            )
        
        # Low confidence
        threshold = cfg.PERSONA_THRESHOLDS.get(target_persona, cfg.VALIDATION_THRESHOLD)
        if validation_score < threshold:
            feedback_parts.append(
                f"⚠️ Low Confidence: Score {validation_score:.2f} < {threshold}. "
                f"Make the review MORE characteristic of '{target_persona}'."
            )
        
        # Specific persona guidance with Bengali examples
        persona_guidance = {
            "Die-hard Fan": "Use MORE emotional language, superlatives (অসাধারণ, অনবদ্য, মন ছুঁয়ে গেল), and detailed praise. Show EXTREME enthusiasm with exclamations!",
            "Enthusiastic Casual": "AVOID Die-hard Fan words (অসাধারণ, দারুণ, মন ছুঁয়ে গেল). Use MODERATE words (ভালো লাগলো, বেশ ভালো, সুন্দর). Mention BOTH positives AND minor negatives with 'তবে', 'কিন্তু', 'একটু'.",
            "Indifferent Casual": "Be BRIEF and critical. Use negative/neutral words (সাধারণ, তেমন কিছু না, খারাপ). Focus on negatives. Keep it SHORT (100-150 words). Show minimal engagement."
        }
        
        feedback_parts.append(
            f"💡 Guidance: {persona_guidance.get(target_persona, '')}"
        )
        
        feedback = "\n\n".join(feedback_parts)
        
        logger.info(f"[REFLECTOR] Feedback generated, retry: {should_retry}")
        
        # Add to history
        iteration_record = {
            "attempt": generation_attempt,
            "review": generated_review,
            "score": validation_score,
            "passed": validation_passed,
            "predicted": predicted_persona,
            "feedback": feedback
        }
        
        history = list(iteration_history) if iteration_history else []
        history.append(iteration_record)
        
        return {
            "reflection_feedback": feedback,
            "should_retry": should_retry,
            "iteration_history": history
        }
    
    except Exception as e:
        logger.error(f"[REFLECTOR] Exception: {e}", exc_info=True)
        return {
            "error_message": f"Reflector error: {str(e)}",
            "should_retry": False,
            "workflow_complete": True
        }
