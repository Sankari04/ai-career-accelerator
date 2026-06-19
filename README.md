# 🚀 AI Career Accelerator

An AI-powered career development platform built with Python, Streamlit, and the Google Gemini API.

## Features

| Module | Description |
|---|---|
| 📄 Resume Builder | One-page ATS-optimised resume — PDF & DOCX export |
| ✉️ Cover Letter | Personalised cover letters with PDF & DOCX export |
| 🔍 ATS Analyzer | Resume scoring, keyword extraction, JD matching |
| 🌐 Portfolio Builder | AI-generated deploy-ready HTML portfolio site |
| 🗺️ Career Roadmap | Month-by-month milestone plans with skills & certs |
| 🔗 LinkedIn Optimizer | Optimised headlines, About section, and SEO keywords |

All generated content persists across navigation — no re-generating when switching modules.

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/Sankari04/ai-career-accelerator.git
cd ai-career-accelerator
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure your API key
```bash
cp .env1 .env
# Open .env and paste your Gemini API key
```
Get a free key at [Google AI Studio](https://aistudio.google.com/app/apikey).

### 4. Run the app
```bash
streamlit run app.py
```

## ⚠️ Security Note
Never commit your `.env` file. It is listed in `.gitignore`.
Always use `.env1` as the template for collaborators.

## Tech Stack
- [Streamlit](https://streamlit.io/)
- [Google Gemini API](https://ai.google.dev/)
- [python-docx](https://python-docx.readthedocs.io/)
- [fpdf](http://www.fpdf.org/)
- [PyPDF2](https://pypdf2.readthedocs.io/)
