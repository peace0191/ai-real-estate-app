"""
VIP 고객 저장/불러오기
"""
import csv
import os

CUSTOMER_FILE = "data/vip_customers.csv"
FIELDS = [
    "name", "phone", "deal_type",
    "budget_min", "budget_max",
    "area_min", "area_max",
    "pref_region", "grade", "memo",
    # 하위 호환 필드
    "budget", "min_size", "region",
]


def _ensure():
    os.makedirs("data", exist_ok=True)


def save_customer(customer: dict):
    _ensure()
    exists = os.path.exists(CUSTOMER_FILE)
    with open(CUSTOMER_FILE, "a", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        if not exists:
            w.writeheader()
        w.writerow({k: customer.get(k, "") for k in FIELDS})


def load_customers() -> list:
    _ensure()
    if not os.path.exists(CUSTOMER_FILE):
        return []
    with open(CUSTOMER_FILE, "r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))
