def detect_undervalued(property_price, market_price):

    discount_rate = (market_price - property_price) / market_price

    if discount_rate >= 0.1:
        return True, discount_rate
    else:
        return False, discount_rate