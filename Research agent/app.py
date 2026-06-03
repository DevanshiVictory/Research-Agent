import streamlit as st
from openai import OpenAI

# ── API Client (hardcoded) ────────────────────────────────────────────────────
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)
MODEL = "openrouter/free"

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Company Intelligence Agent",
    page_icon="🔍",
    layout="wide",
)

# ── Styles ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #4F46E5, #7C3AED);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stButton > button {
        background: linear-gradient(90deg, #4F46E5, #7C3AED);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
    }
    .stButton > button:hover { opacity: 0.9; }
    section[data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<p class="main-title">🔍 Company Intelligence Agent</p>', unsafe_allow_html=True)
st.markdown("Enter a company name to generate a full AI-powered research & recommendation report.")
st.divider()

# ── Prompt Builder ────────────────────────────────────────────────────────────
def build_prompt(company: str) -> str:
    return f"""You are a senior business intelligence analyst and AI strategy consultant.
A client has asked you to research the company: **{company}**

Generate a comprehensive, structured intelligence report with the following 5 sections.
Be specific to this company — avoid generic filler. Use your knowledge and reasoning.

---

## 1. 🏢 Company Overview
- What does the company do?
- Industry and sector
- Scale (revenue range, employee count if known, founded year)
- Geographic presence (cities, states, countries)

## 2. 📊 Key Business Information
- Major products / services / offerings
- Recent notable developments (last 1–2 years)
- Known expansion plans or upcoming projects
- Key partnerships, subsidiaries, or notable facts

## 3. ⚠️ Potential Business Challenges
Analyze and explain:
- Market or competitive challenges
- Operational bottlenecks specific to this type of business
- Sales and lead conversion challenges
- Customer experience pain points
- Regulatory or compliance risks (if any)
*Explain the reasoning behind each challenge you identify.*

## 4. 🤖 AI Opportunities (Company-Specific)
Suggest 5–7 concrete, specific AI use cases for this company. For each:
- Name the opportunity
- Explain how it applies specifically to {company}
- Describe the expected business impact

Do NOT give generic suggestions. Tie each one directly to the company's business model.

## 5. 🎯 Personalized CEO Pitch (One Page)
Write a compelling, professional pitch as if you are walking into a meeting with the CEO of {company}.
Include:
- Why you reached out to them specifically
- The top 2–3 challenges you identified
- The AI solutions you'd recommend and why they matter NOW
- A clear, confident call to action

Tone: Confident, specific, data-aware, and respectful of their time.

---
Format the report clearly with headers, bullet points, and readable structure.
"""

# ── Streaming ─────────────────────────────────────────────────────────────────
def stream_report(company: str):
    stream = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": build_prompt(company)}],
        stream=True,
        max_tokens=4000,
        extra_headers={
            "HTTP-Referer": "https://company-intelligence-agent.streamlit.app",
            "X-Title": "Company Intelligence Agent",
        }
    )
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# ── Main Input ────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    company_name = st.text_input(
        "Company Name",
        placeholder="e.g. Prestige Group, Adani Realty, Sobha...",
        label_visibility="collapsed",
    )
with col2:
    generate = st.button("Generate Report 🚀")

# ── Generate ──────────────────────────────────────────────────────────────────
if generate:
    if not company_name.strip():
        st.warning("⚠️ Please enter a company name.")
    else:
        st.divider()
        st.subheader(f"📄 Intelligence Report: {company_name.strip()}")

        with st.spinner(f"Researching {company_name.strip()}... this may take 20–40 seconds."):
            report_placeholder = st.empty()
            full_report = ""
            try:
                for chunk in stream_report(company_name.strip()):
                    full_report += chunk
                    report_placeholder.markdown(full_report)

                st.success("✅ Report generated successfully!")
                st.download_button(
                    label="⬇️ Download Report as .txt",
                    data=full_report,
                    file_name=f"{company_name.strip().replace(' ', '_')}_report.txt",
                    mime="text/plain",
                )
            except Exception as e:
                err = str(e)
                if "429" in err:
                    st.error("⚠️ Rate limit hit. Please wait a moment and try again.")
                else:
                    st.error(f"Something went wrong: {e}")