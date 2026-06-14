"""
app.py
AI Career Accelerator — main entry point.
Session state is initialised once here; all modules read/write from it
so generated content persists across sidebar navigation.
"""

import os
import streamlit as st
from dotenv import load_dotenv
from streamlit_option_menu import option_menu

# ── Page config must be the very first Streamlit call ─────────────────────────
st.set_page_config(
    page_title="AI Career Accelerator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session state: initialise all module keys before any module runs ──────────
from utils import session_state as ss
ss.init_session_state()

# ── Load CSS ──────────────────────────────────────────────────────────────────
def _load_css():
    path = os.path.join(os.path.dirname(__file__), "utils", "style.css")
    if os.path.exists(path):
        with open(path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Module imports ─────────────────────────────────────────────────────────────
from modules import (
    resume_builder,
    resume_analyzer,
    portfolio_builder,
    career_roadmap,
    linkedin_optimizer,
    cover_letter_generator,
)

# ── Session state indicator helpers ──────────────────────────────────────────

def _indicator(module: str, field: str = "content") -> str:
    """Return a small dot badge if the module has stored data."""
    return " 🟢" if ss.has_result(module, field) else ""


# ── Sidebar + routing ─────────────────────────────────────────────────────────

def main():
    _load_css()
    load_dotenv()

    with st.sidebar:
        st.markdown(
            "<div style='text-align:center;margin-bottom:20px;'>"
            "<h1 class='gradient-text' style='font-size:2rem;margin-bottom:0;'>"
            "🚀 AI Career</h1>"
            "<h1 class='gradient-text' style='font-size:2rem;margin-top:0;'>"
            "Accelerator</h1></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='text-align:center;color:#94a3b8;font-size:0.85rem;"
            "margin-bottom:24px;'>Your intelligent career growth platform.</p>",
            unsafe_allow_html=True,
        )

        # Navigation — green dot shows when a module has saved data
        selection = option_menu(
            menu_title=None,
            options=[
                "Dashboard",
                f"Resume Builder{_indicator('resume')}",
                f"Cover Letter{_indicator('cover')}",
                f"ATS Analyzer{_indicator('ats', 'score')}",
                f"Portfolio Builder{_indicator('portfolio', 'html')}",
                f"Career Roadmap{_indicator('roadmap')}",
                f"LinkedIn Optimizer{_indicator('linkedin', 'headlines')}",
            ],
            icons=[
                "house",
                "file-earmark-person",
                "envelope-paper",
                "graph-up-arrow",
                "globe",
                "map",
                "linkedin",
            ],
            menu_icon="cast",
            default_index=0,
            styles={
                "container":         {"padding": "0!important",
                                      "background-color": "transparent"},
                "icon":              {"color": "#c084fc", "font-size": "17px"},
                "nav-link":          {"font-size": "14px", "text-align": "left",
                                      "margin": "3px 0",
                                      "--hover-color": "rgba(255,255,255,0.05)",
                                      "font-family": "Outfit"},
                "nav-link-selected": {"background-color": "rgba(139,92,246,0.2)",
                                      "border-left": "4px solid #8b5cf6",
                                      "color": "#f8fafc"},
            },
        )

        st.markdown("---")

        # API key status badge
        api_key = os.getenv("GEMINI_API_KEY", "")
        if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
            st.markdown(
                "<div style='background:rgba(239,68,68,0.1);"
                "border:1px solid rgba(239,68,68,0.3);border-radius:12px;"
                "padding:10px;text-align:center;'>"
                "<span style='color:#fca5a5;font-weight:600;font-size:0.85rem;'>"
                "⚠️ API Key Missing</span></div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<div style='background:rgba(16,185,129,0.1);"
                "border:1px solid rgba(16,185,129,0.3);border-radius:12px;"
                "padding:10px;text-align:center;'>"
                "<span style='color:#6ee7b7;font-weight:600;font-size:0.85rem;'>"
                "✨ AI Engine Active</span></div>",
                unsafe_allow_html=True,
            )

        # Session data summary
        st.markdown("<br>", unsafe_allow_html=True)
        _session_summary()

    # ── Strip indicator dots from the selection label before routing ──────────
    clean = selection.replace(" 🟢", "").strip()

    if   clean == "Dashboard":          _render_dashboard()
    elif clean == "Resume Builder":     resume_builder.render()
    elif clean == "Cover Letter":       cover_letter_generator.render()
    elif clean == "ATS Analyzer":       resume_analyzer.render()
    elif clean == "Portfolio Builder":  portfolio_builder.render()
    elif clean == "Career Roadmap":     career_roadmap.render()
    elif clean == "LinkedIn Optimizer": linkedin_optimizer.render()


def _session_summary():
    """Small sidebar widget showing which modules have saved data."""
    modules = {
        "Resume":    ss.has_result("resume"),
        "Cover":     ss.has_result("cover"),
        "ATS":       ss.has_result("ats", "score"),
        "Portfolio": ss.has_result("portfolio", "html"),
        "Roadmap":   ss.has_result("roadmap"),
        "LinkedIn":  ss.has_result("linkedin", "headlines"),
    }
    saved = [k for k, v in modules.items() if v]
    if saved:
        st.markdown(
            "<p style='color:#94a3b8;font-size:0.78rem;margin-bottom:4px;'>"
            "💾 Saved this session:</p>",
            unsafe_allow_html=True,
        )
        chips = " ".join(
            f"<span style='background:rgba(139,92,246,0.15);"
            f"border:1px solid rgba(139,92,246,0.3);"
            f"padding:2px 8px;border-radius:10px;font-size:0.75rem;'>{m}</span>"
            for m in saved
        )
        st.markdown(chips, unsafe_allow_html=True)


# ── Dashboard ─────────────────────────────────────────────────────────────────

def _render_dashboard():
    st.markdown("<div class='animate-fade-in'>", unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align:center;padding:50px 0 36px;'>
            <span class='premium-badge'>Version 2.0 · Session-Persistent AI Suite</span>
            <h1 style='font-size:4rem;margin-bottom:8px;line-height:1.1;'>
                Supercharge Your <br><span class='gradient-text'>Career Journey</span>
            </h1>
            <p style='font-size:1.2rem;color:#94a3b8;max-width:580px;margin:16px auto 0;'>
                All 6 AI tools — results saved for your entire session.
                No re-generating when you navigate.
            </p>
        </div>
    """, unsafe_allow_html=True)

    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.metric("AI Tools",       "6",     "Integrated")
    sc2.metric("ATS Optimised",  "99%",   "Match Rate")
    sc3.metric("Portfolio Gen",  "< 10s", "Speed")
    sc4.metric("Session State",  "∞",     "Persistent")

    st.markdown("### ✨ Feature Suite")

    features = [
        ("📄", "Resume Builder",
         "One-page, ATS-optimised resume with PDF & DOCX export. "
         "Generate once, download unlimited times."),
        ("✉️", "Cover Letter",
         "Formal, personalised cover letter tailored to any role and company."),
        ("🔍", "ATS Analyzer",
         "Upload your PDF resume for granular ATS scoring, keyword extraction, "
         "and JD matching."),
        ("🌐", "Portfolio Builder",
         "Two-step AI generates your copywriting then wraps it in a stunning "
         "deploy-ready HTML site."),
        ("🗺️", "Career Roadmap",
         "Month-by-month milestone plan with skills, certs, projects, and "
         "interview tips."),
        ("🔗", "LinkedIn Optimizer",
         "Optimised headlines, magnetic About section, and SEO keyword list "
         "for any target role."),
    ]

    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(
                f"<div class='glass-card animate-fade-in' "
                f"style='animation-delay:{0.1*(i+1)}s;'>"
                f"<div style='font-size:2rem;margin-bottom:8px;'>{icon}</div>"
                f"<h3 style='margin-top:0;font-size:1.2rem;'>{title}</h3>"
                f"<p style='color:#cbd5e1;font-size:0.9rem;line-height:1.5;'>{desc}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
