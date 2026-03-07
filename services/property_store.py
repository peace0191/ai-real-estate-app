"""
property_store.py — JSON 파일 영속 저장
새로고침해도 데이터 유지. session_state는 캐시용으로만 사용.
"""
import json, os
from datetime import datetime

PROP_FILE   = "data/properties.json"
DEMAND_FILE = "data/demands.json"
SHORTS_FILE = "data/shorts_candidates.json"

def _load(path):
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def _save(path, data):
    os.makedirs("data", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ── 공급 매물 ────────────────────────────────────────────────
def get_all_properties():
    return _load(PROP_FILE)

def add_property(p: dict) -> str:
    props = get_all_properties()
    p["id"] = f"P{len(props)+1:04d}"
    p["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    p.setdefault("status", "검수대기")
    props.append(p)
    _save(PROP_FILE, props)
    return p["id"]

def update_property(prop_id: str, updates: dict):
    props = get_all_properties()
    for p in props:
        if p.get("id") == prop_id:
            p.update(updates)
            break
    _save(PROP_FILE, props)

def delete_property(prop_id: str):
    props = [p for p in get_all_properties() if p.get("id") != prop_id]
    _save(PROP_FILE, props)

# ── 수요 ─────────────────────────────────────────────────────
def get_demands():
    return _load(DEMAND_FILE)

def add_demand(d: dict) -> str:
    demands = get_demands()
    d["id"] = f"D{len(demands)+1:04d}"
    d["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    demands.append(d)
    _save(DEMAND_FILE, demands)
    return d["id"]

def delete_demand(demand_id: str):
    demands = [d for d in get_demands() if d.get("id") != demand_id]
    _save(DEMAND_FILE, demands)

# ── 숏츠 후보 ────────────────────────────────────────────────
def get_shorts_candidates():
    return _load(SHORTS_FILE)

def add_shorts_candidate(item: dict):
    items = get_shorts_candidates()
    items.append(item)
    _save(SHORTS_FILE, items)

# ── 별칭 함수 (pages 호환용) ────────────────────────────────
def save_property(p: dict) -> str:
    """add_property 별칭"""
    return add_property(p)

def save_shorts_candidate(item: dict):
    """add_shorts_candidate 별칭"""
    add_shorts_candidate(item)

def get_demand_items() -> list:
    """수요 목록 반환"""
    return get_demands()

def get_supply_items() -> list:
    """공급 매물 반환 (deal_side=공급 또는 category=supply)"""
    return [p for p in get_all_properties()
            if p.get("deal_side") == "공급" or p.get("category") == "supply"]

def get_co_broker_items() -> list:
    """공동중개 매물 반환"""
    return [p for p in get_all_properties()
            if p.get("co_broker") or p.get("category") == "joint"]

def get_reviewed_items() -> list:
    """승인 완료 매물 반환"""
    return [p for p in get_all_properties() if p.get("status") == "승인"]

def save_reviewed_item(item: dict):
    """검수 정보 저장 (id 기준 업데이트)"""
    prop_id = item.get("id")
    if prop_id:
        update_property(prop_id, item)
    else:
        add_property(item)

# ── 알림 ─────────────────────────────────────────────────────
ALERT_FILE = "data/alerts.json"

def get_alerts() -> list:
    return _load(ALERT_FILE)

def push_alert(title: str, message: str, level: str = "info"):
    """알림 저장 (최근 100건 유지)"""
    alerts = get_alerts()
    alerts.insert(0, {
        "title":      title,
        "message":    message,
        "level":      level,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    _save(ALERT_FILE, alerts[:100])

