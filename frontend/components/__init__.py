"""Frontend components package for UAE Legal Assistant."""

from frontend.components.styling import apply_custom_styling, set_page_config, render_header
from frontend.components.chat_history import (
    initialize_chat_history,
    display_chat_messages,
    add_message,
    clear_chat_history,
    export_chat_history,
    ChatHistoryManager,
)
from frontend.components.sidebar import (
    render_sidebar,
    get_sidebar_settings,
    render_faq_section,
    render_chat_management_section,
    render_about_section,
)
from frontend.components.utils import (
    run_legal_query,
    format_answer_with_metadata,
    show_info_message,
    show_warning_message,
    show_success_message,
)

__all__ = [
    "apply_custom_styling",
    "set_page_config",
    "render_header",
    "initialize_chat_history",
    "display_chat_messages",
    "add_message",
    "clear_chat_history",
    "export_chat_history",
    "ChatHistoryManager",
    "render_sidebar",
    "get_sidebar_settings",
    "render_faq_section",
    "render_chat_management_section",
    "render_about_section",
    "run_legal_query",
    "format_answer_with_metadata",
    "show_info_message",
    "show_warning_message",
    "show_success_message",
]
