"""
matching_service.py
수요 ↔ 공급 AI 매칭 엔진
점수 기준: 지역(30) + 유형(20) + 거래(20) + 가격(20) + 면적(10) = 100점
"""
from services.property_store import get_all_properties, get_demands


def score(demand: dict, supply: dict) -> int:
    s = 0
    if demand.get("region") == supply.get("region"):   s += 30
    if demand.get("type")   == supply.get("type"):     s += 20
    if demand.get("trade")  == supply.get("trade"):    s += 20

    try:
        d_price = float(demand.get("budget", 0))
        s_price = float(supply.get("price",  0))
        if   s_price <= d_price:        s += 20
        elif s_price <= d_price * 1.1:  s += 10
    except Exception:
        pass

    try:
        d_area = float(demand.get("area", 0))
        s_area = float(supply.get("area", 0))
        ratio  = abs(d_area - s_area) / max(d_area, 1)
        if   ratio <= 0.10: s += 10
        elif ratio <= 0.20: s += 5
    except Exception:
        pass

    return s


def _grade(sc):
    if sc >= 80: return "🔥 강력추천"
    if sc >= 60: return "⭐ 추천"
    if sc >= 50: return "✅ 검토"
    return "➖ 미달"


def get_matches(min_score: int = 0) -> list:
    demands  = get_demands()
    supplies = [p for p in get_all_properties()
                if p.get("category") in ("supply", "joint")
                and p.get("status") in ("승인", "검수대기", "숏츠후보")]

    results = []
    for d in demands:
        for s in supplies:
            sc = score(d, s)
            if sc >= min_score:
                results.append({
                    "demand_id":   d.get("id",""),
                    "demand_name": d.get("name",""),
                    "demand_phone":d.get("phone",""),
                    "supply_id":   s.get("id",""),
                    "supply_name": s.get("name",""),
                    "region":      s.get("region",""),
                    "type":        s.get("type",""),
                    "trade":       s.get("trade",""),
                    "price":       s.get("price",0),
                    "area":        s.get("area",0),
                    "score":       sc,
                    "grade":       _grade(sc),
                })
    return sorted(results, key=lambda x: x["score"], reverse=True)


def high_match_count() -> int:
    return len([m for m in get_matches() if m["score"] >= 50])
