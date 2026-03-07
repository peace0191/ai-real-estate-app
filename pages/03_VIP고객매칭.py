import streamlit as st
from services.customer_match_engine import match_customer

st.set_page_config(page_title="VIP 고객 매칭", layout="wide")

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
  .result-card {
    background: white; border: 2px solid #D4AF37;
    border-radius: 14px; padding: 1.2rem 1.5rem;
    margin-bottom: 0.8rem;
    box-shadow: 0 4px 14px rgba(212,175,55,0.15);
  }
  .no-result {
    background: #f8fafc; border: 1px dashed #cbd5e1;
    border-radius: 12px; padding: 2rem; text-align: center;
    color: #94a3b8; font-size: 1rem;
  }
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
  <h2>👑 VIP 고객 매칭</h2>
  <p>고객 예산 · 최소 면적 조건에 맞는 매물을 즉시 추천합니다.</p>
</div>
""", unsafe_allow_html=True)

# ── 고객 조건 입력 ────────────────────────────────────────────
st.subheader("🎯 고객 조건 입력")

col1, col2 = st.columns(2)
with col1:
    budget = st.number_input(
        "💰 고객 예산 (억)",
        min_value=0.0, max_value=200.0,
        value=30.0, step=0.5,
        help="억 단위로 입력하세요. 예: 30 → 30억"
    )
with col2:
    min_size = st.number_input(
        "📐 최소 면적 (㎡)",
        min_value=0, max_value=500,
        value=84, step=1,
        help="희망 최소 면적을 ㎡ 단위로 입력하세요."
    )

customer = {
    "budget":   budget,
    "min_size": min_size,
}

st.caption(f"📌 설정 조건: 예산 **{budget}억** 이하 · 면적 **{min_size}㎡** 이상")

st.divider()

# ── 샘플 매물 목록 ────────────────────────────────────────────
properties = [
    {"name": "래미안 블레스티지",         "price": "28", "size": 84,  "floor": "중층", "direction": "남향"},
    {"name": "디에이치 퍼스트아이파크",   "price": "31", "size": 84,  "floor": "고층", "direction": "남향"},
    {"name": "대치 SK뷰",                "price": "27", "size": 84,  "floor": "저층", "direction": "동향"},
    {"name": "개포 래미안 포레스트",      "price": "25", "size": 74,  "floor": "중층", "direction": "남향"},
    {"name": "역삼 자이",                "price": "18", "size": 59,  "floor": "고층", "direction": "남향"},
    {"name": "대치 은마아파트",           "price": "22", "size": 76,  "floor": "저층", "direction": "서향"},
    {"name": "도곡 렉슬",                "price": "35", "size": 114, "floor": "고층", "direction": "남향"},
    {"name": "개포 주공",                "price": "20", "size": 49,  "floor": "중층", "direction": "동향"},
]

# ── 매칭 실행 ─────────────────────────────────────────────────
if st.button("🔍 매칭 실행", type="primary", use_container_width=True):

    with st.spinner("고객 조건에 맞는 매물을 탐색 중..."):
        result = match_customer(customer, properties)

    st.subheader(f"✅ 추천 매물 — {len(result)}건")

    if not result:
        st.markdown("""
        <div class="no-result">
          🔍 조건에 맞는 매물이 없습니다.<br>
          <span style="font-size:0.85rem">예산을 높이거나 최소 면적을 줄여보세요.</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        for i, p in enumerate(result, 1):
            price_diff = budget - float(p["price"])
            size       = p.get("size", p.get("area", "-"))
            floor_     = p.get("floor", "-")
            direction  = p.get("direction", "-")

            st.markdown(f"""
<div class="result-card">
  <div style="display:flex;justify-content:space-between;align-items:center">
    <div>
      <span style="font-size:1.1rem;font-weight:900;color:#0A1F44">
        {i}. {p['name']}
      </span><br>
      <span style="font-size:0.85rem;color:#555">
        면적 {size}㎡ &nbsp;|&nbsp; {floor_} &nbsp;|&nbsp; {direction}
      </span>
    </div>
    <div style="text-align:right">
      <div style="font-size:1.5rem;font-weight:900;color:#0A1F44">
        {p['price']}억
      </div>
      <div style="font-size:0.78rem;color:#22c55e;font-weight:700">
        예산 대비 {price_diff:.1f}억 여유
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

        # 원본 데이터 보기
        with st.expander("📋 표 형식으로 보기"):
            import pandas as pd
            df = pd.DataFrame(result)
            rename = {"name":"단지명","price":"가격(억)","size":"면적(㎡)",
                      "floor":"층","direction":"방향"}
            st.dataframe(
                df.rename(columns={k:v for k,v in rename.items() if k in df.columns}),
                use_container_width=True, hide_index=True
            )

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
