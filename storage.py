# storage.py
import json, os, threading
from datetime import datetime

_DB_PATH = os.path.join(os.path.dirname(__file__), "tokens.json")
_LOCK = threading.Lock()

def _load():
    if not os.path.exists(_DB_PATH):
        return {"users": {}, "logs": []}
    with open(_DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def _save(data):
    tmp = _DB_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    os.replace(tmp, _DB_PATH)

def ensure_user(user_id: str, name="User", role="student", token_limit=100000):
    with _LOCK:
        db = _load()
        users = db["users"]
        if user_id not in users:
            users[user_id] = {
                "id": user_id,
                "name": name,
                "role": role,
                "token_limit": token_limit,
                "token_used": 0
            }
            _save(db)
        return db["users"][user_id]

def get_user(user_id: str):
    with _LOCK:
        db = _load()
        return db["users"].get(user_id)

def update_user(user_id: str, **fields):
    with _LOCK:
        db = _load()
        if user_id not in db["users"]:
            return None
        db["users"][user_id].update(fields)
        _save(db)
        return db["users"][user_id]

def add_log(user_id: str, request_type: str, model: str, tokens_used: int, cost_usd: float):
    with _LOCK:
        db = _load()
        log = {
            "id": len(db["logs"]) + 1,
            "user_id": user_id,
            "request_type": request_type,
            "model": model,
            "tokens_used": tokens_used,
            "cost_usd": cost_usd,
            "timestamp": datetime.utcnow().isoformat()
        }
        db["logs"].append(log)
        _save(db)
        return log

def get_logs(user_id: str):
    with _LOCK:
        db = _load()
        return [l for l in db["logs"] if l["user_id"] == user_id]
