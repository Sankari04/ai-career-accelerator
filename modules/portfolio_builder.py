"""
portfolio_builder.py
AI Portfolio Builder — two-step AI generation (copy → HTML),
full result persisted in session state so preview survives navigation.
"""

import streamlit as st
import streamlit.components.v1 as components
from utils.api_client import generate_response
from utils import session_state as ss


def _copy_prompt(name, skills, projects, education, certifications) -> str:
    return f"""
Act as a top Silicon Valley copywriter. Generate polished portfolio copy for:

Name: {name}
Skills: {skills}
Projects: {projects}
Education: {education}
Certifications: {certifications}

Produce:
1. **Headline / Tagline** — catchy one-liner.
2. **About Me** — engaging ~150-word paragraph that sells value.
3. **Skills Summary** — categorised skill groups.
4. **Project Highlights** — results-focused descriptions per project.
5. **Call to Action** — strong closing statement.
"""


def _html_prompt(copy_text: str) -> str:
    return f"""
You are a world-class UI engineer. Wrap the content below in a complete,
stunning single-page HTML portfolio with inline CSS only.

Requirements:
- Dark theme (#0f172a → #1e1b4b gradient background).
- Glassmorphism project cards (rgba + backdrop-filter).
- Google Fonts: 'Outfit' and 'Inter'.
- Sticky navbar, responsive layout.
- Subtle fade-in animations.
- Project cards with hover scale effect and gradient border.

Content:
{copy_text}

Return ONLY raw HTML — no markdown code fences.
"""


def render():
    st.markdown("<div class='animate-fade-in'>", unsafe_allow_html=True)

    st.markdown("<h1 style='margin-bottom:0;'>🌐 Portfolio Builder</h1>",
                unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8;font-size:1.1rem;'>Generate a deploy-ready "
                "personal site — preview and download persisted across navigation.</p>",
                unsafe_allow_html=True)

    # ── Input form ────────────────────────────────────────────────────────────
    with st.form("portfolio_form"):
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0;color:#a78bfa;'>Profile Information</h3>",
                    unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            name   = st.text_input("Full Name *", placeholder="Jane Doe")
            skills = st.text_area("Key Skills *",
                                  placeholder="React, Node.js, UI/UX…", height=100)
        with c2:
            education      = st.text_area("Education",
                                          placeholder="BSc Computer Science…", height=100)
            certifications = st.text_area("Certifications",
                                          placeholder="AWS Certified Developer…", height=100)

        st.markdown("<h3 style='margin-top:10px;color:#a78bfa;'>Projects</h3>",
                    unsafe_allow_html=True)
        projects = st.text_area("Projects (brief overview)",
                                placeholder="1. E-commerce Platform — React/Node\n"
                                            "2. AI Chatbot — Python/OpenAI",
                                height=120)
        st.markdown("</div>", unsafe_allow_html=True)

        submitted = st.form_submit_button(
            "✨ Generate Portfolio", use_container_width=True)

    # ── Generation ────────────────────────────────────────────────────────────
    if submitted:
        if not name or not skills:
            st.error("⚠️ Name and Skills are required.")
        else:
            with st.spinner("🧠 Step 1 — writing portfolio copy…"):
                copy_text = generate_response(
                    _copy_prompt(name, skills, projects, education, certifications))

            with st.spinner("🎨 Step 2 — designing the HTML site…"):
                html = generate_response(_html_prompt(copy_text))
                # Strip accidental markdown fences
                html = html.strip()
                if html.startswith("```"):
                    html = re.sub(r"^```[a-z]*\n?", "", html)
                    html = re.sub(r"\n?```$", "", html)

            ss.set_value("portfolio", "text",  copy_text)
            ss.set_value("portfolio", "html",  html)
            ss.set_value("portfolio", "name",  name.replace(" ", "_"))
            st.success("✅ Portfolio generated and saved to your session!")

    # ── Display stored result ─────────────────────────────────────────────────
    _show_result()
    st.markdown("</div>", unsafe_allow_html=True)


def _show_result():
    data = ss.get("portfolio")
    if not data.get("html"):
        return

    tab1, tab2 = st.tabs(["👁️ Live Preview", "📝 Copy Outline"])

    with tab1:
        st.markdown("<div class='glass-card animate-fade-in'>",
                    unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col2:
            fname = data.get("name", "portfolio")
            st.download_button("📥 Download HTML",
                data=data["html"],
                file_name=f"{fname}_Portfolio.html",
                mime="text/html",
                use_container_width=True,
                key="portfolio_html_dl")
        with col1:
            st.markdown("#### Interactive Preview")
        components.html(data["html"], height=820, scrolling=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='glass-card animate-fade-in'>",
                    unsafe_allow_html=True)
        st.markdown("### Copywriting Outline")
        st.markdown(data["text"])
        st.markdown("</div>", unsafe_allow_html=True)


# re import needed inside module for the strip
import re
