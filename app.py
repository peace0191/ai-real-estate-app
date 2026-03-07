import streamlit as st

st.set_page_config(
    page_title="AI 예약 자동 매칭 챗봇 부동산플랫폼",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 브랜드 CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
  html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }

  /* 사이드바 */
  [data-testid="stSidebar"] { background: linear-gradient(180deg,#0A1F44 0%,#1E2F5B 100%); }
  [data-testid="stSidebar"] * { color: #f8f8f8 !important; }
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stRadio label { color: #D4AF37 !important; }

  /* 헤더 */
  .main-header {
    background: linear-gradient(135deg,#0A1F44 0%,#1E3A6E 60%,#0A1F44 100%);
    padding: 2rem 2.5rem 1.5rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    border: 1px solid #D4AF37;
  }
  .main-header h1 { color:#D4AF37; font-weight:900; font-size:1.9rem; margin:0; }
  .main-header p  { color:#b0c4de; margin:0.3rem 0 0; font-size:0.95rem; }

  /* 골드 라인 */
  .gold-line { border:none; border-top:2px solid #D4AF37; margin:1rem 0; }

  /* 카드 */
  .info-card {
    background:#f7f9fc; border:1px solid #dde3ef;
    border-radius:12px; padding:1.2rem 1.5rem; margin-bottom:1rem;
  }

  /* 메트릭 */
  [data-testid="metric-container"] { background:#eef2ff; border-radius:10px; padding:0.8rem; }

  /* 푸터 */
  .footer-box {
    background:#0A1F44; color:#b0c4de;
    border-radius:12px; padding:1.5rem 2rem;
    font-size:0.78rem; line-height:1.8;
    border-top:3px solid #D4AF37; margin-top:3rem;
  }
  .footer-box strong { color:#D4AF37; }
</style>
""", unsafe_allow_html=True)

# ── 헤더 ────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>🏠 AI 예약 자동 매칭 챗봇 부동산플랫폼</h1>
  <p>AI 실거래가 분석 · 사전예약 매칭 · 공동중개 네트워크 · 자동 숏츠 광고</p>
</div>
""", unsafe_allow_html=True)

# ── 메인 대시보드 카드 ───────────────────────────────────────────
from services.property_store import (
    get_all_properties, get_demand_items, get_supply_items,
    get_co_broker_items, get_reviewed_items
)
from services.matching_service import build_matches

all_props   = get_all_properties()
demand_list = get_demand_items()
supply_list = get_supply_items()
co_broker   = get_co_broker_items()
reviewed    = get_reviewed_items()
matches     = build_matches(demand_list, supply_list)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("📋 총 매물 접수", len(all_props))
c2.metric("🔵 수요 의뢰", len(demand_list))
c3.metric("🟢 공급 의뢰", len(supply_list))
c4.metric("🟠 공동중개", len(co_broker))
c5.metric("🤝 매칭 후보", len(matches))

st.markdown('<hr class="gold-line">', unsafe_allow_html=True)

# ── 메뉴 카드 ────────────────────────────────────────────────────
col_a, col_b, col_c, col_d = st.columns(4)

with col_a:
    st.markdown("""
    <div class="info-card">
      <h3 style="color:#0A1F44">🏠 매물 접수</h3>
      <p style="font-size:0.88rem;color:#555">수요·공급·공동중개 매물을 등록합니다.<br>
      사진 2장(공간별)·30초 이하 영상 필수</p>
    </div>""", unsafe_allow_html=True)

with col_b:
    st.markdown("""
    <div class="info-card">
      <h3 style="color:#0A1F44">📊 AI 저평가 분석</h3>
      <p style="font-size:0.88rem;color:#555">국토부 실거래가·KB시세·네이버 매물 기준으로<br>
      저평가 매물을 자동 분석합니다.</p>
    </div>""", unsafe_allow_html=True)

with col_c:
    st.markdown("""
    <div class="info-card">
      <h3 style="color:#0A1F44">🤝 AI 자동 매칭</h3>
      <p style="font-size:0.88rem;color:#555">수요↔공급을 AI가 자동 점수화하여<br>
      최적 매물을 실시간 매칭합니다.</p>
    </div>""", unsafe_allow_html=True)

with col_d:
    st.markdown("""
    <div class="info-card">
      <h3 style="color:#0A1F44">🎬 자동 숏츠 광고</h3>
      <p style="font-size:0.88rem;color:#555">저평가 추천 매물을 유튜브 숏츠로<br>
      자동 제작·업로드합니다.</p>
    </div>""", unsafe_allow_html=True)

# ── 최근 매칭 미리보기 ───────────────────────────────────────────
if matches:
    st.subheader("🔴 실시간 AI 매칭 상위 후보")
    for m in matches[:3]:
        st.success(
            f"🤝 **{m['demand_name']}** ↔ **{m['supply_name']}**  |  "
            f"{m['region']} / {m['property_type']} / {m['trade_type']}  |  "
            f"매칭비율 **{m['score']}%**"
        )

# ── 푸터 ────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-box">
  <strong>AI 예약 자동 매칭 챗봇 부동산플랫폼</strong><br>
  운영: <strong>롯데타워앤강남빌딩부동산중개(주)</strong><br>
  개설등록번호 11680-2023-00078 &nbsp;|&nbsp; 사업자등록번호 461-86-02740<br>
  서울특별시 강남구 대치동 938외1, 삼환아르누보2, 507호<br>
  대표전화 <strong>02-578-8285</strong> &nbsp;|&nbsp; 휴대전화 <strong>010-8985-8945</strong>
</div>
""", unsafe_allow_html=True)
