"""
VIP 고객 자동 매칭 엔진
"""


def _to_float(val):
    try:
        return float(str(val).replace(",", "").strip())
    except:
        return 0.0


def _extract_num(text):
    import re
    m = re.search(r"[\d.]+", str(text))
    return float(m.group()) if m else 0.0


def calc_match_score(customer: dict, prop: dict) -> int:
    score = 0
    budget    = _to_float(customer.get("budget", 0))
    min_size  = _extract_num(customer.get("min_size", 0))
    c_region  = str(customer.get("region", "")).strip()
    c_deal    = str(customer.get("deal_type", "")).strip()

    p_price   = _to_float(prop.get("price", 0))
    p_size    = _extract_num(prop.get("size", 0))
    p_region  = str(prop.get("region", "")).strip()
    p_deal    = str(prop.get("deal_type", "")).strip()

    if p_price <= budget:
        score += 40
    elif p_price <= budget * 1.05:
        score += 20

    if p_size >= min_size:
        score += 30
    elif p_size >= min_size * 0.9:
        score += 15

    if c_region and p_region:
        if c_region in p_region or p_region in c_region:
            score += 20

    if c_deal and p_deal and c_deal == p_deal:
        score += 10

    return score


def match_vip_customer(customer: dict, properties: list) -> list:
    result = []
    for prop in properties:
        score = calc_match_score(customer, prop)
        if score > 0:
            item = prop.copy()
            item["match_score"] = score
            result.append(item)
    result.sort(key=lambda x: x["match_score"], reverse=True)
    return result
