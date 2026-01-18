# 🛡️ FinClarify | Access.AI Hackathon
### **The Agentic Guardian for Inclusive Banking**

> **Where Artificial Intelligence meets Zero-Trust Financial Safety.**  
> *A submission for the TCS Access.AI Hackathon*

---

## 📖 Overview

**FinClarify** is an AI-powered "Guardian Middleware" designed to make banking safe and accessible for Persons with Disabilities (PwDs).

Current banking apps operate on a "frictionless" model, assuming users have perfect memory, vision, and impulse control. For neurodiverse users, the elderly, or those with cognitive impairments, this design philosophy can lead to duplicates payments, accidental overdrafts, and financial vulnerability.

**FinClarify solves this by:**
1.  **Intercepting** every transaction in real-time.
2.  **Analyzing** intent and safety using a **Multi-Agent AI Swarm**.
3.  **Enforcing** physical guardrails (removing buttons) when critical risks are detected.
4.  **Adapting** the UI via Generative AI to match the user's specific disability (Plain English, Audio, or High-Contrast visuals).

---

## ✨ Key Features

*   **🧠 Multi-Agent Logic:** Uses **LangGraph** to separate concerns. An *Investigator Agent* detects math/history facts, while an *Empathy Agent* generates the UI.
*   **🔒 Zero-Trust Guardrails:** Hard-coded protection against **Zero Balance** draining and **Duplicate Transactions**.
*   **🔊 Multi-Modal Output:** Auto-playing audio instructions (TTS), Lottie Animations, and dynamic Waterfall Charts to visualize math.
*   **👥 5 Distinct Personas:** Custom rules engines for Memory Impairment (Alzheimer's), ADHD (Impulse Control), Dyslexia, Visual, and Hearing impairments.
*   **🏗️ Enterprise Simulation:** A full-stack architecture featuring a **FastAPI Banking Core** and a **Streamlit Client Portal**.

---

## 🛠️ Tech Stack

*   **Architecture:** Client-Server (REST API).
*   **Frontend:** Python Streamlit, Plotly, Streamlit-Lottie.
*   **Backend (Banking Core):** FastAPI, Uvicorn, Pydantic.
*   **AI Orchestration:** LangChain, LangGraph.
*   **LLM Inference:** Groq API (Llama-3 / GPT-OSS).
*   **Accessibility Tools:** gTTS (Google Text-to-Speech), WCAG color standards.

---

## 📂 Project Structure

```text
finclarify/
├── agents.py           # The AI Brain (LangGraph Multi-Agent implementation)
├── client.py           # The Frontend (Streamlit FinClarify Portal)
├── server.py           # The Backend (FastAPI Core Banking System)
├── .env                # API Keys 
├── pyproject.toml      # Dependency management
└── README.md           # Documentation
```

---

## 🚀 Installation & Setup

### Prerequisites
*   Python 3.9+
*   An API Key from [Groq](https://console.groq.com)

### 1. Clone & Dependencies
FinClarify manages dependencies using `uv` (or `pip`).

```bash
# Install UV (if not installed) or use standard pip
pip install fastapi uvicorn requests plotly streamlit langchain-groq langgraph gTTS streamlit-lottie python-dotenv

# OR using uv
uv add fastapi uvicorn requests plotly streamlit langchain-groq langgraph gTTS streamlit-lottie python-dotenv
```

### 2. Environment Config
Create a `.env` file in the root folder:

```ini
GROQ_API_KEY=gsk_your_actual_api_key_here
```

---

## ▶️ Running the Application

FinClarify mimics a real-world environment. You must run the **Banking Core (Server)** and the **User Portal (Client)** simultaneously.

**⚠️ YOU NEED TWO SEPARATE TERMINAL WINDOWS.**

### Terminal 1: The Banking Server
This runs the core ledger, authentication, and history log.
```bash
# Run server binding to all interfaces to bypass local proxies
uv run uvicorn server:app --reload --host 0.0.0.0 --port 8000
```
*Wait until you see: `Uvicorn running on http://0.0.0.0:8000`*

### Terminal 2: The User Client
This runs the interactive application.
```bash
uv run streamlit run client.py
```

---

## 🧪 Demo Scenarios (Evaluation Guide)

Log in to the portal using these credentials to test specific accessibility guardrails.

### Scenario A: Memory Protection (Preventing Duplicates)
*   **User:** `bob` | **Pass:** `123`
*   **Context:** Bob has Memory Impairment.
*   **Action:** Try to pay **"Electric Co"** exactly **$120.00**.
*   **Result:** The Agents detect this exists in history. A **RED STOP Banner** appears. The "Confirm" button is physically removed.
*   **Audio:** *"Stop. You have already paid this bill."*

### Scenario B: Zero-Balance Safety
*   **User:** `charlie` | **Pass:** `123`
*   **Context:** Charlie (Dyslexia) struggles with complex numbers.
*   **Action:** Try to pay **$45.00** (This matches his exact balance).
*   **Result:** **RED STOP Banner**. "Wallet Empty Warning."
*   **Innovation:** A **Waterfall Chart** visualizes the balance dropping to zero, aiding cognitive understanding.

### Scenario C: Impulse Control (ADHD)
*   **User:** `alice` | **Pass:** `123`
*   **Context:** Alice has ADHD.
*   **Action:**
    1. Check the box **"Simulate 2:00 AM"**.
    2. Try to pay **$150.00**.
*   **Result:** **ORANGE CAUTION Banner**.
*   **Behavior:** Positive Friction. The user is asked to verify intent before proceeding, slowing down impulsive actions.

### Scenario D: Admin Interoperability
*   **User:** `admin` | **Pass:** `admin`
*   **Action:** View the **System-Wide Ledger**. You will see transactions from Alice or Diana reflected in real-time, proving the backend is persistent and robust.

---

## ⚖️ Evaluation Criteria Mapping

| Criterion | Implementation |
| :--- | :--- |
| **Clarity** | Clear distinction between Backend logic and Agentic reasoning. 5 Distinct personas. |
| **Innovation** | Moving from passive assistance to **Active Agentic Protection** (hard-blocking risky actions). |
| **Accessibility** | Solution speaks (Audio), shows (Charts/Lottie), and tells (Plain Text). |
| **Business Impact** | Prevents "friendly fraud," reduces chargeback operational costs, and enables "Vulnerable Customer" compliance. |

---

## 🔮 Future Roadmap

*   **Biometric Sentiment Analysis:** Detecting user distress via camera API to trigger automatic support calls.
*   **Predictive Trends:** Using ML to predict manic spending episodes based on historical velocity, not just static rules.
*   **Open Banking Plugin:** Porting FinClarify to a Chrome Extension to overlay on top of *any* bank (Chase, Citi, HSBC).

---

> Built with ❤️ for the **Access.AI Hackathon**
