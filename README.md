# ◈ DecisionLog — AI Decision Extractor

> *Minute-takers tell you what happened. DecisionLog tells you why things are the way they are.*

**Built by ShayOX · GDG London Build with AI Hackathon 2026**

---

## What is DecisionLog?

Every team makes dozens of decisions every week. But three months later, nobody can remember why. The decision is buried in a Slack thread. The reasoning is gone. The alternatives considered — forgotten entirely.

DecisionLog fixes this. Paste any workplace discussion — Slack thread, email chain, meeting notes — and Gemini 2.5 extracts every decision automatically. No forms. No manual logging. Just paste and go.

---

## Live Demo

🌐 **[shayoxdecisionlog.streamlit.app](https://shayoxdecisionlog.streamlit.app)**

📹 **[Demo Video](https://youtu.be/13K4kAW59WE)**

---

## What it extracts

For every decision found in your discussion:

| Field | Description |
|-------|-------------|
| **Decision** | The specific choice that was made |
| **Reasoning** | Why this option was selected |
| **Alternatives Rejected** | What was considered and ruled out |
| **Owner** | Who is accountable for execution |
| **Confidence** | High / Medium / Low |
| **Tags** | Topic keywords for search and filtering |

The **Alternatives Rejected** field is the killer feature — no minute-taker reliably captures why you *didn't* do something. DecisionLog does it automatically, every time.

---

## Tech Stack

- **Frontend:** Streamlit
- **AI:** Gemini 2.5 Flash (Google)
- **Language:** Python 3.11
- **Deployment:** Streamlit Community Cloud

---

## Local Setup

```bash
git clone https://github.com/saileshvyas/decisionlog.git
cd decisionlog
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

Run:
```bash
streamlit run app.py
```

---

## Roadmap

| Version | Timeline | Capabilities |
|---------|----------|-------------|
| **v1** | Now | Paste input · Gemini extraction · Session log · CSV export |
| **v2** | 2 weeks | Slack bot · Google Meet integration · Firestore persistence |
| **v3** | Q2 2026 | Ambient AI · BigQuery analytics · Conflict detection · Weekly digest |

---

## Security & Enterprise Design

Built with enterprise readiness in mind:

- **SSO** via Google Workspace — no separate credentials
- **Vertex AI** for production (data residency guarantees)
- **RBAC** — team scoping, role-based access
- **GDPR** — retention policies, right to erasure
- **Immutable audit log** — append-only decision records
- **Google Secret Manager** for secrets in production

---

## About

Built solo in a single day by **Sailesh Vyas** for the GDG London Build with AI Hackathon 2026.

I am not a software engineer. I don't have a technical background. But I believe AI has fundamentally changed what one person can build — and this project is my proof of that.

---

*Part of the ShayOX Internal Tools Platform*