import streamlit as st
from layout import init_session_state, apply_theme
from code_editor import render_code_editor
from chatbot import render_chatbot

# ── Page Config ──────────────────────────────
st.set_page_config(
    page_title="Pro Code Playground",
    page_icon="💻",
    layout="wide"
)
init_session_state()

# ── Header ───────────────────────────────────
st.title("Pro Code Playground")
st.markdown("Write, execute & export multi-language snippets, with built‑in AI assistance.")

# ── Theme Toggle ─────────────────────────────
_, _, theme_col = st.columns([3, 6, 1])
with theme_col:
    if st.button("🌙 Dark Mode" if not st.session_state.dark_mode else "☀️ Light Mode"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ── Apply Theme ──────────────────────────────
colors, ace_theme = apply_theme()

# ── Layout ───────────────────────────────────
editor_col, assistant_col = st.columns((2, 1), gap="large")

with editor_col:
    st.subheader("Editor")
    render_code_editor(ace_theme)

with assistant_col:
    st.subheader("Code Assistant")
    render_chatbot(
        st.session_state.code,
        st.session_state.get("stdin", ""),
        st.session_state.get("code_output", ""),
        st.session_state.get("error_output", "")
    )

# ── Footer ───────────────────────────────────
st.markdown("""
<div style='text-align:center; margin-top:1rem; opacity:0.6;'>
  Built with ❤️ & Streamlit by Vaibhav
</div>
""", unsafe_allow_html=True)
