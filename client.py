import streamlit as st
import requests
import time
import pandas as pd
import plotly.graph_objects as go
import base64
from gtts import gTTS
from io import BytesIO
from streamlit_lottie import st_lottie
from agents import build_graph

# --- NETWORK ---
s = requests.Session()
s.trust_env = False
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="FinClarify", page_icon="🛡️", layout="wide")

# --- CSS ---
st.markdown("""<style>
div.stButton > button {width: 100%; border-radius: 8px;}
h1 {color: #2E7D32;}
</style>""", unsafe_allow_html=True)

# --- ASSETS ---
LOTTIE_STOP = "https://assets10.lottiefiles.com/packages/lf20_khtrvr9z.json"
LOTTIE_WARN = "https://assets10.lottiefiles.com/packages/lf20_5tkzkblw.json"
LOTTIE_GO = "https://assets10.lottiefiles.com/packages/lf20_znxmwbj8.json"

# --- FUNCTIONS ---
def get_lottie(url):
    try: return s.get(url, timeout=1).json()
    except: return None

def autoplay_audio(text):
    if not text: return
    try:
        tts = gTTS(text=text, lang='en')
        fp = BytesIO(); tts.write_to_fp(fp); fp.seek(0)
        b64 = base64.b64encode(fp.read()).decode()
        md = f"""<audio id="snd" autoplay><source src="data:audio/mp3;base64,{b64}"></audio><script>setTimeout(()=>document.getElementById("snd").play(),500);</script>"""
        st.markdown(md, unsafe_allow_html=True)
    except: pass

def logout(): st.session_state.clear(); st.rerun()

# --- STATE ---
if "agent_graph" not in st.session_state: st.session_state.agent_graph = build_graph()
if "auth" not in st.session_state: st.session_state.auth = None
if "role" not in st.session_state: st.session_state.role = None
if "step" not in st.session_state: st.session_state.step = "HOME"

# ================================
# 1. LOGIN
# ================================
if not st.session_state.auth:
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.title("FinClarify Login")
        
        # Connection Status
        try: 
            s.get(API_URL, timeout=1)
            st.success("🟢 Banking Core Online")
        except: 
            st.error("🔴 Server Offline. Check Terminal 1.")
            st.stop()

        with st.form("login_form"):
            u = st.text_input("Username").strip().lower()
            p = st.text_input("Password", type="password")
            if st.form_submit_button("Sign In"):
                try:
                    res = s.post(f"{API_URL}/login", json={"username":u, "password":p})
                    if res.status_code == 200:
                        d = res.json()
                        st.session_state.auth = d["user_id"]
                        st.session_state.role = d["role"]
                        st.session_state.u_name = d.get("name","User")
                        st.rerun()
                    else: st.error("❌ Login Failed. Check server logs.")
                except Exception as e:
                    st.error(f"Network Error: {e}")
        
        with st.expander("Details"):
            st.text("bob / 123  (Memory)\nalice / 123  (ADHD)\ncharlie / 123  (Dyslexia)\ndiana / 123  (Visual)")

# ================================
# 2. ADMIN
# ================================
elif st.session_state.role == "admin":
    st.sidebar.button("Logout", on_click=logout)
    st.title("Admin Ledger")
    logs = s.get(f"{API_URL}/admin/logs").json()
    if logs: st.dataframe(logs, use_container_width=True)
    else: st.info("No Transactions yet.")
    if st.button("Refresh"): st.rerun()

# ================================
# 3. USER
# ================================
elif st.session_state.role == "user":
    uid = st.session_state.auth
    
    try:
        udata = s.get(f"{API_URL}/account/{uid}").json()
        bal = udata.get("balance", 0)
    except: st.error("Server Disconnected"); st.stop()

    with st.sidebar:
        st.title(st.session_state.u_name)
        st.success(f"Mode: {udata.get('profile', 'Standard')}")
        late = st.checkbox("Simulate 2AM")
        st.button("Log Out", on_click=logout)

    if st.session_state.step == "HOME":
        st.metric("Balance", f"${bal:.2f}")
        c1, c2 = st.columns([1, 1])
        with c1:
            with st.form("pay"):
                st.subheader("Send Money")
                mer = st.text_input("Merchant", "Electric Co")
                amt = st.number_input("Amount", 0.0, step=10.0)
                if st.form_submit_button("Pay"):
                    st.session_state.mer = mer
                    st.session_state.amt = amt
                    st.session_state.step = "POPUP"
                    st.rerun()
        with c2:
            st.markdown("**History**")
            for t in udata.get('history',[])[:3]:
                st.markdown(f"- **${t['amount']}** to {t['merchant']}")
                st.divider()

    elif st.session_state.step == "POPUP":
        with st.spinner("AI Analysis..."):
            # 1. API Risk Logic
            r_api = s.post(f"{API_URL}/analyze_risk", json={"user_id":uid, "merchant":st.session_state.mer, "amount":st.session_state.amt, "is_late_night":late}).json()
            
            # 2. Agent Logic
            agent_in = {
                "user_profile": udata['profile'], 
                "request_data": {"amount":st.session_state.amt, "merchant":st.session_state.mer, "is_late_night":late}, 
                "bank_data": {"balance":bal, "history":udata.get("history",[]), "risk_analysis":r_api}, 
                "investigation_report":"", "compliance_decision":"", "final_json":{}, "ui_action":""
            }
            res = st.session_state.agent_graph.invoke(agent_in)
            act, data = res['ui_action'], res['final_json']

        c = "#C62828" if act == "STOP" else ("#EF6C00" if act == "CAUTION" else "#2E7D32")
        ico = "🛑" if act == "STOP" else ("⚠️" if act == "CAUTION" else "✅")
        
        st.markdown(f"<div style='background:{c};padding:20px;border-radius:15px;color:white;text-align:center'><h1>{ico} {data.get('headline')}</h1></div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns([1, 2])
        with c1:
            fig = go.Figure(go.Waterfall(orientation="v", measure=["relative","relative","total"],
                 x=["Start","Pay","End"], y=[bal, -st.session_state.amt, bal-st.session_state.amt],
                 decreasing={"marker":{"color":c}}, totals={"marker":{"color":"#444"}}))
            fig.update_layout(height=180, margin=dict(t=0,b=0,l=0,r=0)); st.plotly_chart(fig, use_container_width=True)
            l = get_lottie(LOTTIE_STOP if act=="STOP" else (LOTTIE_WARN if act=="CAUTION" else LOTTIE_GO))
            if l: st_lottie(l, height=80)

        with c2:
            st.markdown(f"#### {data.get('simple_explanation')}")
            st.info(f"💡 {data.get('financial_tip')}")
            autoplay_audio(data.get('audio_script'))
            
            if act == "STOP":
                st.error("System Blocked.")
                if st.button("Cancel"): st.session_state.step="HOME"; st.rerun()
            elif act == "CAUTION":
                ca, cb = st.columns(2)
                if ca.button("Confirm"): 
                    s.post(f"{API_URL}/execute", json={"user_id":uid, "merchant":st.session_state.mer, "amount":st.session_state.amt})
                    st.success("Done"); time.sleep(1); st.session_state.step="HOME"; st.rerun()
                if cb.button("Cancel"): st.session_state.step="HOME"; st.rerun()
            else:
                if st.button("Send Money"):
                    s.post(f"{API_URL}/execute", json={"user_id":uid, "merchant":st.session_state.mer, "amount":st.session_state.amt})
                    st.success("Done"); time.sleep(1); st.session_state.step="HOME"; st.rerun()