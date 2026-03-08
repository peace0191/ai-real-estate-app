import streamlit as st
from services.customer_store import save_customer, load_customers
import pandas as pd

st.title("👑 VIP 고객 등록")
st.caption("VIP 고객 정보를 등록하고 AI 매칭을 위한 조건을 저장합니다.")
st.markdown("---")

tab1, tab2 = st.tabs(["➕ 신규 등록", "📋 전체 목록"])

with tab1:
    with st.form("vip_form"):
        c1, c2 = st.columns(2)
        with c1:
            name        = st.text_input("고객명 *", "홍길동")
            phone       = st.text_input("연락처", "010-0000-0000")
            deal_type   = st.selectbox("원하는 거래 유형", ["매매","전세","월세","단기임대"])
            budget_min  = st.number_input("최소 예산 (억)", min_value=0.0, value=20.0, step=0.5)
            budget_max  = st.number_input("최대 예산 (억)", min_value=0.0, value=40.0, step=0.5)
        with c2:
            area_min    = st.number_input("최소 면적 (㎡)", min_value=0, value=60, step=5)
            area_max    = st.number_input("최대 면적 (㎡)", min_value=0, value=130, step=5)
            pref_region = st.text_input("선호 지역 (쉼표 구분)", "대치동, 역삼동")
            grade       = st.selectbox("고객 등급", ["VIP","VVIP","일반"])
            memo        = st.text_area("메모", "학군 우선, 실거주 목적", height=80)
        submitted = st.form_submit_button("💾 VIP 고객 등록", use_container_width=True)

    if submitted:
        if not name:
            st.error("고객명을 입력하세요.")
        else:
            save_customer({
                "name": name, "phone": phone,
                "deal_type": deal_type,
                "budget_min": str(budget_min), "budget_max": str(budget_max),
                "area_min": str(area_min), "area_max": str(area_max),
                "pref_region": pref_region,
                "grade": grade, "memo": memo,
            })
            st.success(f"✅ '{name}' 고객이 VIP 목록에 등록되었습니다!")
            st.balloons()

with tab2:
    customers = load_customers()
    if not customers:
        st.info("등록된 VIP 고객이 없습니다.")
    else:
        df = pd.DataFrame(customers)
        grade_filter = st.multiselect("등급 필터", ["VVIP","VIP","일반"], default=["VVIP","VIP","일반"])
        if "grade" in df.columns:
            df = df[df["grade"].isin(grade_filter)]
        st.dataframe(df, use_container_width=True)
        st.caption(f"총 {len(df)}명")
        st.download_button(
            "📥 CSV 다운로드", df.to_csv(index=False, encoding="utf-8-sig"),
            file_name="vip_customers.csv", mime="text/csv"
        )
