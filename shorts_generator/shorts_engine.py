"""
shorts_engine.py
고급형 / 급매형 / 심플형 3가지 스타일 숏츠 스크립트 자동 생성
"""
from datetime import datetime


def generate(prop: dict, analysis: dict, tone: str = "고급형") -> str:
    name   = prop.get("name", "")
    region = prop.get("region", "")
    ptype  = prop.get("type", "아파트")
    trade  = prop.get("trade", "매매")
    price  = int(prop.get("price", 0))
    area   = prop.get("area", 0)
    grade  = analysis.get("grade", "✅")
    rate   = analysis.get("rate", 0)
    now    = datetime.now().strftime("%Y-%m-%d %H:%M")

    header = f"🎬 AI 자동 생성 숏츠 스크립트 [{tone}]  |  {now}  |  {prop.get('id','')}"
    bar    = "━" * 44

    if tone == "고급형":
        return f"""{header}
{bar}

[오프닝 — 0~3초]
{grade} {region}의 핵심 입지, 지금이 기회입니다.

[본문 — 3~20초]
📍 {name}
🏠 {ptype}  |  💼 {trade}  |  💰 {price:,}만원
📐 전용 {area}㎡

🤖 AI 분석 결과
→ AI 기준가 대비 {rate}% 저평가 확인
→ 3중 비교 (국토부 · KB · 네이버) 검증 완료

[클로징 — 20~30초]
프리미엄 매물은 먼저 보는 사람이 잡습니다.
지금 바로 연락하세요.

📞 02-578-8285 / 010-8985-8945
롯데타워앤강남빌딩부동산중개(주)

[해시태그]
#{region} #{ptype} #{trade} #저평가매물 #AI부동산 #강남부동산 #부동산투자"""

    elif tone == "급매형":
        return f"""{header}
{bar}

🚨 [오프닝 — 0~3초]
지금 당장 확인하세요! 급매 나왔습니다.

⚡ [본문 — 3~20초]
{grade} 급매  |  {region} {ptype}

💰 {price:,}만원  /  {area}㎡
📉 시세보다 {rate}% 저렴 — AI 검증

⏰ 선착순 상담 운영 중
자리 없으면 못 잡습니다!

☎ [클로징 — 20~30초]
02-578-8285  /  010-8985-8945
롯데타워앤강남빌딩부동산중개(주)

[해시태그]
#급매 #{region}급매 #{ptype}급매 #저평가 #부동산급매"""

    else:  # 심플형
        return f"""{header}
{bar}

{name}
{region} · {ptype} · {trade}
{price:,}만원 · {area}㎡

저평가율 {rate}%  {grade}

02-578-8285
롯데타워앤강남빌딩부동산중개(주)"""
