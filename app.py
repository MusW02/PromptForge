import streamlit as st
import os
from dotenv import load_dotenv
from src.generator import generate_prompt
from src.history import load_history, save_to_history, clear_history

# Load .env for local dev; Streamlit Cloud uses st.secrets
load_dotenv()

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PromptForge",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

:root {
    --bg:        #0a0a0f;
    --surface:   #12121a;
    --border:    #1e1e2e;
    --accent:    #7fff6e;
    --accent2:   #6ef0ff;
    --text:      #e8e8f0;
    --muted:     #6b6b7e;
    --danger:    #ff6e6e;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}

h1, h2, h3 { font-family: 'Syne', sans-serif; font-weight: 800; }

.forge-header {
    display: flex; align-items: center; gap: 12px;
    padding: 0 0 24px 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 28px;
}
.forge-logo {
    font-family: 'Space Mono', monospace;
    font-size: 28px; font-weight: 700;
    color: var(--accent);
    letter-spacing: -1px;
}
.forge-sub {
    font-size: 13px; color: var(--muted);
    font-family: 'Space Mono', monospace;
}

.target-badge {
    display: inline-block;
    padding: 4px 12px; border-radius: 20px;
    font-size: 11px; font-family: 'Space Mono', monospace;
    font-weight: 700; letter-spacing: 1px; text-transform: uppercase;
    margin-right: 6px; margin-bottom: 6px; cursor: pointer;
}
.badge-cursor  { background: #1a1a2e; color: var(--accent2); border: 1px solid var(--accent2); }
.badge-claude  { background: #1a1a2e; color: #ff9f6e;        border: 1px solid #ff9f6e; }
.badge-both    { background: #1a1a2e; color: var(--accent);   border: 1px solid var(--accent); }

.output-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 8px;
    padding: 20px 24px;
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    line-height: 1.7;
    white-space: pre-wrap;
    word-wrap: break-word;
    color: var(--text);
}
.output-box.loading {
    border-left-color: var(--accent2);
    color: var(--muted);
    font-style: italic;
}
.output-box.error {
    border-left-color: var(--danger);
    color: var(--danger);
}

.meta-chip {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 8px 14px;
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    color: var(--muted);
    display: inline-block;
    margin-right: 8px;
}
.meta-chip span { color: var(--accent); font-weight: 700; }

.history-item {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 10px;
    cursor: pointer;
    transition: border-color 0.2s;
}
.history-item:hover { border-color: var(--accent); }
.history-target {
    font-size: 10px; font-family: 'Space Mono', monospace;
    text-transform: uppercase; letter-spacing: 1px;
    color: var(--accent); margin-bottom: 4px;
}
.history-preview {
    font-size: 12px; color: var(--muted);
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}

.stTextArea textarea {
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 15px !important;
    caret-color: var(--accent) !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent) !important;
}

.stButton > button {
    background: var(--accent) !important;
    color: #0a0a0f !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    letter-spacing: 1px !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 10px 28px !important;
    text-transform: uppercase !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

div[data-testid="stSelectbox"] > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

.stRadio > div { gap: 12px; }
.stRadio label { color: var(--text) !important; font-size: 14px; }

[data-testid="stMarkdownContainer"] p { color: var(--text); }

.section-label {
    font-size: 11px; font-family: 'Space Mono', monospace;
    text-transform: uppercase; letter-spacing: 2px;
    color: var(--muted); margin-bottom: 8px;
}

.tip-box {
    background: #0d1a0d;
    border: 1px solid #1a3a1a;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 12px;
    color: #6ab06a;
    font-family: 'Space Mono', monospace;
    margin-top: 12px;
}

footer { display: none !important; }
#MainMenu { display: none !important; }
header { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "result"       not in st.session_state: st.session_state.result       = ""
if "input_echo"   not in st.session_state: st.session_state.input_echo   = ""
if "token_est"    not in st.session_state: st.session_state.token_est    = 0
if "generating"   not in st.session_state: st.session_state.generating   = False

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="forge-logo">⚡ PromptForge</div>', unsafe_allow_html=True)
    st.markdown('<div class="forge-sub">v1.0 · DeepSeek V3 (Ollama Cloud)</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<div class="section-label">Target Tool</div>', unsafe_allow_html=True)
    target = st.selectbox(
        "", ["Cursor", "Claude", "Both (Cursor + Claude)"],
        label_visibility="collapsed"
    )

    st.markdown('<div class="section-label" style="margin-top:20px">Task Type</div>', unsafe_allow_html=True)
    task_type = st.selectbox(
        "", ["Auto-detect", "Write new code", "Edit / refactor existing code",
             "Debug / fix a bug", "Explain code", "Write tests", "Other"],
        label_visibility="collapsed"
    )

    st.markdown('<div class="section-label" style="margin-top:20px">Response Style</div>', unsafe_allow_html=True)
    style = st.radio(
        "", ["Minimal (code only)", "Balanced", "Detailed (with explanation)"],
        label_visibility="collapsed", index=1
    )

    st.markdown("---")
    st.markdown('<div class="section-label">History</div>', unsafe_allow_html=True)

    history = load_history()
    if history:
        for i, item in enumerate(reversed(history[-6:])):
            st.markdown(f"""
            <div class="history-item">
                <div class="history-target">{item['target']}</div>
                <div class="history-preview">{item['input'][:60]}…</div>
            </div>""", unsafe_allow_html=True)
        if st.button("Clear History", key="clear_hist"):
            clear_history()
            st.rerun()
    else:
        st.markdown('<div style="color:#6b6b7e; font-size:12px; font-family: Space Mono, monospace;">No history yet.</div>', unsafe_allow_html=True)

# ── Main area ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="forge-header">
    <div>
        <div class="forge-logo">⚡ PromptForge</div>
        <div class="forge-sub">Turns messy ideas → precision prompts for Cursor & Claude</div>
    </div>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="section-label">Your idea (messy english is fine)</div>', unsafe_allow_html=True)
    user_input = st.text_area(
        "",
        height=220,
        placeholder="e.g.  make a button that turn red when click and show popup say success also fix the thing where it break on mobile",
        label_visibility="collapsed",
        key="user_input"
    )

    st.markdown('<div class="section-label" style="margin-top:12px">Language / Framework (optional)</div>', unsafe_allow_html=True)
    lang = st.text_input("", placeholder="e.g. React, Python, TypeScript, Django…", label_visibility="collapsed")

    generate_clicked = st.button("⚡ FORGE PROMPT", key="generate")

    st.markdown("""
    <div class="tip-box">
    💡 TIP — The messier your input, the more this tool helps.<br>
    Grammar mistakes, half-thoughts, mixed ideas — all fine.
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="section-label">Generated Prompt</div>', unsafe_allow_html=True)

    if generate_clicked:
        if not user_input.strip():
            st.markdown('<div class="output-box error">⚠ Please enter something to forge.</div>', unsafe_allow_html=True)
        else:
            api_key = os.getenv("OLLAMA_API_KEY", "") or st.secrets.get("OLLAMA_API_KEY", "")
            if not api_key:
                st.markdown('<div class="output-box error">⚠ OLLAMA_API_KEY not set. Add it to your .env file.</div>', unsafe_allow_html=True)
            else:
                with st.spinner("Forging your prompt…"):
                    result, tokens_used, error = generate_prompt(
                        raw_input=user_input,
                        target=target,
                        task_type=task_type,
                        style=style,
                        language=lang,
                        api_key=api_key,
                    )

                if error:
                    st.markdown(f'<div class="output-box error">⚠ {error}</div>', unsafe_allow_html=True)
                else:
                    st.session_state.result     = result
                    st.session_state.token_est  = tokens_used
                    st.session_state.input_echo = user_input
                    save_to_history(user_input, target, result)

    if st.session_state.result:
        # Meta chips
        word_count = len(st.session_state.result.split())
        est_response_tokens = max(50, word_count * 3)
        st.markdown(f"""
        <div style="margin-bottom:12px">
            <div class="meta-chip">Generator tokens used: <span>{st.session_state.token_est}</span></div>
            <div class="meta-chip">Prompt words: <span>{word_count}</span></div>
            <div class="meta-chip">Est. response tokens saved: <span>~{est_response_tokens}</span></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f'<div class="output-box">{st.session_state.result}</div>', unsafe_allow_html=True)

        st.code(st.session_state.result, language="markdown")

        col_a, col_b = st.columns(2)
        with col_a:
            st.download_button(
                "⬇ Download .txt",
                data=st.session_state.result,
                file_name="forged_prompt.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with col_b:
            if st.button("🔄 Regenerate", key="regen", use_container_width=True):
                st.session_state.result = ""
                st.rerun()
    else:
        st.markdown('<div class="output-box loading">Your forged prompt will appear here…\n\nPaste your rough idea on the left and hit ⚡ FORGE PROMPT.</div>', unsafe_allow_html=True)