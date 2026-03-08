"""
deposit_risk_engine.py
보증금 안전 점수 엔진 (집품/전세안전 기반)
"""


def deposit_safety_score(deposit: float, property_value: float) -> tuple[int, str]:
    """
    deposit: 보증금 (억)
    property_value: 매물 시세 (억)
    returns: (점수, 등급)
    """
    if property_value <= 0:
        return 0, "정보 없음"

    ratio = deposit / property_value

    if ratio < 0.5:
        return 10, "✅ 안전"
    elif ratio < 0.65:
        return 7, "👍 양호"
    elif ratio < 0.80:
        return 4, "⚠️ 주의"
    else:
        return -10, "🚨 위험"


def analyze_jeonse_risk(data: dict) -> dict:
    """전세 / 월세 위험도 종합 분석"""
    deposit = float(str(data.get("deposit", 0)).replace("억", "").replace(",", "") or 0)
    prop_val = float(str(data.get("property_value", 0)).replace("억", "").replace(",", "") or 0)
    has_mortgage = bool(data.get("has_mortgage", False))
    mortgage_amt = float(str(data.get("mortgage_amount", 0)).replace("억", "").replace(",", "") or 0)

    score, grade = deposit_safety_score(deposit, prop_val)

    if has_mortgage and prop_val > 0:
        total_exposure = (deposit + mortgage_amt) / prop_val
        if total_exposure > 0.9:
            score -= 15
            grade = "🚨 위험 (근저당 포함)"
        elif total_exposure > 0.75:
            score -= 7
            grade = "⚠️ 주의 (근저당 포함)"

    advice = ""
    if score < 0:
        advice = "계약 전 반드시 전문가 상담 및 등기부등본 확인이 필요합니다."
    elif score < 5:
        advice = "전세권 설정 또는 전세보증보험 가입을 권장합니다."
    else:
        advice = "전세보증보험 가입 후 계약하시면 더욱 안전합니다."

    return {
        "score": score,
        "grade": grade,
        "advice": advice,
        "deposit_ratio": round(deposit / prop_val * 100, 1) if prop_val > 0 else 0,
    }
