"""
linkedin_optimizer.py
LinkedIn Profile Optimizer — persists optimised copy in session state.
"""

import re
import streamlit as st
from utils.api_client import generate_response
from utils import session_state as ss


def _extract(text: str, start: str, end: str) -> str:
    pattern = f"{re.escape(start)}(.*?){re.escape(end)}"
    m = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else ""


def _build_prompt(target_role, current_headline, current_about) -> str:
    return f"""
Act as an expert LinkedIn profile optimiser.

Target Role: {target_role}
Current Headline: {current_headline}
Current About/Background: {current_about}

Respond using EXACTLY these tags:

[HEADLINES_START]
(3 keyword-rich LinkedIn headlines as bullet points)
[HEADLINES_END]

[ABOUT_START]
(Compelling About section: strong hook, key skills, Specialties bullet list, CTA)
[ABOUT_END]

[KEYWORDS_START]
(10–15 comma-separated SEO keywords for this role)
[KEYWORDS_END]
"""


def render():
    st.markdown("<div class='animate-fade-in'>", unsafe_allow_html=True)

    st.markdown("<h1 style='margin-bottom:0;'>🔗 LinkedIn Optimizer</h1>",
                unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8;font-size:1.1rem;'>Transform your "
                "profile into a recruiter magnet — results saved across navigation.</p>",
                unsafe_allow_html=True)

    # ── Input form ────────────────────────────────────────────────────────────
    with st.form("linkedin_form"):
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0;color:#a78bfa;'>Profile Details</h3>",
                    unsafe_allow_html=True)
        target_role       = st.text_input("Target Role / Industry *",
                                          placeholder="Senior Full Stack Developer")
        current_headline  = st.text_input("Current Headline",
                                          placeholder="Software Engineer at TechCorp")
        current_about     = st.text_area("Current About / Background *",
                                         height=130,
                                         placeholder="Developer with 5 years of experience…")
        st.markdown("</div>", unsafe_allow_html=True)

        submitted = st.form_submit_button(
            "✨ Optimise My Profile", use_container_width=True)

    # ── Generation ────────────────────────────────────────────────────────────
    if submitted:
        if not target_role or not current_about:
            st.error("⚠️ Target Role and About section are required.")
        else:
            with st.spinner("🧠 Analysing recruiter patterns and crafting copy…"):
                raw = generate_response(_build_prompt(target_role,
                                                      current_headline,
                                                      current_about))
            ss.set_value("linkedin", "headlines",          _extract(raw, "[HEADLINES_START]", "[HEADLINES_END]"))
            ss.set_value("linkedin", "about",              _extract(raw, "[ABOUT_START]",      "[ABOUT_END]"))
            ss.set_value("linkedin", "keywords",           _extract(raw, "[KEYWORDS_START]",   "[KEYWORDS_END]"))
            ss.set_value("linkedin", "original_headline",  current_headline)
            st.success("✅ Profile optimisation saved to your session!")

    # ── Display stored result ─────────────────────────────────────────────────
    _show_result()
    st.markdown("</div>", unsafe_allow_html=True)


def _show_result():
    data = ss.get("linkedin")
    if not data.get("headlines"):
        return

    st.markdown("---")
    st.markdown("<div class='glass-card animate-fade-in'>", unsafe_allow_html=True)
    st.markdown("### 📊 Before vs After")

    # Headlines
    st.markdown("<h4 style='color:#60a5fa;'>✨ Optimised Headlines</h4>",
                unsafe_allow_html=True)
    if data.get("original_headline"):
        st.markdown(
            f"<p style='color:#f87171;text-decoration:line-through;'>"
            f"Before: {data['original_headline']}</p>",
            unsafe_allow_html=True)
    st.markdown("<p style='color:#34d399;'>After (choose one):</p>",
                unsafe_allow_html=True)
    st.code(data["headlines"], language="markdown")

    # About section
    st.markdown("<h4 style='color:#60a5fa;margin-top:28px;'>📖 Magnetic About Section</h4>",
                unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8;'>Copy this directly into your LinkedIn profile:</p>",
                unsafe_allow_html=True)
    st.code(data["about"], language="markdown")

    # Keywords
    st.markdown("<h4 style='color:#60a5fa;margin-top:28px;'>🔑 SEO Keywords</h4>",
                unsafe_allow_html=True)
    chips = " ".join(
        f"<span style='background:rgba(16,185,129,0.2);"
        f"border:1px solid rgba(16,185,129,0.4);"
        f"padding:4px 12px;border-radius:20px;font-size:0.85rem;"
        f"margin:4px;display:inline-block;'>{k.strip()}</span>"
        for k in data["keywords"].split(",") if k.strip()
    )
    st.markdown(chips or "<em style='color:#94a3b8'>No keywords extracted.</em>",
                unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
