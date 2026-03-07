import streamlit as st
from ai_engine.undervalue_engine import calculate_undervalue, get_sample_prices
from services.property_store import save_shorts_candidate, push_alert

st.set_page_config(page_title="AI 저평가 분석", layout="wide")

st.markdown("""
<style>
  .page-title{background:linear-gradient(135deg,#0A1F44,#1E3A6E);padding:1.5rem 2rem;
    border-radius:12px;border-bottom:3px solid #D4AF37;margin-bottom:1.5rem;}
  .page-title h2{color:#D4AF37;margin:0;}
  .page-title p{color:#b0c4de;margin:0.3rem 0 0;font-size:0.9rem;}
  .result-box{border-radius:14px;padding:1.5rem;margin-top:1rem;}
  .result-hot{background:#fff7ed;border:2px solid #f97316;}
  .result-good{background:#f0fdf4;border:2px solid #22c55e;}
  .result-normal{background:#f8fafc;border:2px solid #94a3b8;}
  .result-over{background:#fff1f2;border:2px solid #ef4444;}
  .big-rate{font-size:3rem;font-weight:900;line-height:1.1;}
  .footer-box{background:#0A1F44;color:#b0c4de;border-radius:12px;padding:1rem 1.5rem;
    font-size:0.75rem;line-height:1.8;border-top:3px solid #D4AF37;margin-top:2rem;}
  .footer-box strong{color:#D4AF37;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-title">
  <h2>📊 AI 실거래가 비교 저평가 분석</h2>
  <p>국토부 실거래가 · KB시세 · 네이버 매물 평균을 기준으로 저평가 매물을 자동 분석합니다.</p>
</div>
""", unsafe_allow_html=True)

st.info("💡 아래에 매물 정보를 입력하면 AI가 기준가 대비 저평가율을 자동으로 계산합니다.")

c1, c2 = st.columns(2)

with c1:
    st.subheader("매물 정보 입력")
    prop_name  = st.text_input("매물명 (단지명)")
    prop_type  = st.selectbox("매물 유형", ["아파트","주상복합","오피스텔","상가"])
    region     = st.selectbox("지역", ["강남구 대치동","강남구 개포동","강남구 역삼동",
                                       "송파구 신천동","성수동","용산구 한남동","기타"])
    listing_price = st.number_input("현재 매물 가격 (만원)", min_value=0, value=0, step=100)
    area       = st.number_input("전용면적 (㎡)", min_value=0.0, value=84.0, step=1.0)

with c2:
    st.subheader("시세 데이터 입력 (선택·자동 입력 가능)")
    sample = get_sample_prices(region, prop_type)
    real_tx = st.number_input("국토부 실거래가 평균 (만원)",
                               value=int(sample.get("real_tx", 0)), step=100)
    kb_price = st.number_input("KB 시세 (만원)",
                                value=int(sample.get("kb", 0)), step=100)
    naver_price = st.number_input("네이버 매물 평균가 (만원)",
                                   value=int(sample.get("naver", 0)), step=100)

    st.caption("📌 지역·유형 선택 시 샘플 시세가 자동 입력됩니다. 실제 시세로 수정 가능합니다.")

st.divider()

if st.button("🔍 AI 저평가 분석 실행", type="primary", use_container_width=True):
    if listing_price <= 0:
        st.error("매물 가격을 입력해 주세요.")
    else:
        ai_ref, rate, label = calculate_undervalue(listing_price, real_tx, kb_price, naver_price)

        # 색상 클래스 결정
        if rate >= 10:   box_cls = "result-hot"
        elif rate >= 5:  box_cls = "result-good"
        elif rate >= 0:  box_cls = "result-normal"
        else:            box_cls = "result-over"

        # 색상
        color = "#f97316" if rate >= 10 else ("#22c55e" if rate >= 5 else ("#64748b" if rate >= 0 else "#ef4444"))

        st.markdown(f"""
        <div class="result-box {box_cls}">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <div>
              <h3 style="margin:0;color:#0A1F44">{prop_name or region + " " + prop_type}</h3>
              <p style="margin:0.3rem 0;color:#555">지역: {region} | 유형: {prop_type} | 면적: {area}㎡</p>
            </div>
            <div style="text-align:center">
              <div class="big-rate" style="color:{color}">{rate:+.1f}%</div>
              <div style="font-size:1.2rem;font-weight:700">{label}</div>
            </div>
          </div>
          <hr style="border-color:#ddd;margin:1rem 0">
          <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;text-align:center">
            <div><div style="font-size:0.8rem;color:#888">AI 기준가</div>
              <div style="font-size:1.3rem;font-weight:700;color:#0A1F44">{ai_ref:,.0f}만원</div></div>
            <div><div style="font-size:0.8rem;color:#888">매물 가격</div>
              <div style="font-size:1.3rem;font-weight:700;color:#1d4ed8">{listing_price:,.0f}만원</div></div>
            <div><div style="font-size:0.8rem;color:#888">차액</div>
              <div style="font-size:1.3rem;font-weight:700;color:{color}">{ai_ref-listing_price:+,.0f}만원</div></div>
            <div><div style="font-size:0.8rem;color:#888">평당가(공급)</div>
              <div style="font-size:1.3rem;font-weight:700;color:#555">
                {listing_price/(area/3.305):.0f}만원</div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if rate >= 5:
            st.success(f"✅ **{label}** 매물입니다. 숏츠 광고 후보로 등록하시겠습니까?")
            if st.button("🎬 숏츠 광고 후보 등록", key="shorts_reg"):
                save_shorts_candidate({
                    "name": prop_name or f"{region} {prop_type}",
                    "region": region,
                    "property_type": prop_type,
                    "listing_price": listing_price,
                    "ai_ref_price": ai_ref,
                    "undervalue_rate": rate,
                    "label": label,
                })
                push_alert("숏츠 후보 등록",
                           f"{prop_name or region+' '+prop_type} — 저평가율 {rate:.1f}% 숏츠 후보 등록됨",
                           "success")
                st.success("🎬 숏츠 광고 후보로 등록되었습니다!")

st.markdown("""
<div class="footer-box">
  <strong>AI 예약 자동 매칭 챗봇 부동산플랫폼</strong> | 운영: <strong>롯데타워앤강남빌딩부동산중개(주)</strong><br>
  개설등록번호 11680-2023-00078 | 사업자등록번호 461-86-02740<br>
  서울 강남구 대치동 938외1, 삼환아르누보2, 507호 | <strong>02-578-8285</strong> / 010-8985-8945
</div>
""", unsafe_allow_html=True)
