"""Chat history management for the UAE Legal Assistant."""
import streamlit as st
import json
from datetime import datetime
from pathlib import Path


class ChatHistoryManager:
    """Manages conversation history for the application."""
    
    def __init__(self, storage_dir: str = ".chat_history"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
    
    def save_conversation(self, messages: list, title: str = None) -> str:
        """Save a conversation to disk."""
        if not messages:
            return None
        
        if title is None:
            title = f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.storage_dir / filename
        
        data = {
            "title": title,
            "timestamp": datetime.now().isoformat(),
            "messages": messages
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return str(filepath)
    
    def load_conversation(self, filepath: str) -> dict:
        """Load a conversation from disk."""
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def list_conversations(self) -> list:
        """List all saved conversations."""
        conversations = []
        for filepath in sorted(self.storage_dir.glob("*.json"), reverse=True):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                conversations.append({
                    "path": str(filepath),
                    "title": data.get("title", "Untitled"),
                    "timestamp": data.get("timestamp", ""),
                    "messages_count": len(data.get("messages", []))
                })
            except Exception:
                continue
        return conversations
    
    def delete_conversation(self, filepath: str) -> bool:
        """Delete a saved conversation."""
        try:
            Path(filepath).unlink()
            return True
        except Exception:
            return False


def initialize_chat_history():
    """Initialize chat history in session state."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_manager" not in st.session_state:
        st.session_state.chat_manager = ChatHistoryManager()


def display_chat_messages():
    """Display all messages in the chat history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def add_message(role: str, content: str):
    """Add a message to the chat history."""
    st.session_state.messages.append({
        "role": role,
        "content": content
    })


def clear_chat_history():
    """Clear the current chat history."""
    st.session_state.messages = []
    st.rerun()


def export_chat_history():
    """Export current chat history as markdown."""
    if not st.session_state.messages:
        return ""
    
    md = f"# Chat History\n\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    for msg in st.session_state.messages:
        role = msg["role"].upper()
        md += f"## {role}\n\n{msg['content']}\n\n"
    
    return md
