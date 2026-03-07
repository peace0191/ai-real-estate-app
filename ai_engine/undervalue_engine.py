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
