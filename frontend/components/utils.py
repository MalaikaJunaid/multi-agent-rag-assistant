"""Utility functions for the UAE Legal Assistant."""
import streamlit as st
from typing import Optional, Dict, Any


def run_legal_query(graph_app, query: str, config: Dict[str, Any]) -> Optional[str]:
    """
    Execute a legal query through the LangGraph application.
    
    Args:
        graph_app: The compiled LangGraph application
        query: User's legal question
        config: Configuration dictionary with recursion_limit and other settings
    
    Returns:
        The synthesized answer or an error message
    """
    initial_state = {
        "query": query,
        "messages": [],
        "retrieved_documents": [],
        "synthesis": "",
        "is_factually_correct": False
    }
    
    try:
        final_state = graph_app.invoke(initial_state, config={"recursion_limit": config.get("recursion_limit", 5)})
        return final_state.get("synthesis", "No answer generated")
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "rate limit" in error_msg.lower():
            return "⚠️ **Rate Limited:** Too many requests. Please wait a moment and try again."
        elif "401" in error_msg or "unauthorized" in error_msg.lower():
            return "⚠️ **Authentication Error:** API credentials not configured. Check your OPENROUTER_API_KEY."
        else:
            return f"⚠️ **Error:** {error_msg[:200]}"


def render_loading_spinner():
    """Render a custom loading message with spinner."""
    st.markdown("🔍 Searching legal documents and verifying answers...")


def format_answer_with_metadata(answer: str, query: str) -> str:
    """
    Format the answer with metadata about the query.
    
    Args:
        answer: The AI-generated answer
        query: The original user query
    
    Returns:
        Formatted answer with metadata
    """
    metadata = f"""
    <div class="info-box">
    <strong>Query:</strong> {query}
    </div>
    """
    return metadata + answer


def show_info_message(title: str, message: str):
    """Display an info message box."""
    st.markdown(f"""
    <div class="info-box">
    <strong>{title}</strong><br>
    {message}
    </div>
    """, unsafe_allow_html=True)


def show_warning_message(title: str, message: str):
    """Display a warning message box."""
    st.markdown(f"""
    <div class="warning-box">
    <strong>⚠️ {title}</strong><br>
    {message}
    </div>
    """, unsafe_allow_html=True)


def show_success_message(title: str, message: str):
    """Display a success message box."""
    st.markdown(f"""
    <div class="success-box">
    <strong>✅ {title}</strong><br>
    {message}
    </div>
    """, unsafe_allow_html=True)
