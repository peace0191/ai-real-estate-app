import streamlit as st
import pandas as pd
from services.ai_price_engine import find_undervalued

st.set_page_config(page_title="AI 저평가 매물 추천", layout="wide")

# CSS
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
  html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
  [data-testid="stSidebar"] { background: linear-gradient(180deg,#0A1F44,#1E2F5B); }
  [data-testid="stSidebar"] * { color: #f8f8f8 !important; }
  .page-title {
    background: linear-gradient(135deg,#0A1F44,#1E3A6E);
    padding: 1.5rem 2rem; border-radius: 12px;
    border-bottom: 3px solid #D4AF37; margin-bottom: 1.5rem;
  }
  .page-title h2 { color: #D4AF37; margin: 0; font-size: 1.5rem; }
  .page-title p  { color: #b0c4de; margin: 0.3rem 0 0; font-size: 0.88rem; }
  .footer-box {
    background: #0A1F44; color: #b0c4de; border-radius: 12px;
    padding: 1.2rem 1.5rem; font-size: 0.75rem; line-height: 1.9;
    border-top: 3px solid #D4AF37; margin-top: 3rem;
  }
  .footer-box strong { color: #D4AF37; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-title">
  <h2>🤖 AI 저평가 매물 추천</h2>
  <p>AI가 시장가격 대비 저평가 매물을 찾아드립니다.</p>
</div>
""", unsafe_allow_html=True)

# ── 시장 시세 입력 ────────────────────────────────────────────
market_price = st.number_input(
    "해당 단지 평균 시세 (억)",
    value=30.0,
    min_value=1.0,
    max_value=200.0,
    step=0.5,
    help="AI 점수 계산 기준이 되는 지역 평균 시세를 입력하세요."
)

st.caption(f"📌 현재 기준 시세: **{market_price}억원** — 이 가격 대비 저평가 매물을 찾습니다.")

st.divider()

# ── 샘플 매물 목록 ────────────────────────────────────────────
sample_properties = [
    {"name": "래미안 블레스티지",         "price": "28", "floor": "중층", "direction": "남향", "size": 84},
    {"name": "디에이치 퍼스트아이파크",   "price": "31", "floor": "고층", "direction": "남향", "size": 84},
    {"name": "대치 SK뷰",                "price": "27", "floor": "저층", "direction": "동향", "size": 84},
    {"name": "개포 래미안 포레스트",      "price": "25", "floor": "중층", "direction": "남향", "size": 74},
    {"name": "역삼 자이",                "price": "18", "floor": "고층", "direction": "남향", "size": 59},
    {"name": "대치 은마아파트",           "price": "22", "floor": "저층", "direction": "서향", "size": 76},
]

st.info(f"📋 분석 대상 샘플 매물 {len(sample_properties)}건 — 아래 버튼을 눌러 AI 점수를 계산하세요.")

# ── AI 추천 실행 ─────────────────────────────────────────────
if st.button("🔍 AI 추천 실행", type="primary", use_container_width=True):

    with st.spinner("AI가 저평가 매물을 분석 중입니다..."):
        df = find_undervalued(sample_properties, market_price)

    st.success(f"✅ AI 추천 매물 TOP {len(df)}건")

    # AI 점수에 따른 등급 컬럼 추가
    def get_grade(score):
        if score >= 70: return "🔥 강력추천"
        if score >= 50: return "⭐ 추천"
        if score >= 30: return "✅ 검토"
        return "➖ 관심"

    df["등급"] = df["ai_score"].apply(get_grade)
    df["시세대비"] = df["price"].apply(
        lambda p: f"{(market_price - float(p)) / market_price * 100:.1f}% 저평가"
        if float(p) < market_price else f"{(float(p) - market_price) / market_price * 100:.1f}% 고평가"
    )

    # 컬럼명 한글화
    df_display = df.rename(columns={
        "name": "단지명", "price": "가격(억)", "floor": "층",
        "direction": "방향", "size": "면적(㎡)", "ai_score": "AI 점수"
    })

    st.dataframe(
        df_display[["단지명", "가격(억)", "층", "방향", "면적(㎡)", "AI 점수", "등급", "시세대비"]],
        use_container_width=True,
        hide_index=True,
    )

    # 상위 1위 하이라이트
    if not df.empty:
        top = df.iloc[0]
        st.markdown(f"""
        <div style="background:#fff7ed;border:2px solid #f97316;border-radius:12px;padding:1.2rem 1.5rem;margin-top:1rem;">
          <h4 style="color:#c2410c;margin:0">🔥 AI 최우선 추천 매물</h4>
          <p style="margin:0.5rem 0 0;font-size:1rem;">
            <b>{top['name']}</b> — <b>{top['price']}억</b>
            ({top['floor']} · {top['direction']} · {top['size']}㎡)<br>
            <span style="color:#f97316;font-weight:700;font-size:1.2rem">AI 점수: {top['ai_score']}점</span>
          </p>
        </div>
        """, unsafe_allow_html=True)

# 푸터
st.markdown("""
<div class="footer-box">
  <strong>AI 예약 자동 매칭 챗봇 부동산플랫폼</strong><br>
  운영: <strong>롯데타워앤강남빌딩부동산중개(주)</strong><br>
  개설등록번호 11680-2023-00078 &nbsp;|&nbsp; 사업자등록번호 461-86-02740<br>
  서울특별시 강남구 대치동 938외1, 삼환아르누보2, 507호<br>
  대표전화 <strong>02-578-8285</strong> &nbsp;|&nbsp; 휴대전화 <strong>010-8985-8945</strong>
</div>
""", unsafe_allow_html=True)
