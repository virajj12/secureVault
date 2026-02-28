"""
SecureVault — Black & Gray Theme CSS Injection
Injects a sleek monochrome dark theme with glassmorphism and scroll animations.
"""

import streamlit as st


def inject_custom_css():
    """Inject the full black & gray CSS theme into the Streamlit page."""
    st.markdown("""
    <style>
    /* ═══════════════════════════════════════════════════════
       FONTS
       ═══════════════════════════════════════════════════════ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&family=JetBrains+Mono:wght@400;500;700&display=swap');

    /* ═══════════════════════════════════════════════════════
       ROOT VARIABLES
       ═══════════════════════════════════════════════════════ */
    :root {
        --bg-primary: #0a0a0a;
        --bg-secondary: #111111;
        --bg-tertiary: #1a1a1a;
        --bg-card: rgba(18, 18, 18, 0.75);
        --accent-primary: #d4d4d4;
        --accent-secondary: #a0a0a0;
        --accent-tertiary: #808080;
        --accent-green: #8fca8f;
        --accent-amber: #c9a84c;
        --accent-red: #c96464;
        --text-primary: #e8e8e8;
        --text-secondary: #a0a0a0;
        --text-muted: #666666;
        --glass-bg: rgba(20, 20, 20, 0.65);
        --glass-border: rgba(200, 200, 200, 0.10);
        --glass-hover: rgba(200, 200, 200, 0.20);
        --glow-primary: 0 0 20px rgba(200, 200, 200, 0.10);
        --glow-secondary: 0 0 20px rgba(150, 150, 150, 0.10);
        --radius: 12px;
        --radius-lg: 20px;
    }

    /* ═══════════════════════════════════════════════════════
       GLOBAL RESET & APP BACKGROUND
       ═══════════════════════════════════════════════════════ */
    .stApp {
        background: linear-gradient(160deg, #000000 0%, #0a0a0a 40%, #111111 70%, #0d0d0d 100%) !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
    }

    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background:
            radial-gradient(ellipse 600px 400px at 15% 25%, rgba(255, 255, 255, 0.02) 0%, transparent 100%),
            radial-gradient(ellipse 500px 350px at 85% 65%, rgba(200, 200, 200, 0.02) 0%, transparent 100%),
            radial-gradient(ellipse 400px 300px at 50% 90%, rgba(150, 150, 150, 0.015) 0%, transparent 100%);
        pointer-events: none;
        z-index: 0;
        animation: bgPulse 20s ease-in-out infinite alternate;
    }

    @keyframes bgPulse {
        0%   { opacity: 0.5; }
        50%  { opacity: 1; }
        100% { opacity: 0.5; }
    }

    /* ═══════════════════════════════════════════════════════
       HEADER & SIDEBAR
       ═══════════════════════════════════════════════════════ */
    [data-testid="stHeader"] {
        background: rgba(10, 10, 10, 0.9) !important;
        backdrop-filter: blur(16px) !important;
        border-bottom: 1px solid var(--glass-border) !important;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(195deg, #0e0e0e 0%, #0a0a0a 100%) !important;
        border-right: 1px solid var(--glass-border) !important;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdown"] p,
    [data-testid="stSidebar"] .stMarkdown p {
        color: var(--text-secondary) !important;
    }

    section[data-testid="stSidebar"] .stRadio label span {
        color: var(--text-primary) !important;
    }

    /* ═══════════════════════════════════════════════════════
       TYPOGRAPHY
       ═══════════════════════════════════════════════════════ */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        letter-spacing: -0.02em;
    }

    h1 {
        background: linear-gradient(135deg, #ffffff 0%, #b0b0b0 55%, #808080 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        font-weight: 900 !important;
        font-size: 2.4rem !important;
    }

    h2 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
    }

    h3 {
        color: var(--accent-primary) !important;
        font-weight: 600 !important;
    }

    p, span, li, label, .stMarkdown, .stMarkdown p {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ═══════════════════════════════════════════════════════
       BUTTONS
       ═══════════════════════════════════════════════════════ */
    .stButton > button {
        background: linear-gradient(135deg, #555555 0%, #333333 100%) !important;
        color: #fff !important;
        border: none !important;
        border-radius: var(--radius) !important;
        padding: 0.65rem 2rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.3px;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
        position: relative;
        overflow: hidden;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #666666 0%, #444444 100%) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5), 0 0 50px rgba(200, 200, 200, 0.05) !important;
    }

    .stButton > button:active {
        transform: translateY(-1px) !important;
    }

    /* Secondary / outline style for specific buttons */
    .stButton > button[kind="secondary"] {
        background: transparent !important;
        border: 1px solid var(--glass-border) !important;
        color: var(--accent-primary) !important;
    }

    /* ═══════════════════════════════════════════════════════
       FORM INPUTS
       ═══════════════════════════════════════════════════════ */
    .stTextInput > div > div > input,
    .stPasswordInput > div > div > input,
    .stTextInput input,
    input[type="text"],
    input[type="password"] {
        background: rgba(15, 15, 15, 0.65) !important;
        border: 1px solid rgba(200, 200, 200, 0.10) !important;
        border-radius: var(--radius) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput > div > div > input:focus,
    .stPasswordInput > div > div > input:focus,
    input[type="text"]:focus,
    input[type="password"]:focus {
        border-color: #808080 !important;
        box-shadow: 0 0 0 2px rgba(200, 200, 200, 0.08), var(--glow-primary) !important;
        outline: none !important;
    }

    .stTextInput label,
    .stPasswordInput label {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }

    /* ═══════════════════════════════════════════════════════
       SELECT / DROPDOWN
       ═══════════════════════════════════════════════════════ */
    .stSelectbox > div > div {
        background: rgba(15, 15, 15, 0.65) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius) !important;
    }

    .stSelectbox label {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        font-size: 0.85rem !important;
    }

    /* ═══════════════════════════════════════════════════════
       TABS
       ═══════════════════════════════════════════════════════ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(15, 15, 15, 0.4);
        padding: 4px;
        border-radius: var(--radius);
        border: 1px solid var(--glass-border);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 10px;
        color: var(--text-muted) !important;
        font-weight: 500;
        padding: 10px 24px;
        transition: all 0.3s ease;
        border: none !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: var(--text-primary) !important;
        background: rgba(200, 200, 200, 0.05) !important;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(200, 200, 200, 0.08) !important;
        color: #ffffff !important;
        font-weight: 600;
        box-shadow: 0 0 15px rgba(200, 200, 200, 0.05);
    }

    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }

    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }

    /* ═══════════════════════════════════════════════════════
       METRICS
       ═══════════════════════════════════════════════════════ */
    [data-testid="stMetric"] {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-lg) !important;
        padding: 1.25rem 1.4rem !important;
        backdrop-filter: blur(16px) !important;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    [data-testid="stMetric"]:hover {
        border-color: rgba(200, 200, 200, 0.25) !important;
        box-shadow: var(--glow-primary) !important;
        transform: translateY(-4px) !important;
    }

    [data-testid="stMetricLabel"] p {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        font-size: 0.78rem !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricDelta"] {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* ═══════════════════════════════════════════════════════
       DATAFRAME & TABLE
       ═══════════════════════════════════════════════════════ */
    .stDataFrame {
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius) !important;
        overflow: hidden !important;
    }

    [data-testid="stDataFrame"] > div {
        border-radius: var(--radius) !important;
    }

    /* ═══════════════════════════════════════════════════════
       EXPANDER
       ═══════════════════════════════════════════════════════ */
    .streamlit-expanderHeader {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius) !important;
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }

    .streamlit-expanderContent {
        background: rgba(15, 15, 15, 0.5) !important;
        border: 1px solid var(--glass-border) !important;
        border-top: none !important;
        border-radius: 0 0 var(--radius) var(--radius) !important;
    }

    /* ═══════════════════════════════════════════════════════
       ALERTS / MESSAGES
       ═══════════════════════════════════════════════════════ */
    [data-testid="stAlert"] {
        border-radius: var(--radius) !important;
        border-left-width: 4px !important;
    }

    .stSuccess, div[data-testid="stAlert"][data-baseweb-alert-kind="positive"] {
        background: rgba(143, 202, 143, 0.06) !important;
        border-color: var(--accent-green) !important;
    }

    .stError, div[data-testid="stAlert"][data-baseweb-alert-kind="negative"] {
        background: rgba(201, 100, 100, 0.06) !important;
        border-color: var(--accent-red) !important;
    }

    .stWarning, div[data-testid="stAlert"][data-baseweb-alert-kind="warning"] {
        background: rgba(201, 168, 76, 0.06) !important;
        border-color: var(--accent-amber) !important;
    }

    .stInfo, div[data-testid="stAlert"][data-baseweb-alert-kind="info"] {
        background: rgba(200, 200, 200, 0.04) !important;
        border-color: #808080 !important;
    }

    /* ═══════════════════════════════════════════════════════
       DIVIDERS
       ═══════════════════════════════════════════════════════ */
    hr {
        border: none !important;
        border-top: 1px solid var(--glass-border) !important;
        margin: 1.5rem 0 !important;
    }

    /* ═══════════════════════════════════════════════════════
       SCROLLBAR
       ═══════════════════════════════════════════════════════ */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #555555, #333333);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #777777, #444444);
    }

    /* ═══════════════════════════════════════════════════════
       KEYFRAME ANIMATIONS
       ═══════════════════════════════════════════════════════ */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(35px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-35px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeInLeft {
        from { opacity: 0; transform: translateX(-40px); }
        to   { opacity: 1; transform: translateX(0); }
    }

    @keyframes fadeInRight {
        from { opacity: 0; transform: translateX(40px); }
        to   { opacity: 1; transform: translateX(0); }
    }

    @keyframes scaleIn {
        from { opacity: 0; transform: scale(0.9); }
        to   { opacity: 1; transform: scale(1); }
    }

    @keyframes glowPulse {
        0%, 100% { box-shadow: 0 0 20px rgba(200, 200, 200, 0.05); }
        50%      { box-shadow: 0 0 40px rgba(200, 200, 200, 0.12), 0 0 80px rgba(150, 150, 150, 0.05); }
    }

    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50%      { transform: translateY(-12px); }
    }

    @keyframes shimmer {
        0%   { background-position: -200% center; }
        100% { background-position: 200% center; }
    }

    @keyframes borderGlow {
        0%, 100% { border-color: rgba(200, 200, 200, 0.08); }
        50%      { border-color: rgba(200, 200, 200, 0.20); }
    }

    @keyframes spin {
        from { transform: rotate(0deg); }
        to   { transform: rotate(360deg); }
    }

    @keyframes typewriter {
        from { width: 0; }
        to   { width: 100%; }
    }

    @keyframes gradientFlow {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* ═══════════════════════════════════════════════════════
       ANIMATION UTILITY CLASSES
       ═══════════════════════════════════════════════════════ */
    .sv-fade-up     { animation: fadeInUp 0.7s ease-out both; }
    .sv-fade-down   { animation: fadeInDown 0.7s ease-out both; }
    .sv-fade-left   { animation: fadeInLeft 0.7s ease-out both; }
    .sv-fade-right  { animation: fadeInRight 0.7s ease-out both; }
    .sv-scale-in    { animation: scaleIn 0.6s ease-out both; }
    .sv-glow        { animation: glowPulse 3s ease-in-out infinite; }
    .sv-float       { animation: float 4s ease-in-out infinite; }

    .sv-delay-1 { animation-delay: 0.1s; }
    .sv-delay-2 { animation-delay: 0.2s; }
    .sv-delay-3 { animation-delay: 0.3s; }
    .sv-delay-4 { animation-delay: 0.4s; }
    .sv-delay-5 { animation-delay: 0.5s; }
    .sv-delay-6 { animation-delay: 0.6s; }
    .sv-delay-7 { animation-delay: 0.7s; }
    .sv-delay-8 { animation-delay: 0.8s; }
    .sv-delay-9 { animation-delay: 0.9s; }
    .sv-delay-10 { animation-delay: 1.0s; }

    /* ═══════════════════════════════════════════════════════
       REUSABLE COMPONENT CLASSES
       ═══════════════════════════════════════════════════════ */

    /* Glass Card */
    .sv-glass {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-lg);
        padding: 1.75rem;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .sv-glass:hover {
        border-color: var(--glass-hover);
        box-shadow: var(--glow-primary);
        transform: translateY(-4px);
    }

    /* Badge */
    .sv-badge {
        display: inline-block;
        padding: 0.25rem 0.85rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    .sv-badge-cyan {
        background: rgba(200, 200, 200, 0.10);
        color: #d0d0d0;
        border: 1px solid rgba(200, 200, 200, 0.20);
    }

    .sv-badge-purple {
        background: rgba(180, 180, 180, 0.10);
        color: #c0c0c0;
        border: 1px solid rgba(180, 180, 180, 0.20);
    }

    .sv-badge-green {
        background: rgba(143, 202, 143, 0.10);
        color: var(--accent-green);
        border: 1px solid rgba(143, 202, 143, 0.20);
    }

    .sv-badge-red {
        background: rgba(201, 100, 100, 0.10);
        color: var(--accent-red);
        border: 1px solid rgba(201, 100, 100, 0.20);
    }

    .sv-badge-amber {
        background: rgba(201, 168, 76, 0.10);
        color: var(--accent-amber);
        border: 1px solid rgba(201, 168, 76, 0.20);
    }

    /* Hero Tag */
    .sv-hero-tag {
        display: inline-block;
        padding: 0.35rem 1.2rem;
        background: rgba(200, 200, 200, 0.06);
        border: 1px solid rgba(200, 200, 200, 0.15);
        border-radius: 24px;
        color: #c0c0c0;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* Gradient Text */
    .sv-gradient-text {
        background: linear-gradient(135deg, #ffffff 0%, #b0b0b0 50%, #808080 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .sv-gradient-text-subtle {
        background: linear-gradient(135deg, var(--text-primary) 0%, #b0b0b0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* Neon line divider */
    .sv-neon-line {
        height: 2px;
        background: linear-gradient(90deg, transparent, #555555, #888888, transparent);
        border: none;
        margin: 2rem 0;
        border-radius: 2px;
    }

    /* Stat card */
    .sv-stat-card {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(16px);
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .sv-stat-card:hover {
        border-color: rgba(200, 200, 200, 0.25);
        box-shadow: var(--glow-primary);
        transform: translateY(-5px);
    }

    .sv-stat-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.2rem;
        font-weight: 700;
        line-height: 1.2;
    }

    .sv-stat-label {
        font-size: 0.8rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.4rem;
    }

    /* Feature card */
    .sv-feature-card {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-lg);
        padding: 2rem 1.5rem;
        text-align: center;
        backdrop-filter: blur(16px);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .sv-feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #555555, #999999);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .sv-feature-card:hover {
        border-color: var(--glass-hover);
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.3);
        transform: translateY(-6px);
    }

    .sv-feature-card:hover::before {
        opacity: 1;
    }

    .sv-feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }

    .sv-feature-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }

    .sv-feature-desc {
        font-size: 0.88rem;
        color: var(--text-secondary);
        line-height: 1.6;
    }

    /* Avatar */
    .sv-avatar {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.2rem;
        color: white;
        flex-shrink: 0;
    }

    .sv-avatar-lg {
        width: 80px;
        height: 80px;
        font-size: 2rem;
    }

    /* Table row animation */
    .sv-log-row {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid rgba(200, 200, 200, 0.05);
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: background 0.2s ease;
    }

    .sv-log-row:hover {
        background: rgba(200, 200, 200, 0.03);
    }

    /* Glow border card - for login form */
    .sv-login-card {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-lg);
        padding: 2.5rem;
        backdrop-filter: blur(20px);
        max-width: 440px;
        margin: 0 auto;
        animation: borderGlow 4s ease-in-out infinite;
    }

    /* Progress ring for security score */
    .sv-ring {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 1.5rem;
        color: #c0c0c0;
        position: relative;
        margin: 0 auto;
    }

    .sv-ring::before {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 50%;
        border: 3px solid rgba(200, 200, 200, 0.08);
    }

    .sv-ring::after {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 50%;
        border: 3px solid #888888;
        border-right-color: transparent;
        border-bottom-color: transparent;
        animation: spin 3s linear infinite;
    }

    /* 2FA Badge */
    .sv-2fa-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: rgba(200, 200, 200, 0.05);
        border: 1px dashed rgba(200, 200, 200, 0.15);
        border-radius: var(--radius);
        color: #999999;
        font-size: 0.85rem;
        font-weight: 500;
    }

    /* Toggle placeholder */
    .sv-toggle-placeholder {
        position: relative;
        width: 48px;
        height: 26px;
        background: rgba(100, 100, 100, 0.3);
        border-radius: 13px;
        display: inline-block;
        cursor: not-allowed;
        opacity: 0.5;
    }

    .sv-toggle-placeholder::after {
        content: '';
        position: absolute;
        top: 3px;
        left: 3px;
        width: 20px;
        height: 20px;
        background: var(--text-muted);
        border-radius: 50%;
        transition: all 0.3s ease;
    }

    /* Section Heading */
    .sv-section-heading {
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--glass-border);
    }

    /* Particle canvas container */
    .sv-particles {
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 0;
    }

    /* Main content lift over particles */
    .main .block-container {
        position: relative;
        z-index: 1;
    }

    /* Hide default Streamlit footer */
    footer { visibility: hidden; }

    /* Hide the "Made with Streamlit" */
    .viewerBadge_container__r5tak { display: none; }

    </style>
    """, unsafe_allow_html=True)


def inject_page_animations():
    """Inject scroll-triggered animation observer (runs once per page)."""
    st.markdown("""
    <style>
    /* Elements start hidden and animate when rendered */
    .sv-observe {
        opacity: 0;
        transform: translateY(30px);
        transition: opacity 0.6s ease-out, transform 0.6s ease-out;
    }

    .sv-observe.sv-visible {
        opacity: 1;
        transform: translateY(0);
    }
    </style>
    """, unsafe_allow_html=True)

    # IntersectionObserver script injected via component
    st.components.v1.html("""
    <script>
    // Access the parent Streamlit frame
    const parent = window.parent.document;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('sv-visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    // Observe all elements with the sv-observe class
    function observeElements() {
        const elements = parent.querySelectorAll('.sv-observe:not(.sv-visible)');
        elements.forEach(el => observer.observe(el));
    }

    // Run immediately and again after a short delay (for Streamlit re-renders)
    observeElements();
    setTimeout(observeElements, 500);
    setTimeout(observeElements, 1500);
    setTimeout(observeElements, 3000);
    </script>
    """, height=0, scrolling=False)
