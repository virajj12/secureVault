"""
SecureVault — User Portal
User login + account dashboard with details, login history, and 2FA placeholder.
"""

import streamlit as st
from datetime import datetime
from utils.styles import inject_custom_css, inject_page_animations
from utils.db import init_auth_db, seed_default_users, get_user_login_history
from utils.auth import init_session_state, login, logout, is_authenticated, get_current_user

# ─── Page Config ────────────────────────────────────────────
st.set_page_config(
    page_title="User Portal — SecureVault",
    page_icon="👤",
    layout="wide"
)

init_auth_db()
seed_default_users()
init_session_state()
inject_custom_css()

# ─── Sidebar ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">👤</div>
        <div class="sv-gradient-text" style="font-size: 1.1rem; font-weight: 800;">User Portal</div>
        <div style="color: #555555; font-size: 0.7rem; letter-spacing: 2px; text-transform: uppercase; margin-top: 0.2rem;">Personal Dashboard</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    if is_authenticated("user"):
        user = get_current_user()
        st.markdown(f"""
        <div style="text-align:center; padding: 0.5rem;">
            <div class="sv-avatar" style="background: {user['avatar_color']}; margin: 0 auto 0.5rem;">
                {user['full_name'][0].upper()}
            </div>
            <div style="font-weight: 600; color: #e0e0e0;">{user['full_name']}</div>
            <span class="sv-badge sv-badge-cyan">USER</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("")
        if st.button("🚪 Logout", use_container_width=True, key="sidebar_logout_user"):
            logout()
            st.rerun()


# ═══════════════════════════════════════════════════════════
# USER LOGIN (shown when not authenticated)
# ═══════════════════════════════════════════════════════════
if not is_authenticated("user"):
    # If logged in as admin, show access message
    if is_authenticated("admin"):
        st.markdown("""
        <div style="text-align: center; padding: 4rem 1rem; animation: fadeInUp 0.7s ease-out both;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">👤</div>
            <div style="font-size: 2rem; font-weight: 900; background: linear-gradient(135deg, #ffffff, #b0b0b0, #808080); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">User Portal</div>
            <div style="color: #a0a0a0; font-size: 1.05rem; margin-top: 0.5rem;">
                You are currently logged in as an <strong>Administrator</strong>.<br>
                Please log out first to access the User Portal.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # User Login Form
    st.markdown("""
    <div style="text-align: center; padding: 2rem 1rem 1rem; animation: fadeInUp 0.7s ease-out both;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">👤</div>
        <div style="font-size: 2rem; font-weight: 900; background: linear-gradient(135deg, #ffffff, #b0b0b0, #808080); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">User Login</div>
        <div style="color: #a0a0a0; margin-top: 0.5rem; margin-bottom: 0.5rem;">
            Access your personal dashboard and account settings.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sv-login-card sv-fade-up sv-delay-2">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("user_login_form", clear_on_submit=False):
            st.markdown("""
            <div class="sv-section-heading" style="text-align: center;">
                🔑 Account Access
            </div>
            """, unsafe_allow_html=True)

            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")

            st.markdown("")
            submitted = st.form_submit_button("🔓  Sign In", use_container_width=True)

            if submitted:
                if username and password:
                    if login(username, password, "user"):
                        st.success("✅ Welcome back! Loading your dashboard...")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials. Please try again.")
                else:
                    st.warning("⚠️ Please enter both username and password.")

        st.markdown("""
        <div style="text-align: center; margin-top: 0.5rem;">
            <span class="sv-2fa-badge">🔒 2FA Coming Soon</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Demo credentials hint
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem;">
        <div class="sv-glass" style="display: inline-block; padding: 1rem 2rem;">
            <div style="color: #555555; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.4rem;">Demo Credentials</div>
            <div style="color: #a0a0a0; font-size: 0.85rem;">
                <code style="color: #d0d0d0; background: rgba(200,200,200,0.06); padding: 0.15rem 0.4rem; border-radius: 4px;">john_doe</code> /
                <code style="color: #d0d0d0; background: rgba(200,200,200,0.06); padding: 0.15rem 0.4rem; border-radius: 4px;">user123</code>
                &nbsp;&nbsp;or&nbsp;&nbsp;
                <code style="color: #b0b0b0; background: rgba(200,200,200,0.06); padding: 0.15rem 0.4rem; border-radius: 4px;">jane_smith</code> /
                <code style="color: #b0b0b0; background: rgba(200,200,200,0.06); padding: 0.15rem 0.4rem; border-radius: 4px;">user456</code>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    inject_page_animations()
    st.stop()


# ═══════════════════════════════════════════════════════════
# USER DASHBOARD (shown when authenticated as user)
# ═══════════════════════════════════════════════════════════

user = get_current_user()

# ─── Header ─────────────────────────────────────────────────
st.markdown(f"""
<div style="padding: 0.5rem 0 1rem; animation: fadeInUp 0.7s ease-out both;">
    <div style="font-size: 2rem; font-weight: 900; background: linear-gradient(135deg, #ffffff, #b0b0b0, #808080); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.2rem;">My Dashboard</div>
    <div style="color: #a0a0a0; font-size: 0.9rem; margin: 0;">
        Welcome back, <strong>{user['full_name']}</strong>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Dashboard Tabs ─────────────────────────────────────────
tab_account, tab_security, tab_history = st.tabs(["👤 Account Details", "🔐 Security Settings", "📋 Login History"])

# ── Tab 1: Account Details ─────────────────────────────────
with tab_account:
    acol1, acol2 = st.columns([1, 2])

    with acol1:
        st.markdown(f"""
        <div class="sv-glass" style="text-align: center; padding: 2rem; animation: fadeInUp 0.7s ease-out both;">
            <div class="sv-avatar sv-avatar-lg" style="background: {user['avatar_color']}; margin: 0 auto 1rem;">
                {user['full_name'][0].upper()}
            </div>
            <div style="font-weight: 700; font-size: 1.3rem; color: #e0e0e0; margin-bottom: 0.3rem;">
                {user['full_name']}
            </div>
            <span class="sv-badge sv-badge-cyan">USER</span>
            <div style="margin-top: 1rem;">
                <div class="sv-ring" style="width: 80px; height: 80px; font-size: 1rem; margin: 0 auto;">
                    <span style="z-index: 1;">A+</span>
                </div>
                <div style="color: #555555; font-size: 0.78rem; margin-top: 0.5rem; text-transform: uppercase; letter-spacing: 1px;">Security Score</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with acol2:
        st.markdown(f"""
        <div class="sv-glass" style="animation: fadeInUp 0.7s ease-out 0.2s both;">
            <div class="sv-section-heading">Account Information</div>
        </div>
        """, unsafe_allow_html=True)

        # Use individual st.markdown calls for each field to avoid Streamlit HTML sanitizer issues
        info_fields = [
            ("Username", f"@{user['username']}"),
            ("Email", user['email']),
            ("Full Name", user['full_name']),
            ("Role", "USER"),
            ("Account Created", user['created_at'][:10] if user['created_at'] else 'N/A'),
            ("Last Login", user['last_login'] or 'First login'),
        ]

        icol1, icol2 = st.columns(2)
        for idx, (label, value) in enumerate(info_fields):
            target_col = icol1 if idx % 2 == 0 else icol2
            with target_col:
                if label == "Role":
                    st.markdown(f"""
                    <div style="padding: 0.8rem; border-bottom: 1px solid rgba(200,200,200,0.08);">
                        <div style="color: #555555; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.3rem;">{label}</div>
                        <span class="sv-badge sv-badge-cyan">USER</span>
                    </div>
                    """, unsafe_allow_html=True)
                elif label in ("Account Created", "Last Login"):
                    st.markdown(f"""
                    <div style="padding: 0.8rem; border-bottom: 1px solid rgba(200,200,200,0.08);">
                        <div style="color: #555555; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.3rem;">{label}</div>
                        <div style="color: #c0c0c0; font-family: 'JetBrains Mono', monospace; font-size: 0.88rem;">{value}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="padding: 0.8rem; border-bottom: 1px solid rgba(200,200,200,0.08);">
                        <div style="color: #555555; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.3rem;">{label}</div>
                        <div style="color: #e0e0e0; font-weight: 500;">{value}</div>
                    </div>
                    """, unsafe_allow_html=True)

# ── Tab 2: Security Settings ──────────────────────────────
with tab_security:
    st.markdown("""
    <div style="margin-bottom: 1.5rem; animation: fadeInUp 0.7s ease-out both;">
        <div style="color: #d0d0d0; font-weight: 600; font-size: 1.17rem; margin-bottom: 0.3rem;">Security & Privacy</div>
        <div style="color: #a0a0a0; font-size: 0.88rem;">
            Manage your account security settings and authentication preferences.
        </div>
    </div>
    """, unsafe_allow_html=True)

    sec1, sec2 = st.columns(2)

    with sec1:
        # Password section
        st.markdown("""
        <div class="sv-glass" style="animation: fadeInUp 0.7s ease-out both;">
            <div class="sv-section-heading">Password</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="padding: 0.5rem 0;">
            <div style="color: #e0e0e0; font-weight: 500; margin-bottom: 0.3rem;">Password Status</div>
            <div style="color: #a0a0a0; font-size: 0.85rem;">Your password is hashed with PBKDF2-HMAC-SHA256 (100,000 iterations)</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="margin-top: 0.5rem;"><span class="sv-badge sv-badge-green">SECURE</span></div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(200,200,200,0.08);">
            <div style="color: #555555; font-size: 0.82rem;">🔒 Password change functionality will be available in a future update.</div>
        </div>
        """, unsafe_allow_html=True)

    with sec2:
        # 2FA section
        tfa_enabled = user.get("two_fa_enabled", 0)
        st.markdown("""
        <div class="sv-glass" style="animation: fadeInUp 0.7s ease-out 0.2s both;">
            <div class="sv-section-heading">Two-Factor Authentication (2FA)</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="padding: 0.5rem 0;">
            <div style="color: #e0e0e0; font-weight: 500; margin-bottom: 0.3rem;">TOTP Authentication</div>
            <div style="color: #a0a0a0; font-size: 0.85rem;">Add an extra layer of security with time-based one-time passwords.</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(200,200,200,0.08);">
            <span class="sv-2fa-badge">🔒 Coming Soon — TOTP integration is being developed</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="margin-top: 1rem; padding: 0.8rem; background: rgba(200, 200, 200, 0.03); border-radius: 12px; border: 1px dashed rgba(200,200,200,0.10);">
            <div style="color: #555555; font-size: 0.82rem; line-height: 1.6;">
                <strong style="color: #a0a0a0;">Planned features:</strong><br>
                • QR code generation for authenticator apps<br>
                • Backup recovery codes<br>
                • Per-session 2FA verification<br>
                • Hardware key support (FIDO2)
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Session security
    st.markdown("""
    <div class="sv-glass" style="margin-top: 1rem; animation: fadeInUp 0.7s ease-out 0.3s both;">
        <div class="sv-section-heading">Active Session</div>
    </div>
    """, unsafe_allow_html=True)
    scol1, scol2 = st.columns([4, 1])
    with scol1:
        st.markdown("""
        <div style="color: #e0e0e0; font-weight: 500; margin-bottom: 0.3rem;">Current Session</div>
        <div style="color: #a0a0a0; font-size: 0.85rem;">Secured with session-state isolation. No cookies stored.</div>
        """, unsafe_allow_html=True)
    with scol2:
        st.markdown('<span class="sv-badge sv-badge-green">● ACTIVE</span>', unsafe_allow_html=True)

# ── Tab 3: Login History ──────────────────────────────────
with tab_history:
    st.markdown("""
    <div style="margin-bottom: 1rem; animation: fadeInUp 0.7s ease-out both;">
        <div style="color: #d0d0d0; font-weight: 600; font-size: 1.17rem; margin-bottom: 0.3rem;">Your Login History</div>
        <div style="color: #a0a0a0; font-size: 0.88rem;">
            Review your recent authentication activity. Contact an admin if you see suspicious entries.
        </div>
    </div>
    """, unsafe_allow_html=True)

    history = get_user_login_history(user["username"], 20)

    if history:
        # Table header
        st.markdown("""
        <div class="sv-glass" style="padding: 0; overflow: hidden;">
            <div style="display: flex; background: rgba(200, 200, 200, 0.03); border-bottom: 2px solid rgba(200, 200, 200, 0.08);">
                <div style="flex: 2; padding: 0.75rem 0.8rem; color: #555555; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Timestamp</div>
                <div style="flex: 1; padding: 0.75rem 0.8rem; color: #555555; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">IP Address</div>
                <div style="flex: 1; padding: 0.75rem 0.8rem; color: #555555; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Status</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Render each row individually to avoid Streamlit HTML sanitizer issues
        for i, log in enumerate(history):
            status_badge = (
                '<span class="sv-badge sv-badge-green">SUCCESS</span>'
                if log["status"] == "success"
                else '<span class="sv-badge sv-badge-red">FAILED</span>'
            )
            delay_class = f"sv-delay-{min(i + 1, 10)}"
            st.markdown(f"""
            <div class="sv-fade-up {delay_class}" style="display: flex; border-bottom: 1px solid rgba(200, 200, 200, 0.04); align-items: center;">
                <div style="flex: 2; padding: 0.65rem 0.8rem; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #c0c0c0;">
                    {log['login_time']}
                </div>
                <div style="flex: 1; padding: 0.65rem 0.8rem; color: #555555; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem;">
                    {log['ip_address']}
                </div>
                <div style="flex: 1; padding: 0.65rem 0.8rem;">{status_badge}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="text-align: right; padding: 0.5rem 0; color: #555555; font-size: 0.78rem;">
            Showing {len(history)} entries
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("📭 No login history yet. Your activity will appear here after your next login.")

inject_page_animations()
