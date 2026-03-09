"""
11_고객관리.py
고객 관리 · 고객 그룹 관리 — 파발마 스타일
탭: 고객 목록 | 고객 등록 | 고객 그룹 관리 | 고객 상세 / 상담이력
"""
import streamlit as st
import pandas as pd
from datetime import datetime, date
from services.customer_store import (
    load_customers, save_customer, update_customer, delete_customer,
    load_groups, save_group, update_group, delete_group,
    refresh_group_counts, get_group_names,
)
from services.property_store import push_alert

st.set_page_config(page_title="고객관리", layout="wide")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;900&display=swap');
*, html, body { font-family: 'Noto Sans KR', sans-serif; }

.page-header {
  background: linear-gradient(135deg,#0A1F44 0%,#1E3A6E 60%,#0A1F44 100%);
  padding: 1.3rem 2rem 1.1rem; border-radius: 14px;
  border-bottom: 3px solid #D4AF37; margin-bottom: 1.3rem;
}
.page-header h2 { color:#D4AF37; margin:0; font-weight:900; font-size:1.45rem; }
.page-header p  { color:#b0c4de; margin:0.2rem 0 0; font-size:0.86rem; }

/* 파발마 툴바 */
.toolbar {
  display:flex; gap:6px; margin-bottom:0.8rem; flex-wrap:wrap;
}
.tb-btn {
  background:#0A1F44; color:#D4AF37; border:1px solid #D4AF37;
  padding:6px 14px; border-radius:6px; font-size:0.82rem;
  font-weight:700; cursor:pointer; white-space:nowrap;
}
.tb-btn:hover { background:#1E3A6E; }

/* 고객 테이블 행 */
.cust-row {
  display:grid;
  grid-template-columns: 28px 80px 90px 90px 70px 70px 110px 120px 70px 1fr;
  gap:4px; align-items:center;
  padding:5px 8px; border-bottom:1px solid #f0f0f0;
  font-size:0.83rem; background:#fff;
}
.cust-row:hover { background:#f0f4ff; }
.cust-header {
  background:#0A1F44; color:#D4AF37; font-weight:700;
  border-radius:6px 6px 0 0;
}

/* 태그 */
.grade-vvip { background:#7c3aed;color:#fff;padding:2px 8px;border-radius:4px;font-size:0.72rem; }
.grade-vip  { background:#dc2626;color:#fff;padding:2px 8px;border-radius:4px;font-size:0.72rem; }
.grade-gen  { background:#6b7280;color:#fff;padding:2px 8px;border-radius:4px;font-size:0.72rem; }
.status-진행 { background:#22c55e;color:#fff;padding:2px 8px;border-radius:4px;font-size:0.72rem; }
.status-완료 { background:#3b82f6;color:#fff;padding:2px 8px;border-radius:4px;font-size:0.72rem; }
.status-보류 { background:#f59e0b;color:#fff;padding:2px 8px;border-radius:4px;font-size:0.72rem; }

/* 그룹 카드 */
.group-card {
  border:1px solid #e2e8f0; border-radius:10px;
  padding:0.8rem 1rem; margin-bottom:0.5rem;
  background:#fff; border-left:4px solid #D4AF37;
  display:flex; justify-content:space-between; align-items:center;
}
.group-name { font-weight:700; color:#0A1F44; font-size:0.95rem; }
.group-cnt  { background:#eef2ff; color:#1d4ed8; padding:2px 10px;
              border-radius:999px; font-size:0.8rem; font-weight:700; }

/* 상세 카드 */
.detail-card {
  background:#f7f9fc; border:1px solid #dde3ef;
  border-radius:14px; padding:1.2rem 1.4rem;
}
.detail-card h4 { color:#0A1F44; margin:0 0 0.8rem; font-size:1rem; font-weight:900; }

/* 메트릭 */
[data-testid="metric-container"] { background:#eef2ff; border-radius:10px; padding:0.7rem; }

/* 입력폼 박스 */
.form-box {
  background:#f7f9fc; border:1px solid #dde3ef;
  border-radius:14px; padding:1.3rem 1.5rem; margin-bottom:1rem;
}

/* 푸터 */
.footer-box { background:#0A1F44; color:#b0c4de; border-radius:12px;
  padding:1rem 1.5rem; font-size:0.75rem; line-height:1.8;
  border-top:3px solid #D4AF37; margin-top:2rem; }
.footer-box strong { color:#D4AF37; }
</style>
""", unsafe_allow_html=True)

# ── 헤더 ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
  <h2>👥 고객 관리 · 고객 그룹 관리</h2>
  <p>파발마 스타일 고객 목록 · 등록 · 그룹 관리 · 상담이력</p>
</div>
""", unsafe_allow_html=True)

# ── 데이터 로드 ───────────────────────────────────────────────────────────────
refresh_group_counts()
customers = load_customers()
groups    = load_groups()
grp_names = get_group_names()

# ── 요약 메트릭 ───────────────────────────────────────────────────────────────
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("👥 전체 고객",  len(customers))
m2.metric("💜 VVIP",      sum(1 for c in customers if c.get("grade") == "VVIP"))
m3.metric("❤️ VIP",        sum(1 for c in customers if c.get("grade") == "VIP"))
m4.metric("🟢 진행중",     sum(1 for c in customers if c.get("status") == "진행중"))
m5.metric("🗂 그룹 수",    len(groups))

st.divider()

# ── 탭 ───────────────────────────────────────────────────────────────────────
tab_list, tab_reg, tab_group, tab_detail = st.tabs([
    "📋 고객 목록",
    "➕ 고객 등록",
    "🗂 고객그룹 관리",
    "📄 고객 상세 / 상담이력",
])


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — 고객 목록 (파발마 스타일)
# ════════════════════════════════════════════════════════════════════════════
with tab_list:
    st.markdown("#### 📋 고객 목록")

    # ── 필터 바 ─────────────────────────────────────────────────────────────
    f1, f2, f3, f4, f5, f6 = st.columns([1.5, 1.2, 1.2, 1.5, 1.5, 1])
    with f1:
        fgrp   = st.selectbox("고객그룹", ["전체"] + grp_names, key="fgrp")
    with f2:
        fsort  = st.selectbox("의뢰구분", ["전체","매도","매수","임대","임차"], key="fsort")
    with f3:
        fgrado = st.selectbox("등급", ["전체","VVIP","VIP","일반"], key="fgrado")
    with f4:
        fstat  = st.selectbox("업무상태", ["전체","진행중","완료","보류"], key="fstat")
    with f5:
        fsrch  = st.text_input("고객명/연락처 검색", placeholder="이름 또는 전화번호", key="fsrch")
    with f6:
        st.markdown("<div style='padding-top:1.6rem;'>", unsafe_allow_html=True)
        if st.button("🔍 검색", use_container_width=True, key="search_btn"):
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ── 데이터 필터링 ────────────────────────────────────────────────────────
    filtered = customers[:]
    if fgrp   != "전체": filtered = [c for c in filtered if c.get("group","")    == fgrp]
    if fsort  != "전체": filtered = [c for c in filtered if c.get("deal_type","") == fsort]
    if fgrado != "전체": filtered = [c for c in filtered if c.get("grade","")    == fgrado]
    if fstat  != "전체": filtered = [c for c in filtered if c.get("status","")   == fstat]
    if fsrch:
        filtered = [c for c in filtered
                    if fsrch in c.get("name","") or fsrch in c.get("phone","")]

    # ── 파발마 테이블 ────────────────────────────────────────────────────────
    total_label = f"총 : {len(filtered)}건"
    st.caption(total_label)

    if not filtered:
        st.info("조건에 맞는 고객이 없습니다. 등록 탭에서 고객을 추가하세요.")
    else:
        # 헤더
        st.markdown("""
        <div class="cust-row cust-header">
          <div>선택</div>
          <div>고객명</div>
          <div>고객번호</div>
          <div>연락처</div>
          <div>구분</div>
          <div>등급</div>
          <div>고객그룹</div>
          <div>선호지역</div>
          <div>업무상태</div>
          <div>등록일</div>
        </div>
        """, unsafe_allow_html=True)

        # 행 목록
        for c in filtered:
            grade = c.get("grade", "일반")
            stat  = c.get("status", "진행중")
            g_cls = "grade-vvip" if grade=="VVIP" else ("grade-vip" if grade=="VIP" else "grade-gen")
            s_cls = "status-진행" if "진행" in stat else ("status-완료" if "완료" in stat else "status-보류")
            st.markdown(f"""
            <div class="cust-row">
              <div>☐</div>
              <div><b>{c.get("name","-")}</b></div>
              <div style="color:#888;font-size:0.79rem;">{c.get("id","")}</div>
              <div>{c.get("phone","-")}</div>
              <div>{c.get("deal_type", c.get("deal_side","-"))}</div>
              <div><span class="{g_cls}">{grade}</span></div>
              <div style="font-size:0.8rem;">{c.get("group","기본그룹")}</div>
              <div style="font-size:0.8rem;">{c.get("pref_region", c.get("region","-"))}</div>
              <div><span class="{s_cls}">{stat}</span></div>
              <div style="color:#999;font-size:0.78rem;">{c.get("created_at","")[:10]}</div>
            </div>""", unsafe_allow_html=True)

    # ── 액션 버튼 바 ─────────────────────────────────────────────────────────
    st.markdown("---")
    a1, a2, a3, a4, _ = st.columns([1,1,1,1,4])
    with a1:
        if st.button("📥 CSV 내보내기", use_container_width=True):
            df = pd.DataFrame(filtered)
            csv = df.to_csv(index=False, encoding="utf-8-sig")
            st.download_button("⬇ 다운로드", csv,
                               file_name=f"고객목록_{date.today()}.csv",
                               mime="text/csv")
    with a2:
        if st.button("🔄 새로고침", use_container_width=True):
            st.rerun()
    with a3:
        st.caption(f"전체 {len(customers)}명 | 필터 {len(filtered)}명")


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — 고객 등록
# ════════════════════════════════════════════════════════════════════════════
with tab_reg:
    st.markdown("#### ➕ 신규 고객 등록")
    st.caption("고객 기본정보와 매물 조건을 입력합니다.")

    with st.form("customer_reg_form", clear_on_submit=True):
        st.markdown('<div class="form-box">', unsafe_allow_html=True)
        st.markdown("**📌 기본 정보**")

        r1c1, r1c2, r1c3 = st.columns(3)
        with r1c1:
            reg_name   = st.text_input("고객명 *", placeholder="홍길동")
            reg_phone  = st.text_input("연락처 *", placeholder="010-0000-0000")
            reg_email  = st.text_input("이메일",   placeholder="example@email.com")
        with r1c2:
            reg_grade  = st.selectbox("고객 등급", ["일반","VIP","VVIP"])
            reg_group  = st.selectbox("고객 그룹", grp_names if grp_names else ["기본그룹"])
            reg_source = st.selectbox("유입경로",
                ["직접방문","카카오톡","네이버블로그","유튜브","지인소개","전화","기타"])
        with r1c3:
            reg_deal   = st.selectbox("의뢰구분", ["매수","매도","임차","임대","기타"])
            reg_status = st.selectbox("업무상태", ["진행중","완료","보류","대기"])
            reg_date   = st.date_input("상담일자", value=date.today())

        st.markdown("**🏠 매물 조건**")
        r2c1, r2c2, r2c3 = st.columns(3)
        with r2c1:
            reg_region = st.text_input("선호 지역", placeholder="강남구 대치동, 역삼동")
            reg_ptype  = st.selectbox("매물종류", ["아파트","오피스텔","빌라","상가","토지","기타"])
        with r2c2:
            reg_bmin   = st.text_input("예산 최소(만원)", placeholder="예: 50000")
            reg_bmax   = st.text_input("예산 최대(만원)", placeholder="예: 100000")
        with r2c3:
            reg_amin   = st.text_input("면적 최소(㎡)",  placeholder="예: 60")
            reg_amax   = st.text_input("면적 최대(㎡)",  placeholder="예: 120")

        reg_memo = st.text_area("특이사항 / 메모",
                                 placeholder="학군 우선, 역세권 필수, 저층 선호 등",
                                 height=70)
        st.markdown("</div>", unsafe_allow_html=True)

        reg_submit = st.form_submit_button("💾 고객 등록", type="primary",
                                            use_container_width=True)

    if reg_submit:
        if reg_name.strip() and reg_phone.strip():
            cid = save_customer({
                "name":        reg_name,
                "phone":       reg_phone,
                "email":       reg_email,
                "grade":       reg_grade,
                "group":       reg_group,
                "source":      reg_source,
                "deal_type":   reg_deal,
                "deal_side":   reg_deal,
                "status":      reg_status,
                "consult_date":str(reg_date),
                "pref_region": reg_region,
                "region":      reg_region,
                "property_type": reg_ptype,
                "budget_min":  reg_bmin,
                "budget_max":  reg_bmax,
                "budget":      reg_bmax,
                "area_min":    reg_amin,
                "area_max":    reg_amax,
                "memo":        reg_memo,
            })
            push_alert("신규 고객 등록", f"{reg_name}({reg_phone}) [{reg_grade}] {reg_region}", "info")
            st.success(f"✅ **{reg_name}** 님이 고객 목록에 등록되었습니다! (ID: {cid})")
            st.balloons()
        else:
            st.warning("⚠️ 고객명과 연락처는 필수 입력사항입니다.")


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — 고객 그룹 관리 (파발마 고객그룹관리 팝업 스타일)
# ════════════════════════════════════════════════════════════════════════════
with tab_group:
    st.markdown("#### 🗂 고객 그룹 관리")
    st.caption("파발마 스타일의 고객 그룹(타깃 리스트)을 관리합니다.")

    # ── 그룹 추가 ────────────────────────────────────────────────────────────
    with st.expander("➕ 새 그룹 추가", expanded=True):
        with st.form("group_add_form", clear_on_submit=True):
            g1c1, g1c2 = st.columns([2, 3])
            with g1c1:
                new_grp_name = st.text_input("그룹명 *",
                                              placeholder="예: 30평대 대상 26번, 대치래미안 25평 세입자")
            with g1c2:
                new_grp_memo = st.text_input("메모",
                                              placeholder="그룹 설명 (선택)")
            g_submit = st.form_submit_button("➕ 그룹 추가", use_container_width=True)
        if g_submit:
            if new_grp_name.strip():
                gid = save_group(new_grp_name.strip(), new_grp_memo.strip())
                st.success(f"✅ 그룹 '{new_grp_name}' 추가 완료! (ID: {gid})")
                st.rerun()
            else:
                st.warning("그룹명을 입력하세요.")

    # ── 그룹 목록 ────────────────────────────────────────────────────────────
    refresh_group_counts()
    groups_now = load_groups()

    st.markdown("---")

    # 헤더 행
    gh1, gh2, gh3, gh4 = st.columns([3, 1, 1.5, 1])
    with gh1: st.markdown("**고객그룹명**")
    with gh2: st.markdown("**고객수**")
    with gh3: st.markdown("**등록일**")
    with gh4: st.markdown("**삭제**")

    for g in groups_now:
        gc1, gc2, gc3, gc4 = st.columns([3, 1, 1.5, 1])
        with gc1:
            new_name = st.text_input(
                f"그룹명_{g['id']}", value=g["name"],
                label_visibility="collapsed", key=f"gname_{g['id']}"
            )
            if new_name != g["name"]:
                update_group(g["id"], {"name": new_name})
                st.rerun()
        with gc2:
            cnt = g.get("count", 0)
            color = "#1d4ed8" if cnt > 0 else "#9ca3af"
            st.markdown(
                f'<div style="color:{color};font-weight:700;padding-top:0.5rem;">{cnt}</div>',
                unsafe_allow_html=True
            )
        with gc3:
            st.markdown(
                f'<div style="padding-top:0.5rem;font-size:0.85rem;color:#666;">{g.get("created_at","")}</div>',
                unsafe_allow_html=True
            )
        with gc4:
            if g["name"] != "기본그룹":  # 기본그룹은 삭제 불가
                if st.button("🗑", key=f"gdel_{g['id']}", help="그룹 삭제"):
                    delete_group(g["id"])
                    st.success(f"'{g['name']}' 그룹을 삭제했습니다.")
                    st.rerun()
            else:
                st.markdown('<div style="padding-top:0.4rem;color:#ccc;">잠금</div>',
                            unsafe_allow_html=True)

    st.divider()

    # ── 일괄 관리 ────────────────────────────────────────────────────────────
    st.markdown("##### 👥 고객 → 그룹 일괄 이동")
    st.caption("특정 조건의 고객을 선택한 그룹으로 이동시킵니다.")

    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        move_from = st.selectbox("현재 그룹", grp_names, key="move_from")
    with mc2:
        move_to   = st.selectbox("이동할 그룹", grp_names, key="move_to")
    with mc3:
        st.markdown("<div style='padding-top:1.6rem;'>", unsafe_allow_html=True)
        if st.button("✅ 일괄 이동", use_container_width=True, key="batch_move"):
            moved = 0
            for c in load_customers():
                if c.get("group") == move_from:
                    update_customer(c["id"], {"group": move_to})
                    moved += 1
            st.success(f"✅ {moved}명을 '{move_to}' 그룹으로 이동했습니다.")
            refresh_group_counts()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — 고객 상세 / 상담이력
# ════════════════════════════════════════════════════════════════════════════
with tab_detail:
    st.markdown("#### 📄 고객 상세 조회 · 상담이력")

    customers_now = load_customers()
    if not customers_now:
        st.info("등록된 고객이 없습니다.")
    else:
        # 고객 선택
        cust_options = {
            f"{c.get('name','-')} ({c.get('phone','-')}) [{c.get('id','')}]": c
            for c in customers_now
        }
        selected_key = st.selectbox("고객 선택", list(cust_options.keys()), key="detail_sel")
        sel_cust     = cust_options[selected_key]

        st.divider()

        d1, d2 = st.columns(2)

        # 좌측 — 기본 정보
        with d1:
            st.markdown('<div class="detail-card">', unsafe_allow_html=True)
            st.markdown("**📌 기본 정보**")

            grade = sel_cust.get("grade", "일반")
            g_cls = "grade-vvip" if grade=="VVIP" else ("grade-vip" if grade=="VIP" else "grade-gen")
            stat  = sel_cust.get("status","진행중")
            s_cls = "status-진행" if "진행" in stat else ("status-완료" if "완료" in stat else "status-보류")

            st.markdown(f"""
            <table style="width:100%;font-size:0.88rem;border-collapse:collapse;">
              <tr><td style="color:#888;padding:5px 8px;width:100px;">고객명</td>
                  <td><b>{sel_cust.get("name","-")}</b></td></tr>
              <tr><td style="color:#888;padding:5px 8px;">고객ID</td>
                  <td style="color:#999;">{sel_cust.get("id","")}</td></tr>
              <tr><td style="color:#888;padding:5px 8px;">연락처</td>
                  <td>{sel_cust.get("phone","-")}</td></tr>
              <tr><td style="color:#888;padding:5px 8px;">이메일</td>
                  <td>{sel_cust.get("email","-")}</td></tr>
              <tr><td style="color:#888;padding:5px 8px;">등급</td>
                  <td><span class="{g_cls}">{grade}</span></td></tr>
              <tr><td style="color:#888;padding:5px 8px;">그룹</td>
                  <td>{sel_cust.get("group","기본그룹")}</td></tr>
              <tr><td style="color:#888;padding:5px 8px;">유입경로</td>
                  <td>{sel_cust.get("source","직접")}</td></tr>
              <tr><td style="color:#888;padding:5px 8px;">업무상태</td>
                  <td><span class="{s_cls}">{stat}</span></td></tr>
              <tr><td style="color:#888;padding:5px 8px;">등록일</td>
                  <td>{sel_cust.get("created_at","")}</td></tr>
            </table>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # 우측 — 매물 조건
        with d2:
            st.markdown('<div class="detail-card">', unsafe_allow_html=True)
            st.markdown("**🏠 매물 조건**")
            st.markdown(f"""
            <table style="width:100%;font-size:0.88rem;border-collapse:collapse;">
              <tr><td style="color:#888;padding:5px 8px;width:100px;">의뢰구분</td>
                  <td>{sel_cust.get("deal_type", sel_cust.get("deal_side","-"))}</td></tr>
              <tr><td style="color:#888;padding:5px 8px;">선호지역</td>
                  <td>{sel_cust.get("pref_region", sel_cust.get("region","-"))}</td></tr>
              <tr><td style="color:#888;padding:5px 8px;">매물종류</td>
                  <td>{sel_cust.get("property_type","-")}</td></tr>
              <tr><td style="color:#888;padding:5px 8px;">예산(최소)</td>
                  <td>{sel_cust.get("budget_min","-")}만원</td></tr>
              <tr><td style="color:#888;padding:5px 8px;">예산(최대)</td>
                  <td>{sel_cust.get("budget_max", sel_cust.get("budget","-"))}만원</td></tr>
              <tr><td style="color:#888;padding:5px 8px;">면적(최소)</td>
                  <td>{sel_cust.get("area_min","-")}㎡</td></tr>
              <tr><td style="color:#888;padding:5px 8px;">면적(최대)</td>
                  <td>{sel_cust.get("area_max","-")}㎡</td></tr>
              <tr><td style="color:#888;padding:5px 8px;">메모</td>
                  <td style="font-size:0.83rem;">{sel_cust.get("memo","-")}</td></tr>
            </table>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # ── 상태 수정 ─────────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("**✏️ 정보 수정**")
        ec1, ec2, ec3, ec4 = st.columns(4)
        with ec1:
            new_grade  = st.selectbox("등급 변경", ["일반","VIP","VVIP"],
                                       index=["일반","VIP","VVIP"].index(sel_cust.get("grade","일반")),
                                       key="edit_grade")
        with ec2:
            new_status = st.selectbox("상태 변경", ["진행중","완료","보류","대기"],
                                       index=["진행중","완료","보류","대기"].index(sel_cust.get("status","진행중"))
                                             if sel_cust.get("status") in ["진행중","완료","보류","대기"] else 0,
                                       key="edit_status")
        with ec3:
            new_group  = st.selectbox("그룹 변경", grp_names,
                                       index=grp_names.index(sel_cust.get("group","기본그룹"))
                                             if sel_cust.get("group","기본그룹") in grp_names else 0,
                                       key="edit_group")
        with ec4:
            st.markdown("<div style='padding-top:1.6rem;'>", unsafe_allow_html=True)
            if st.button("💾 저장", use_container_width=True, key="edit_save"):
                update_customer(sel_cust["id"], {
                    "grade":  new_grade,
                    "status": new_status,
                    "group":  new_group,
                })
                st.success("✅ 고객 정보가 수정되었습니다.")
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        # ── 상담이력 등록 ─────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("**💬 상담이력 등록**")

        if "consult_history" not in st.session_state:
            st.session_state.consult_history = {}

        cid = sel_cust.get("id","")
        if cid not in st.session_state.consult_history:
            st.session_state.consult_history[cid] = []

        with st.form(f"consult_form_{cid}", clear_on_submit=True):
            cc1, cc2 = st.columns([1, 2])
            with cc1:
                c_date   = st.date_input("상담일", value=date.today())
                c_method = st.selectbox("상담방법", ["전화","방문","카카오톡","문자","이메일"])
                c_result = st.selectbox("상담결과", ["상담중","계약예정","계약완료","이탈","재연락"])
            with cc2:
                c_memo = st.text_area("상담내용 *", height=100,
                                       placeholder="상담 내용, 요구사항, 특이사항 등")
            c_submit = st.form_submit_button("📝 상담이력 저장", use_container_width=True)

        if c_submit:
            if c_memo.strip():
                st.session_state.consult_history[cid].append({
                    "date":   str(c_date),
                    "method": c_method,
                    "result": c_result,
                    "memo":   c_memo,
                    "logged": datetime.now().strftime("%Y-%m-%d %H:%M"),
                })
                push_alert("상담이력 등록",
                           f"{sel_cust.get('name','-')} | {c_method} | {c_result}", "info")
                st.success("✅ 상담이력이 저장되었습니다.")
            else:
                st.warning("상담내용을 입력해 주세요.")

        # 이력 목록
        history = st.session_state.consult_history.get(cid, [])
        if history:
            st.markdown(f"**📋 상담이력 ({len(history)}건)**")
            for h in reversed(history):
                res_color = ("#22c55e" if h["result"]=="계약완료"
                             else "#f59e0b" if h["result"]=="계약예정"
                             else "#94a3b8")
                st.markdown(f"""
                <div style="border:1px solid #e2e8f0;border-radius:8px;
                            padding:0.7rem 1rem;margin-bottom:0.4rem;
                            border-left:4px solid {res_color};background:#fff;">
                  <span style="font-weight:700;color:#0A1F44;">{h["date"]}</span>
                  &nbsp;|&nbsp; {h["method"]}
                  &nbsp;|&nbsp;
                  <span style="color:{res_color};font-weight:700;">{h["result"]}</span>
                  <span style="color:#aaa;font-size:0.78rem;float:right;">{h["logged"]}</span><br>
                  <span style="font-size:0.86rem;color:#555;">{h["memo"]}</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.caption("등록된 상담이력이 없습니다.")

        # ── 고객 삭제 ─────────────────────────────────────────────────────────
        st.markdown("---")
        with st.expander("⚠️ 고객 삭제", expanded=False):
            st.warning(f"**{sel_cust.get('name','-')}** 고객을 삭제하면 복구할 수 없습니다.")
            if st.button("🗑 고객 영구 삭제", type="primary", key="del_cust"):
                delete_customer(sel_cust["id"])
                st.success("삭제되었습니다.")
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
