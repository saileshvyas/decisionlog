import streamlit as st
import google.generativeai as genai
import json
import re
import os
from datetime import datetime
import pandas as pd

st.set_page_config(
    page_title="DecisionLog — ShayOX",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&display=swap');

:root {
    --bg:           #0d1117;
    --surface:      #161b27;
    --surface2:     #1e2438;
    --border:       #252d42;
    --border-light: #2e3850;
    --accent:       #ff7a59;
    --accent-hover: #ff8f73;
    --accent-glow:  rgba(255,122,89,0.15);
    --green:        #00bfa5;
    --green-bg:     rgba(0,191,165,0.12);
    --red:          #ff5252;
    --red-bg:       rgba(255,82,82,0.1);
    --yellow:       #ffca28;
    --yellow-bg:    rgba(255,202,40,0.1);
    --text:         #f0f2f8;
    --text-sec:     #a0a8c0;
    --text-muted:   #606880;
    --white:        #ffffff;
    --card-orange-bg: #fff3f0;
    --card-orange-val:#ff7a59;
    --card-teal-bg:   #e8faf7;
    --card-teal-val:  #00bfa5;
    --card-blue-bg:   #eef2ff;
    --card-blue-val:  #4361ee;
    --sidebar-bg:   #1a0e0a;
    --sidebar-top:  #2d1208;
}

* { font-family: 'Lexend', -apple-system, sans-serif !important; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"],
.main {
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── NUKE keyboard_double_arrow completely ── */
[data-testid="stSidebarCollapsedControl"] *,
[data-testid="stSidebarCollapsedControl"] span,
[data-testid="stSidebarCollapsedControl"] svg,
.eyeqlp50, [class*="collapsedControl"] span {
    font-size: 0 !important;
    width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
    visibility: hidden !important;
    display: none !important;
}
[data-testid="stSidebarCollapsedControl"] {
    background: var(--accent) !important;
    border: none !important;
    border-radius: 0 8px 8px 0 !important;
    width: 28px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
[data-testid="stSidebarCollapsedControl"]::after {
    content: '◈';
    font-size: 1rem !important;
    color: white !important;
    visibility: visible !important;
    display: block !important;
    font-family: 'Lexend', sans-serif !important;
}

/* ── Kill top bar text artifact ── */
[data-testid="stHeader"] {
    background-color: var(--surface) !important;
    border-bottom: 1px solid var(--border) !important;
}
[data-testid="stHeader"] * { color: var(--text) !important; }
/* Hide the keyboard_double text in header area */
header [data-testid="stToolbar"] span:first-child,
header span.material-symbols-rounded,
[data-testid="stHeader"] span:not([data-testid]) {
    display: none !important;
    font-size: 0 !important;
    visibility: hidden !important;
}

/* ── SIDEBAR — rich orange gradient ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2d1208 0%, #1f0d06 30%, #160b05 60%, #0f0703 100%) !important;
    border-right: 1px solid rgba(255,122,89,0.25) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,122,89,0.2) !important; }

/* Sidebar labels */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stTextInput label,
[data-testid="stSidebar"] .stSelectbox label {
    color: rgba(255,200,180,0.8) !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
}

/* Sidebar inputs */
[data-testid="stSidebar"] .stTextInput input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,122,89,0.25) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,122,89,0.25) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] span {
    color: var(--text) !important;
}

/* Sidebar button */
[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,122,89,0.15) !important;
    border: 1px solid rgba(255,122,89,0.4) !important;
    color: var(--accent) !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,122,89,0.25) !important;
    transform: none !important;
}

.block-container { padding: 2rem 3rem !important; max-width: 1400px !important; }

/* ── Sidebar branding ── */
.shayox-brand {
    padding: 0.5rem 0 0.2rem 0;
}
.shayox-logo {
    font-size: 2rem;
    font-weight: 700;
    color: var(--white);
    letter-spacing: -0.5px;
    line-height: 1;
}
.shayox-logo span { color: var(--accent); }
.shayox-tag {
    font-size: 0.78rem;
    color: rgba(255,180,160,0.6);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-top: 0.15rem;
    margin-bottom: 0.5rem;
}
.product-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(255,122,89,0.15);
    border: 1px solid rgba(255,122,89,0.35);
    padding: 0.3rem 0.8rem;
    border-radius: 100px;
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--accent);
    margin-top: 0.4rem;
}
.product-pill .d { font-size: 1rem; }

/* ── Animations ── */
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulseBadge {
    0%   { box-shadow: 0 0 0 0 rgba(255,122,89,1), 0 0 20px rgba(255,122,89,0.6); transform: scale(1); }
    30%  { box-shadow: 0 0 0 18px rgba(255,122,89,0.3), 0 0 40px rgba(255,122,89,0.4); transform: scale(1.08); }
    60%  { box-shadow: 0 0 0 32px rgba(255,122,89,0), 0 0 60px rgba(255,122,89,0); transform: scale(1); }
    100% { box-shadow: 0 0 0 0 rgba(255,122,89,0), 0 0 0px rgba(255,122,89,0); transform: scale(1); }
}
@keyframes diamondSpin {
    0%   { transform: rotate(0deg) scale(1); }
    20%  { transform: rotate(15deg) scale(1.15); }
    50%  { transform: rotate(-15deg) scale(1.15); }
    80%  { transform: rotate(10deg) scale(1.05); }
    100% { transform: rotate(0deg) scale(1); }
}
@keyframes cardFadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes glowPulse {
    0%, 100% { opacity: 0.4; transform: scale(1); }
    50%       { opacity: 0.7; transform: scale(1.15); }
}

/* ── Hero ── */
.hero-wrap {
    position: relative;
    padding: 2.5rem 2.5rem 2rem 2.5rem;
    border-radius: 18px;
    margin-bottom: 2rem;
    overflow: hidden;
    background: linear-gradient(135deg, #161b27, #1e2438, #1a1520, #12151f);
    background-size: 300% 300%;
    animation: gradientShift 8s ease infinite;
    border: 1px solid var(--border);
}
.hero-glow {
    position: absolute;
    top: -80px; right: -80px;
    width: 380px; height: 380px;
    background: radial-gradient(circle, rgba(255,122,89,0.18) 0%, transparent 65%);
    animation: glowPulse 4s ease-in-out infinite;
    pointer-events: none;
}
.hero-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
    z-index: 1;
    animation: fadeSlideUp 0.6s ease both;
}
.hero-title {
    font-size: 3.4rem;
    font-weight: 700;
    color: var(--white);
    letter-spacing: -1.5px;
    margin: 0;
    line-height: 1.05;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.hero-title .log { color: var(--accent); }
.hero-diamond {
    color: var(--accent);
    font-size: 5rem;
    display: inline-block;
    animation: diamondSpin 4s ease-in-out infinite;
    line-height: 1;
}
.hero-sub {
    font-size: 1.1rem;
    color: var(--text-sec);
    margin-top: 0.7rem;
    font-weight: 300;
    animation: fadeSlideUp 0.6s ease 0.15s both;
}
.hero-right {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.7rem;
    animation: fadeSlideUp 0.6s ease 0.25s both;
}
.hero-badge {
    background: rgba(255,122,89,0.18);
    border: 1.5px solid var(--accent);
    color: var(--accent);
    padding: 0.55rem 1.4rem;
    border-radius: 100px;
    font-size: 0.9rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    animation: pulseBadge 2s ease-out infinite;
    white-space: nowrap;
}
.hero-shayox {
    font-size: 0.82rem;
    color: var(--text-muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 500;
}
.hero-shayox span { color: var(--accent); font-weight: 700; }

/* ── Section headings ── */
.section-heading {
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 1rem;
}

/* ── HubSpot metric cards ── */
[data-testid="stMetric"] {
    border-radius: 14px !important;
    padding: 1.5rem !important;
    border: none !important;
    animation: cardFadeIn 0.5s ease both !important;
}
[data-testid="stMetricValue"] { font-size: 2.6rem !important; font-weight: 700 !important; line-height: 1 !important; }
[data-testid="stMetricLabel"] p { font-size: 0.88rem !important; font-weight: 500 !important; text-transform: uppercase !important; letter-spacing: 0.07em !important; }
[data-testid="stMetric"]:nth-of-type(1) { background: var(--card-orange-bg) !important; }
[data-testid="stMetric"]:nth-of-type(1) [data-testid="stMetricValue"] { color: var(--card-orange-val) !important; }
[data-testid="stMetric"]:nth-of-type(1) [data-testid="stMetricLabel"] p { color: var(--card-orange-val) !important; opacity: 0.8; }
[data-testid="stMetric"]:nth-of-type(2) { background: var(--card-teal-bg) !important; }
[data-testid="stMetric"]:nth-of-type(2) [data-testid="stMetricValue"] { color: var(--card-teal-val) !important; }
[data-testid="stMetric"]:nth-of-type(2) [data-testid="stMetricLabel"] p { color: var(--card-teal-val) !important; opacity: 0.8; }
[data-testid="stMetric"]:nth-of-type(3) { background: var(--card-blue-bg) !important; }
[data-testid="stMetric"]:nth-of-type(3) [data-testid="stMetricValue"] { color: var(--card-blue-val) !important; }
[data-testid="stMetric"]:nth-of-type(3) [data-testid="stMetricLabel"] p { color: var(--card-blue-val) !important; opacity: 0.8; }

/* ── White paste box ── */
.stTextArea textarea {
    background: #ffffff !important;
    border: 1.5px solid #e0e4ef !important;
    border-radius: 12px !important;
    color: #1a1d2e !important;
    font-size: 1rem !important;
    line-height: 1.7 !important;
    padding: 1.1rem !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}
.stTextArea textarea::placeholder { color: #a0a8c0 !important; }

/* ── Main inputs ── */
.stTextInput input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-size: 1rem !important;
    padding: 0.65rem 1rem !important;
}
.stTextInput input:focus { border-color: var(--accent) !important; box-shadow: 0 0 0 3px var(--accent-glow) !important; }
.stTextInput input::placeholder { color: var(--text-muted) !important; }

/* ── Main selectbox ── */
.stSelectbox > div > div,
[data-testid="stSelectbox"] > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-size: 1rem !important;
}
[data-testid="stSelectbox"] span { color: var(--text) !important; font-size: 1rem !important; }
[data-testid="stSelectbox"] svg { fill: var(--text-muted) !important; }
[data-testid="stSelectboxVirtualDropdown"] { background: var(--surface2) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; }
[data-testid="stSelectboxVirtualDropdown"] li { color: var(--text) !important; font-size: 1rem !important; }
[data-testid="stSelectboxVirtualDropdown"] li:hover { background: var(--border) !important; }

/* ── Extract button ── */
.stButton > button {
    background: var(--accent) !important;
    color: var(--white) !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.75rem 2.2rem !important;
    box-shadow: 0 2px 12px rgba(255,122,89,0.35) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: var(--accent-hover) !important;
    box-shadow: 0 4px 20px rgba(255,122,89,0.5) !important;
    transform: translateY(-1px) !important;
}
/* Clear button — second button in row gets ghost style */
div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton > button {
    background: transparent !important;
    color: var(--text-muted) !important;
    border: 1px solid var(--border-light) !important;
    box-shadow: none !important;
    font-size: 0.9rem !important;
    padding: 0.75rem 1rem !important;
}
div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton > button:hover {
    background: var(--surface2) !important;
    color: var(--red) !important;
    border-color: var(--red) !important;
    transform: none !important;
    box-shadow: none !important;
}

.tip-text { font-size: 0.95rem; color: var(--text-muted); margin-top: 0.8rem; font-weight: 300; }

/* ── Decision cards ── */
.decision-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.6rem 1.6rem 1.6rem 2.1rem;
    margin-bottom: 1.1rem;
    position: relative;
    overflow: hidden;
    animation: cardFadeIn 0.4s ease both;
    transition: all 0.2s;
}
.decision-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    background: linear-gradient(180deg, var(--accent), var(--accent-hover));
}
.decision-card:hover { border-color: var(--border-light); box-shadow: 0 6px 30px rgba(0,0,0,0.4); transform: translateY(-2px); }
.card-meta { font-size: 0.78rem; font-weight: 500; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 0.6rem; }
.card-decision { font-size: 1.15rem; font-weight: 600; color: var(--white); margin-bottom: 1.3rem; line-height: 1.45; }
.card-field-label { font-size: 0.75rem; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.35rem; }
.card-field-value { font-size: 0.95rem; color: var(--text-sec); line-height: 1.5; }
.owner-value { color: var(--accent); font-weight: 500; }

.badge { display: inline-flex; align-items: center; padding: 0.28rem 0.8rem; border-radius: 100px; font-size: 0.78rem; font-weight: 600; }
.badge-high   { background: var(--green-bg);  color: var(--green);  border: 1px solid rgba(0,191,165,0.35); }
.badge-medium { background: var(--yellow-bg); color: var(--yellow); border: 1px solid rgba(255,202,40,0.35); }
.badge-low    { background: var(--red-bg);    color: var(--red);    border: 1px solid rgba(255,82,82,0.35); }

.tag-pill { display: inline-block; background: var(--surface2); border: 1px solid var(--border-light); color: var(--text-sec); border-radius: 6px; padding: 0.2rem 0.6rem; font-size: 0.8rem; margin-right: 0.4rem; margin-top: 0.4rem; }
.alt-pill { display: inline-block; background: var(--red-bg); border: 1px solid rgba(255,82,82,0.25); color: var(--red); border-radius: 6px; padding: 0.2rem 0.6rem; font-size: 0.8rem; margin-right: 0.4rem; margin-top: 0.4rem; }

.divider { border: none; border-top: 1px solid var(--border); margin: 2rem 0; }

.empty-state {
    text-align: center;
    padding: 5rem 2rem;
    background: var(--surface);
    border: 1px dashed var(--border-light);
    border-radius: 14px;
    animation: fadeSlideUp 0.5s ease both;
}
.empty-mark {
    font-size: 8rem;
    margin-bottom: 1rem;
    color: var(--accent);
    font-weight: 700;
    display: inline-block;
    animation: diamondSpin 5s ease-in-out infinite;
    line-height: 1;
}
.empty-title { font-size: 1.15rem; font-weight: 600; color: var(--text-sec); margin-bottom: 0.5rem; }
.empty-sub   { font-size: 0.95rem; color: var(--text-muted); }

hr { border-color: var(--border) !important; }
</style>
""", unsafe_allow_html=True)

# ── Gemini config ─────────────────────────────────────────────────────────────
try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    gemini_api_key = "AIzaSyDRnYq9NCfSIK3wcGjTpTfj9wN3yifbMc0"


# ── JS: Remove keyboard_double_arrow from DOM entirely ────────────────────────
st.components.v1.html("""
<script>
// Inject background glow overlay
const glowDiv = document.createElement('div');
glowDiv.id = 'shayox-bg-glow';
glowDiv.style.cssText = `
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    z-index: 0;
    background:
        radial-gradient(ellipse 55% 45% at 98% 2%, rgba(255,122,89,0.08) 0%, transparent 55%),
        radial-gradient(ellipse 35% 25% at 2% 98%, rgba(255,122,89,0.05) 0%, transparent 50%);
`;
if (!document.getElementById('shayox-bg-glow')) {
    document.body.appendChild(glowDiv);
}

function nukeKeyboardArrow() {
    // Target the sidebar collapsed control and strip its text nodes
    const btns = document.querySelectorAll('[data-testid="stSidebarCollapsedControl"]');
    btns.forEach(btn => {
        // Remove all child nodes that are text or material icon spans
        Array.from(btn.childNodes).forEach(node => {
            if (node.nodeType === 3) node.remove(); // text nodes
        });
        const spans = btn.querySelectorAll('span');
        spans.forEach(span => {
            if (span.textContent.includes('keyboard')) {
                span.textContent = '';
                span.style.display = 'none';
            }
        });
    });
    // Also check the header for the artifact
    const header = document.querySelector('[data-testid="stHeader"]');
    if (header) {
        const spans = header.querySelectorAll('span');
        spans.forEach(span => {
            if (span.textContent.includes('keyboard')) {
                span.textContent = '';
                span.style.display = 'none';
            }
        });
    }
}
// Run immediately and keep watching for DOM changes
nukeKeyboardArrow();
setInterval(nukeKeyboardArrow, 500);
const observer = new MutationObserver(nukeKeyboardArrow);
observer.observe(document.body, { childList: true, subtree: true });
</script>
""", height=0)

if gemini_api_key:
    genai.configure(api_key=gemini_api_key)

# ── Session state ─────────────────────────────────────────────────────────────
if "decisions" not in st.session_state:
    st.session_state.decisions = []
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="shayox-brand">
        <div class="shayox-logo">Shay<span>OX</span></div>
        <div class="shayox-tag">Internal Tools Platform</div>
        <div class="product-pill"><span class="d">◈</span> DecisionLog</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("<p style='color:#00bfa5;font-size:1rem;font-weight:500;margin:0;'>● Gemini 2.0 connected</p>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<p style='color:rgba(255,200,180,0.7);font-size:0.88rem;font-weight:500;margin-bottom:0.5rem;'>Context <span style=\"opacity:0.5\">(optional)</span></p>", unsafe_allow_html=True)
    project_tag = st.text_input("Project / Topic", placeholder="e.g. Q2 Roadmap")
    source_type = st.selectbox("Source type", ["Slack thread", "Email chain", "Meeting notes", "Document", "Other"])
    st.divider()
    st.markdown("<p style='color:rgba(255,180,150,0.5);font-size:0.88rem;line-height:1.7;'>Paste any workplace discussion — Slack threads, emails, meeting notes — and extract structured decision records automatically.</p>", unsafe_allow_html=True)
    if st.session_state.decisions:
        st.divider()
        if st.button("Clear log"):
            st.session_state.decisions = []
            st.rerun()

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-glow"></div>
    <div class="hero-inner">
        <div>
            <div class="hero-title">
                <span class="hero-diamond">◈</span>
                Decision<span class="log">Log</span>
            </div>
            <div class="hero-sub">Turn messy discussions into structured, searchable decision records</div>
        </div>
        <div class="hero-right">
            <div class="hero-badge">GDG London 2026</div>
            <div class="hero-shayox">by <span>ShayOX</span></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Metrics ───────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Decisions Logged", len(st.session_state.decisions))
with col2:
    owners = list({d.get("owner","") for d in st.session_state.decisions if d.get("owner") and d.get("owner") != "Unknown"})
    st.metric("Unique Owners", len(owners))
with col3:
    topics = list({d.get("project","") for d in st.session_state.decisions if d.get("project")})
    st.metric("Topics Tracked", len(topics))

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-heading">Paste your discussion</div>', unsafe_allow_html=True)
discussion_input = st.text_area(
    "input",
    value=st.session_state.input_text,
    placeholder="Paste a Slack thread, email chain, or meeting notes here...\n\nExample: 'After debate we agreed to use PostgreSQL over MongoDB. Sarah owns the migration. Redis was ruled out due to persistence concerns. Target: end of sprint 4.'",
    height=200,
    label_visibility="collapsed"
)
st.session_state.input_text = discussion_input
col_btn, col_clr, col_tip = st.columns([1.2, 0.7, 3.5])
with col_btn:
    extract_btn = st.button("◈  Extract Decisions")
with col_clr:
    if st.button("✕  Clear"):
        st.session_state.input_text = ""
        st.rerun()
with col_tip:
    st.markdown("<p class='tip-text'>Works with Slack threads, email chains, meeting notes, or any text discussion. No character limit.</p>", unsafe_allow_html=True)

# ── Extraction ────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are an expert at analysing workplace discussions and extracting structured decision records.
Given a discussion, extract ALL decisions made.
For EACH decision return a JSON object with:
- "decision": specific decision made
- "reasoning": why this option was chosen
- "alternatives": list of rejected alternatives (array of strings)
- "owner": person responsible (or "Unknown")
- "confidence": "high", "medium", or "low"
- "tags": 2-4 keyword tags (array of strings)
Return ONLY a valid JSON array. No preamble, no markdown fences. Empty array [] if no decisions found."""

def extract_decisions(text, project, source):
    model = genai.GenerativeModel(model_name="gemini-2.5-flash", system_instruction=SYSTEM_PROMPT)
    context = f"Source: {source}\nProject: {project or 'Not specified'}\n\nDiscussion:\n{text}"
    response = model.generate_content(context)
    raw = response.text.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"^```\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)

if extract_btn:
    if not discussion_input.strip():
        st.warning("Please paste some discussion text to analyse.")
    else:
        with st.spinner("Analysing with Gemini..."):
            try:
                new_decisions = extract_decisions(discussion_input, project_tag, source_type)
                if not new_decisions:
                    st.info("No clear decisions found. Try pasting a discussion with explicit choices or agreements.")
                else:
                    timestamp = datetime.now().strftime("%d %b %Y, %H:%M")
                    for d in new_decisions:
                        d["extracted_at"] = timestamp
                        d["source"] = source_type
                        d["project"] = project_tag or "General"
                        d["id"] = len(st.session_state.decisions) + 1
                        st.session_state.decisions.append(d)
                    count = len(new_decisions)
                    st.session_state.input_text = ""
                    st.success(f"✓ Extracted {count} decision{'s' if count != 1 else ''} successfully.")
                    st.rerun()
            except json.JSONDecodeError:
                st.error("Could not parse Gemini's response. Please try again.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ── Decision Log ──────────────────────────────────────────────────────────────
st.markdown("<hr class='divider'>", unsafe_allow_html=True)

if st.session_state.decisions:
    col_s, col_f, col_e = st.columns([3, 1, 1])
    with col_s:
        search = st.text_input("search", placeholder="Search by keyword, owner, or topic...", label_visibility="collapsed")
    with col_f:
        conf_filter = st.selectbox("conf", ["All", "high", "medium", "low"], label_visibility="collapsed")
    with col_e:
        if st.button("Export CSV"):
            df = pd.DataFrame(st.session_state.decisions)
            df["alternatives"] = df["alternatives"].apply(lambda x: " | ".join(x) if isinstance(x, list) else x)
            df["tags"] = df["tags"].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)
            csv = df.to_csv(index=False)
            st.download_button("Download", csv, "decision_log.csv", "text/csv")

    st.markdown("<div style='margin-bottom:0.75rem;'></div>", unsafe_allow_html=True)
    filtered = st.session_state.decisions.copy()
    if search:
        q = search.lower()
        filtered = [d for d in filtered if q in d.get("decision","").lower() or q in d.get("owner","").lower() or q in d.get("project","").lower() or any(q in t.lower() for t in d.get("tags",[]))]
    if conf_filter != "All":
        filtered = [d for d in filtered if d.get("confidence") == conf_filter]

    st.markdown(f'<div class="section-heading">{len(filtered)} decision{"s" if len(filtered)!=1 else ""} · newest first</div>', unsafe_allow_html=True)

    for d in reversed(filtered):
        alts = d.get("alternatives", [])
        conf = d.get("confidence", "medium")
        conf_badge = f'<span class="badge badge-{conf}">{conf} confidence</span>'
        tags_html = "".join(f'<span class="tag-pill">{t}</span>' for t in d.get("tags",[]))
        alts_html = "".join(f'<span class="alt-pill">✕ {a}</span>' for a in alts) if alts else "<span style='color:#606880;font-size:0.85rem;'>None recorded</span>"
        st.markdown(f"""
        <div class="decision-card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.6rem;">
                <div class="card-meta">#{d.get('id','?')} &nbsp;·&nbsp; {d.get('extracted_at','')} &nbsp;·&nbsp; {d.get('source','')}</div>
                {conf_badge}
            </div>
            <div class="card-decision">{d.get('decision','')}</div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1.5rem;margin-bottom:1.2rem;">
                <div><div class="card-field-label">Reasoning</div><div class="card-field-value">{d.get('reasoning','Not specified')}</div></div>
                <div><div class="card-field-label">Owner</div><div class="card-field-value owner-value">◈ {d.get('owner','Unknown')}</div></div>
                <div><div class="card-field-label">Project</div><div class="card-field-value">▸ {d.get('project','General')}</div></div>
            </div>
            <div style="margin-bottom:0.8rem;"><div class="card-field-label">Alternatives Rejected</div><div style="margin-top:0.35rem;">{alts_html}</div></div>
            <div>{tags_html}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-mark">◈</div>
        <div class="empty-title">No decisions logged yet</div>
        <div class="empty-sub">Paste a discussion above and hit Extract Decisions to get started.</div>
    </div>
    """, unsafe_allow_html=True)