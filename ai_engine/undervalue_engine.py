"""
undervalued_engine.py
AI 기준가 vs 매물 가격 → 5단계 등급 + 배지 색상
"""

GRADES = [
    (15,  "🔥", "강력추천", "#e74c3c", "AI기준가 대비 즉시 매수 검토"),
    (10,  "⭐", "추천",    "#f39c12", "AI기준가 대비 적극 추천"),
    ( 5,  "✅", "관심",    "#2ecc71", "AI기준가 대비 관심 매물"),
    ( 0,  "➖", "적정가",  "#7f8c8d", "시세 수준 적정 가격"),
    (-99, "📈", "고평가",  "#e74c3c", "AI기준가 초과 — 주의"),
]


def analyze(ai_ref: float, listing: float) -> dict:
    """
    Returns:
        rate   : 저평가율 (%) — 양수=저평가, 음수=고평가
        grade  : 이모지 등급
        label  : 한글 등급명
        color  : 배지 색상 hex
        desc   : 설명 문구
        recommend: bool
    """
    try:
        ai_ref  = float(ai_ref)
        listing = float(listing)
        if ai_ref <= 0 or listing <= 0:
            return _err()
        rate = round((ai_ref - listing) / ai_ref * 100, 1)
        for threshold, grade, label, color, desc in GRADES:
            if rate >= threshold:
                return dict(rate=rate, grade=grade, label=label,
                            color=color, desc=desc,
                            recommend=(grade in ("🔥","⭐","✅")))
        return _err()
    except Exception as e:
        return _err(str(e))


def _err(msg="분석불가"):
    return dict(rate=0, grade="❓", label=msg, color="#555", desc=msg, recommend=False)


def batch(properties: list, price_fn) -> list:
    """공급 매물 리스트 일괄 분석 — 저평가율 내림차순 정렬"""
    results = []
    for p in properties:
        prices   = price_fn(p.get("region",""), p.get("type","아파트"), float(p.get("area",0)))
        analysis = analyze(prices["AI기준가"], float(p.get("price",0)))
        results.append({**p, "prices": prices, "analysis": analysis})
    return sorted(results, key=lambda x: x["analysis"]["rate"], reverse=True)


# ── 02_AI저평가분석 페이지 호환 함수 ──────────────────────────
def calculate_undervalue(listing_price: float, real_tx: float,
                          kb_price: float, naver_price: float):
    """
    세 시세의 평균을 AI 기준가로 계산 후 저평가율 반환
    Returns: (ai_ref_price, undervalue_rate, label_str)
    """
    prices = [p for p in [real_tx, kb_price, naver_price] if p > 0]
    if not prices or listing_price <= 0:
        return 0, 0, "➖ 데이터 없음"
    ai_ref = sum(prices) / len(prices)
    rate   = round((ai_ref - listing_price) / ai_ref * 100, 1)
    for threshold, grade, label, color, desc in GRADES:
        if rate >= threshold:
            return ai_ref, rate, f"{grade} {label}"
    return ai_ref, rate, "📈 고평가"


# 지역·유형별 샘플 시세 데이터 (실거래가 API 연동 전 목업)
_SAMPLE_DB = {
    ("강남구 대치동", "아파트"):    {"real_tx": 280000, "kb": 285000, "naver": 290000},
    ("강남구 개포동", "아파트"):    {"real_tx": 260000, "kb": 265000, "naver": 262000},
    ("강남구 역삼동", "아파트"):    {"real_tx": 200000, "kb": 205000, "naver": 208000},
    ("강남구 역삼동", "오피스텔"):  {"real_tx":  90000, "kb":  92000, "naver":  91000},
    ("송파구 신천동", "아파트"):    {"real_tx": 240000, "kb": 245000, "naver": 242000},
    ("성수동",        "아파트"):    {"real_tx": 180000, "kb": 185000, "naver": 183000},
    ("성수동",        "상가"):      {"real_tx":  50000, "kb":  52000, "naver":  51000},
    ("용산구 한남동", "아파트"):    {"real_tx": 300000, "kb": 305000, "naver": 308000},
    ("기타",          "아파트"):    {"real_tx": 100000, "kb": 102000, "naver": 101000},
}

def get_sample_prices(region: str, prop_type: str) -> dict:
    """지역·유형에 맞는 샘플 시세 반환 (국토부 API 연동 전 목업)"""
    key = (region, prop_type)
    return _SAMPLE_DB.get(key, {"real_tx": 100000, "kb": 102000, "naver": 101000})

