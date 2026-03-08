"""
AI 홍보 문구 자동 생성 엔진
유튜브 숏츠 / SNS / 블로그 / 단톡방 / 카드뉴스
"""

OFFICE  = "롯데타워앤강남빌딩부동산중개(주)"
TEL     = "02-578-8285"
MOBILE  = "010-8985-8945"


def generate_marketing_content(data: dict) -> dict:
    area   = data.get("area_name",    "")
    name   = data.get("complex_name", "")
    price  = data.get("price",        "")
    size   = data.get("area_size",    "")
    floor_ = data.get("floor_info",   "")
    p1 = data.get("point_1", "")
    p2 = data.get("point_2", "")
    p3 = data.get("point_3", "")
    title  = f"{area} {name}".strip()

    pts = [p for p in [p1,p2,p3] if str(p).strip()]

    youtube_script = f"""🏠 {title}

면적 {size}  가격 {price}  {floor_}

{"✔ " + chr(10).join(pts) if pts else ""}

📞 문의
{OFFICE}
{TEL}"""

    sns_text = f"""📢 {title}

💰 {price}
📐 {size}  🏗 {floor_}

{chr(10).join(["✔ " + p for p in pts])}

📞 {TEL}"""

    blog_text = f"""📢 {title} 매물 소개

📍 위치: {area}
🏢 단지: {name}
💰 가격: {price}
📐 면적: {size}
🏗 층수: {floor_}

{"✨ 주요 특장점" + chr(10) + chr(10).join(["• " + p for p in pts]) if pts else ""}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏢 {OFFICE}
☎ {TEL}  📱 {MOBILE}
📍 서울 강남구 대치동 938외1, 삼환아르누보2, 507호
개설등록번호: 11680-2023-00078"""

    kakao_group_text = f"""[공동중개 가능 매물]

{title}
가격: {price}  면적: {size}

{chr(10).join(pts)}

문의 {TEL}"""

    return {
        "youtube_script":   youtube_script,
        "sns_text":         sns_text,
        "blog_text":        blog_text,
        "kakao_group_text": kakao_group_text,
    }


def generate_card_news_content(data: dict) -> dict:
    area  = data.get("area_name", "")
    name  = data.get("complex_name", "")
    price = data.get("price", "")
    size  = data.get("area_size", "")
    floor_= data.get("floor_info", "")
    p1,p2,p3 = data.get("point_1",""),data.get("point_2",""),data.get("point_3","")
    title    = f"{area} {name}".strip()
    subtitle = f"{price} | {size} | {floor_}".strip(" |")
    pts      = [p for p in [p1,p2,p3] if str(p).strip()]

    sns_caption = f"""📢 {title}

💰 {price}
📐 {size}

{"  ".join(pts)}

📞 {TEL}"""

    thumbnail_text = f"{title}\n{price}\n{size}\n{pts[0] if pts else ''}"

    return {
        "title":          title,
        "subtitle":       subtitle,
        "badge_text":     "AI 추천 매물",
        "short_copy":     "\n".join(pts),
        "sns_caption":    sns_caption,
        "thumbnail_text": thumbnail_text,
    }
