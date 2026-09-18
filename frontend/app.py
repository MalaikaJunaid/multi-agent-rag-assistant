import streamlit as st
import sys
from pathlib import Path

# Add project root to the system path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from backend.main import app as graph_app
from frontend.components import (
    set_page_config,
    apply_custom_styling,
    render_header,
    initialize_chat_history,
    display_chat_messages,
    add_message,
    render_sidebar,
    get_sidebar_settings,
)


# ===== INITIALIZATION =====
set_page_config()
apply_custom_styling()
initialize_chat_history()


# ===== MAIN LAYOUT =====
render_header()
render_sidebar()

# Main chat area
chat_container = st.container()

# Handle quick question from sidebar FAQ
if "quick_question" in st.session_state and st.session_state.quick_question:
    prompt = st.session_state.quick_question
    st.session_state.quick_question = None
else:
    prompt = None

# Display existing chat messages
with chat_container:
    display_chat_messages()

# Accept user input
if user_input := st.chat_input("E.g., What are the rules for annual leave?"):
    prompt = user_input

# Process the prompt if available
if prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    add_message("user", prompt)

    # Generate and display the assistant's response
    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching legal documents and verifying facts..."):
            initial_state = {
                "query": prompt,
                "messages": [],
                "retrieved_documents": [],
                "synthesis": "",
                "is_factually_correct": False
            }
            
            settings = get_sidebar_settings()
            
            try:
                # Cap the execution at 5 steps to prevent infinite API loops
                final_state = graph_app.invoke(initial_state, config={"recursion_limit": settings.get("recursion_limit", 5)})
                answer = final_state["synthesis"]
                sources = final_state.get("retrieved_documents", [])
                
                st.markdown(answer)
                
                # Display the retrieved documents in an expander below the answer
                if sources:
                    with st.expander("📄 View Referenced Legal Text"):
                        for idx, doc in enumerate(sources):
                            st.info(f"**Chunk {idx+1}:**\n\n{doc}")
                            
            except Exception as e:
                error_msg = str(e)
                # Catch the recursion error specifically by checking the string
                if "Recursion limit" in error_msg:
                    answer = "⚠️ **Verification Failed:** The AI models could not synthesize a strictly verified answer within the retry limit. This occasionally happens with free routing models. Please try rephrasing your question."
                else:
                    answer = f"⚠️ **System Error:** {error_msg}"
                
                st.error(answer)
    
    add_message("assistant", answer)