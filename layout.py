import streamlit as st

def init_session_state():
    """Set up initial values in session_state if not already defined."""
    st.session_state.setdefault("dark_mode", False)
    st.session_state.setdefault("code", "")
    st.session_state.setdefault("stdin", "")
    st.session_state.setdefault("language", "Python")

def apply_theme():
    """Apply the selected theme and return color palette + ACE theme."""
    dark = st.session_state.dark_mode

    colors = {
        "bg": "#0f1620" if dark else "#f5f5f5",
        "panel_bg": "#1c2330" if dark else "#ffffff",
        "text": "#e3e8f1" if dark else "#1a1a1a",
        "accent": "#ff5252",
        "border": "#2a3240" if dark else "#dddddd",
        "shadow": "rgba(0,0,0,0.3)" if dark else "rgba(0,0,0,0.1)",
    }

    ace_theme = "monokai" if dark else "chrome"

    lang = st.session_state.get("language", "python").lower()
    ace_lang_map = {
        "c++": "c_cpp",
        "c#": "csharp",
        "javascript": "javascript",
        "python": "python",
        "java": "java",
        "c": "c"
    }
    ace_lang = ace_lang_map.get(lang, "python")

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {colors["bg"]};
            color: {colors["text"]};
            transition: background-color 0.3s ease, color 0.3s ease;
            animation: fadeIn 0.4s ease;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        [data-testid="stSidebar"] {{
            background-color: {colors["panel_bg"]} !important;
        }}

        .ace_editor, .ace_scroller {{
            background: {colors["panel_bg"]} !important;
            box-shadow: 0 4px 8px {colors["shadow"]} !important;
            border-radius: 8px !important;
        }}

        textarea, input, .stTextArea textarea {{
            background: {colors["panel_bg"]} !important;
            color: {colors["text"]} !important;
            border: 1px solid {colors["border"]} !important;
            border-radius: 4px !important;
        }}

        label, .stTextLabel, .stTextArea label {{
            color: {colors["text"]} !important;
        }}

        button, .stDownloadButton > button {{
            background-color: {colors["accent"]} !important;
            color: #fff !important;
            border-radius: 6px !important;
        }}
        button:hover {{
            transform: scale(1.05) !important;
        }}

        .chat-container {{
            background: {colors["panel_bg"]} !important;
            border: 1px solid {colors["border"]} !important;
            border-radius: 8px !important;
            padding: 1rem;
            max-height: 480px;
            overflow-y: auto;
        }}

        .chat-message {{
            margin-bottom: 1rem;
            padding: 0.75rem 1rem;
            border-radius: 12px;
        }}
        .user-message {{
            background: rgba(100,149,237,0.2);
            align-self: flex-end;
        }}
        .bot-message {{
            background: rgba(200,200,200,0.2);
            align-self: flex-start;
        }}

        pre code {{
            display: block;
            padding: 0.5rem;
            background: rgba(0,0,0,0.1);
            border-radius: 4px;
            overflow-x: auto;
        }}

        /* Fix selectbox and file uploader in dark mode */
        section[data-testid="stSelectbox"] label,
        section[data-testid="stFileUploader"] label {{
            color: {colors["text"]} !important;
        }}

        section[data-testid="stSelectbox"] div[data-baseweb="select"] {{
            background-color: {colors["panel_bg"]} !important;
            color: {colors["text"]} !important;
            border: 1px solid {colors["border"]} !important;
            border-radius: 6px !important;
        }}

        section[data-testid="stFileUploader"] .stFileUploaderDropzone {{
            background-color: {colors["panel_bg"]} !important;
            color: {colors["text"]} !important;
            border: 1px dashed {colors["border"]};
            border-radius: 8px;
        }}

        section[data-testid="stFileUploader"] .row-widget.stButton > button {{
            background-color: {colors["accent"]} !important;
            color: white !important;
            border-radius: 6px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    return colors, ace_theme
