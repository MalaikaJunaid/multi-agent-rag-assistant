"""Sidebar components for the UAE Legal Assistant."""
import streamlit as st
from frontend.components.chat_history import (
    export_chat_history, clear_chat_history, ChatHistoryManager
)


# FAQ data
FAQ_DATA = [
    {
        "question": "What is the maximum probation period for an employee under UAE law?",
        "category": "Labor Law"
    },
    {
        "question": "What are the rules for annual leave in UAE?",
        "category": "Labor Law"
    },
    {
        "question": "How is sick leave calculated under UAE labor law?",
        "category": "Labor Law"
    },
    {
        "question": "What are the maternity leave provisions in UAE?",
        "category": "Labor Law"
    },
    {
        "question": "What is the legal minimum wage in UAE?",
        "category": "Labor Law"
    },
    {
        "question": "How are personal data rights protected under UAE law?",
        "category": "Data Protection"
    },
    {
        "question": "What are the regulations for data processing and storage?",
        "category": "Data Protection"
    },
    {
        "question": "What are employee privacy rights in UAE?",
        "category": "Labor Law"
    },
]


def render_sidebar():
    """Render the main sidebar with all controls and information."""
    with st.sidebar:
        st.markdown("### ⚙️ Assistant Settings")
        st.divider()
        
        # Temperature setting
        temperature = st.slider(
            "Response Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.1,
            help="Lower = more deterministic, Higher = more creative"
        )
        st.session_state.temperature = temperature
        
        # Recursion limit
        recursion_limit = st.slider(
            "Max Verification Retries",
            min_value=1,
            max_value=10,
            value=5,
            help="Maximum times the fact-checker can retry the answer"
        )
        st.session_state.recursion_limit = recursion_limit
        
        st.divider()
        
        # FAQ section
        render_faq_section()
        
        st.divider()
        
        # Chat management
        render_chat_management_section()
        
        st.divider()
        
        # About section
        render_about_section()


def render_faq_section():
    """Render the FAQ section in the sidebar."""
    st.markdown("### 📋 Common Questions")
    
    # Category filter
    categories = ["All"] + list(set(faq["category"] for faq in FAQ_DATA))
    selected_category = st.selectbox(
        "Filter by category",
        categories,
        label_visibility="collapsed"
    )
    
    # Filter FAQ
    filtered_faq = (
        FAQ_DATA if selected_category == "All"
        else [faq for faq in FAQ_DATA if faq["category"] == selected_category]
    )
    
    # Display FAQ with quick-select buttons
    for idx, faq in enumerate(filtered_faq):
        col1, col2 = st.columns([0.1, 0.9])
        with col1:
            st.caption(f"Q{idx + 1}")
        with col2:
            if st.button(
                faq["question"],
                key=f"faq_btn_{idx}",
                use_container_width=True
            ):
                st.session_state.quick_question = faq["question"]
                st.rerun()


def render_chat_management_section():
    """Render chat history and management controls."""
    st.markdown("### 💬 Conversation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export Chat", use_container_width=True):
            export_text = export_chat_history()
            st.download_button(
                "⬇️ Download",
                export_text,
                "chat_history.md",
                "text/markdown",
                use_container_width=True
            )
    
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            clear_chat_history()
    
    # Show recent conversations
    try:
        manager = ChatHistoryManager()
        conversations = manager.list_conversations()
        
        if conversations:
            st.markdown("**Recent Conversations:**")
            for conv in conversations[:3]:  # Show last 3
                col1, col2 = st.columns([0.85, 0.15])
                with col1:
                    if st.button(
                        f"📄 {conv['title'][:30]}...",
                        key=f"conv_{conv['path']}",
                        use_container_width=True
                    ):
                        loaded = manager.load_conversation(conv['path'])
                        st.session_state.messages = loaded.get('messages', [])
                        st.rerun()
                with col2:
                    if st.button("🗑", key=f"del_{conv['path']}", help="Delete"):
                        manager.delete_conversation(conv['path'])
                        st.rerun()
    except Exception:
        pass


def render_about_section():
    """Render the about section."""
    st.markdown("### ℹ️ About")
    
    st.markdown("""
    **UAE Legal Assistant** is an AI-powered system that:
    - 🔍 Searches official UAE legal documents
    - ✅ Verifies answers for accuracy
    - 🔄 Retries if needed to ensure correctness
    - 📋 Provides citations and context
    
    **Laws covered:**
    - Federal Labor Law
    - Data Protection Law
    
    **Note:** This is for informational purposes. Consult official legal sources for critical decisions.
    """)
    
    st.markdown(
        "---\n*Last updated: 2026-09-18*"
    )


def get_sidebar_settings() -> dict:
    """Get current sidebar settings as a dictionary."""
    return {
        "temperature": st.session_state.get("temperature", 0.0),
        "recursion_limit": st.session_state.get("recursion_limit", 5),
    }
