"""
03_실시간매칭관리.py
AI 공동매물 매칭 · 수요/공급 예약 · 공동 멤버 예약 UI
파발마 스타일 참고 — 있습니다(공급) / 구합니다(수요) / 공동중개
"""
import streamlit as st
from datetime import datetime, date
from services.property_store import (
    get_demand_items, get_supply_items, get_co_broker_items,
    get_all_properties, push_alert, add_demand, add_property,
    get_demands
)
from services.matching_service import get_matches

st.set_page_config(page_title="AI 매칭·예약 관리", layout="wide")

# ── 공통 CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;900&display=swap');
*, html, body { font-family: 'Noto Sans KR', sans-serif; }

/* 상단 헤더 */
.page-header {
  background: linear-gradient(135deg,#0A1F44 0%,#1E3A6E 60%,#0A1F44 100%);
  padding: 1.4rem 2rem 1.2rem;
  border-radius: 14px;
  border-bottom: 3px solid #D4AF37;
  margin-bottom: 1.4rem;
}
.page-header h2 { color:#D4AF37; margin:0; font-weight:900; font-size:1.55rem; }
.page-header p  { color:#b0c4de; margin:0.3rem 0 0; font-size:0.88rem; }

/* 파발마식 탭 버튼 영역 */
.pabalma-bar {
  display:flex; gap:8px; margin-bottom:1rem;
}
.btn-itda  { background:#e91e8c; color:#fff; border:none; padding:9px 22px; border-radius:8px;
             font-weight:700; font-size:0.92rem; cursor:pointer; }
.btn-guhda { background:#1565c0; color:#fff; border:none; padding:9px 22px; border-radius:8px;
             font-weight:700; font-size:0.92rem; cursor:pointer; }
.btn-joint { background:#e65100; color:#fff; border:none; padding:9px 22px; border-radius:8px;
             font-weight:700; font-size:0.92rem; cursor:pointer; }

/* 색상 태그 */
.tag-supply { display:inline-block;padding:2px 10px;border-radius:999px;
              background:#fce4ec;color:#c2185b;font-weight:700;font-size:0.76rem;margin-right:4px;}
.tag-demand { display:inline-block;padding:2px 10px;border-radius:999px;
              background:#e3f2fd;color:#1565c0;font-weight:700;font-size:0.76rem;margin-right:4px;}
.tag-joint  { display:inline-block;padding:2px 10px;border-radius:999px;
              background:#fff3e0;color:#e65100;font-weight:700;font-size:0.76rem;margin-right:4px;}
.tag-match  { display:inline-block;padding:2px 10px;border-radius:999px;
              background:#e8f5e9;color:#2e7d32;font-weight:700;font-size:0.76rem;margin-right:4px;}
.tag-res    { display:inline-block;padding:2px 10px;border-radius:999px;
              background:#ede7f6;color:#6a1b9a;font-weight:700;font-size:0.76rem;margin-right:4px;}

/* 매물 카드 */
.item-card {
  border:1px solid #e2e8f0; border-radius:12px;
  padding:0.9rem 1.1rem; margin-bottom:0.6rem;
  background:#fff; transition: box-shadow .2s;
}
.item-card:hover { box-shadow: 0 4px 18px rgba(10,31,68,.09); }

/* 있습니다 카드 */
.card-supply { border-left: 4px solid #e91e8c; }
/* 구합니다 카드 */
.card-demand { border-left: 4px solid #1565c0; }
/* 공동중개 카드 */
.card-joint  { border-left: 4px solid #e65100; }

/* 매칭 결과 카드 */
.match-card {
  border:2px solid #22c55e; border-radius:12px;
  padding:1rem 1.2rem; margin-bottom:0.8rem;
  background:#f0fdf4;
}
.score-bar-bg  { background:#e2e8f0; border-radius:8px; height:10px; margin-top:0.5rem; }
.score-bar-fill{ height:10px; border-radius:8px; }

/* 예약 폼 */
.res-form-box {
  background:#f7f9fc; border:1px solid #dde3ef;
  border-radius:14px; padding:1.4rem 1.6rem; margin-bottom:1rem;
}
.res-form-box h4 { color:#0A1F44; font-weight:900; margin:0 0 0.9rem; font-size:1.05rem; }

/* 예약 리스트 */
.res-card {
  border:1px solid #d1d5db; border-radius:10px;
  padding:0.8rem 1rem; margin-bottom:0.5rem;
  background:#fff; border-left:4px solid #7c3aed;
}

/* 메트릭 카드 */
[data-testid="metric-container"] {
  background:#eef2ff; border-radius:10px; padding:0.7rem;
}

/* 푸터 */
.footer-box {
  background:#0A1F44; color:#b0c4de;
  border-radius:12px; padding:1rem 1.5rem;
  font-size:0.75rem; line-height:1.8;
  border-top:3px solid #D4AF37; margin-top:2rem;
}
.footer-box strong { color:#D4AF37; }

/* 날짜 검색 바 */
.search-bar {
  background:#f1f5f9; border-radius:10px;
  padding:0.8rem 1rem; margin-bottom:1rem;
  display:flex; align-items:center; gap:10px;
}
</style>
""", unsafe_allow_html=True)

# ── 헤더 ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
  <h2>📊 AI 공동매물 매칭 · 수요/공급 예약 관리</h2>
  <p>
    🟥 <b>있습니다(공급)</b> &nbsp;|&nbsp;
    🟦 <b>구합니다(수요)</b> &nbsp;|&nbsp;
    🟧 <b>공동중개</b> &nbsp;|&nbsp;
    🟩 <b>AI 자동 매칭 결과</b> &nbsp;|&nbsp;
    🟪 <b>매물 예약 등록</b>
  </p>
</div>
""", unsafe_allow_html=True)

# ── 데이터 로드 ───────────────────────────────────────────────────────────────
demand_list = get_demand_items()
supply_list = get_supply_items()
co_list     = get_co_broker_items()
matches     = get_matches()

# 예약 데이터 (session_state)
if "reservations" not in st.session_state:
    st.session_state.reservations = []

# ── 요약 메트릭 ───────────────────────────────────────────────────────────────
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("🟥 있습니다(공급)",   len(supply_list))
m2.metric("🟦 구합니다(수요)",   len(demand_list))
m3.metric("🟧 공동중개",         len(co_list))
m4.metric("🤝 AI 매칭 후보",     len(matches))
m5.metric("📅 예약 접수",        len(st.session_state.reservations))

st.divider()

# ── 날짜/검색 필터 바 ─────────────────────────────────────────────────────────
with st.expander("🔍 날짜·조건 검색 필터", expanded=False):
    fb1, fb2, fb3, fb4 = st.columns(4)
    with fb1:
        fdate_s = st.date_input("조회 시작일", value=date(2026, 1, 1), key="fdate_s")
    with fb2:
        fdate_e = st.date_input("조회 종료일",  value=date.today(),     key="fdate_e")
    with fb3:
        fregion = st.selectbox("지역 필터", ["전체","강남구 대치동","강남구 개포동",
                                              "강남구 역삼동","송파구 신천동","성수동","용산구 한남동"])
    with fb4:
        ftype   = st.selectbox("유형 필터",["전체","아파트","오피스텔","빌라","상가","토지"])

# ── 메인 탭 ──────────────────────────────────────────────────────────────────
tab_supply, tab_demand, tab_joint, tab_match, tab_reserve = st.tabs([
    "🟥 있습니다(공급 파발마)",
    "🟦 구합니다(수요 파발마)",
    "🟧 공동중개 장부",
    "🤝 AI 자동 매칭 결과",
    "📅 매물 예약 등록",
])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — 있습니다 (공급 파발마)
# ════════════════════════════════════════════════════════════════════════════
with tab_supply:

    st.markdown("#### 🟥 있습니다 — 공급 매물 파발마 목록")
    st.caption("공급자가 등록한 매물을 파발마 방식으로 조회합니다.")

    # ── 간편 등록 폼 (있습니다) ────────────────────────────────────────────
    with st.expander("➕ 있습니다 매물 간편 등록", expanded=False):
        with st.form("form_supply"):
            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                s_name    = st.text_input("매물명 / 단지명", placeholder="예: 개포래미안블레스티지")
                s_type    = st.selectbox("매물종류", ["아파트","오피스텔","빌라","상가","토지","기타"])
                s_region  = st.selectbox("매물위치(시/도)", ["서울","경기","인천","부산","기타"])
                s_gu      = st.text_input("구/동", placeholder="예: 강남구 대치동")
            with sc2:
                s_trade   = st.selectbox("거래구분", ["매매","전세","월세","단기임대"])
                s_price   = st.text_input("매매가(만원)", placeholder="예: 150000")
                s_deposit = st.text_input("보증금(만원)", placeholder="전세·월세만")
                s_rent    = st.text_input("월세(만원)", placeholder="월세만")
            with sc3:
                s_area    = st.text_input("공급면적(㎡)", placeholder="예: 84")
                s_floor   = st.text_input("층수", placeholder="예: 15층")
                s_move_in = st.text_input("이사예정일", placeholder="예: 2026-05-01")
                s_memo    = st.text_area("특이사항", height=68,
                                         placeholder="금액조절 가능, 즉시입주, 역세권 등")
            s_tags = st.multiselect("매물 특징 태그",
                ["금액조절 가능한","바로 볼 수 있는","새로 지은","손님 대기중입니다",
                 "역세권에 위치한","풀 수리 깨끗한","전세대출 가능한","주차 가능한",
                 "즉시 입주 가능한","풀 옵션인"])
            s_submit = st.form_submit_button("📤 있습니다 파발마 전송", type="primary",
                                              use_container_width=True)
        if s_submit:
            if s_name.strip():
                add_property({
                    "category": "supply", "deal_side": "공급",
                    "name": s_name, "type": s_type, "region": f"{s_region} {s_gu}",
                    "trade": s_trade, "price": s_price, "deposit": s_deposit,
                    "rent": s_rent, "area": s_area, "floor": s_floor,
                    "move_in": s_move_in, "memo": s_memo, "tags": s_tags,
                    "submitter_type": "중개사"
                })
                push_alert("공급 매물 등록", f"있습니다: {s_name} / {s_gu} / {s_trade}", "success")
                st.success(f"✅ '{s_name}' 있습니다 파발마 전송 완료!")
                st.rerun()
            else:
                st.warning("매물명을 입력해 주세요.")

    # ── 있습니다 목록 ──────────────────────────────────────────────────────
    supply_now = get_supply_items()
    if not supply_now:
        st.info("공급 매물이 없습니다. 위 폼에서 '있습니다' 매물을 등록하세요.")
    else:
        for i, item in enumerate(reversed(supply_now), 1):
            tags_html = "".join(
                f'<span style="background:#fce4ec;color:#c2185b;border-radius:4px;'
                f'padding:1px 7px;font-size:0.73rem;margin-right:3px;">{t}</span>'
                for t in (item.get("tags") or [])
            )
            st.markdown(f"""
            <div class="item-card card-supply">
              <span class="tag-supply">있습니다</span>
              <span style="font-weight:700;font-size:1rem;">{item.get("name", item.get("property_name","-"))}</span>
              <span style="color:#888;font-size:0.82rem;margin-left:8px;">{item.get("created_at","")}</span><br>
              <span style="font-size:0.87rem;">
                📍 <b>{item.get("region","-")}</b> &nbsp;|&nbsp;
                🏷 {item.get("type", item.get("property_type","-"))} &nbsp;|&nbsp;
                💰 거래: {item.get("trade", item.get("trade_type","-"))} &nbsp;|&nbsp;
                매매가: <b>{item.get("price","-")}만원</b>
                {f"&nbsp;|&nbsp; 보증: {item.get('deposit','')}만원" if item.get("deposit") else ""}
                {f"&nbsp;|&nbsp; 월세: {item.get('rent','')}만원" if item.get("rent") else ""}
                &nbsp;|&nbsp; 면적: {item.get("area","-")}㎡
                {f"&nbsp;|&nbsp; {item.get('floor','')}층" if item.get("floor") else ""}
              </span><br>
              <div style="margin-top:4px;">{tags_html}</div>
              {f'<div style="font-size:0.82rem;color:#555;margin-top:3px;">📝 {item.get("memo","")}</div>' if item.get("memo") else ""}
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — 구합니다 (수요 파발마)
# ════════════════════════════════════════════════════════════════════════════
with tab_demand:

    st.markdown("#### 🟦 구합니다 — 수요 파발마 목록")
    st.caption("수요자(고객)가 구하는 매물 조건을 파발마 방식으로 조회합니다.")

    # ── 간편 등록 폼 (구합니다) ───────────────────────────────────────────
    with st.expander("➕ 구합니다 수요 간편 등록", expanded=False):
        with st.form("form_demand"):
            dc1, dc2, dc3 = st.columns(3)
            with dc1:
                d_name    = st.text_input("의뢰인 이름")
                d_phone   = st.text_input("연락처", placeholder="010-XXXX-XXXX")
                d_type    = st.selectbox("매물종류", ["아파트","오피스텔","빌라","상가","토지","기타"])
                d_region  = st.text_input("희망지역", placeholder="강남구 대치동")
            with dc2:
                d_trade   = st.selectbox("거래구분", ["매매","전세","월세","단기임대"])
                d_budget  = st.text_input("매매가 범위(만원)", placeholder="예: 80000~120000")
                d_deposit = st.text_input("보증금 범위(만원)", placeholder="전세·월세만")
                d_rent    = st.text_input("월세 범위(만원)", placeholder="월세만")
            with dc3:
                d_area_s  = st.text_input("면적 최소(㎡)", placeholder="예: 60")
                d_area_e  = st.text_input("면적 최대(㎡)", placeholder="예: 100")
                d_rooms   = st.text_input("방수", placeholder="예: 2~3")
                d_move_in = st.text_input("이사 희망일", placeholder="예: 2026-06-01")
            d_tags = st.multiselect("희망 특징",
                ["금액조절 가능한","바로 볼 수 있는","새로 지은","손님 대기중입니다",
                 "역세권에 위치한","풀 수리 깨끗한","전세대출 가능한","주차 가능한",
                 "즉시 입주 가능한","풀 옵션인"])
            d_memo   = st.text_area("추가 요청사항", height=60,
                                     placeholder="학군 우선, 역세권 필수, 저층 선호 등")
            d_submit = st.form_submit_button("📤 구합니다 파발마 전송", type="primary",
                                              use_container_width=True)
        if d_submit:
            if d_name.strip():
                add_demand({
                    "name": d_name, "phone": d_phone,
                    "type": d_type, "region": d_region,
                    "trade": d_trade, "budget": d_budget,
                    "deposit": d_deposit, "rent": d_rent,
                    "area": f"{d_area_s}~{d_area_e}", "rooms": d_rooms,
                    "move_in": d_move_in, "tags": d_tags, "memo": d_memo,
                    "submitter_type": "고객",
                    "client_name": d_name, "property_type": d_type,
                    "trade_type": d_trade,
                })
                push_alert("수요 등록", f"구합니다: {d_name} / {d_region} / {d_trade}", "info")
                st.success(f"✅ '{d_name}' 구합니다 파발마 전송 완료!")
                st.rerun()
            else:
                st.warning("의뢰인 이름을 입력해 주세요.")

    # ── 구합니다 목록 ─────────────────────────────────────────────────────
    demand_now = get_demand_items()
    if not demand_now:
        st.info("수요 의뢰가 없습니다. 위 폼에서 '구합니다' 수요를 등록하세요.")
    else:
        for item in reversed(demand_now):
            tags_html = "".join(
                f'<span style="background:#e3f2fd;color:#1565c0;border-radius:4px;'
                f'padding:1px 7px;font-size:0.73rem;margin-right:3px;">{t}</span>'
                for t in (item.get("tags") or [])
            )
            name = item.get("name", item.get("client_name", "-"))
            st.markdown(f"""
            <div class="item-card card-demand">
              <span class="tag-demand">구합니다</span>
              <b>{name}</b>
              <span style="color:#888;font-size:0.82rem;">&nbsp;{item.get("phone","")}</span>
              <span style="color:#aaa;font-size:0.78rem;margin-left:8px;">{item.get("created_at","")}</span><br>
              <span style="font-size:0.87rem;">
                📍 <b>{item.get("region","-")}</b> &nbsp;|&nbsp;
                🏷 {item.get("type", item.get("property_type","-"))} &nbsp;|&nbsp;
                💰 {item.get("trade", item.get("trade_type","-"))} &nbsp;|&nbsp;
                예산: <b>{item.get("budget","-")}만원</b>
                {f"&nbsp;|&nbsp; 보증: {item.get('deposit','')}만원" if item.get("deposit") else ""}
                {f"&nbsp;|&nbsp; 월세: {item.get('rent','')}만원" if item.get("rent") else ""}
                &nbsp;|&nbsp; 면적: {item.get("area","-")}㎡
              </span><br>
              <div style="margin-top:4px;">{tags_html}</div>
              {f'<div style="font-size:0.82rem;color:#555;margin-top:3px;">📝 {item.get("memo","")}</div>' if item.get("memo") else ""}
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — 공동중개 장부
# ════════════════════════════════════════════════════════════════════════════
with tab_joint:

    st.markdown("#### 🟧 공동중개 — 공동매물 파발마 장부")
    st.caption("공동중개 등록 매물을 조회하고 새로 등록합니다.")

    with st.expander("➕ 공동중개 매물 등록", expanded=False):
        with st.form("form_joint"):
            jc1, jc2 = st.columns(2)
            with jc1:
                j_name    = st.text_input("매물명", placeholder="예: 대치동 시세대비 저평가 아파트")
                j_type    = st.selectbox("매물종류", ["아파트","오피스텔","빌라","상가","토지","기타"])
                j_region  = st.text_input("위치", placeholder="예: 강남구 대치동 개포래미안")
                j_trade   = st.selectbox("거래구분", ["매매","전세","월세"])
            with jc2:
                j_price   = st.text_input("가격(만원)")
                j_area    = st.text_input("면적(㎡)")
                j_contact = st.text_input("담당 중개사 연락처")
                j_share   = st.selectbox("수수료 분배", ["50:50","40:60","60:40","협의"])
            j_memo = st.text_area("협력 요청 사항", height=60,
                                   placeholder="공동중개 조건, 특이사항 등")
            j_submit = st.form_submit_button("📤 공동중개 파발마 전송", type="primary",
                                              use_container_width=True)
        if j_submit:
            if j_name.strip():
                add_property({
                    "category": "joint", "co_broker": True,
                    "name": j_name, "type": j_type, "region": j_region,
                    "trade": j_trade, "price": j_price, "area": j_area,
                    "contact": j_contact, "fee_share": j_share, "memo": j_memo,
                    "submitter_type": "공동중개"
                })
                push_alert("공동중개 등록", f"{j_name} / {j_region} / {j_trade}", "success")
                st.success(f"✅ '{j_name}' 공동중개 등록 완료!")
                st.rerun()
            else:
                st.warning("매물명을 입력해 주세요.")

    co_now = get_co_broker_items()
    if not co_now:
        st.info("공동중개 매물이 없습니다.")
    else:
        for item in reversed(co_now):
            st.markdown(f"""
            <div class="item-card card-joint">
              <span class="tag-joint">공동중개</span>
              <b>{item.get("name", item.get("property_name", "-"))}</b>
              <span style="color:#aaa;font-size:0.78rem;margin-left:8px;">{item.get("created_at","")}</span><br>
              <span style="font-size:0.87rem;">
                📍 <b>{item.get("region","-")}</b> &nbsp;|&nbsp;
                🏷 {item.get("type", item.get("property_type","-"))} &nbsp;|&nbsp;
                💰 {item.get("trade", item.get("trade_type","-"))} &nbsp;|&nbsp;
                가격: <b>{item.get("price","-")}만원</b> &nbsp;|&nbsp;
                면적: {item.get("area","-")}㎡
                {f"&nbsp;|&nbsp; 수수료: {item.get('fee_share','')}" if item.get("fee_share") else ""}
              </span>
              {f'<div style="font-size:0.82rem;color:#555;margin-top:3px;">📝 {item.get("memo","")}</div>' if item.get("memo") else ""}
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — AI 자동 매칭 결과
# ════════════════════════════════════════════════════════════════════════════
with tab_match:

    st.markdown("#### 🤝 AI 자동 매칭 결과")
    st.caption("수요↔공급·공동중개 매물을 AI가 자동 점수화하여 최적 매물을 실시간 매칭합니다.")

    min_score = st.slider("최소 매칭 점수 필터", 0, 100, 50, 5, key="minscore")

    matches_filtered = [m for m in matches if m.get("score", 0) >= min_score]

    if not matches_filtered:
        st.info("현재 조건에 맞는 매칭 후보가 없습니다. 수요·공급 매물을 더 등록하거나 최소 점수를 낮춰보세요.")
    else:
        st.success(f"🔴 **{len(matches_filtered)}건**의 매칭 후보가 있습니다.")
        for idx, m in enumerate(matches_filtered):
            sc   = m.get("score", 0)
            col  = "#22c55e" if sc >= 80 else ("#f59e0b" if sc >= 65 else "#94a3b8")
            grad = "#22c55e" if sc >= 80 else ("#f59e0b" if sc >= 65 else "#94a3b8")
            grade_label = m.get("grade", "")

            cl, cr = st.columns([4, 1])
            with cl:
                st.markdown(f"""
                <div class="match-card">
                  <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                      <span class="tag-demand">수요자</span>
                      <b>{m.get("demand_name","-")}</b>
                      <span style="color:#888;font-size:0.82rem;">{m.get("demand_phone","")}</span>
                    </div>
                    <div style="font-size:1.3rem;">⇄</div>
                    <div>
                      <span class="tag-supply">공급매물</span>
                      <b>{m.get("supply_name","-")}</b>
                    </div>
                  </div>
                  <div style="font-size:0.86rem;margin-top:0.5rem;color:#374151;">
                    📍 {m.get("region","-")} &nbsp;|&nbsp;
                    🏷 {m.get("type","-")} &nbsp;|&nbsp;
                    💰 {m.get("trade","-")} &nbsp;|&nbsp;
                    가격: {m.get("price","-")}만원 &nbsp;|&nbsp;
                    면적: {m.get("area","-")}㎡
                  </div>
                  <div class="score-bar-bg">
                    <div class="score-bar-fill" style="width:{sc}%;background:{grad};"></div>
                  </div>
                  <div style="font-size:0.82rem;color:#555;margin-top:3px;">
                    매칭 점수: <b style="color:{col};">{sc}점</b> &nbsp;
                    <span style="background:#f0fdf4;border:1px solid {col};color:{col};
                                 padding:1px 8px;border-radius:6px;font-size:0.78rem;">{grade_label}</span>
                  </div>
                </div>""", unsafe_allow_html=True)
            with cr:
                st.metric("매칭", f"{sc}%")
                if st.button("📣 알림 등록", key=f"alert_{idx}"):
                    push_alert("고확률 매칭",
                               f"{m.get('demand_name','-')} ↔ {m.get('supply_name','-')} | {sc}%",
                               "success")
                    st.success("알림 등록!")
                if st.button("📅 예약 전환", key=f"res_{idx}"):
                    st.session_state.reservations.append({
                        "type": "매칭예약",
                        "client": m.get("demand_name", "-"),
                        "phone":  m.get("demand_phone", "-"),
                        "property": m.get("supply_name", "-"),
                        "region": m.get("region", "-"),
                        "trade":  m.get("trade", "-"),
                        "price":  m.get("price", "-"),
                        "score":  sc,
                        "date":   datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "status": "예약대기",
                    })
                    st.success("📅 예약 탭에 등록됨!")


# ════════════════════════════════════════════════════════════════════════════
# TAB 5 — 매물 예약 등록 (수요자·공급자·공동중개 멤버 예약 UI)
# ════════════════════════════════════════════════════════════════════════════
with tab_reserve:

    st.markdown("#### 📅 매물 예약 등록 — 수요자·공급자·공동중개 멤버")
    st.caption("고객이 직접 예약하거나 매칭 탭에서 '예약 전환' 버튼으로 자동 등록됩니다.")

    # 상단 — 예약 유형 선택
    rv_type = st.radio(
        "예약 구분",
        ["🔵 수요자 (구하는 분)", "🟢 공급자 (있습니다)", "🟠 공동중개 멤버"],
        horizontal=True, key="rv_type"
    )

    with st.container():
        st.markdown('<div class="res-form-box">', unsafe_allow_html=True)

        rb1, rb2 = st.columns(2)
        with rb1:
            rv_name   = st.text_input("예약자 이름 *", key="rv_name")
            rv_phone  = st.text_input("연락처 *",     key="rv_phone",
                                       placeholder="010-XXXX-XXXX")
            rv_date   = st.date_input("상담 희망일 *", key="rv_date")
            rv_time   = st.selectbox("희망 시간 *",
                ["09:00","10:00","11:00","13:00","14:00","15:00","16:00","17:00","18:00"],
                key="rv_time")
        with rb2:
            rv_region = st.selectbox("희망 지역", [
                "강남구 대치동","강남구 개포동","강남구 역삼동","강남구 논현동",
                "송파구 신천동","송파구 잠실동","성수동","용산구 한남동","기타"
            ], key="rv_region")
            rv_ptype  = st.selectbox("매물종류",
                ["아파트","오피스텔","빌라","상가","토지","기타"], key="rv_ptype")
            rv_trade  = st.selectbox("거래구분",
                ["매매","전세","월세","단기임대"], key="rv_trade")
            rv_budget = st.text_input("예산 / 매매가(만원)", key="rv_budget",
                                       placeholder="예: 80000")

        rv_memo = st.text_area("요청사항 / 특이사항", key="rv_memo",
                                placeholder="학군 우선, 역세권, 즉시입주, 공동중개 조건 등",
                                height=70)

        if st.button("✅ 예약 등록 완료", type="primary", use_container_width=True, key="rv_submit"):
            if rv_name.strip() and rv_phone.strip():
                new_res = {
                    "type":     rv_type.split()[1],
                    "client":   rv_name,
                    "phone":    rv_phone,
                    "date":     str(rv_date),
                    "time":     rv_time,
                    "region":   rv_region,
                    "ptype":    rv_ptype,
                    "trade":    rv_trade,
                    "budget":   rv_budget,
                    "memo":     rv_memo,
                    "status":   "예약대기",
                    "created":  datetime.now().strftime("%Y-%m-%d %H:%M"),
                }
                st.session_state.reservations.append(new_res)
                push_alert("신규 예약",
                           f"{rv_name}({rv_phone}) | {rv_date} {rv_time} | {rv_region} {rv_trade}",
                           "success")
                st.balloons()
                st.success(
                    f"✅ **{rv_name}** 님의 예약이 완료되었습니다!\n"
                    f"📅 {rv_date} {rv_time} | 담당자가 연락드리겠습니다."
                )
            else:
                st.warning("⚠️ 이름과 연락처는 필수 입력사항입니다.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ── 예약 목록 ─────────────────────────────────────────────────────────
    st.divider()
    st.markdown("#### 📋 예약 접수 목록")

    reservations = st.session_state.reservations
    if not reservations:
        st.info("접수된 예약이 없습니다. 위 폼에서 예약하거나 [AI 매칭] 탭에서 '예약 전환'하세요.")
    else:
        # 상태별 집계
        rm1, rm2, rm3 = st.columns(3)
        rm1.metric("📋 전체 예약",  len(reservations))
        rm2.metric("⏳ 예약대기",   sum(1 for r in reservations if r.get("status")=="예약대기"))
        rm3.metric("✅ 상담완료",    sum(1 for r in reservations if r.get("status")=="상담완료"))

        for ridx, res in enumerate(reversed(reservations)):
            rtype = res.get("type", "")
            if "수요자" in rtype or "수요" in rtype:
                tag_cls="tag-demand"
            elif "공급자" in rtype or "공급" in rtype:
                tag_cls="tag-supply"
            elif "공동" in rtype:
                tag_cls="tag-joint"
            else:
                tag_cls="tag-match"

            status_color = "#22c55e" if res.get("status") == "상담완료" else "#f59e0b"
            st.markdown(f"""
            <div class="res-card">
              <span class="{tag_cls}">{res.get("type","-")}</span>
              <span class="tag-res" style="font-size:0.73rem;background:#ede7f6;color:#6a1b9a;">
                {res.get("status","예약대기")}
              </span>
              <b style="margin-left:6px;">{res.get("client","-")}</b>
              <span style="color:#888;font-size:0.82rem;"> {res.get("phone","")}</span>
              <span style="color:#aaa;font-size:0.75rem;float:right;">{res.get("created","")}</span><br>
              <span style="font-size:0.85rem;">
                📅 <b>{res.get("date","-")} {res.get("time","")}</b> &nbsp;|&nbsp;
                📍 {res.get("region","-")} &nbsp;|&nbsp;
                🏷 {res.get("ptype", res.get("property",""))} &nbsp;|&nbsp;
                💰 {res.get("trade","-")} {res.get("budget","")}
                {f"만원" if res.get("budget") else ""}
              </span>
              {f'<div style="font-size:0.81rem;color:#555;margin-top:2px;">📝 {res.get("memo","")}</div>' if res.get("memo") else ""}
            </div>""", unsafe_allow_html=True)

            # 상태 변경 버튼
            rc1, rc2, rc3, _ = st.columns([1,1,1,3])
            actual_idx = len(reservations) - 1 - ridx
            with rc1:
                if st.button("✅ 상담완료", key=f"rc_done_{ridx}"):
                    st.session_state.reservations[actual_idx]["status"] = "상담완료"
                    st.rerun()
            with rc2:
                if st.button("❌ 취소", key=f"rc_cancel_{ridx}"):
                    st.session_state.reservations[actual_idx]["status"] = "취소됨"
                    st.rerun()
            with rc3:
                if st.button("🗑 삭제", key=f"rc_del_{ridx}"):
                    st.session_state.reservations.pop(actual_idx)
                    st.rerun()

# ── 푸터 ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-box">
  <strong>AI 예약 자동 매칭 챗봇 부동산플랫폼</strong> |
  운영: <strong>롯데타워앤강남빌딩부동산중개(주)</strong><br>
  개설등록번호 11680-2023-00078 | 사업자등록번호 461-86-02740<br>
  서울 강남구 대치동 938외1, 삼환아르누보2, 507호 |
  <strong>02-578-8285</strong> / 010-8985-8945
</div>
""", unsafe_allow_html=True)
