"""
career_roadmap.py
AI Career Roadmap — generates a structured milestone-card roadmap
and persists it in session state across navigation.
"""

import streamlit as st
from utils.api_client import generate_response
from utils import session_state as ss


CAREER_OPTIONS = [
    "Select Career Path",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "Data Analyst",
    "Data Scientist",
    "AI/Machine Learning Engineer",
    "UI/UX Designer",
    "Cloud Engineer",
    "DevOps Engineer",
    "Cybersecurity Analyst",
    "Product Manager",
]


def _build_prompt(goal: str) -> str:
    return f"""
You are an expert career counsellor and senior tech lead.
A user wants to become a highly successful '{goal}'.

Produce a comprehensive career guide in Markdown. Be structured and concise.

## 🎯 Core Skills to Master
(Categorised by priority — beginner → advanced)

## 🏗️ Portfolio Projects
(Exactly 3 standout projects with suggested tech stack and expected outcome)

## 📜 Recommended Certifications
(Industry-recognised certs ranked by ROI)

## 📅 6-Month Milestone Roadmap
Format EXACTLY as milestone cards using this structure for each month block:

### 🗓️ Month 1–2 · Foundations
**Goal:** (one sentence)
**Actions:**
- action 1
- action 2
- action 3

### 🗓️ Month 3–4 · Building
**Goal:** (one sentence)
**Actions:**
- action 1
- action 2
- action 3

### 🗓️ Month 5–6 · Launch
**Goal:** (one sentence)
**Actions:**
- action 1
- action 2
- action 3

## 💡 Insider Interview Tips
(Exactly 3 concise, role-specific tips)
"""


def render():
    st.markdown("<div class='animate-fade-in'>", unsafe_allow_html=True)

    st.markdown("<h1 style='margin-bottom:0;'>🗺️ Career Roadmap</h1>",
                unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8;font-size:1.1rem;'>Get a detailed, "
                "month-by-month plan — saved so you can revisit any time.</p>",
                unsafe_allow_html=True)

    # ── Input form ────────────────────────────────────────────────────────────
    with st.form("roadmap_form"):
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0;color:#a78bfa;'>Career Selection</h3>",
                    unsafe_allow_html=True)
        selected = st.selectbox("Desired Role *", CAREER_OPTIONS, index=0)
        custom   = st.text_input("Or type a custom career goal (overrides dropdown)",
                                 placeholder="e.g., Blockchain Developer")
        st.markdown("</div>", unsafe_allow_html=True)

        submitted = st.form_submit_button(
            "🚀 Generate Roadmap", use_container_width=True)

    # ── Generation ────────────────────────────────────────────────────────────
    if submitted:
        goal = custom.strip() if custom.strip() else selected
        if goal == "Select Career Path":
            st.error("⚠️ Please select a career path or type a custom goal.")
        else:
            with st.spinner(f"🧠 Mapping the optimal path to {goal}…"):
                content = generate_response(_build_prompt(goal))
            ss.set_value("roadmap", "goal",    goal)
            ss.set_value("roadmap", "content", content)
            st.success(f"✅ Roadmap for **{goal}** saved to your session!")

    # ── Display stored result ─────────────────────────────────────────────────
    _show_result()
    st.markdown("</div>", unsafe_allow_html=True)


def _show_result():
    data = ss.get("roadmap")
    if not data.get("content"):
        return

    goal    = data["goal"]
    content = data["content"]

    st.markdown("---")
    st.markdown(f"### 🚀 Your Roadmap — {goal}")

    # Split into sections and render each as a milestone card
    sections = content.split("\n## ")
    for i, section in enumerate(sections):
        if not section.strip():
            continue
        # Re-attach the ## prefix for all but the first chunk
        header_md = section if i == 0 else f"## {section}"

        st.markdown("<div class='glass-card animate-fade-in' "
                    "style='margin-bottom:16px;'>",
                    unsafe_allow_html=True)
        st.markdown(header_md)
        st.markdown("</div>", unsafe_allow_html=True)
