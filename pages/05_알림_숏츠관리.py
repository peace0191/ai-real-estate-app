import streamlit as st
from services.property_store import get_alerts, get_shorts_candidates

st.set_page_config(page_title="사전알림 · 숏츠 후보", layout="wide")

st.markdown("""
<style>
  .page-title{background:linear-gradient(135deg,#0A1F44,#1E3A6E);padding:1.5rem 2rem;
    border-radius:12px;border-bottom:3px solid #D4AF37;margin-bottom:1.5rem;}
  .page-title h2{color:#D4AF37;margin:0;} .page-title p{color:#b0c4de;margin:0.3rem 0 0;}
  .shorts-card{border-radius:14px;padding:1.2rem 1.5rem;margin-bottom:0.8rem;}
  .footer-box{background:#0A1F44;color:#b0c4de;border-radius:12px;padding:1rem 1.5rem;
    font-size:0.75rem;line-height:1.8;border-top:3px solid #D4AF37;margin-top:2rem;}
  .footer-box strong{color:#D4AF37;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-title">
  <h2>🔔 사전알림 보기창 · 🎬 숏츠 광고 자동 생성</h2>
  <p>관리자 알림 확인 및 저평가 추천 매물의 유튜브 숏츠 광고 생성 관리</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔔 사전알림 보기", "🎬 숏츠 광고 후보 관리"])

with tab1:
    alerts = get_alerts()
    if not alerts:
        st.info("등록된 알림이 없습니다.")
    else:
        st.caption(f"총 {len(alerts)}건 알림")
        for a in alerts:
            lvl   = a.get("level", "info")
            title = a.get("title", "-")
            msg   = a.get("message", "-")
            if lvl == "success":   st.success(f"✅ **{title}** — {msg}")
            elif lvl == "warning": st.warning(f"⚠️ **{title}** — {msg}")
            elif lvl == "error":   st.error(f"🚨 **{title}** — {msg}")
            else:                  st.info(f"ℹ️ **{title}** — {msg}")

with tab2:
    cands = get_shorts_candidates()
    if not cands:
        st.info("숏츠 제작 후보가 없습니다. [AI 저평가 분석] 탭에서 등록하세요.")
    else:
        st.caption(f"숏츠 후보 {len(cands)}건 — 하루 최대 30건 자동 생성 예정")
        for idx, sc in enumerate(cands):
            rate  = sc.get("undervalue_rate", 0)
            label = sc.get("label", "")
            color = "#f97316" if rate >= 10 else "#22c55e"
            st.markdown(f"""
            <div class="shorts-card" style="border:2px solid {color};background:{'#fff7ed' if rate>=10 else '#f0fdf4'}">
              <b style="font-size:1.05rem">{sc.get("name","-")}</b> &nbsp;
              <span style="color:{color};font-weight:700">{label} | 저평가율 {rate:.1f}%</span><br>
              <span style="font-size:0.88rem;color:#555">
                지역: {sc.get("region","-")} | 유형: {sc.get("property_type","-")} |
                매물가: {sc.get("listing_price",0):,}만원 | AI기준가: {sc.get("ai_ref_price",0):,}만원
              </span>
            </div>""", unsafe_allow_html=True)

            with st.expander(f"📋 숏츠 스크립트 미리보기 #{idx+1}"):
                diff = sc.get('ai_ref_price', 0) - sc.get('listing_price', 0)
                st.markdown(f"""
**🎬 유튜브 숏츠 광고 스크립트**

---
📍 **{sc.get("region","-")} {sc.get("property_type","-")}**

💰 매물 가격: **{sc.get("listing_price",0):,}만원**
📊 AI 기준가 대비: **{rate:.1f}% 저평가** ({diff:+,.0f}만원 절약!)
🏷️ 추천 등급: **{label}**

---
✅ 지금 바로 상담 예약하세요!

📞 **02-578-8285** / 010-8985-8945
🏢 롯데타워앤강남빌딩부동산중개(주)
서울 강남구 대치동 삼환아르누보2, 507호

`#AI부동산 #저평가매물 #{sc.get("region","").replace(" ","")} #투자추천`
                """)
                st.caption("💡 실제 숏츠 생성은 MoviePy 서버 연동 후 자동 업로드됩니다.")

        # SNS 발송 UI
        st.divider()
        st.subheader("📨 SNS · 이메일 알림 발송")
        c1, c2 = st.columns(2)
        with c1:
            send_target = st.text_area("발송 대상 연락처 (쉼표 구분)", height=100,
                                        placeholder="010-xxxx-xxxx, 010-yyyy-yyyy")
            send_channel = st.multiselect("발송 채널",
                                           ["카카오톡 알림톡", "SMS", "이메일", "Instagram DM", "YouTube"])
        with c2:
            st.info("📌 선택된 숏츠 후보 중 저평가율 상위 매물을 자동으로 발송합니다.")
            if st.button("📤 선별 알림 발송", use_container_width=True, type="primary"):
                if send_target and send_channel:
                    st.success(f"✅ {', '.join(send_channel)} 채널로 발송 요청이 등록되었습니다!")
                    st.caption("(실제 발송은 카카오비즈니스·AWS SES 연동 후 처리됩니다)")
                else:
                    st.warning("대상 연락처와 발송 채널을 선택하세요.")

st.markdown("""
<div class="footer-box">
  <strong>AI 예약 자동 매칭 챗봇 부동산플랫폼</strong> | 운영: <strong>롯데타워앤강남빌딩부동산중개(주)</strong><br>
  개설등록번호 11680-2023-00078 | 사업자등록번호 461-86-02740<br>
  서울 강남구 대치동 938외1, 삼환아르누보2, 507호 | <strong>02-578-8285</strong> / 010-8985-8945
</div>
""", unsafe_allow_html=True)
