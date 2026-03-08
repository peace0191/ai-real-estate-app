"""
AI 저평가 매물 점수 계산 엔진
국토부 실거래가 + KB 시세 + 지역테마 + 보증금 안전 통합 점수
"""

# 지역별 테마 프리미엄
THEME_PREMIUM = {
    # 교육 프리미엄
    "대치동": {"theme": "교육", "premium": 10},
    "역삼동": {"theme": "교육", "premium": 8},
    "개포동": {"theme": "교육", "premium": 9},
    "도곡동": {"theme": "교육", "premium": 8},
    "삼성동": {"theme": "교육", "premium": 7},
    # 럭셔리 주거
    "한남동": {"theme": "럭셔리", "premium": 10},
    "청담동": {"theme": "럭셔리", "premium": 10},
    "압구정동": {"theme": "럭셔리", "premium": 9},
    "방배동": {"theme": "럭셔리", "premium": 8},
    "서초동": {"theme": "럭셔리", "premium": 7},
    "평창동": {"theme": "럭셔리", "premium": 8},
    # 한강벨트 투자
    "성수동": {"theme": "한강벨트", "premium": 9},
    "잠실동": {"theme": "한강벨트", "premium": 8},
    "용산동": {"theme": "한강벨트", "premium": 9},
    "마포동": {"theme": "한강벨트", "premium": 7},
    "신천동": {"theme": "한강벨트", "premium": 7},
}


def _region_theme_score(region: str) -> float:
    for key, val in THEME_PREMIUM.items():
        if key in region:
            return val["premium"] * 0.5  # 최대 5점
    return 2.0


def calculate_ai_score(data: dict) -> dict:
    """
    data 키:
        price         : 매물 가격 (억, float)
        kb_price      : KB 시세 (억, float)
        trade_price   : 실거래 평균 (억, float)
        school_score  : 학군 점수 0-10 (float)
        demand        : 수요 점수 0-10 (float)
        development   : 개발 호재 (bool)
        deposit_ratio : 보증금/매물가 비율 (float, 전월세만)
        region        : 지역명 (str)
    """
    score = 0.0

    price       = float(data.get("price", 0))
    kb_price    = float(data.get("kb_price", price))
    trade_price = float(data.get("trade_price", price))
    school      = float(data.get("school_score", 5))
    demand      = float(data.get("demand", 5))
    development = bool(data.get("development", False))
    dep_ratio   = float(data.get("deposit_ratio", 0.5))
    region      = str(data.get("region", ""))

    # 1. 실거래가 대비 점수 (35%)
    if trade_price > 0:
        gap_t = (trade_price - price) / trade_price * 100
        score += min(max(gap_t * 0.35, 0), 35)

    # 2. KB 시세 대비 점수 (20%)
    if kb_price > 0:
        gap_k = (kb_price - price) / kb_price * 100
        score += min(max(gap_k * 0.20, 0), 20)

    # 3. 수요/학군 점수 (20%)
    score += (school / 10) * 10
    score += (demand / 10) * 10

    # 4. 개발 호재 (5%)
    if development:
        score += 5

    # 5. 지역 테마 점수 (15%)
    score += _region_theme_score(region)

    # 6. 보증금 안전 (전월세) (5%)
    if dep_ratio > 0:
        if dep_ratio < 0.6:
            score += 5
        elif dep_ratio < 0.8:
            score += 2
        else:
            score -= 3

    total = round(min(score, 100), 1)

    if total >= 70:
        grade = "🔥 매우 저평가 — 강력 추천"
    elif total >= 50:
        grade = "⭐ 저평가 — 추천"
    elif total >= 35:
        grade = "👍 관심 매물"
    else:
        grade = "보통"

    return {"ai_score": total, "grade": grade}
