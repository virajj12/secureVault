"""
SecureVault — Admin Portal
Admin login + dashboard with login activity logs, timestamps, and user management.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from utils.styles import inject_custom_css, inject_page_animations
from utils.db import init_auth_db, seed_default_users, get_login_logs, get_login_stats, get_all_users
from utils.auth import init_session_state, login, logout, is_authenticated, get_current_user

# ─── Page Config ────────────────────────────────────────────
st.set_page_config(
    page_title="Admin Portal — SecureVault",
    page_icon="🛡️",
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
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🛡️</div>
        <div class="sv-gradient-text" style="font-size: 1.1rem; font-weight: 800;">Admin Portal</div>
        <div style="color: #555555; font-size: 0.7rem; letter-spacing: 2px; text-transform: uppercase; margin-top: 0.2rem;">Restricted Access</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    if is_authenticated("admin"):
        user = get_current_user()
        st.markdown(f"""
        <div style="text-align:center; padding: 0.5rem;">
            <div class="sv-avatar" style="background: {user['avatar_color']}; margin: 0 auto 0.5rem;">
                {user['full_name'][0].upper()}
            </div>
            <div style="font-weight: 600; color: #e0e0e0;">{user['full_name']}</div>
            <span class="sv-badge sv-badge-purple">ADMIN</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("")
        if st.button("🚪 Logout", use_container_width=True, key="sidebar_logout"):
            logout()
            st.rerun()


# ═══════════════════════════════════════════════════════════
# ADMIN LOGIN (shown when not authenticated)
# ═══════════════════════════════════════════════════════════
if not is_authenticated("admin"):
    # If logged in as user, show access denied
    if is_authenticated("user"):
        st.markdown("""
        <div style="text-align: center; padding: 4rem 1rem; animation: fadeInUp 0.7s ease-out both;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">⛔</div>
            <div style="font-size: 2rem; font-weight: 900; background: linear-gradient(135deg, #ffffff, #b0b0b0, #808080); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Access Restricted</div>
            <div style="color: #a0a0a0; font-size: 1.05rem; margin-top: 0.5rem;">
                This portal requires <strong>Administrator</strong> credentials.<br>
                You are currently logged in as a <strong>User</strong>.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # Admin Login Form
    st.markdown("""
    <div style="text-align: center; padding: 2rem 1rem 1rem; animation: fadeInUp 0.7s ease-out both;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">🛡️</div>
        <div style="font-size: 2rem; font-weight: 900; background: linear-gradient(135deg, #ffffff, #b0b0b0, #808080); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Administrator Login</div>
        <div style="color: #a0a0a0; margin-top: 0.5rem; margin-bottom: 0.5rem;">
            Authorized personnel only. All access attempts are logged.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sv-login-card sv-fade-up sv-delay-2">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("admin_login_form", clear_on_submit=False):
            st.markdown("""
            <div class="sv-section-heading" style="text-align: center;">
                🔐 Secure Authentication
            </div>
            """, unsafe_allow_html=True)

            username = st.text_input("Username", placeholder="Enter admin username")
            password = st.text_input("Password", type="password", placeholder="Enter password")

            st.markdown("")
            submitted = st.form_submit_button("🔓  Authenticate", use_container_width=True)

            if submitted:
                if username and password:
                    if login(username, password, "admin"):
                        st.success("✅ Authentication successful! Loading dashboard...")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials or insufficient privileges.")
                else:
                    st.warning("⚠️ Please enter both username and password.")

        st.markdown("""
        <div style="text-align: center; margin-top: 0.5rem;">
            <span class="sv-2fa-badge">🔒 2FA Coming Soon</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    inject_page_animations()
    st.stop()


# ═══════════════════════════════════════════════════════════
# ADMIN DASHBOARD (shown when authenticated as admin)
# ═══════════════════════════════════════════════════════════

user = get_current_user()
stats = get_login_stats()

# ─── Header ─────────────────────────────────────────────────
st.markdown(f"""
<div style="padding: 0.5rem 0 1rem; animation: fadeInUp 0.7s ease-out both;">
    <div style="font-size: 2rem; font-weight: 900; background: linear-gradient(135deg, #ffffff, #b0b0b0, #808080); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.2rem;">Command Center</div>
    <div style="color: #a0a0a0; font-size: 0.9rem; margin: 0;">
        Welcome back, <strong>{user['full_name']}</strong> · Last updated: {datetime.now().strftime("%H:%M:%S")}
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Stats Cards ────────────────────────────────────────────
st.markdown('<div class="sv-observe">', unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Total Users", stats["total_users"], delta=None)
with m2:
    st.metric("Total Logins", stats["total_logins"], delta=None)
with m3:
    st.metric("Successful", stats["successful_logins"],
              delta=f"{stats['failed_logins']} failed" if stats['failed_logins'] > 0 else "0 failed")
with m4:
    st.metric("Active (24h)", stats["active_24h"], delta=None)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="sv-neon-line"></div>', unsafe_allow_html=True)

# ─── Dashboard Tabs ─────────────────────────────────────────
tab_logs, tab_users, tab_security = st.tabs(["📋 Login Activity", "👥 User Management", "🛡️ Security Overview"])

# ── Tab 1: Login Activity ──────────────────────────────────
with tab_logs:
    st.markdown('<div style="margin-bottom: 1rem; animation: fadeInUp 0.7s ease-out both;"><div style="color: #d0d0d0; font-weight: 600; font-size: 1.17rem; margin-bottom: 0.3rem;">Login Activity Log</div><div style="color: #a0a0a0; font-size: 0.88rem;">Complete audit trail of all authentication attempts with timestamps.</div></div>', unsafe_allow_html=True)

    # Filters
    filter_cols = st.columns([2, 2, 2, 1])
    with filter_cols[0]:
        filter_role = st.selectbox("Filter by Role", ["All", "admin", "user"], key="log_filter_role")
    with filter_cols[1]:
        filter_status = st.selectbox("Filter by Status", ["All", "success", "failed"], key="log_filter_status")
    with filter_cols[2]:
        search_user = st.text_input("Search Username", placeholder="Type to search...", key="log_search")
    with filter_cols[3]:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Refresh", key="refresh_logs", use_container_width=True):
            st.rerun()

    # Fetch and filter logs
    logs = get_login_logs(200)

    if filter_role != "All":
        logs = [l for l in logs if l["role"] == filter_role]
    if filter_status != "All":
        logs = [l for l in logs if l["status"] == filter_status]
    if search_user:
        logs = [l for l in logs if search_user.lower() in l["username"].lower()]

    if logs:
        # Build HTML table
        rows_html = ""
        for i, log in enumerate(logs):
            status_badge = (
                '<span class="sv-badge sv-badge-green">SUCCESS</span>'
                if log["status"] == "success"
                else '<span class="sv-badge sv-badge-red">FAILED</span>'
            )
            role_badge = (
                '<span class="sv-badge sv-badge-purple">ADMIN</span>'
                if log["role"] == "admin"
                else '<span class="sv-badge sv-badge-cyan">USER</span>'
            )
            delay_class = f"sv-delay-{min(i + 1, 10)}"

            rows_html += f'<tr style="border-bottom: 1px solid rgba(200, 200, 200, 0.05);"><td style="padding: 0.65rem 0.8rem; color: #555555; font-family: JetBrains Mono, monospace; font-size: 0.8rem;">#{log["id"]}</td><td style="padding: 0.65rem 0.8rem; font-weight: 500; color: #e0e0e0;">{log["username"]}</td><td style="padding: 0.65rem 0.8rem;">{role_badge}</td><td style="padding: 0.65rem 0.8rem; font-family: JetBrains Mono, monospace; font-size: 0.82rem; color: #c0c0c0;">{log["login_time"]}</td><td style="padding: 0.65rem 0.8rem; color: #555555; font-family: JetBrains Mono, monospace; font-size: 0.82rem;">{log["ip_address"]}</td><td style="padding: 0.65rem 0.8rem;">{status_badge}</td></tr>'

        table_html = f'<div class="sv-glass" style="padding: 0; overflow: hidden; overflow-x: auto;"><table style="width: 100%; border-collapse: collapse; min-width: 700px;"><thead><tr style="background: rgba(200, 200, 200, 0.03); border-bottom: 2px solid rgba(200, 200, 200, 0.08);"><th style="padding: 0.75rem 0.8rem; text-align: left; color: #555555; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">ID</th><th style="padding: 0.75rem 0.8rem; text-align: left; color: #555555; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Username</th><th style="padding: 0.75rem 0.8rem; text-align: left; color: #555555; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Role</th><th style="padding: 0.75rem 0.8rem; text-align: left; color: #555555; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Timestamp</th><th style="padding: 0.75rem 0.8rem; text-align: left; color: #555555; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">IP Address</th><th style="padding: 0.75rem 0.8rem; text-align: left; color: #555555; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Status</th></tr></thead><tbody>{rows_html}</tbody></table></div><div style="text-align: right; padding: 0.5rem 0; color: #555555; font-size: 0.78rem;">Showing {len(logs)} entries</div>'
        st.markdown(table_html, unsafe_allow_html=True)
    else:
        st.info("📭 No login records match your filters. Login activity will appear here once users authenticate.")

# ── Tab 2: User Management ─────────────────────────────────
with tab_users:
    st.markdown('<div style="margin-bottom: 1rem; animation: fadeInUp 0.7s ease-out both;"><div style="color: #d0d0d0; font-weight: 600; font-size: 1.17rem; margin-bottom: 0.3rem;">Registered Users</div><div style="color: #a0a0a0; font-size: 0.88rem;">Overview of all user accounts in the system.</div></div>', unsafe_allow_html=True)

    users = get_all_users()

    if users:
        user_cards = ""
        for i, u in enumerate(users):
            role_badge = (
                '<span class="sv-badge sv-badge-purple">ADMIN</span>'
                if u["role"] == "admin"
                else '<span class="sv-badge sv-badge-cyan">USER</span>'
            )
            status_dot = (
                '<span style="color: #8fca8f;">●</span> Active'
                if u["is_active"]
                else '<span style="color: #c96464;">●</span> Inactive'
            )
            tfa_status = (
                '<span class="sv-badge sv-badge-green">Enabled</span>'
                if u["two_fa_enabled"]
                else '<span class="sv-badge sv-badge-amber">Not Set</span>'
            )
            avatar_color = u.get("avatar_color", "#808080")
            initial = u["full_name"][0].upper() if u["full_name"] else "?"
            delay_class = f"sv-delay-{min(i + 1, 10)}"

            user_cards += f'<div class="sv-glass" style="display: flex; align-items: center; gap: 1.2rem; padding: 1.2rem 1.5rem; margin-bottom: 0.8rem;"><div class="sv-avatar" style="background: {avatar_color};">{initial}</div><div style="flex: 1;"><div style="font-weight: 600; font-size: 1rem; color: #e0e0e0;">{u["full_name"]}</div><div style="color: #555555; font-size: 0.82rem;">@{u["username"]} · {u["email"]}</div></div><div style="text-align: center;">{role_badge}</div><div style="text-align: center; font-size: 0.82rem; color: #a0a0a0;">{status_dot}</div><div style="text-align: center;">{tfa_status}</div><div style="text-align: right; font-family: JetBrains Mono, monospace; font-size: 0.78rem; color: #555555;">Joined: {u["created_at"][:10] if u["created_at"] else "N/A"}</div></div>'

        st.markdown(user_cards, unsafe_allow_html=True)
    else:
        st.info("No users registered yet.")

# ── Tab 3: Security Overview ──────────────────────────────
with tab_security:
    st.markdown('<div style="margin-bottom: 1.5rem; animation: fadeInUp 0.7s ease-out both;"><div style="color: #d0d0d0; font-weight: 600; font-size: 1.17rem; margin-bottom: 0.3rem;">System Security Status</div><div style="color: #a0a0a0; font-size: 0.88rem;">Real-time security health and configuration overview.</div></div>', unsafe_allow_html=True)

    sec1, sec2 = st.columns(2)

    with sec1:
        success_rate = (
            round(stats["successful_logins"] / stats["total_logins"] * 100, 1)
            if stats["total_logins"] > 0 else 100
        )
        threat_level = "LOW" if stats["failed_logins"] < 5 else ("MEDIUM" if stats["failed_logins"] < 15 else "HIGH")
        threat_color = "green" if threat_level == "LOW" else ("amber" if threat_level == "MEDIUM" else "red")

        st.markdown(f'<div class="sv-glass" style="text-align: center; animation: fadeInUp 0.7s ease-out both;"><div class="sv-section-heading">Security Score</div><div class="sv-ring" style="margin: 1rem auto;"><span>{success_rate}%</span></div><div style="margin-top: 1rem; color: #a0a0a0; font-size: 0.88rem;">Authentication Success Rate</div></div>', unsafe_allow_html=True)

    with sec2:
        st.markdown('<div class="sv-glass" style="animation: fadeInUp 0.7s ease-out 0.2s both;"><div class="sv-section-heading">Threat Assessment</div></div>', unsafe_allow_html=True)

        threat_items = [
            ("Threat Level", f'<span class="sv-badge sv-badge-{threat_color}">{threat_level}</span>'),
            ("Failed Attempts", f'<span style="color: #c96464; font-family: \'JetBrains Mono\', monospace; font-weight: 600;">{stats["failed_logins"]}</span>'),
            ("Encryption", '<span class="sv-badge sv-badge-green">AES-256 ✓</span>'),
            ("Key Derivation", '<span class="sv-badge sv-badge-green">PBKDF2 ✓</span>'),
            ("2FA Status", '<span class="sv-badge sv-badge-amber">Available</span>'),
        ]
        for label, badge in threat_items:
            st.markdown(f'<div style="display: flex; justify-content: space-between; align-items: center; padding: 0.6rem 0; border-bottom: 1px solid rgba(200,200,200,0.08);"><span style="color: #a0a0a0; font-size: 0.88rem;">{label}</span>{badge}</div>', unsafe_allow_html=True)

inject_page_animations()
