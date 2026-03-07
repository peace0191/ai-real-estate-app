import streamlit as st
from services.property_store import (
    get_demand_items, get_supply_items, get_co_broker_items, push_alert
)
from services.matching_service import build_matches

st.set_page_config(page_title="실시간 매칭관리", layout="wide")

st.markdown("""
<style>
  .page-title{background:linear-gradient(135deg,#0A1F44,#1E3A6E);padding:1.5rem 2rem;
    border-radius:12px;border-bottom:3px solid #D4AF37;margin-bottom:1.5rem;}
  .page-title h2{color:#D4AF37;margin:0;} .page-title p{color:#b0c4de;margin:0.3rem 0 0;font-size:0.9rem;}
  .tag-c{display:inline-block;padding:3px 10px;border-radius:999px;
    background:#dbeafe;color:#1d4ed8;font-weight:700;font-size:0.78rem;margin-right:4px;}
  .tag-b{display:inline-block;padding:3px 10px;border-radius:999px;
    background:#dcfce7;color:#166534;font-weight:700;font-size:0.78rem;margin-right:4px;}
  .tag-d{display:inline-block;padding:3px 10px;border-radius:999px;
    background:#fef3c7;color:#92400e;font-weight:700;font-size:0.78rem;margin-right:4px;}
  .tag-s{display:inline-block;padding:3px 10px;border-radius:999px;
    background:#ede9fe;color:#6d28d9;font-weight:700;font-size:0.78rem;margin-right:4px;}
  .tag-co{display:inline-block;padding:3px 10px;border-radius:999px;
    background:#fee2e2;color:#b91c1c;font-weight:700;font-size:0.78rem;margin-right:4px;}
  .item-card{border:1px solid #e2e8f0;border-radius:12px;padding:1rem 1.2rem;margin-bottom:0.7rem;}
  .match-card{border:2px solid #22c55e;border-radius:12px;padding:1rem 1.2rem;margin-bottom:0.8rem;background:#f0fdf4;}
  .footer-box{background:#0A1F44;color:#b0c4de;border-radius:12px;padding:1rem 1.5rem;
    font-size:0.75rem;line-height:1.8;border-top:3px solid #D4AF37;margin-top:2rem;}
  .footer-box strong{color:#D4AF37;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-title">
  <h2>📊 실시간 매물 매칭관리 창</h2>
  <p>수요↔공급 AI 자동 매칭 · 공동중개 장부 · 색상별 가독성 매물 관리</p>
</div>
""", unsafe_allow_html=True)

demand  = get_demand_items()
supply  = get_supply_items()
co      = get_co_broker_items()
matches = build_matches(demand, supply)

# 요약 메트릭
m1, m2, m3, m4 = st.columns(4)
m1.metric("🔵 수요 접수", len(demand))
m2.metric("🟢 공급 접수", len(supply))
m3.metric("🟠 공동중개", len(co))
m4.metric("🤝 매칭 후보", len(matches))

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(["🔵 수요 장부", "🟢 공급 장부", "🟠 공동중개 장부", "🤝 실시간 매칭 결과"])

# ── 수요 장부 ──────────────────────────────────────────────────
with tab1:
    if not demand:
        st.info("수요 접수 내역이 없습니다. [매물 접수] 페이지에서 수요를 등록하세요.")
    for item in demand:
        sub = "tag-c" if item.get("submitter_type") == "고객" else "tag-b"
        st.markdown(f"""
        <div class="item-card">
          <span class="{sub}">{item.get("submitter_type","-")}</span>
          <span class="tag-d">수요</span>
          <b>{item.get("client_name","-")}</b>
          <span style="color:#888;font-size:0.85rem"> | {item.get("phone","-")}</span><br>
          <span style="font-size:0.88rem">
            지역: <b>{item.get("region","-")}</b> &nbsp;|&nbsp;
            유형: {item.get("property_type","-")} &nbsp;|&nbsp;
            거래: {item.get("trade_type","-")} &nbsp;|&nbsp;
            예산: <b>{item.get("budget","-")}만원</b> &nbsp;|&nbsp;
            면적: {item.get("area","-")}㎡
          </span>
        </div>""", unsafe_allow_html=True)

# ── 공급 장부 ──────────────────────────────────────────────────
with tab2:
    if not supply:
        st.info("공급 접수 내역이 없습니다. [매물 접수] 페이지에서 공급을 등록하세요.")
    for item in supply:
        sub = "tag-c" if item.get("submitter_type") == "고객" else "tag-b"
        st.markdown(f"""
        <div class="item-card">
          <span class="{sub}">{item.get("submitter_type","-")}</span>
          <span class="tag-s">공급</span>
          <b>{item.get("property_name", item.get("client_name", "-"))}</b><br>
          <span style="font-size:0.88rem">
            지역: <b>{item.get("region","-")}</b> &nbsp;|&nbsp;
            유형: {item.get("property_type","-")} &nbsp;|&nbsp;
            거래: {item.get("trade_type","-")} &nbsp;|&nbsp;
            가격: <b>{item.get("price","-")}만원</b> &nbsp;|&nbsp;
            면적: {item.get("area","-")}㎡
          </span>
        </div>""", unsafe_allow_html=True)

# ── 공동중개 장부 ─────────────────────────────────────────────
with tab3:
    if not co:
        st.info("공동중개 매물이 없습니다.")
    for item in co:
        st.markdown(f"""
        <div class="item-card" style="border-left:4px solid #f97316;">
          <span class="tag-co">공동중개</span>
          <b>{item.get("property_name", item.get("client_name", "-"))}</b><br>
          <span style="font-size:0.88rem">
            지역: {item.get("region","-")} |
            거래: {item.get("trade_type","-")} |
            가격: {item.get("price","-")}만원 |
            접수: {item.get("submitter_type","-")}
          </span>
        </div>""", unsafe_allow_html=True)

# ── 실시간 매칭 결과 ──────────────────────────────────────────
with tab4:
    if not matches:
        st.info("현재 매칭 가능한 후보가 없습니다. 수요·공급 매물을 더 등록하세요.")
    for idx, m in enumerate(matches):
        score = m["score"]
        bar_color = "#22c55e" if score >= 80 else ("#f59e0b" if score >= 65 else "#94a3b8")
        c_l, c_r = st.columns([4, 1])
        with c_l:
            st.markdown(f"""
            <div class="match-card">
              <b>🔵 수요자:</b> {m["demand_name"]} &nbsp;&nbsp;
              <b>🟢 공급매물:</b> {m["supply_name"]}<br>
              <span style="font-size:0.88rem">
                지역: {m["region"]} | 유형: {m["property_type"]} |
                거래: {m["trade_type"]} | 가격: {m["price"]}만원
              </span><br>
              <div style="margin-top:0.5rem;background:#e2e8f0;border-radius:8px;height:12px;">
                <div style="width:{score}%;background:{bar_color};border-radius:8px;height:12px;"></div>
              </div>
            </div>""", unsafe_allow_html=True)
        with c_r:
            st.metric("매칭", f"{score}%")
            if st.button("📣 알림 등록", key=f"alert_{idx}"):
                push_alert("고확률 매칭 발생",
                           f"{m['demand_name']} ↔ {m['supply_name']} | 매칭비율 {score}%",
                           "success")
                st.success("알림 등록됨!")

st.markdown("""
<div class="footer-box">
  <strong>AI 예약 자동 매칭 챗봇 부동산플랫폼</strong> | 운영: <strong>롯데타워앤강남빌딩부동산중개(주)</strong><br>
  개설등록번호 11680-2023-00078 | 사업자등록번호 461-86-02740<br>
  서울 강남구 대치동 938외1, 삼환아르누보2, 507호 | <strong>02-578-8285</strong> / 010-8985-8945
</div>
""", unsafe_allow_html=True)
