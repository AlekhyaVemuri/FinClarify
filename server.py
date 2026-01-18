import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="FinClarify Core Banking")

# 1. NETWORK SECURITY: Allow All Connections (Fixes Proxy issues)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. MODELS
class LoginRequest(BaseModel):
    username: str
    password: str

class TransactionRequest(BaseModel):
    user_id: str
    merchant: str
    amount: float
    is_late_night: bool = False

# 3. DATABASE (LOWERCASE KEYS for reliability)
DATABASE = {
    "bob": {"username": "bob", "password": "123", "name": "Bob (Memory)", "profile": "Memory Impairment", "balance": 850.0, "history": [{"date": "2024-01-15", "merchant": "Electric Co", "amount": 120.00}]},
    "alice": {"username": "alice", "password": "123", "name": "Alice (ADHD)", "profile": "ADHD/Impulse", "balance": 2500.0, "history": []},
    "charlie": {"username": "charlie", "password": "123", "name": "Charlie (Dyslexia)", "profile": "Cognitive/Dyslexia", "balance": 45.0, "history": []},
    "diana": {"username": "diana", "password": "123", "name": "Diana (Visual)", "profile": "Visual Impairment", "balance": 1200.0, "history": []},
    "admin": {"username": "admin", "password": "admin", "name": "System Admin", "profile": "Admin", "balance": 0.0, "history": []}
}
SYSTEM_TRANSACTION_LOG = []

# 4. ENDPOINTS WITH DEBUGGING
@app.get("/")
def health_check():
    return {"status": "ok", "msg": "FinClarify Server is Running"}

@app.post("/login")
def login(creds: LoginRequest):
    # DEBUG PRINT (Look at your Terminal 1 when clicking login)
    print(f"-------- LOGIN ATTEMPT --------")
    print(f"INPUT: user='{creds.username}', pass='{creds.password}'")
    
    u = creds.username.strip().lower()
    
    if u in DATABASE:
        stored_pass = DATABASE[u]["password"]
        if stored_pass == creds.password:
            print(">> SUCCESS: Access Granted")
            role = "admin" if u == "admin" else "user"
            return {"role": role, "user_id": u, "name": DATABASE[u]["name"]}
        else:
            print(f">> FAIL: Password mismatch. Expected '{stored_pass}', Got '{creds.password}'")
    else:
        print(f">> FAIL: User '{u}' not found in Database")
    
    raise HTTPException(401, "Invalid Credentials")

@app.get("/account/{user_id}")
def get_account(user_id: str):
    return DATABASE.get(user_id, {})

@app.post("/analyze_risk")
def analyze_risk(txn: TransactionRequest):
    print(f"ANALYZING: {txn.amount} for {txn.user_id}")
    user = DATABASE.get(txn.user_id)
    if not user: return {"risk": "SAFE"}
    bal = user['balance']
    
    if txn.amount > bal: return {"risk": "CRITICAL", "code": "ERR_NSF"}
    if txn.amount == bal: return {"risk": "CRITICAL", "code": "ERR_ZERO"}
    
    for t in user['history']:
        if t['merchant'].lower().strip() == txn.merchant.lower().strip() and float(t['amount']) == float(txn.amount):
             return {"risk": "CRITICAL", "code": "ERR_DUPLICATE"}

    if txn.amount > 100:
        if txn.is_late_night: return {"risk": "HIGH", "code": "WARN_IMPULSE"}
        return {"risk": "MODERATE", "code": "WARN_LARGE"}

    return {"risk": "SAFE", "code": "OK"}

@app.post("/execute")
def execute(txn: TransactionRequest):
    user = DATABASE[txn.user_id]
    user['balance'] -= txn.amount
    user['history'].insert(0, {"date": str(datetime.date.today()), "merchant": txn.merchant, "amount": txn.amount})
    SYSTEM_TRANSACTION_LOG.insert(0, {"time": str(datetime.datetime.now()), "user": user['name'], "amt": txn.amount})
    return {"status": "SUCCESS"}

@app.get("/admin/logs")
def get_logs(): return SYSTEM_TRANSACTION_LOG