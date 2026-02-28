"""
SecureVault — Landing Page
Sleek hero section with scroll animations, feature cards, and CTAs.
"""

import streamlit as st
from utils.styles import inject_custom_css, inject_page_animations
from utils.db import init_auth_db, seed_default_users
from utils.auth import init_session_state, is_authenticated

# ─── Page Config ────────────────────────────────────────────
st.set_page_config(
    page_title="SecureVault Enterprise",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Initialize ─────────────────────────────────────────────
init_auth_db()
seed_default_users()
init_session_state()
inject_custom_css()

# ─── Sidebar ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🛡️</div>
        <div class="sv-gradient-text" style="font-size: 1.2rem; font-weight: 800;">SecureVault</div>
        <div style="color: #666666; font-size: 0.75rem; letter-spacing: 2px; text-transform: uppercase; margin-top: 0.25rem;">Enterprise Security</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    if is_authenticated():
        user = st.session_state.user
        st.markdown(f"""
        <div style="text-align:center; padding: 0.5rem;">
            <div class="sv-avatar" style="background: {user['avatar_color']}; margin: 0 auto 0.5rem;">
                {user['full_name'][0].upper()}
            </div>
            <div style="font-weight: 600; color: #e0e0e0;">{user['full_name']}</div>
            <span class="sv-badge sv-badge-{'purple' if user['role'] == 'admin' else 'cyan'}">{user['role'].upper()}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("👈 Use the navigation to log in via **Admin Portal** or **User Portal**.")

# ─── Hero Section ───────────────────────────────────────────
st.markdown("""
<div style="text-align: center; padding: 3rem 1rem 1.5rem; animation: fadeInUp 0.7s ease-out both;">
<div class="sv-hero-tag" style="animation: fadeInUp 0.7s ease-out 0.1s both;">🔒 Enterprise Security Platform</div>
<div style="font-size: 3.8rem; font-weight: 900; background: linear-gradient(135deg, #ffffff 0%, #b0b0b0 40%, #808080 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin: 1.2rem 0 0.8rem; line-height: 1.1; letter-spacing: -0.03em; animation: fadeInUp 0.7s ease-out 0.2s both;">SecureVault</div>
<div style="font-size: 1.2rem; color: #a0a0a0; max-width: 600px; margin: 0 auto 2rem; line-height: 1.7; animation: fadeInUp 0.7s ease-out 0.3s both;">Industry-grade encrypted data management with role-based access control, real-time audit trails, and military-level security protocols.</div>
</div>
""", unsafe_allow_html=True)

# ─── Stats Bar ──────────────────────────────────────────────
st.markdown("""
<div class="sv-observe" style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; padding: 0 1rem 2rem;">
<div class="sv-stat-card sv-fade-up sv-delay-3" style="min-width: 160px; flex: 1; max-width: 220px;"><div class="sv-stat-value sv-gradient-text">AES-256</div><div class="sv-stat-label">Encryption Standard</div></div>
<div class="sv-stat-card sv-fade-up sv-delay-4" style="min-width: 160px; flex: 1; max-width: 220px;"><div class="sv-stat-value" style="color: #c0c0c0;">99.99%</div><div class="sv-stat-label">Uptime SLA</div></div>
<div class="sv-stat-card sv-fade-up sv-delay-5" style="min-width: 160px; flex: 1; max-width: 220px;"><div class="sv-stat-value" style="color: #a0a0a0;">PBKDF2</div><div class="sv-stat-label">Key Derivation</div></div>
<div class="sv-stat-card sv-fade-up sv-delay-6" style="min-width: 160px; flex: 1; max-width: 220px;"><div class="sv-stat-value" style="color: #909090;">2FA</div><div class="sv-stat-label">Ready Architecture</div></div>
</div>
""", unsafe_allow_html=True)

# ─── Neon Divider ───────────────────────────────────────────
st.markdown('<div class="sv-neon-line sv-observe"></div>', unsafe_allow_html=True)

# ─── Features Section ──────────────────────────────────────
st.markdown("""
<div class="sv-observe" style="text-align: center; margin-bottom: 1.5rem;">
<span class="sv-badge sv-badge-purple" style="margin-bottom: 0.5rem;">Core Capabilities</span>
<div style="font-size: 1.8rem; font-weight: 700; margin-top: 0.5rem;">Enterprise-Grade Security Features</div>
</div>
""", unsafe_allow_html=True)

cols = st.columns(3)

features = [
    {
        "icon": "🔐",
        "title": "End-to-End Encryption",
        "desc": "All data encrypted at rest and in transit using Fernet symmetric encryption with HKDF-derived keys and HMAC integrity verification.",
        "delay": "1"
    },
    {
        "icon": "👥",
        "title": "Role-Based Access",
        "desc": "Separate Admin and User portals with distinct privilege levels. Admins monitor, users access — zero overlap in permissions.",
        "delay": "2"
    },
    {
        "icon": "📋",
        "title": "Real-Time Audit Trail",
        "desc": "Every login attempt logged with timestamps, IP addresses, and status. Complete visibility into all authentication events.",
        "delay": "3"
    },
]

for col, feat in zip(cols, features):
    with col:
        st.markdown(f'<div class="sv-feature-card sv-observe sv-fade-up sv-delay-{feat["delay"]}"><span class="sv-feature-icon">{feat["icon"]}</span><div class="sv-feature-title">{feat["title"]}</div><div class="sv-feature-desc">{feat["desc"]}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

cols2 = st.columns(3)

features2 = [
    {
        "icon": "🛡️",
        "title": "Blind Index Search",
        "desc": "Searchable encryption using HMAC trapdoors — query encrypted data without ever exposing plaintext to the database layer.",
        "delay": "4"
    },
    {
        "icon": "🔑",
        "title": "2FA Ready Architecture",
        "desc": "Built-in schema support for TOTP-based two-factor authentication. Enable it per-user when your security policy requires it.",
        "delay": "5"
    },
    {
        "icon": "📊",
        "title": "Admin Dashboard",
        "desc": "Real-time overview of all user activity, login statistics, security metrics, and system health — all in one command center.",
        "delay": "6"
    },
]

for col, feat in zip(cols2, features2):
    with col:
        st.markdown(f'<div class="sv-feature-card sv-observe sv-fade-up sv-delay-{feat["delay"]}"><span class="sv-feature-icon">{feat["icon"]}</span><div class="sv-feature-title">{feat["title"]}</div><div class="sv-feature-desc">{feat["desc"]}</div></div>', unsafe_allow_html=True)

# ─── Neon Divider ───────────────────────────────────────────
st.markdown('<div class="sv-neon-line sv-observe"></div>', unsafe_allow_html=True)

# ─── How It Works Section ──────────────────────────────────
st.markdown("""
<div class="sv-observe" style="text-align: center; margin-bottom: 2rem;">
<span class="sv-badge sv-badge-cyan" style="margin-bottom: 0.5rem;">How It Works</span>
<div style="font-size: 1.8rem; font-weight: 700; margin-top: 0.5rem;">Three Steps to Total Security</div>
</div>
""", unsafe_allow_html=True)

step_cols = st.columns(3)
steps = [
    {"num": "01", "icon": "🔓", "title": "Authenticate", "desc": "Log in through your designated portal with role-based credential verification and audit logging."},
    {"num": "02", "icon": "🔒", "title": "Encrypt & Store", "desc": "All sensitive data is encrypted with derived keys before storage. Even the search index uses blind HMAC trapdoors."},
    {"num": "03", "icon": "📡", "title": "Monitor & Audit", "desc": "Every action is logged with timestamps. Admins get a real-time dashboard of all security events across the platform."},
]

for col, step in zip(step_cols, steps):
    with col:
        st.markdown(f'<div class="sv-observe sv-fade-up" style="text-align: center; padding: 1rem;"><div style="font-family: JetBrains Mono, monospace; font-size: 3rem; font-weight: 900; background: linear-gradient(135deg, rgba(200,200,200,0.15), rgba(120,120,120,0.15)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;">{step["num"]}</div><div style="font-size: 2rem; margin-bottom: 0.5rem;">{step["icon"]}</div><div style="font-weight: 700; font-size: 1.1rem; color: #e0e0e0; margin-bottom: 0.4rem;">{step["title"]}</div><div style="color: #a0a0a0; font-size: 0.88rem; line-height: 1.6;">{step["desc"]}</div></div>', unsafe_allow_html=True)

# ─── Neon Divider ───────────────────────────────────────────
st.markdown('<div class="sv-neon-line sv-observe"></div>', unsafe_allow_html=True)

# ─── CTA Section ───────────────────────────────────────────
st.markdown("""
<div class="sv-observe sv-fade-up" style="text-align: center; padding: 2rem 1rem 3rem;">
<div style="font-size: 1.6rem; font-weight: 700; margin-bottom: 0.8rem;">Ready to Get Started?</div>
<div style="color: #a0a0a0; font-size: 1rem; margin-bottom: 0.5rem;">Navigate to your portal using the sidebar to begin.</div>
</div>
""", unsafe_allow_html=True)

cta_cols = st.columns([1, 1, 1, 1, 1])
with cta_cols[1]:
    if st.button("🛡️  Admin Portal", use_container_width=True):
        st.switch_page("pages/1_Admin_Portal.py")
with cta_cols[3]:
    if st.button("👤  User Portal", use_container_width=True):
        st.switch_page("pages/2_User_Portal.py")

# ─── Footer ────────────────────────────────────────────────
st.markdown("""
<div class="sv-observe" style="text-align: center; padding: 2rem 1rem 1rem; margin-top: 2rem;">
<div class="sv-neon-line" style="max-width: 300px; margin: 0 auto 1.5rem;"></div>
<div style="color: #555555; font-size: 0.78rem; letter-spacing: 0.5px;">SecureVault Enterprise &copy; 2026 &nbsp;&middot;&nbsp; All data encrypted with AES-256 &nbsp;&middot;&nbsp; Built with 🛡️ Security First</div>
</div>
""", unsafe_allow_html=True)

# ─── Inject Scroll Observer ────────────────────────────────
inject_page_animations()
