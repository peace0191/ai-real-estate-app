import streamlit as st
import pandas as pd
from services.customer_store import load_customers
from services.data_ingestion_engine import load_internal_properties
from services.vip_match_engine import match_vip_customer
from services.ai_score_engine import calculate_ai_score

st.title("🤖 VIP 자동 매칭")
st.caption("등록된 VIP 고객과 AI 분석 매물을 자동으로 매칭합니다.")
st.markdown("---")

customers = load_customers()
df_props  = load_internal_properties()

if not customers:
    st.warning("등록된 VIP 고객이 없습니다. 먼저 'VIP 고객 등록' 메뉴에서 고객을 등록하세요.")
    st.stop()

customer_names = [f"{c.get('name','')} ({c.get('grade','일반')})" for c in customers]
sel_idx = st.selectbox("매칭할 VIP 고객 선택", range(len(customer_names)), format_func=lambda i: customer_names[i])
customer = customers[sel_idx]

st.markdown(f"""
| 항목 | 내용 |
|------|------|
| 고객명 | {customer.get('name','')} |
| 등급 | {customer.get('grade','')} |
| 거래 유형 | {customer.get('deal_type','')} |
| 예산 | {customer.get('budget_min','')}~{customer.get('budget_max','')}억 |
| 면적 | {customer.get('area_min','')}~{customer.get('area_max','')}㎡ |
| 선호 지역 | {customer.get('pref_region','')} |
""")

if st.button("🤖 AI 자동 매칭 시작", use_container_width=True, type="primary"):
    customer_dict = {
        "name":       customer.get("name",""),
        "deal_type":  customer.get("deal_type","매매"),
        "budget_min": float(customer.get("budget_min", 0)),
        "budget_max": float(customer.get("budget_max", 99)),
        "area_min":   float(customer.get("area_min", 0)),
        "area_max":   float(customer.get("area_max", 999)),
        "pref_region": [r.strip() for r in customer.get("pref_region","").split(",") if r.strip()],
    }

    matches = match_vip_customer(customer_dict, df_props.to_dict("records"))

    if not matches:
        st.warning("조건에 맞는 매물이 없습니다.")
    else:
        st.success(f"✅ {len(matches)}건 매칭 완료!")
        for m in matches[:8]:
            mscore = m.get("match_score", 0)
            ai     = calculate_ai_score(m)
            with st.expander(f"🏠 [매칭 {mscore}점 | AI {ai['ai_score']}점] {m.get('complex_name','')} {m.get('deal_type','')} {m.get('price','')}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**지역**: {m.get('area_name','')}")
                    st.write(f"**면적**: {m.get('area_size','')}")
                    st.write(f"**층**: {m.get('floor_info','')}")
                    st.write(f"**방향**: {m.get('direction','')}")
                with c2:
                    st.metric("매칭 점수", f"{mscore}점")
                    st.metric("AI 저평가 점수", f"{ai['ai_score']}점 ({ai['grade']})")
                    st.write(f"**포인트**: {m.get('point_1','')} / {m.get('point_2','')}")

                # 카카오 공유 링크
                title = f"{m.get('complex_name','')} {m.get('deal_type','')} {m.get('price','')}"
                desc  = f"{m.get('area_size','')} | {m.get('point_1','')} | {m.get('point_2','')}"
                st.link_button("📤 카카오 공유", f"06_카카오공유센터?title={title}&desc={desc}")
