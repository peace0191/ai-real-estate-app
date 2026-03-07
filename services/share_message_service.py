"""
share_message_service.py
매물 홍보 문구 자동 생성 서비스
"""


def build_property_share_data(data: dict) -> dict:
    deal = data.get("deal_type", "매매")
    area = data.get("area_name", "")
    name = data.get("complex_name", "")
    price = data.get("price", "")
    rent = data.get("monthly_rent", "")
    size = data.get("area_size", "")
    floor_ = data.get("floor_info", "")
    direction = data.get("direction", "")
    p1 = data.get("point_1", "")
    p2 = data.get("point_2", "")
    p3 = data.get("point_3", "")
    url = data.get(
        "app_url",
        "https://ai-real-estate-app-nvbi9ytwq6gh6tmztd4tpu.streamlit.app"
    )

    price_str = price
    if deal == "월세" and rent:
        price_str = f"보증금 {price} / 월세 {rent}"
    elif deal == "전세":
        price_str = f"전세 {price}"
    elif deal == "매매":
        price_str = f"매매가 {price}"
    elif deal == "단기임대" and rent:
        price_str = f"보증금 {price} / 단기임대 {rent}"

    points = [p for p in [p1, p2, p3] if str(p).strip()]
    point_str = " · ".join(points) if points else ""

    title_parts = []
    if deal:
        title_parts.append(f"[{deal}]")
    if area:
        title_parts.append(area)
    if name:
        title_parts.append(name)
    if price_str:
        title_parts.append(price_str)

    title = " ".join(title_parts).strip()
    if len(title) > 45:
        title = title[:43] + "…"

    desc_parts = []
    if size:
        desc_parts.append(f"면적 {size}")
    if floor_:
        desc_parts.append(f"{floor_}")
    if direction:
        desc_parts.append(direction)
    if point_str:
        desc_parts.append(point_str)
    desc_parts.append("롯데타워앤강남빌딩부동산중개(주) ☎ 02-578-8285")
    description = " | ".join(desc_parts).strip()

    sms_lines = [
        f"🏠 [{deal}] {area} {name}".strip(),
        f"💰 {price_str}".strip(),
    ]

    extra = " ".join([x for x in [size, floor_, direction] if x]).strip()
    if extra:
        sms_lines.append(f"📐 {extra}")
    if point_str:
        sms_lines.append(f"✅ {point_str}")

    sms_lines.append(f"▶ 상세보기: {url}")
    sms_lines.append("롯데타워앤강남빌딩 ☎ 02-578-8285")
    sms_message = "\n".join([line for line in sms_lines if line.strip()])

    blog_lines = [
        f"📢 {deal} 매물 안내",
        "",
        f"🏢 단지: {name}" if name else "",
        f"📍 위치: {area}" if area else "",
        f"💰 가격: {price_str}" if price_str else "",
        f"📐 면적: {size}" if size else "",
        f"🏗 층수: {floor_}" if floor_ else "",
        f"🧭 방향: {direction}" if direction else "",
    ]

    if points:
        blog_lines.append("")
        blog_lines.append("✨ 주요 특장점")
        for p in points:
            blog_lines.append(f"• {p}")

    blog_lines += [
        "",
        "━" * 28,
        "🏢 롯데타워앤강남빌딩부동산중개(주)",
        "☎ 대표전화: 02-578-8285",
        "📱 휴대전화: 010-8985-8945",
        "📍 서울 강남구 대치동 938외1, 삼환아르누보2, 507호",
        "개설등록번호: 11680-2023-00078",
        "",
        f"▶ 앱에서 더 많은 매물 보기: {url}",
    ]

    blog_text = "\n".join([line for line in blog_lines if line])

    return {
        "title": title,
        "description": description,
        "sms_message": sms_message,
        "blog_text": blog_text,
    }