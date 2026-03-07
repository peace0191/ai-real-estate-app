"""
share_message_service.py
매물 홍보 문구 자동 생성 서비스

카카오 공유 제목/설명,
SMS 문구,
블로그/단톡방 문구를 자동 생성하여 반환합니다.
"""


def build_property_share_data(data: dict) -> dict:
    """
    매물 정보를 받아 각 채널별 홍보 문구를 반환합니다.

    Parameters
    ----------
    data : dict
        deal_type    : 거래 유형 (매매 / 전세 / 월세 / 단기임대)
        area_name    : 지역명
        complex_name : 단지명 or 건물명
        price        : 가격 (문자열)
        monthly_rent : 월세 (월세/단기임대일 경우)
        area_size    : 면적
        floor_info   : 층 정보
        direction    : 방향
        point_1/2/3  : 핵심 포인트
        app_url      : 앱 URL

    Returns
    -------
    dict
        title        : 카카오 공유 제목
        description  : 카카오 공유 설명
        sms_message  : SMS 발송용 문구
        blog_text    : 블로그/단톡방용 전체 문구
    """

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

    # ---------------------------------
    # 가격 표시 조합
    # ---------------------------------
    price_str = price

    if deal == "월세" and rent:
        price_str = f"보증금 {price} / 월세 {rent}"
    elif deal == "전세":
        price_str = f"전세 {price}"
    elif deal == "매매":
        price_str = f"매매가 {price}"
    elif deal == "단기임대" and rent:
        price_str = f"보증금 {price} / 단기임대 {rent}"

    # ---------------------------------
    # 핵심 포인트
    # ---------------------------------
    points = [p for p in [p1, p2, p3] if str(p).strip()]
    point_str = " · ".join(points) if points else ""

    # ---------------------------------
    # 카카오 공유 제목 (45자 이내 권장)
    # ---------------------------------
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

    # ---------------------------------
    # 카카오 공유 설명
    # ---------------------------------
    desc_parts = []

    if size:
        desc_parts.append(f"면적 {size}")
    if floor_:
        desc_parts.append(floor_)
    if direction:
        desc_parts.append(direction)
    if point_str:
        desc_parts.append(point_str)

    desc_parts.append("롯데타워앤강남빌딩부동산중개(주) ☎ 02-578-8285")
    description = " | ".join(desc_parts).strip()

    # ---------------------------------
    # 문자(SMS) 문구
    # ---------------------------------
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

    # ---------------------------------
    # 블로그 / 단톡방 전체 문구
    # ---------------------------------
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

    blog_text = "\n".join(
        [line for line in blog_lines if line is not None and line != ""]
    )

    return {
        "title": title,
        "description": description,
        "sms_message": sms_message,
        "blog_text": blog_text,
    }