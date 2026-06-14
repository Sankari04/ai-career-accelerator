"""
session_state.py
Centralized session state initialization and helpers.
All module results are stored here so they persist across navigation.
"""

import streamlit as st

# Keys used across all modules
SESSION_KEYS = {
    "resume":   {"content": None, "pdf": None, "docx": None},
    "cover":    {"content": None, "pdf": None, "docx": None},
    "portfolio":{"text": None, "html": None, "name": None},
    "ats":      {"score": None, "strengths": None, "weaknesses": None,
                 "keywords": None, "suggestions": None,
                 "match_pct": None, "missing": None, "match_suggestions": None},
    "roadmap":  {"goal": None, "content": None},
    "linkedin": {"headlines": None, "about": None, "keywords": None,
                 "original_headline": None},
}


def init_session_state():
    """Call once at app startup to ensure all keys exist."""
    for module, defaults in SESSION_KEYS.items():
        key = f"ss_{module}"
        if key not in st.session_state:
            st.session_state[key] = dict(defaults)  # shallow copy of defaults


def get(module: str) -> dict:
    """Return the session-state dict for a module."""
    return st.session_state[f"ss_{module}"]


def set_value(module: str, field: str, value):
    """Set a single field inside a module's session dict."""
    st.session_state[f"ss_{module}"][field] = value


def has_result(module: str, field: str = "content") -> bool:
    """Return True if the module already has a stored result."""
    data = st.session_state.get(f"ss_{module}", {})
    return data.get(field) is not None
