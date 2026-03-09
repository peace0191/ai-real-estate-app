"""
customer_store.py — 고객 데이터 영속 저장 (JSON)
  - 고객 목록 (customers.json)
  - 고객 그룹 목록 (customer_groups.json)
  - VIP 고객 호환 (vip_customers.csv → customers.json 통합)
"""
import json
import csv
import os
from datetime import datetime

CUSTOMER_FILE    = "data/customers.json"
GROUP_FILE       = "data/customer_groups.json"
VIP_LEGACY_FILE  = "data/vip_customers.csv"   # 레거시 호환

# ── 공통 IO ──────────────────────────────────────────────────────────────────
def _load(path: str, default=None):
    os.makedirs("data", exist_ok=True)
    if default is None:
        default = []
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def _save(path: str, data):
    os.makedirs("data", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ══════════════════════════════════════════════════════════════════════════════
# 고객 CRUD
# ══════════════════════════════════════════════════════════════════════════════
def load_customers() -> list:
    """전체 고객 목록 반환 (레거시 CSV 자동 마이그레이션)"""
    _migrate_vip_csv()
    return _load(CUSTOMER_FILE)

def save_customer(customer: dict) -> str:
    """고객 신규 저장. 자동 ID 부여 후 ID 반환."""
    customers = load_customers()
    customer["id"]         = f"C{len(customers)+1:04d}"
    customer["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    customer.setdefault("status",  "진행중")
    customer.setdefault("grade",   "일반")
    customer.setdefault("group",   "기본그룹")
    customer.setdefault("source",  "직접")   # 유입경로
    customers.append(customer)
    _save(CUSTOMER_FILE, customers)
    return customer["id"]

def update_customer(cid: str, updates: dict):
    customers = load_customers()
    for c in customers:
        if c.get("id") == cid:
            c.update(updates)
            break
    _save(CUSTOMER_FILE, customers)

def delete_customer(cid: str):
    customers = [c for c in load_customers() if c.get("id") != cid]
    _save(CUSTOMER_FILE, customers)

def get_customer_by_id(cid: str) -> dict:
    for c in load_customers():
        if c.get("id") == cid:
            return c
    return {}


# ══════════════════════════════════════════════════════════════════════════════
# 고객 그룹 CRUD
# ══════════════════════════════════════════════════════════════════════════════
def load_groups() -> list:
    default = [
        {"id": "G0001", "name": "기본그룹",  "count": 0, "created_at": "2024-01-01", "memo": ""},
    ]
    return _load(GROUP_FILE, default)

def save_group(name: str, memo: str = "") -> str:
    groups = load_groups()
    # 중복 방지
    for g in groups:
        if g.get("name") == name:
            return g.get("id", "")
    gid  = f"G{len(groups)+1:04d}"
    groups.append({
        "id":         gid,
        "name":       name,
        "memo":       memo,
        "count":      0,
        "created_at": datetime.now().strftime("%Y-%m-%d"),
    })
    _save(GROUP_FILE, groups)
    return gid

def update_group(gid: str, updates: dict):
    groups = load_groups()
    for g in groups:
        if g.get("id") == gid:
            g.update(updates)
            break
    _save(GROUP_FILE, groups)

def delete_group(gid: str):
    groups = [g for g in load_groups() if g.get("id") != gid]
    _save(GROUP_FILE, groups)

def refresh_group_counts():
    """고객 목록을 기준으로 각 그룹의 count 재계산"""
    customers = load_customers()
    groups    = load_groups()
    count_map = {}
    for c in customers:
        grp = c.get("group", "기본그룹")
        count_map[grp] = count_map.get(grp, 0) + 1
    for g in groups:
        g["count"] = count_map.get(g["name"], 0)
    _save(GROUP_FILE, groups)

def get_group_names() -> list:
    return [g["name"] for g in load_groups()]


# ══════════════════════════════════════════════════════════════════════════════
# 레거시 VIP CSV → JSON 마이그레이션 (1회 자동 실행)
# ══════════════════════════════════════════════════════════════════════════════
def _migrate_vip_csv():
    if not os.path.exists(VIP_LEGACY_FILE):
        return
    if os.path.exists(CUSTOMER_FILE) and os.path.getsize(CUSTOMER_FILE) > 5:
        return   # 이미 마이그레이션 완료
    try:
        with open(VIP_LEGACY_FILE, "r", newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        customers = []
        for i, row in enumerate(rows, 1):
            row["id"]         = f"C{i:04d}"
            row["created_at"] = row.get("created_at", "2024-01-01 00:00")
            row.setdefault("status", "진행중")
            row.setdefault("group",  "기본그룹")
            row.setdefault("source", "직접")
            customers.append(row)
        _save(CUSTOMER_FILE, customers)
    except Exception:
        pass
