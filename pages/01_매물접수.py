import streamlit as st

# 공유 서비스 불러오기
from services.share_message_service import build_property_share_data

APP_URL = "https://ai-real-estate-app-nvbi9ytwq6gh6tmztd4tpu.streamlit.app"

st.title("📋 매물 접수")
st.caption("매물을 등록하면 홍보 문구와 카카오 공유 문구가 자동 생성됩니다.")

st.markdown("---")

# ---------------------------
# 매물 입력 폼
# ---------------------------
with st.form("property_form"):

    c1, c2 = st.columns(2)

    with c1:
        deal_type = st.selectbox(
            "거래 유형",
            ["매매", "전세", "월세", "단기임대"]
        )

        area_name = st.text_input(
            "지역",
            "강남구 대치동"
        )

        complex_name = st.text_input(
            "단지명 / 건물명",
            "예: 개포래미안블레스티지"
        )

        price = st.text_input(
            "가격",
            "예: 29억"
        )

        monthly_rent = st.text_input(
            "월세 (월세/단기임대만)",
            ""
        )

        area_size = st.text_input(
            "면적",
            "예: 84㎡ / 34평"
        )

    with c2:

        floor_info = st.text_input(
            "층 정보",
            "예: 15층"
        )

        direction = st.text_input(
            "방향",
            "예: 남향"
        )

        point_1 = st.text_input(
            "핵심 포인트 1",
            "예: 학군 우수"
        )

        point_2 = st.text_input(
            "핵심 포인트 2",
            "예: 역세권"
        )

        point_3 = st.text_input(
            "핵심 포인트 3",
            "예: 즉시 입주 가능"
        )

    submitted = st.form_submit_button("매물 등록")

st.markdown("---")

# ---------------------------
# 결과 생성
# ---------------------------
if submitted:

    property_data = {
        "deal_type": deal_type,
        "area_name": area_name,
        "complex_name": complex_name,
        "price": price,
        "monthly_rent": monthly_rent,
        "area_size": area_size,
        "floor_info": floor_info,
        "direction": direction,
        "point_1": point_1,
        "point_2": point_2,
        "point_3": point_3,
        "app_url": APP_URL,
    }

    result = build_property_share_data(property_data)

    st.success("매물 홍보 문구가 자동 생성되었습니다.")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📌 카카오 공유 제목")
        st.code(result["title"])

        st.subheader("🟡 카카오 공유 설명")
        st.code(result["description"])

    with col2:

        st.subheader("📱 문자 발송 문구")
        st.code(result["sms_message"])

    st.markdown("---")

    st.subheader("📝 블로그 / 단톡방 홍보 문구")

    st.code(result["blog_text"])

    st.markdown("---")

    st.info("""
이 문구를 그대로 사용하면 됩니다.

1️⃣ 카카오톡 공유  
2️⃣ 문자 발송  
3️⃣ 블로그 / 단톡방 홍보  
4️⃣ 고객 상담 안내  

다음 단계에서는 카카오 공유 페이지와 자동 연결됩니다.
""")