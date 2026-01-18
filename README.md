# FinClarify | Autonomous Financial Safeguard Platform for Inclusive Banking

> **Category:** ACCESS.AI: AI for Accessibility & Inclusion  
> **Status:** Production-Ready MVP  
> **Core Concept:** Zero-Trust Agentic Middleware for Inclusive Finance

---

## 📖 Executive Summary

**FinClarify** is an AI-powered financial middleware designed to transform banking from a transactional utility into an empathetic, active guardian for Persons with Disabilities (PwDs).

Standard digital banking focuses on "frictionless" speed, which can be hazardous for users with cognitive, memory, or impulse control impairments. FinClarify introduces **Agentic Guardianship**: a zero-trust architecture that actively analyzes transaction intent, verifies safety rules in real-time, and intervenes to prevent duplicate payments, unintended overdrafts, and impulse spending.

This solution does not merely "read" the screen; it understands the risk and has the agency to block financial harm before it hits the ledger.

---

## 🏛️ System Architecture

FinClarify functions as a decoupled **Client-Server Enterprise Architecture**:

### 1. The Core Banking API (Backend)
Built on **FastAPI**, this simulates a modern, persistent banking ledger.
*   **Role:** Handles Authentication, Ledger Management, Historical Logging, and Deterministic Rule Analysis (Math/Duplicates).
*   **Zero-Trust Logic:** Provides the system of record and ultimate block/allow status for funds.

### 2. The Agentic Swarm (Intelligence Layer)
Built on **LangGraph**, leveraging **Groq (Llama-3/GPT-OSS)** for real-time inference.
*   **The Investigator:** Forensic agent that analyzes balance math and transaction history for anomalies.
*   **The Compliance Manager:** Policy enforcement agent that maps findings to user disability profiles (e.g., *Memory Impairment = Block Duplicates*).
*   **The Empathy Designer:** Generative agent that creates inclusive assets (Plain English summaries, Audio Scripts, Visual Alert Configuration).

### 3. The Inclusive Client (Frontend)
Built on **Streamlit**, functioning as a WCAG-compliant web portal.
*   **Role:** Renders dynamic interfaces based on Agent output, featuring Lottie animations, Waterfall Charts for financial visualization, and auto-play audio guidance.

---

## ✨ Key Features & Capabilities

| Feature | Accessibility Vector | Implementation Details |
| :--- | :--- | :--- |
| **Active Transaction Blocking** | Memory (Alzheimer's) | Physically disables the "Pay" button when exact duplicate transactions are detected, preventing accidental double-payments. |
| **Dynamic Friction** | Neurodiverse (ADHD) | Introduces review steps (Confirmations) for high-value or late-night transactions to support impulse control. |
| **Visual Math (No Numbers)** | Dyscalculia / Numeracy | Replaces ledger math with **Waterfall Charts**, visualizing funds "draining" to help users grasp financial impact without calculation. |
| **Multi-Modal Output** | Visual / Auditory | Simultaneous delivery of High-Contrast Visuals, Lottie Semantic Animations, and Auto-Play TTS Audio logic. |
| **Plain English Translation** | Cognitive / Dyslexia | Translates complex bank error codes (e.g., `ERR_NSF_404`) into clear warnings like *"Wallet Empty Warning."* |

---

## 🛠️ Technology Stack

*   **Language:** Python 3.9+
*   **API Framework:** FastAPI, Uvicorn
*   **Frontend Interface:** Streamlit, Streamlit-Lottie, Plotly
*   **Agent Orchestration:** LangChain, LangGraph
*   **LLM Inference:** Groq API (High-performance inference)
*   **Accessibility Libraries:** gTTS (Google Text-to-Speech)
*   **Data Models:** Pydantic

---

## 🚀 Installation & Usage Guide

### Prerequisites
*   Python installed on your machine.
*   A valid **Groq API Key**.

### 1. Environmental Setup
Clone the repository and install dependencies.
```bash
uv add fastapi uvicorn requests plotly streamlit langchain-groq langgraph gTTS streamlit-lottie python-dotenv
```

Create a `.env` file in the project root:
```ini
GROQ_API_KEY=gsk_your_key_here
```

### 2. Running the Application
This application mimics a real-world distributed system. You must run the **Server** and **Client** in separate terminal instances.

**Terminal 1: Core Banking Server**
Starts the persistent database and API.
```bash
uv run uvicorn server:app --reload --host 0.0.0.0 --port 8000
```
*> Output should confirm: Uvicorn running on http://0.0.0.0:8000*

**Terminal 2: User Client Portal**
Starts the interface.
```bash
uv run streamlit run client.py
```

---

## 🧪 Demo Login Credentials

To evaluate specific disability guardrails, please use the following credentials (Password is **123** for all):

| Username | Profile | Test Scenario |
| :--- | :--- | :--- |
| **bob** | Memory Impairment | **Duplicate Prevention:** Try to pay "Electric Co" **$120.00** (matches history). Note the red "STOP" block. |
| **alice** | Neurodiverse (ADHD) | **Impulse Control:** Enable "Simulate 2AM" checkbox. Pay **$150.00**. Note the orange "CAUTION" friction. |
| **charlie** | Cognitive (Dyslexia) | **Zero Balance Protection:** Try to pay **$45.00** (his exact balance). Note the visual chart and red block. |
| **diana** | Visual Impairment | **High Value:** Pay **$150.00**. Listen for the automatic Audio Warning description. |
| **admin** | *pass: admin* | **System View:** Login to view the real-time system ledger verifying transaction integrity. |

---

## 🗺️ Future Roadmap

1.  **Phase 1: Universal Mobile Accessibility Service:** Deploying FinClarify as an Android/iOS Accessibility Service to overlay protections on third-party apps (Amazon, Uber) without banking integration.
2.  **Phase 2: Privacy-First Edge Computing:** Migrating from cloud APIs to on-device SLMs (e.g., Phi-3 or Gemma 2B) to process sensitive financial logic entirely offline.
3.  **Phase 3: The Safe-Input Keyboard:** Developing a custom software keyboard that restricts high-value numeric inputs based on preset safety parameters within any application field.
