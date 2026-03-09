"""
08_VIP고객등록.py — 신규 customer_store 호환 버전
"""
import streamlit as st
from services.customer_store import save_customer, load_customers, get_group_names
import pandas as pd

st.set_page_config(page_title="VIP 고객 등록", layout="wide")
st.title("👑 VIP 고객 등록")
st.caption("VIP / VVIP 고객 정보를 빠르게 등록합니다. 전체 고객관리는 [👥 고객관리] 페이지를 이용하세요.")
st.markdown("---")

grp_names = get_group_names()

tab1, tab2 = st.tabs(["➕ 신규 VIP 등록", "📋 VIP 전체 목록"])

with tab1:
    with st.form("vip_form"):
        c1, c2 = st.columns(2)
        with c1:
            name        = st.text_input("고객명 *", "홍길동")
            phone       = st.text_input("연락처", "010-0000-0000")
            deal_type   = st.selectbox("의뢰구분", ["매수","매도","임차","임대","기타"])
            budget_min  = st.number_input("최소 예산 (억)", min_value=0.0, value=20.0, step=0.5)
            budget_max  = st.number_input("최대 예산 (억)", min_value=0.0, value=40.0, step=0.5)
        with c2:
            area_min    = st.number_input("최소 면적 (㎡)", min_value=0, value=60, step=5)
            area_max    = st.number_input("최대 면적 (㎡)", min_value=0, value=130, step=5)
            pref_region = st.text_input("선호 지역 (쉼표 구분)", "대치동, 역삼동")
            grade       = st.selectbox("고객 등급", ["VIP","VVIP","일반"])
            group       = st.selectbox("고객 그룹", grp_names if grp_names else ["기본그룹"])
            memo        = st.text_area("메모", "학군 우선, 실거주 목적", height=70)
        submitted = st.form_submit_button("💾 VIP 고객 등록", use_container_width=True)

    if submitted:
        if not name.strip():
            st.error("고객명을 입력하세요.")
        else:
            cid = save_customer({
                "name": name, "phone": phone,
                "deal_type": deal_type, "deal_side": deal_type,
                "budget_min": str(budget_min), "budget_max": str(budget_max),
                "budget": str(budget_max),
                "area_min": str(area_min), "area_max": str(area_max),
                "pref_region": pref_region, "region": pref_region,
                "grade": grade, "group": group, "memo": memo,
                "status": "진행중", "source": "직접",
            })
            st.success(f"✅ '{name}' 고객이 VIP 목록에 등록되었습니다! (ID: {cid})")
            st.balloons()

with tab2:
    customers = load_customers()
    vip_list  = [c for c in customers if c.get("grade") in ("VVIP","VIP")]
    if not vip_list:
        st.info("등록된 VIP 고객이 없습니다.")
    else:
        df = pd.DataFrame(vip_list)
        grade_filter = st.multiselect("등급 필터", ["VVIP","VIP"], default=["VVIP","VIP"])
        if "grade" in df.columns:
            df = df[df["grade"].isin(grade_filter)]
        st.dataframe(df, use_container_width=True)
        st.caption(f"총 {len(df)}명")
        st.download_button(
            "📥 CSV 다운로드", df.to_csv(index=False, encoding="utf-8-sig"),
            file_name="vip_customers.csv", mime="text/csv"
        )
