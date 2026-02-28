"""
SecureVault — Authentication Module
Handles login, logout, session state, and credential verification.
"""

import streamlit as st
from utils.db import get_user, hash_password, record_login, update_last_login


def init_session_state():
    """Initialize authentication session state keys."""
    defaults = {
        "authenticated": False,
        "user": None,
        "role": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def verify_credentials(username: str, password: str, role: str) -> dict | None:
    """
    Verify username/password against the database for a given role.
    Returns the user dict on success, None on failure.
    """
    user = get_user(username, role)
    if user is None:
        return None

    pw_hash, _ = hash_password(password, user["password_salt"])
    if pw_hash == user["password_hash"]:
        return user
    return None


def login(username: str, password: str, role: str) -> bool:
    """
    Attempt login. Updates session state and records the attempt.
    Returns True on success, False on failure.
    """
    init_session_state()
    user = verify_credentials(username, password, role)

    if user:
        st.session_state.authenticated = True
        st.session_state.user = {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"],
            "created_at": user["created_at"],
            "last_login": user["last_login"],
            "two_fa_enabled": user["two_fa_enabled"],
            "avatar_color": user["avatar_color"],
        }
        st.session_state.role = user["role"]

        # Record successful login
        record_login(user["id"], username, role, "success")
        update_last_login(user["id"])
        return True
    else:
        # Record failed login attempt
        record_login(None, username, role, "failed")
        return False


def logout():
    """Clear session state and log the user out."""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.role = None


def is_authenticated(required_role: str = None) -> bool:
    """Check if user is authenticated (optionally with a specific role)."""
    init_session_state()
    if not st.session_state.authenticated:
        return False
    if required_role and st.session_state.role != required_role:
        return False
    return True


def get_current_user() -> dict | None:
    """Get the currently logged-in user dict."""
    init_session_state()
    return st.session_state.user


def require_auth(role: str) -> bool:
    """
    Gate function for pages. Returns True if authorized, displays error otherwise.
    """
    if not is_authenticated(role):
        return False
    return True
