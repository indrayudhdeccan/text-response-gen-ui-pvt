# Text Response Generator UI

A Streamlit app that sends stateless prompts to **Gemini 3.1 Pro Preview** (via OpenRouter) or **Claude Opus 4.6** and logs every interaction to **Supabase**. Optionally syncs to a live Google Sheet via a Supabase database webhook.

## Features

- Switch between Gemini 3.1 Pro Preview and Claude Opus 4.6 from a dropdown
- Every call is stateless -- no conversation memory
- Each prompt gets a unique UUID
- Prompt, response, model name, and timestamp are stored in Supabase
- Modular LLM layer -- add a new model by creating one file and one registry entry

## Project Structure

```
├── app.py                  # Streamlit UI and orchestration
├── llm/
│   ├── base.py             # Abstract LLMClient base class
│   ├── gemini.py           # Gemini client (OpenRouter)
│   ├── claude.py           # Claude client (Anthropic SDK)
│   └── registry.py         # Model name -> client mapping
├── storage/
│   └── supabase.py         # Supabase insert logic
├── .env.example            # Template for required keys
├── .gitignore
├── requirements.txt
└── README.md
```

## Local Setup

### 1. Clone and install

```bash
git clone https://github.com/deccanAI/text-response-gen-ui.git
cd text-response-gen-ui
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Fill in the values in `.env`:

| Variable | Where to get it |
|---|---|
| `OPENROUTER_API_KEY` | [openrouter.ai/keys](https://openrouter.ai/keys) |
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com/) |
| `SUPABASE_URL` | Supabase dashboard > Project Settings > General (URL is `https://<project-id>.supabase.co`) |
| `SUPABASE_KEY` | Supabase dashboard > Project Settings > API > Publishable key |

### 3. Create the Supabase table

Run this SQL in the Supabase SQL Editor:

```sql
CREATE TABLE responses (
  id UUID PRIMARY KEY,
  prompt TEXT NOT NULL,
  response TEXT NOT NULL,
  model TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 4. Run locally

```bash
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this repo to GitHub (already at `deccanAI/text-response-gen-ui`)
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app** and select the repo, branch `main`, and file `app.py`
4. Go to **Advanced settings > Secrets** and paste:

   ```toml
   OPENROUTER_API_KEY = "your-key"
   ANTHROPIC_API_KEY = "your-key"
   SUPABASE_URL = "https://your-project.supabase.co"
   SUPABASE_KEY = "your-publishable-key"
   ```

5. Click **Deploy** -- your app will be live at `https://<app-name>.streamlit.app`

## Optional: Live Google Sheets Sync

Auto-sync every new row to a Google Sheet using a Supabase database webhook:

1. Create a Google Sheet with headers: `id | prompt | response | model | created_at`
2. Open **Extensions > Apps Script** and deploy a `doPost` web app that appends rows
3. In Supabase, go to **Database > Webhooks**, create a webhook on `INSERT` to the `responses` table pointing to your Apps Script URL

## Adding a New Model

1. Create a new file in `llm/` (e.g. `llm/mistral.py`) with a class that extends `LLMClient`
2. Add an entry to `_REGISTRY` in `llm/registry.py`

That's it -- the UI picks it up automatically.
