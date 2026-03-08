"""
KB 부동산 시세 기반 적정가 산출 엔진
실서비스에서는 KB부동산 Open API 또는 제휴 데이터 사용
"""

# 지역별 KB 프리미엄 배수 (내부 기준값)
REGION_PREMIUM = {
    "대치동":   1.06,
    "역삼동":   1.04,
    "개포동":   1.05,
    "삼성동":   1.05,
    "도곡동":   1.04,
    "한남동":   1.08,
    "청담동":   1.08,
    "압구정동": 1.09,
    "서초동":   1.05,
    "방배동":   1.03,
    "평창동":   1.04,
    "성수동":   1.06,
    "용산동":   1.07,
    "잠실동":   1.05,
    "마포구":   1.03,
}

# 샘플 KB 시세 데이터 (API 연동 전 fallback)
KB_SAMPLE_PRICES = {
    "래미안블레스티지":       31.0,
    "디에이치퍼스트아이파크": 33.5,
    "대치SK뷰":               30.0,
    "역삼레전드힐스":          19.5,
    "시그니엘레지던스":        76.0,
    "한남더힐":               82.0,
    "청담PH129":              92.0,
    "아크로서울포레스트":      41.0,
    "트리마제":               39.0,
    "잠실엘스":               24.5,
    "잠실리센츠":             23.5,
    "압구정현대":             57.0,
    "대치삼환아르누보오피스텔": 5.2,
}


def get_kb_price(apt_name: str, region: str = "", current_price: float = 0) -> float:
    """
    KB 시세 반환
    - apt_name에 해당하는 샘플 KB 시세가 있으면 반환
    - 없으면 지역 프리미엄 배수로 추정
    """
    # 샘플 DB 조회
    for key, kb in KB_SAMPLE_PRICES.items():
        if key in apt_name or apt_name in key:
            return kb

    # 지역 배수로 추정
    premium = REGION_PREMIUM.get(region, 1.03)
    if current_price > 0:
        return round(current_price * premium, 2)

    return 0.0


def kb_price_gap_score(current_price: float, kb_price: float) -> float:
    """KB 시세 대비 저평가 갭 점수(0~100)"""
    if kb_price <= 0:
        return 0.0
    gap = kb_price - current_price
    score = (gap / kb_price) * 100
    return round(max(score, 0.0), 2)
