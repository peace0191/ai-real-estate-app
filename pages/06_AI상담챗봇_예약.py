import streamlit as st
from services.property_store import push_alert

st.set_page_config(page_title="AI 상담 챗봇 · 예약", layout="wide")

st.markdown("""
<style>
  .page-title{background:linear-gradient(135deg,#0A1F44,#1E3A6E);padding:1.5rem 2rem;
    border-radius:12px;border-bottom:3px solid #D4AF37;margin-bottom:1.5rem;}
  .page-title h2{color:#D4AF37;margin:0;} .page-title p{color:#b0c4de;margin:0.3rem 0 0;}
  .chat-bubble-user{background:#dbeafe;padding:0.7rem 1rem;border-radius:12px 12px 0 12px;
    margin:0.4rem 0;max-width:70%;margin-left:auto;font-size:0.92rem;}
  .chat-bubble-ai{background:#f1f5f9;padding:0.7rem 1rem;border-radius:12px 12px 12px 0;
    margin:0.4rem 0;max-width:70%;font-size:0.92rem;border-left:3px solid #D4AF37;}
  .footer-box{background:#0A1F44;color:#b0c4de;border-radius:12px;padding:1rem 1.5rem;
    font-size:0.75rem;line-height:1.8;border-top:3px solid #D4AF37;margin-top:2rem;}
  .footer-box strong{color:#D4AF37;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-title">
  <h2>💬 AI 상담 챗봇 · 사전 예약 매칭</h2>
  <p>AI 챗봇으로 매물 상담 · 상담 예약 · 사전 수요 등록을 진행합니다.</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["💬 AI 상담 챗봇", "📅 상담 예약 등록"])

with tab1:
    # 간단 FAQ 챗봇 (실제 RAG 연동 전 목업)
    FAQ = {
        "대치동": "대치동은 강남구 내 학군이 가장 우수한 지역으로, 현재 AI 기준가 대비 저평가 매물이 있습니다. 자세한 매물은 [AI 저평가 분석] 탭을 확인하세요.",
        "개포동": "개포동은 재건축 완료 단지가 많아 신규 아파트 위주 시장입니다. 현재 AI 기준가 기준 일부 저평가 매물이 포착되고 있습니다.",
        "전세": "전세 매물은 현재 수요가 많습니다. 원하시는 지역과 예산을 알려주시면 AI가 자동으로 매물을 매칭해 드립니다.",
        "매매": "매매 매물은 AI 실거래가 분석으로 저평가 매물을 실시간 탐지합니다. 지역과 예산 범위를 알려주시면 추천해 드립니다.",
        "월세": "월세 매물도 다수 보유하고 있습니다. 희망 지역과 예산을 알려주시면 맞춤 추천드립니다.",
        "상담": "상담은 02-578-8285로 전화하시거나 아래 예약 탭에서 사전 예약하실 수 있습니다.",
        "연락처": "대표 전화: 02-578-8285 / 010-8985-8945\n강남구 대치동 938외1, 삼환아르누보2, 507호",
    }

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "ai", "msg": "안녕하세요! AI 예약 자동 매칭 챗봇 부동산플랫폼입니다. 🏠\n\n대치동·개포동·잠실·성수·용산 지역 매물 상담, 전세·매매·월세 문의, 상담 예약을 도와드립니다.\n\n궁금하신 것을 말씀해 주세요!"}
        ]

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-bubble-user">👤 {msg["msg"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-ai">🤖 {msg["msg"]}</div>', unsafe_allow_html=True)

    user_input = st.chat_input("메시지를 입력하세요 (예: 대치동 전세 있나요?)")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "msg": user_input})

        # 키워드 매칭 응답
        reply = "죄송합니다, 해당 질문에 대한 정보를 찾기 어렵습니다. 02-578-8285로 직접 문의해 주시면 더 자세히 안내해 드립니다."
        for kw, resp in FAQ.items():
            if kw in user_input:
                reply = resp
                break
        if any(w in user_input for w in ["안녕", "hello", "hi"]):
            reply = "안녕하세요! 😊 저는 AI 부동산 매칭 챗봇입니다. 매물 상담, 예약, 저평가 분석을 도와드립니다."

        st.session_state.chat_history.append({"role": "ai", "msg": reply})
        st.rerun()

with tab2:
    st.subheader("📅 상담 예약 등록")
    st.info("💡 원하시는 상담 일시와 조건을 등록하시면 AI가 최적 매물을 사전 매칭합니다.")

    r1, r2 = st.columns(2)
    with r1:
        res_name    = st.text_input("예약자 이름")
        res_phone   = st.text_input("연락처")
        res_date    = st.date_input("희망 상담일")
        res_time    = st.selectbox("희망 시간", ["10:00","11:00","13:00","14:00","15:00","16:00","17:00"])
    with r2:
        res_region  = st.selectbox("희망 지역", ["강남구 대치동","강남구 개포동","강남구 역삼동",
                                                 "송파구 신천동","성수동","용산구 한남동","기타"])
        res_type    = st.selectbox("거래 유형", ["매매","전세","월세"])
        res_budget  = st.text_input("예산 (만원)")
        res_area    = st.text_input("희망 면적 (㎡)")
    res_memo = st.text_area("추가 요청사항", placeholder="예: 학군 우선, 역세권 선호, 저층 선호 등")

    if st.button("✅ 상담 예약 등록", type="primary", use_container_width=True):
        if res_name and res_phone:
            push_alert("신규 상담 예약",
                       f"{res_name}({res_phone}) | {res_date} {res_time} | {res_region} {res_type} {res_budget}만원",
                       "success")
            st.balloons()
            st.success(f"✅ {res_name}님의 상담 예약이 완료되었습니다!\n"
                       f"📅 {res_date} {res_time} | 담당자가 연락드리겠습니다.")
        else:
            st.warning("이름과 연락처를 입력해 주세요.")

st.markdown("""
<div class="footer-box">
  <strong>AI 예약 자동 매칭 챗봇 부동산플랫폼</strong> | 운영: <strong>롯데타워앤강남빌딩부동산중개(주)</strong><br>
  개설등록번호 11680-2023-00078 | 사업자등록번호 461-86-02740<br>
  서울 강남구 대치동 938외1, 삼환아르누보2, 507호 | <strong>02-578-8285</strong> / 010-8985-8945
</div>
""", unsafe_allow_html=True)
