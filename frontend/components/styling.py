"""Styling and theme configuration for the UAE Legal Assistant."""
import streamlit as st


def apply_custom_styling():
    """Apply custom CSS styling to the Streamlit app."""
    st.markdown("""
    <style>
        /* Main title styling */
        h1 {
            color: #1e3a8a;
            font-weight: 700;
            padding-bottom: 10px;
            border-bottom: 3px solid #3b82f6;
        }
        
        /* Chat message styling */
        .stChatMessage {
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
        }
        
        /* User message */
        .stChatMessage[data-testid="chatAvatarIcon-user"] {
            background-color: #f0f9ff;
        }
        
        /* Assistant message */
        .stChatMessage[data-testid="chatAvatarIcon-assistant"] {
            background-color: #f8fafc;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        }
        
        [data-testid="stSidebar"] > div:first-child {
            color: white;
        }
        
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: white;
            margin-top: 20px;
        }
        
        [data-testid="stSidebar"] p {
            color: #e0e7ff;
        }
        
        /* Button styling */
        .stButton > button {
            width: 100%;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }
        
        /* Info boxes */
        .info-box {
            background-color: #e0f2fe;
            border-left: 4px solid #0284c7;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        
        .warning-box {
            background-color: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        
        .success-box {
            background-color: #dcfce7;
            border-left: 4px solid #16a34a;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
    </style>
    """, unsafe_allow_html=True)


def set_page_config():
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title="UAE Legal Assistant",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "About": "UAE Legal Assistant - AI-powered legal information system"
        }
    )


def render_header():
    """Render the main header of the app."""
    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        st.title("⚖️ UAE Legal Assistant")
    with col2:
        st.write("")
    
    st.markdown(
        "**Ask questions about UAE Federal Labor Law and Data Protection Law**",
        help="This assistant uses AI to search and verify legal information from official UAE law documents."
    )
    st.divider()
