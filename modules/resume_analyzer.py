"""
resume_analyzer.py
ATS Resume Analyzer — results persisted in session state so users
can navigate away and return without re-uploading.
"""

import re
import streamlit as st
from utils.api_client import generate_response
from utils.pdf_extractor import extract_text_from_pdf
from utils import session_state as ss


# ── Text extraction helpers ────────────────────────────────────────────────────

def _extract(text: str, start: str, end: str) -> str:
    """Pull content between two marker tags."""
    pattern = f"{re.escape(start)}(.*?){re.escape(end)}"
    m = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else ""


# ── Render ─────────────────────────────────────────────────────────────────────

def render():
    st.markdown("<div class='animate-fade-in'>", unsafe_allow_html=True)

    st.markdown("<h1 style='margin-bottom:0;'>🔍 ATS Analyzer</h1>",
                unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8;font-size:1.1rem;'>Deep ATS scoring, "
                "keyword analysis, and JD matching — results stay in your session.</p>",
                unsafe_allow_html=True)

    # ── Upload + JD area ──────────────────────────────────────────────────────
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload Resume PDF *", type=["pdf"])
    jd       = st.text_area("Job Description (optional — for JD matching)",
                             height=110,
                             placeholder="Paste the job description here…")
    c1, c2 = st.columns(2)
    with c1:
        analyze_btn  = st.button("📊 Analyse Resume", use_container_width=True)
    with c2:
        jd_match_btn = st.button("🎯 Match vs Job Description",
                                 use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Run analysis ──────────────────────────────────────────────────────────
    if uploaded and analyze_btn:
        resume_text = extract_text_from_pdf(uploaded)
        if "Error" in resume_text:
            st.error(resume_text)
        else:
            _run_analysis(resume_text)

    if uploaded and jd_match_btn:
        if not jd.strip():
            st.warning("Please paste a job description to use JD matching.")
        else:
            resume_text = extract_text_from_pdf(uploaded)
            if "Error" in resume_text:
                st.error(resume_text)
            else:
                _run_jd_match(resume_text, jd)

    # ── Always show stored results ────────────────────────────────────────────
    _show_analysis_result()
    _show_jd_match_result()

    st.markdown("</div>", unsafe_allow_html=True)


def _run_analysis(resume_text: str):
    with st.spinner("🧠 Analysing your resume…"):
        prompt = f"""
You are an expert ATS recruiter. Evaluate the resume below.
Respond using EXACTLY these tags:

[SCORE_START](number 0-100)[SCORE_END]
[STRENGTHS_START](bullet points)[STRENGTHS_END]
[WEAKNESSES_START](bullet points)[WEAKNESSES_END]
[KEYWORDS_START](comma-separated keywords found)[KEYWORDS_END]
[SUGGESTIONS_START](detailed markdown improvement steps)[SUGGESTIONS_END]

Resume:
{resume_text}
"""
        raw = generate_response(prompt)

    score_str = _extract(raw, "[SCORE_START]", "[SCORE_END]")
    score = int(re.search(r"\d+", score_str).group()) if re.search(r"\d+", score_str) else 0

    ss.set_value("ats", "score",       score)
    ss.set_value("ats", "strengths",   _extract(raw, "[STRENGTHS_START]",   "[STRENGTHS_END]"))
    ss.set_value("ats", "weaknesses",  _extract(raw, "[WEAKNESSES_START]",  "[WEAKNESSES_END]"))
    ss.set_value("ats", "keywords",    _extract(raw, "[KEYWORDS_START]",    "[KEYWORDS_END]"))
    ss.set_value("ats", "suggestions", _extract(raw, "[SUGGESTIONS_START]", "[SUGGESTIONS_END]"))
    st.success("✅ Analysis complete and saved to your session!")


def _run_jd_match(resume_text: str, jd: str):
    with st.spinner("🧠 Matching resume against job description…"):
        prompt = f"""
You are an expert ATS. Compare the resume to the job description.
Respond using EXACTLY these tags:

[MATCH_START](number 0-100)[MATCH_END]
[MISSING_START](comma-separated missing skills)[MISSING_END]
[SUGGESTIONS_START](actionable tailoring steps in markdown)[SUGGESTIONS_END]

Job Description:
{jd}

Resume:
{resume_text}
"""
        raw = generate_response(prompt)

    match_str = _extract(raw, "[MATCH_START]", "[MATCH_END]")
    pct = int(re.search(r"\d+", match_str).group()) if re.search(r"\d+", match_str) else 0

    ss.set_value("ats", "match_pct",          pct)
    ss.set_value("ats", "missing",            _extract(raw, "[MISSING_START]",    "[MISSING_END]"))
    ss.set_value("ats", "match_suggestions",  _extract(raw, "[SUGGESTIONS_START]","[SUGGESTIONS_END]"))
    st.success("✅ JD match complete and saved to your session!")


def _score_ring(score: int, label: str, color: str = "#8b5cf6"):
    """Render the circular progress ring + label."""
    deg = int((score / 100) * 360)
    st.markdown(
        f"""<div class='glass-card' style='text-align:center;'>
            <h3 style='margin-top:0;color:#a78bfa;'>{label}</h3>
            <div class='circular-progress'
                 style='--progress:{deg}deg;
                        background:conic-gradient({color} {deg}deg,
                        rgba(255,255,255,0.05) 0deg);'>
                <div class='circular-value'>{score}%</div>
            </div>
        </div>""",
        unsafe_allow_html=True)


def _keyword_chips(csv: str, bg: str, border: str):
    chips = " ".join(
        f"<span style='background:{bg};border:1px solid {border};"
        f"padding:4px 12px;border-radius:20px;font-size:0.85rem;"
        f"margin:4px;display:inline-block;'>{k.strip()}</span>"
        for k in csv.split(",") if k.strip()
    )
    st.markdown(chips or "<em style='color:#94a3b8'>None found.</em>",
                unsafe_allow_html=True)


def _show_analysis_result():
    data = ss.get("ats")
    if data.get("score") is None:
        return

    score = data["score"]
    st.markdown("---")
    st.markdown("### 📊 ATS Analysis Results")

    c1, c2 = st.columns([1, 2])
    with c1:
        _score_ring(score, "Overall ATS Score")
        verdict = ("🟢 Excellent" if score >= 80
                   else "🟡 Needs Work" if score >= 60
                   else "🔴 Critical Updates")
        st.markdown(f"<p style='text-align:center;font-weight:600;"
                    f"margin-top:12px;'>{verdict}</p>",
                    unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### 🔑 Detected Keywords")
        _keyword_chips(data["keywords"],
                       "rgba(139,92,246,0.2)", "rgba(139,92,246,0.4)")
        st.markdown("</div>", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("<div class='glass-card' style='border-top:4px solid #34d399;'>",
                    unsafe_allow_html=True)
        st.markdown("### 💪 Strengths")
        st.markdown(data["strengths"])
        st.markdown("</div>", unsafe_allow_html=True)
    with c4:
        st.markdown("<div class='glass-card' style='border-top:4px solid #f87171;'>",
                    unsafe_allow_html=True)
        st.markdown("### ⚠️ Weaknesses")
        st.markdown(data["weaknesses"])
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 💡 Improvement Suggestions")
    st.markdown(data["suggestions"])
    st.markdown("</div>", unsafe_allow_html=True)


def _show_jd_match_result():
    data = ss.get("ats")
    if data.get("match_pct") is None:
        return

    pct = data["match_pct"]
    st.markdown("---")
    st.markdown("### 🎯 JD Match Results")

    c1, c2 = st.columns([1, 2])
    with c1:
        _score_ring(pct, "JD Match Score", "#3b82f6")
    with c2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### ❌ Missing Keywords")
        _keyword_chips(data["missing"],
                       "rgba(248,113,113,0.2)", "rgba(248,113,113,0.4)")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 🔧 Tailoring Suggestions")
    st.markdown(data["match_suggestions"])
    st.markdown("</div>", unsafe_allow_html=True)
