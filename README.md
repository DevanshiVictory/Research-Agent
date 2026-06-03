# Company Intelligence Agent — Documentation

---

## 1. Approach

The goal was to build a practical, beginner-friendly AI agent that takes a company name as input
and produces a structured 5-section intelligence report.

Rather than scraping the web manually, the system leverages a large language model's built-in
knowledge and reasoning to research the company and generate company-specific insights.

The prompt is carefully engineered to force specificity — the model is explicitly told to avoid
generic answers and tie every recommendation to the specific company's business model.

OpenRouter was chosen as the AI gateway because it provides free access to multiple powerful
LLMs (DeepSeek, LLaMA, Mistral, etc.) through a single unified API — no credit card required.

---

## 2. Architecture

```
User (Streamlit UI)
        │
        ▼
app.py (Streamlit frontend)
        │  collects company name
        ▼
build_prompt(company)
        │  constructs a detailed 5-section prompt
        ▼
OpenRouter API  (openrouter/free)
        │  auto-selects best available free LLM
        │  streams the response back
        ▼
Streamlit renders the report in real-time
        │
        ▼
User can download the report as .txt
```

### Key Design Decisions

- **Streaming:** The response streams token-by-token so the user sees output immediately
  instead of waiting 30+ seconds for the full report.
- **Single file:** Entire app is one `app.py` file — easy to understand, run, and demo.
- **openrouter/free router:** Instead of hardcoding a specific model (which can go offline),
  the app uses OpenRouter's free router that automatically picks the best available free model
  for every request.
- **No API key input for users:** The API key is embedded in the backend so users just open
  the app and start using it — no setup required.

---

## 3. AI Tools Used

| Tool | Purpose |
|------|---------|
| OpenRouter API (`openrouter/free`) | Core intelligence: routes to best free LLM available (DeepSeek, LLaMA, Mistral, etc.) |
| Streamlit | Web UI framework — turns a Python script into a web app instantly |
| Claude (claude.ai) | Used during development to help design, write, and debug the code |

### Why OpenRouter?
- Free to use — no credit card required
- Access to 25+ free models (DeepSeek R1, LLaMA 3.3 70B, Mistral, GPT-OSS, etc.)
- Single API key works for all models
- OpenAI-compatible API — works with the standard `openai` Python library
- `openrouter/free` auto-selects the best available model, so the app never breaks
  if one model goes offline

---

## 4. Challenges Faced

### Challenge 1: Making the output company-specific, not generic
**Problem:** LLMs tend to give generic answers like "AI can help with automation and analytics"
that could apply to any company.

**Solution:** The prompt explicitly instructs the model to tie every suggestion to the company's
specific business model, and repeats the company name multiple times throughout the prompt.
The model is told: "Do NOT give generic suggestions. Tie each one directly to the company's
business model."

---

### Challenge 2: Free models going offline / returning 404 errors
**Problem:** Initially, specific free model IDs like `mistralai/mistral-7b-instruct:free` and
`meta-llama/llama-3.1-8b-instruct:free` were hardcoded. These models were later removed from
OpenRouter's free tier, causing 404 "No endpoints found" errors.

**Solution:** Switched to `openrouter/free` — OpenRouter's own free router that automatically
selects the best available free model for each request. This means the app never breaks even if
individual models are removed.

---

### Challenge 3: Long wait time for users
**Problem:** Generating a full 4000-token report takes 20–40 seconds. Without feedback, users
think the app has frozen.

**Solution:** Used streaming API so text appears word-by-word in real time, giving live
feedback that the system is actively working.

---

### Challenge 4: Deployment failure on Streamlit Cloud
**Problem:** When deploying to Streamlit Cloud, the app failed with:
`ERROR: Invalid requirement: 'agent/requirements.txt'`
The `requirements.txt` file was either missing or in the wrong folder.

**Solution:** Created a `requirements.txt` in the root of the GitHub repository (not inside
any subfolder) with the correct dependencies:
```
streamlit
openai
```
Streamlit Cloud automatically detects and installs packages from this file.

---

## 5. How to Run Locally

### Prerequisites
```bash
pip install streamlit openai
```

### Run the app
```bash
python -m streamlit run app.py
```

Then open http://localhost:8501 in your browser.

---

## 6. How to Deploy on Streamlit Cloud

1. Push your code to GitHub with this structure:
```
your-repo/
├── app.py
└── requirements.txt
```
2. Go to share.streamlit.io
3. Connect your GitHub repo
4. Set main file path to `app.py`
5. Click Deploy

---

## 7. Example Output

For a company like **Prestige Group**, the report generates:

- **Overview** — Founded 1986, Bangalore-based real estate developer, presence in 12+ cities
- **Business Info** — Residential, commercial, retail, hospitality projects; recent launches
- **Challenges** — Long sales cycles, inventory management, broker dependency, RERA compliance
- **AI Opportunities** — AI lead scoring, virtual property tours, document automation, chatbot
- **CEO Pitch** — A personalized one-page pitch connecting their challenges to AI solutions

---

## 8. Possible Improvements (Future Scope)

- Add real-time web search (Tavily / Serper API) for latest news about the company
- Export report as PDF
- Add competitor comparison section
- Cache reports to avoid re-generating for the same company
- Add voice input for company name
- Support multiple languages for regional companies
