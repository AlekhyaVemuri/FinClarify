import os
import json
from typing import TypedDict, Dict, Any, List
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END

load_dotenv()
GROQ_MODEL = "openai/gpt-oss-120b"

# --- AGENT STATE (The memory shared between agents) ---
class AgentState(TypedDict):
    # Inputs
    user_profile: str            # "Memory", "ADHD", etc.
    request_data: Dict           # {amount, merchant, is_late_night}
    bank_data: Dict              # {balance, history, risk_analysis_from_server}
    
    # Internal Handover
    investigation_report: str    # Output from Node 1
    compliance_decision: str     # Output from Node 2 (The hard action)
    
    # Final Outputs
    final_json: Dict             # UI Assets
    ui_action: str               # STOP/CAUTION/GO

# =======================================================
# 🕵️ NODE 1: THE INVESTIGATOR AGENT (Data Forensics)
# =======================================================
def investigator_node(state: AgentState):
    """
    Step 1: Look at the raw numbers. Don't decide yet, just find the facts.
    """
    req = state['request_data']
    bank = state['bank_data']
    
    # Construct Evidence
    context = f"""
    REQUEST: Pay ${req['amount']} to '{req['merchant']}' (Late Night: {req['is_late_night']})
    CURRENT BALANCE: ${bank.get('balance', 0)}
    PREVIOUS TRANSACTIONS: {str(bank.get('history', [])[:3])}
    SERVER FLAGS: {str(bank.get('risk_analysis', {}))}
    """
    
    llm = ChatGroq(temperature=0, model_name=GROQ_MODEL, api_key=os.getenv("GROQ_API_KEY"))
    
    system_prompt = """
    You are the Transaction Investigator. Analyze the data for specific triggers.
    
    INVESTIGATION CHECKLIST:
    1. Zero Balance Risk: Does Balance - Amount == 0? (Strictly True/False).
    2. Overdraft Risk: Is Amount > Balance?
    3. High Value Risk: Is Amount > $100?
    4. Duplicate Risk: Does Merchant/Amount match exactly in history?
    
    Output a concise factual report summary.
    """
    
    prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{ctx}")])
    response = prompt | llm
    report = response.invoke({"ctx": context})
    
    return {"investigation_report": report.content}

# =======================================================
# ⚖️ NODE 2: COMPLIANCE MANAGER (Rule Enforcement)
# =======================================================
def compliance_node(state: AgentState):
    """
    Step 2: Apply the Safety Standards based on the Investigator's findings.
    Enforces the User's Rules: 100+ Popups, Zero Balance Rejections.
    """
    profile = state['user_profile']
    report = state['investigation_report']
    req = state['request_data']
    
    llm = ChatGroq(temperature=0, model_name=GROQ_MODEL, api_key=os.getenv("GROQ_API_KEY"))
    
    system_prompt = """
    You are the Safety Compliance Manager. Decide the Action based on findings.
    
    STRICT POLICY RULES:
    1. ZERO BALANCE: If the transaction results in exactly $0.00 left -> ACTION: STOP.
       (Reason: Prevent total funds drain).
       
    2. OVERDRAFT: If Amount > Balance -> ACTION: STOP.
    
    3. DUPLICATE: If duplicate found -> ACTION: STOP.
    
    4. HIGH VALUE ($100+): If Amount > 100 -> ACTION: CAUTION (require confirmation).
       *EXCEPTION: If Profile is 'Neurodiverse/ADHD' AND it is Late Night -> ACTION: STOP.
       
    5. DEFAULT: If no risks -> ACTION: GO.

    User Profile: {profile}
    Investigator Report: {report}
    
    OUTPUT JSON: {{ "action": "STOP/CAUTION/GO", "reason_code": "..." }}
    """
    
    prompt = ChatPromptTemplate.from_messages([("system", system_prompt)])
    res = prompt | llm
    response = res.invoke({"profile": profile, "report": report})
    
    try:
        data = json.loads(response.content.replace("```json", "").replace("```", "").strip())
        action = data['action']
    except:
        action = "STOP" # Fail safe
        
    return {"compliance_decision": action}

# =======================================================
# 🎨 NODE 3: EMPATHY DESIGNER (UX Generation)
# =======================================================
def designer_node(state: AgentState):
    """
    Step 3: Generate the Audio, Visuals, and Text for the specific Action.
    """
    profile = state['user_profile']
    action = state['compliance_decision']
    req = state['request_data']
    
    llm = ChatGroq(temperature=0.4, model_name=GROQ_MODEL, api_key=os.getenv("GROQ_API_KEY"))
    
    sys_prompt = """
    You are FinClarify, an Inclusive UI Designer.
    Create UI content for: Action={action}, Profile={profile}, Amount=${amount}.
    
    DESIGN REQUIREMENTS:
    1. headline: 
       - If STOP/Zero Balance: "EMPTY WALLET PROTECT"
       - If CAUTION/$100+: "HIGH AMOUNT ALERT"
       - If STOP/Duplicate: "DOUBLE PAY ALERT"
       - Max 3-4 words. Uppercase. Emojis allowed.
    
    2. audio_script:
       - If 'Hearing' in profile: "" (Empty).
       - Else: MAX 12 WORDS. Conversational warning. 
       - Example: "Wait. This will leave you with zero dollars."

    3. financial_tip: Educational, grade 5 reading level.

    OUTPUT JSON:
    {{
        "headline": "...",
        "simple_explanation": "...",
        "financial_tip": "...",
        "audio_script": "..."
    }}
    """
    
    chain = ChatPromptTemplate.from_messages([("system", sys_prompt)]) | llm
    res = chain.invoke({"action": action, "profile": profile, "amount": req['amount']})
    
    try:
        content = json.loads(res.content.replace("```json", "").replace("```", "").strip())
    except:
        content = {
            "headline": "SAFETY CHECK",
            "simple_explanation": "We detected a risk.",
            "audio_script": "Please review details.",
            "financial_tip": "Always check details."
        }
        
    return {"final_json": content, "ui_action": action}

# --- COMPILE GRAPH ---
def build_graph():
    wf = StateGraph(AgentState)
    
    # Add Nodes
    wf.add_node("investigator", investigator_node)
    wf.add_node("compliance", compliance_node)
    wf.add_node("designer", designer_node)
    
    # Define Linear Flow
    wf.set_entry_point("investigator")
    wf.add_edge("investigator", "compliance")
    wf.add_edge("compliance", "designer")
    wf.add_edge("designer", END)
    
    return wf.compile()