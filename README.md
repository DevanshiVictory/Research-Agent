# Company Intelligence Agent — Documentation

## 1. Approach

The goal was to build a practical, beginner-friendly AI agent that takes a company name as input
and produces a structured 5-section intelligence report. Rather than scraping the web manually,
the system leverages Claude's built-in knowledge and reasoning to research the company and
generate company-specific insights.

The prompt is carefully engineered to force specificity — the model is explicitly told to avoid
generic answers and tie every recommendation to the specific company's business model.

---

## 2. Architecture

```
User (Streamlit UI)
        │
        ▼
app.py (Streamlit frontend)
        │  collects company name + API key
        ▼
build_prompt(company)
        │  constructs a detailed 5-section prompt
        ▼
Anthropic Claude API (claude-sonnet-4-20250514)
        │  streams the response back
        ▼
Streamlit renders the report in real-time
        │
        ▼
User can download the report as .txt
```

**Key design decisions:**
- **Streaming:** The response streams token-by-token so the user sees output immediately instead of waiting.
- **Single file:** Entire app is one `app.py` file — easy to understand, run, and demo.
- **API key in sidebar:** Keeps credentials out of the code. Alternatively, supports `.env` file.

---

## 3. AI Tools Used

| Tool | Purpose |
|------|---------|
| Claude Sonnet 4 (Anthropic API) | Core intelligence: research, analysis, pitch generation |
| Streamlit | Web UI framework — turns a Python script into a web app |
| Claude (claude.ai) | Used during development to help write and debug the code |

---

## 4. Challenges Faced

### Challenge 1: Making the output company-specific, not generic
**Problem:** LLMs tend to give generic "AI can help with automation and analytics" answers.  
**Solution:** The prompt explicitly instructs the model to tie every suggestion to the company's
specific business model, and repeats the company name multiple times throughout the prompt.

### Challenge 2: Long wait time for users
**Problem:** Generating a full 4000-token report takes 20–40 seconds. Users might think it froze.  
**Solution:** Used Claude's streaming API so text appears word-by-word in real time, giving live
feedback that the system is working.

### Challenge 3: API key management for beginners
**Problem:** Hardcoding API keys in source code is a security risk.  
**Solution:** The app reads the key from a sidebar input or from a `.env` environment variable,
never from the code itself.

---

## 5. How to Run

### Prerequisites
```bash
pip install streamlit anthropic
```

### Run the app
```bash
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

### API Key
- Get your key at https://console.anthropic.com
- Paste it in the sidebar when the app opens
- OR create a `.env` file with: `ANTHROPIC_API_KEY=sk-ant-...`

---

## 6. Example Output Sections

For a company like **Prestige Group**, the report generates:
1. **Overview** — Founded 1986, Bangalore-based real estate developer, presence in 12+ cities
2. **Business Info** — Residential, commercial, retail, hospitality projects; recent IPO news etc.
3. **Challenges** — Long sales cycles, inventory management, broker dependency, RERA compliance
4. **AI Opportunities** — AI lead scoring, virtual property tours, document automation, chatbot
5. **CEO Pitch** — A personalized one-page pitch connecting their challenges to AI solutions

---

## 7. Possible Improvements (Future Scope)

- Add real-time web search (Tavily / Serper API) for latest news about the company
- Export report as PDF
- Add competitor comparison section
- Cache reports to avoid re-generating for same company
- Add voice input for company name
