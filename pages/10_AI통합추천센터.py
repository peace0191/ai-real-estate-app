import streamlit as st
import pandas as pd
from services.data_ingestion_engine import load_internal_properties
from services.ai_score_engine import calculate_ai_score
from services.marketing_ai_engine import generate_marketing_content, generate_card_news_content
from services.card_image_generator import generate_card_set
from services.share_message_service import build_property_share_data

APP_URL = "https://ai-real-estate-app-nvbi9ytwq6gh6tmztd4tpu.streamlit.app"

st.title("🌟 AI 통합 추천 센터")
st.caption("저평가 분석 → 홍보 문구 → 카드뉴스 생성까지 원스톱으로 처리합니다.")
st.markdown("---")

df = load_internal_properties()

st.subheader("🔍 AI 저평가 TOP 매물")

rows = []
for _, row in df.iterrows():
    score_data = calculate_ai_score(row.to_dict())
    rows.append({**row.to_dict(), **score_data})
result_df = pd.DataFrame(rows).sort_values("ai_score", ascending=False)

top5 = result_df.head(5)
cols = st.columns(5)
selected_idx = None
for i, (col, (_, row)) in enumerate(zip(cols, top5.iterrows())):
    with col:
        score = row.get("ai_score", 0)
        color = "🔥" if score>=70 else "⭐" if score>=50 else "👍" if score>=35 else "⚪"
        apt_name = str(row.get("apt", row.get("complex_name", "-")))[:8]
        st.markdown(f"**{color}**")
        st.metric(apt_name, f"{score}점")
        if st.button("선택", key=f"sel_{i}", use_container_width=True):
            st.session_state["selected_prop"] = row.to_dict()

if "selected_prop" in st.session_state:
    prop = st.session_state["selected_prop"]
    st.markdown("---")
    apt  = prop.get('apt', prop.get('complex_name', '-'))
    area = prop.get('region', prop.get('area_name', '-'))
    st.markdown(f"### 📌 선택 매물: {apt} ({area}) | {prop.get('deal_type','')} {prop.get('price','')}억")

    ai = calculate_ai_score(prop)
    c1, c2, c3 = st.columns(3)
    c1.metric("AI 저평가 점수", f"{ai['ai_score']}점")
    c2.metric("등급", ai['grade'])
    c3.metric("지역", prop.get("region", prop.get("area_name", "-")))

    st.markdown("---")
    action = st.radio("🚀 원하는 작업 선택", [
        "📝 홍보 문구 생성",
        "🎬 숏츠 스크립트 생성",
        "🖼️ 카드뉴스 3장 생성",
        "📤 카카오 공유 문구 생성",
    ], horizontal=True)

    if st.button("▶ 실행", use_container_width=True, type="primary"):
        if action == "📝 홍보 문구 생성":
            result = generate_marketing_content(prop)
            st.markdown("**단톡방 문구**")
            st.code(result.get("kakao_group_text",""))
            st.markdown("**블로그 문구**")
            st.code(result.get("blog_text",""))

        elif action == "🎬 숏츠 스크립트 생성":
            result = generate_marketing_content(prop)
            st.markdown("**유튜브 숏츠 스크립트**")
            st.code(result.get("youtube_script",""))
            st.markdown("**SNS 문구**")
            st.code(result.get("sns_text",""))

        elif action == "🖼️ 카드뉴스 3장 생성":
            with st.spinner("카드뉴스 생성 중..."):
                card_data = generate_card_news_content(prop)
                paths = generate_card_set(card_data)
            st.success("카드뉴스 생성 완료!")
            cols2 = st.columns(3)
            for i, (col, path) in enumerate(zip(cols2, paths)):
                with col:
                    try:
                        with open(path, "rb") as f:
                            img_bytes = f.read()
                        st.image(img_bytes, use_container_width=True)
                        st.download_button(f"📥 저장{i+1}", img_bytes, f"card_{i+1}.png", "image/png", key=f"tc_{i}")
                    except Exception as e:
                        st.error(f"오류: {e}")

        elif action == "📤 카카오 공유 문구 생성":
            prop["app_url"] = APP_URL
            result = build_property_share_data(prop)
            st.markdown("**카카오 제목**");   st.code(result["title"])
            st.markdown("**카카오 설명**");   st.code(result["description"])
            st.markdown("**문자 발송 문구**"); st.code(result["sms_message"])
            st.markdown("**단톡방 문구**");   st.code(result["blog_text"])
else:
    st.info("👆 위에서 매물을 선택하면 홍보 자동화가 시작됩니다.")
