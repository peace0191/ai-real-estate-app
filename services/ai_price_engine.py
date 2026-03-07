"""
AI 저평가 매물 분석 엔진
"""

import pandas as pd


def calculate_ai_score(property_data, market_price):

    price = float(property_data["price"].replace("억", ""))

    score = 0

    # 가격 비교
    if price < market_price * 0.9:
        score += 40
    elif price < market_price:
        score += 20

    # 층
    if "중" in property_data["floor"]:
        score += 15
    elif "고" in property_data["floor"]:
        score += 10

    # 방향
    if property_data["direction"] == "남향":
        score += 15

    # 면적
    if property_data["size"] >= 84:
        score += 10

    return score


def find_undervalued(properties, market_price):

    scored = []

    for p in properties:

        score = calculate_ai_score(p, market_price)

        p["ai_score"] = score

        scored.append(p)

    df = pd.DataFrame(scored)

    df = df.sort_values("ai_score", ascending=False)

    return df.head(5)