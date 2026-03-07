"""
customer_match_engine.py
고객(수요자) 조건 기반 매물 매칭 엔진
기존 matching_service.py 보다 더 세밀한 조건 매칭을 지원합니다.

점수 기준 (합계 100점)
  지역    : 30점  (동일 구 20점, 동일 동 +10점)
  거래유형 : 20점
  매물유형 : 15점
  가격     : 20점  (예산 이하 20점, 10% 이내 초과 10점)
  면적     : 10점  (10% 이내 5점, 20% 이내 3점)
  방향     : 5점
"""

from __future__ import annotations


# ── 점수 계산 ────────────────────────────────────────────────
def calc_match_score(customer: dict, property_: dict) -> int:
    """
    수요자 조건(customer)과 매물(property_)의 매칭 점수를 반환합니다.

    Parameters
    ----------
    customer : dict
        region       : 희망 지역 (예: '강남구 대치동')
        trade_type   : 거래 유형 (매매/전세/월세)
        property_type: 매물 유형 (아파트/오피스텔 등)
        budget       : 예산 (만원, 숫자 또는 문자열)
        area         : 희망 면적 (㎡)
        direction    : 희망 방향 (남향/동향 등, 선택)

    property_ : dict
        region       : 매물 지역
        trade_type / trade : 거래 유형
        property_type / type : 매물 유형
        price        : 가격 (만원)
        area         : 면적 (㎡)
        direction    : 방향 (선택)

    Returns
    -------
    int  0~100 점
    """
    score = 0

    # ── 지역 (30점) ─────────────────────────────────────────
    c_region = str(customer.get("region", "")).strip()
    p_region = str(property_.get("region", "")).strip()
    if c_region and p_region:
        if c_region == p_region:
            score += 30
        elif c_region.split()[0] == p_region.split()[0]:  # 같은 구
            score += 20

    # ── 거래 유형 (20점) ─────────────────────────────────────
    c_trade = customer.get("trade_type", customer.get("trade", ""))
    p_trade = property_.get("trade_type", property_.get("trade", ""))
    if c_trade and p_trade and c_trade == p_trade:
        score += 20

    # ── 매물 유형 (15점) ─────────────────────────────────────
    c_type = customer.get("property_type", customer.get("type", ""))
    p_type = property_.get("property_type", property_.get("type", ""))
    if c_type and p_type and c_type == p_type:
        score += 15

    # ── 가격 (20점) ──────────────────────────────────────────
    try:
        budget  = float(str(customer.get("budget", 0)).replace(",", "").replace("만원", "") or 0)
        p_price = float(str(property_.get("price", 0)).replace(",", "").replace("만원", "") or 0)
        if budget > 0 and p_price > 0:
            if p_price <= budget:
                score += 20
            elif p_price <= budget * 1.10:
                score += 10
    except Exception:
        pass

    # ── 면적 (10점) ──────────────────────────────────────────
    try:
        c_area = float(str(customer.get("area", 0)).replace("㎡", "").strip() or 0)
        p_area = float(str(property_.get("area", 0)).replace("㎡", "").strip() or 0)
        if c_area > 0 and p_area > 0:
            ratio = abs(c_area - p_area) / max(c_area, 1)
            if ratio <= 0.10:
                score += 10
            elif ratio <= 0.20:
                score += 5
    except Exception:
        pass

    # ── 방향 (5점) ───────────────────────────────────────────
    c_dir = customer.get("direction", "")
    p_dir = property_.get("direction", "")
    if c_dir and p_dir and c_dir == p_dir:
        score += 5

    return min(score, 100)


# ── 등급 ──────────────────────────────────────────────────────
def get_grade(score: int) -> str:
    if score >= 80: return "🔥 강력추천"
    if score >= 65: return "⭐ 추천"
    if score >= 50: return "✅ 검토"
    if score >= 30: return "🔹 관심"
    return "➖ 미달"


# ── 고객 단일 매칭 ────────────────────────────────────────────
def match_for_customer(customer: dict, properties: list,
                        min_score: int = 0) -> list[dict]:
    """
    한 명의 고객 조건에 맞는 매물 목록을 점수 내림차순으로 반환합니다.

    Parameters
    ----------
    customer   : 고객 조건 dict
    properties : 매물 목록 list[dict]
    min_score  : 최소 점수 필터 (기본 0)

    Returns
    -------
    list[dict]  score / grade 키 포함
    """
    results = []
    for p in properties:
        sc = calc_match_score(customer, p)
        if sc >= min_score:
            results.append({
                **p,
                "match_score": sc,
                "grade":       get_grade(sc),
            })
    return sorted(results, key=lambda x: x["match_score"], reverse=True)


# ── 전체 수요자-매물 매칭 ─────────────────────────────────────
def match_all(customers: list, properties: list,
              min_score: int = 0) -> list[dict]:
    """
    모든 수요자 ↔ 매물 조합의 매칭 결과를 반환합니다.

    Returns
    -------
    list[dict]
        customer_name, customer_phone, property_name,
        region, trade_type, price, area,
        match_score, grade
    """
    results = []
    for c in customers:
        for p in properties:
            sc = calc_match_score(c, p)
            if sc >= min_score:
                results.append({
                    "customer_name":  c.get("name",  c.get("client_name", "-")),
                    "customer_phone": c.get("phone", "-"),
                    "property_name":  p.get("property_name", p.get("address", "-")),
                    "region":         p.get("region", "-"),
                    "trade_type":     p.get("trade_type", p.get("trade", "-")),
                    "property_type":  p.get("property_type", p.get("type", "-")),
                    "price":          p.get("price", 0),
                    "area":           p.get("area", 0),
                    "match_score":    sc,
                    "grade":          get_grade(sc),
                })
    return sorted(results, key=lambda x: x["match_score"], reverse=True)


# ── 고득점 매칭 수 ────────────────────────────────────────────
def high_match_count(customers: list, properties: list,
                     threshold: int = 65) -> int:
    """threshold 점 이상의 매칭 수를 반환합니다."""
    return sum(
        1
        for c in customers
        for p in properties
        if calc_match_score(c, p) >= threshold
    )


# ── 단순 조건 매칭 (예산 + 최소면적 기준) ─────────────────────
def match_customer(customer: dict, properties: list) -> list:
    """
    예산(budget)과 최소 면적(min_size) 조건을 동시에 만족하는
    매물만 반환하는 단순 필터 함수입니다.

    Parameters
    ----------
    customer : dict
        budget   : 최대 예산 (만원, 숫자)
        min_size : 최소 면적 (㎡, 숫자)

    properties : list[dict]
        price : 가격 (만원, 숫자 또는 문자열)
        size  : 면적 (㎡, 숫자)

    Returns
    -------
    list[dict]  조건을 만족하는 매물 목록
    """
    matches = []
    budget   = float(customer.get("budget", 0))
    min_size = float(customer.get("min_size", 0))

    for p in properties:
        try:
            p_price = float(str(p.get("price", 0)).replace(",", "").replace("만원", "") or 0)
            p_size  = float(str(p.get("size",  p.get("area", 0))).replace("㎡", "").strip() or 0)

            if budget >= p_price and p_size >= min_size:
                matches.append(p)
        except Exception:
            continue

    return matches
