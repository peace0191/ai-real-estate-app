"""
realprice_service.py
지역별 실제 시세 기반 가격 계산 (평당 단가 × 면적)
실 서비스 전환 시 국토부 API(data.go.kr) 로 교체
"""

# 지역·유형별 평당 시세 (만원/평, 2026년 1분기 기준)
PRICE_TABLE = {
    "대치동":  {"아파트": 12500, "주상복합": 9800,  "오피스텔": 6200},
    "개포동":  {"아파트": 11500, "주상복합": 8900,  "오피스텔": 5700},
    "역삼동":  {"아파트": 10800, "주상복합": 8200,  "오피스텔": 5100},
    "잠실":    {"아파트":  9800, "주상복합": 7700,  "오피스텔": 4700},
    "성수":    {"아파트":  8800, "주상복합": 7200,  "오피스텔": 4100},
    "한남동":  {"아파트": 13500, "주상복합":10500,  "오피스텔": 6800},
}

# KB시세 = 실거래가 × 1.03, 네이버 = 실거래가 × 0.97
KB_MULT    = 1.03
NAVER_MULT = 0.97


def get_prices(region: str, prop_type: str, area_sqm: float) -> dict:
    """
    Args:
        region:    지역명 (예: "대치동")
        prop_type: 유형 (예: "아파트")
        area_sqm:  전용면적 ㎡
    Returns:
        {국토부실거래가, KB시세, 네이버매물가, AI기준가}  (단위: 만원)
    """
    pyeong   = area_sqm / 3.305
    base_per = PRICE_TABLE.get(region, {}).get(prop_type, 8000)
    
    국토부 = int(base_per * pyeong)
    kb     = int(국토부 * KB_MULT)
    naver  = int(국토부 * NAVER_MULT)
    ai_ref = int((국토부 + kb + naver) / 3)

    return {
        "국토부실거래가": 국토부,
        "KB시세":        kb,
        "네이버매물가":   naver,
        "AI기준가":      ai_ref,
    }


def get_region_avg(region: str, prop_type: str = "아파트") -> int:
    """33㎡(10평) 기준 평당 단가 반환 — 대시보드 차트용"""
    return PRICE_TABLE.get(region, {}).get(prop_type, 8000)
