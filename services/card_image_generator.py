"""
매물 카드뉴스 이미지 자동 생성 (Pillow 기반)
"""
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

OUTPUT_DIR = "generated_cards"
OFFICE = "롯데타워앤강남빌딩부동산중개(주)"
TEL    = "02-578-8285"


def _fonts():
    candidates = ["malgun.ttf", "NanumGothic.ttf", "DejaVuSans.ttf"]
    big, mid, small = None, None, None
    for c in candidates:
        try:
            big   = ImageFont.truetype(c, 54)
            mid   = ImageFont.truetype(c, 34)
            small = ImageFont.truetype(c, 26)
            break
        except:
            pass
    if big is None:
        big = mid = small = ImageFont.load_default()
    return big, mid, small


def _safe_name(text: str) -> str:
    return "".join(c for c in text if c.isalnum() or c in "_- ").strip().replace(" ","_") or "card"


def generate_card_set(card_data: dict) -> list:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    big, mid, small = _fonts()
    title    = card_data.get("title", "")
    subtitle = card_data.get("subtitle", "")
    badge    = card_data.get("badge_text", "AI 추천")
    pts      = [p.strip() for p in card_data.get("short_copy","").split("\n") if p.strip()]
    caption  = card_data.get("sns_caption", "")
    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    paths    = []

    def base():
        img  = Image.new("RGB", (1080, 1350), (248, 250, 252))
        draw = ImageDraw.Draw(img)
        return img, draw

    def badge_box(draw, text, fnt):
        draw.rounded_rectangle((60,50,380,128), radius=22, fill=(254,229,0))
        draw.text((88,74), text, font=fnt, fill=(25,25,25))

    # 카드 1 — 표지
    img1, d1 = base()
    badge_box(d1, badge, small)
    d1.text((60,160), title[:22],   font=big,   fill=(17,24,39))
    d1.text((60,240), title[22:44], font=big,   fill=(17,24,39))
    d1.text((60,320), subtitle,     font=mid,   fill=(55,65,81))
    d1.rounded_rectangle((60,400,1020,1140), radius=24, fill=(255,255,255), outline=(226,232,240), width=2)
    d1.text((100,470), "AI 추천 프리미엄 매물", font=big, fill=(15,23,42))
    d1.text((100,590), "지금 바로 확인하세요", font=mid, fill=(75,85,99))
    d1.text((100,1080), OFFICE, font=small, fill=(75,85,99))
    p1 = os.path.join(OUTPUT_DIR, f"{_safe_name(title)}_01_{ts}.png")
    img1.save(p1); paths.append(p1)

    # 카드 2 — 핵심 포인트
    img2, d2 = base()
    badge_box(d2, "핵심 포인트", small)
    d2.text((60,160), title[:22], font=big, fill=(17,24,39))
    d2.text((60,240), subtitle,   font=mid, fill=(55,65,81))
    d2.rounded_rectangle((60,360,1020,1160), radius=24, fill=(255,255,255), outline=(226,232,240), width=2)
    y = 440
    for pt in pts[:5]:
        d2.text((100, y), f"• {pt}", font=mid, fill=(31,41,55)); y += 100
    d2.text((100,1100), f"문의 {TEL}", font=mid, fill=(17,24,39))
    p2 = os.path.join(OUTPUT_DIR, f"{_safe_name(title)}_02_{ts}.png")
    img2.save(p2); paths.append(p2)

    # 카드 3 — 문의 CTA
    img3, d3 = base()
    badge_box(d3, badge, small)
    d3.text((60,160), title[:22], font=big, fill=(17,24,39))
    d3.text((60,240), "지금 바로 문의하세요", font=mid, fill=(55,65,81))
    d3.rounded_rectangle((60,360,1020,1180), radius=24, fill=(15,23,42))
    lines = [l.strip() for l in caption.split("\n") if l.strip()][:7]
    cy = 430
    for ln in lines:
        d3.text((100, cy), ln[:30], font=mid, fill=(255,255,255)); cy += 88
    d3.text((100,1100), f"☎ {TEL}", font=mid, fill=(254,229,0))
    d3.text((100,1150), OFFICE,     font=small, fill=(255,255,255))
    p3 = os.path.join(OUTPUT_DIR, f"{_safe_name(title)}_03_{ts}.png")
    img3.save(p3); paths.append(p3)

    return paths
