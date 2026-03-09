import streamlit as st
import pandas as pd

# 🔴 추가된 코드 (AI 매칭 기능)
from services.ai_engine.price_ai import detect_undervalued
from services.vip_match_engine import match_vip_customer
from services.notification_service import send_vip_alert
from services.customer_store import load_customers

st.set_page_config(
    page_title="AI 예약 자동 매칭 챗봇 부동산플랫폼",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)import streamlit as st
import pandas as pd

# 🔴 추가된 코드 (AI 매칭 기능)
from services.ai_engine.price_ai import detect_undervalued
from services.vip_match_engine import match_vip_customer
from services.notification_service import send_vip_alert
from services.customer_store import load_customers

st.set_page_config(
    page_title="AI 예약 자동 매칭 챗봇 부동산플랫폼",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 전역 CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;900&display=swap');
  html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }

  /* 사이드바 */
  [data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0A1F44 0%,#1E2F5B 100%);
  }
  [data-testid="stSidebar"] * { color: #f8f8f8 !important; }

  /* 카카오 로그인 전체 오버레이 */
  .login-overlay {
    position: fixed; top:0; left:0; width:100%; height:100%;
    background: linear-gradient(135deg,#0A1F44 0%,#1a2f6b 50%,#0A1F44 100%);
    z-index: 9999;
    display: flex; align-items: center; justify-content: center;
  }
  .login-card {
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(18px);
    border: 1px solid rgba(212,175,55,0.35);
    border-radius: 24px;
    padding: 3rem 3.5rem;
    max-width: 440px; width: 100%;
    box-shadow: 0 24px 64px rgba(0,0,0,0.5);
    text-align: center;
  }
  .login-logo { font-size:3.2rem; margin-bottom:0.4rem; }
  .login-title { color:#D4AF37; font-weight:900; font-size:1.55rem; margin:0; }
  .login-sub   { color:#b0c4de; font-size:0.88rem; margin:0.4rem 0 1.8rem; }
  .kakao-btn {
    display:block; width:100%;
    background:#FEE500; color:#191919;
    border: none; border-radius: 12px;
    padding: 14px 0; font-size: 1.05rem;
    font-weight: 800; cursor: pointer;
    transition: all 0.2s;
    text-decoration: none;
  }
  .kakao-btn:hover { background:#f0d800; box-shadow: 0 4px 18px rgba(254,229,0,0.4); }
  .divider-line { color:#4a6080; font-size:0.8rem; margin:1rem 0; }
  .guest-btn {
    display:block; width:100%;
    background:transparent;
    color:#b0c4de;
    border: 1px solid #3a5080;
    border-radius: 12px;
    padding: 11px 0;
    font-size: 0.92rem; font-weight: 600;
    cursor: pointer; margin-top: 0.6rem;
    transition: all 0.2s;
  }
  .guest-btn:hover { background:rgba(176,196,222,0.1); }
  .login-footer-note {
    color: #607090; font-size:0.75rem; margin-top:1.5rem; line-height:1.6;
  }

  /* 메인 헤더 */
  .main-header {
    background: linear-gradient(135deg,#0A1F44 0%,#1E3A6E 60%,#0A1F44 100%);
    padding: 1.8rem 2.5rem 1.4rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    border: 1px solid #D4AF37;
  }
  .main-header h1 { color:#D4AF37; font-weight:900; font-size:1.75rem; margin:0; }
  .main-header p  { color:#b0c4de; margin:0.3rem 0 0; font-size:0.92rem; }

  /* 유저 배지 */
  .user-badge {
    display:inline-flex; align-items:center; gap:8px;
    background: rgba(212,175,55,0.15);
    border: 1px solid rgba(212,175,55,0.4);
    border-radius: 999px;
    padding: 5px 14px;
    font-size: 0.85rem; color:#D4AF37;
  }

  /* 카드 */
  .info-card {
    background:#f7f9fc; border:1px solid #dde3ef;
    border-radius:12px; padding:1.2rem 1.5rem; margin-bottom:1rem;
    transition: box-shadow .2s;
  }
  .info-card:hover { box-shadow: 0 4px 18px rgba(10,31,68,.09); }
  .info-card h3 { color:#0A1F44; margin:0 0 0.5rem; font-size:1rem; }
  .info-card p  { font-size:0.86rem; color:#555; margin:0; }

  /* 메트릭 */
  [data-testid="metric-container"] { background:#eef2ff; border-radius:10px; padding:0.8rem; }

  /* 골드 라인 */
  .gold-line { border:none; border-top:2px solid #D4AF37; margin:1rem 0; }

  /* 푸터 */
  .footer-box {
    background:#0A1F44; color:#b0c4de;
    border-radius:12px; padding:1.5rem 2rem;
    font-size:0.78rem; line-height:1.8;
    border-top:3px solid #D4AF37; margin-top:3rem;
  }
  .footer-box strong { color:#D4AF37; }
</style>
""", unsafe_allow_html=True)

# ── 세션 초기화 ───────────────────────────────────────────────────────────────
if "logged_in"   not in st.session_state:
    st.session_state.logged_in = False
if "user_name"   not in st.session_state:
    st.session_state.user_name = ""
if "user_type"   not in st.session_state:
    st.session_state.user_type = ""  # "kakao" | "guest" | "admin"

# ════════════════════════════════════════════════════════════════════════════
# 🔐  로그인 화면
# ════════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:

    # 배경색 덮기
    st.markdown("""
    <style>
      [data-testid="stAppViewContainer"] > .main { background: #0A1F44; }
      [data-testid="stSidebar"] { display: none !important; }
      header[data-testid="stHeader"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    # 가운데 로그인 카드
    _, center, _ = st.columns([1, 1.4, 1])
    with center:
        st.markdown("""
        <div style="text-align:center; padding-top:4rem;">
          <div style="font-size:3.5rem;">🏠</div>
          <div style="color:#D4AF37; font-weight:900; font-size:1.7rem; margin:0.2rem 0;">
            AI 부동산 플랫폼
          </div>
          <div style="color:#b0c4de; font-size:0.9rem; margin-bottom:2.5rem;">
            롯데타워앤강남빌딩부동산중개(주)<br>
            AI 실거래가 분석 · 매칭 · 공동중개 네트워크
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── 카카오 로그인 버튼 ────────────────────────────────────────────
        st.markdown("""
        <div style="
          background:rgba(255,255,255,0.06);
          backdrop-filter:blur(16px);
          border:1px solid rgba(212,175,55,0.3);
          border-radius:22px;
          padding:2.2rem 2.5rem 2rem;
          box-shadow:0 20px 60px rgba(0,0,0,0.45);
        ">
          <div style="color:#e2e8f0;font-size:0.95rem;font-weight:600;
                      text-align:center;margin-bottom:1.4rem;">
            로그인하여 서비스를 이용하세요
          </div>
        </div>
        """, unsafe_allow_html=True)

        # 이름 입력 (카카오 OAuth 대신 시뮬레이션)
        login_name = st.text_input(
            "이름 / 닉네임",
            placeholder="예: 홍길동 (공인중개사)",
            label_visibility="collapsed"
        )

        # 카카오 로그인 버튼
        if st.button(
            "💛  카카오톡으로 로그인",
            type="primary",
            use_container_width=True,
            key="kakao_login_btn"
        ):
            name = login_name.strip() or "카카오 사용자"
            st.session_state.logged_in = True
            st.session_state.user_name = name
            st.session_state.user_type = "kakao"
            st.rerun()

        st.markdown(
            '<div style="color:#4a6080;text-align:center;font-size:0.8rem;margin:0.8rem 0;">또는</div>',
            unsafe_allow_html=True
        )

        col_g, col_a = st.columns(2)
        with col_g:
            if st.button("👤 게스트 입장", use_container_width=True, key="guest_btn"):
                st.session_state.logged_in = True
                st.session_state.user_name = "게스트"
                st.session_state.user_type = "guest"
                st.rerun()
        with col_a:
            admin_pw = st.text_input("관리자 PW", type="password",
                                      label_visibility="collapsed",
                                      placeholder="관리자 비밀번호")
            if st.button("🔑 관리자", use_container_width=True, key="admin_btn"):
                if admin_pw == "lotte2025":
                    st.session_state.logged_in = True
                    st.session_state.user_name = "관리자"
                    st.session_state.user_type = "admin"
                    st.rerun()
                else:
                    st.error("비밀번호가 올바르지 않습니다.")

        st.markdown("""
        <div style="color:#506070;font-size:0.73rem;text-align:center;margin-top:1.4rem;line-height:1.7;">
          카카오 로그인은 카카오 계정 연동 개발 키가 필요합니다.<br>
          현재는 이름 입력 후 간편 입장으로 운영됩니다.<br>
          ☎ 02-578-8285 &nbsp;|&nbsp; 서울 강남구 대치동 삼환아르누보2 507호
        </div>
        """, unsafe_allow_html=True)

    st.stop()   # 로그인 전까지 메인화면 렌더 중단


# ════════════════════════════════════════════════════════════════════════════
# 🏠  메인 대시보드 (로그인 후)
# ════════════════════════════════════════════════════════════════════════════
from services.property_store import get_all_properties, get_demands
from services.matching_service import get_matches
from services.customer_store import load_customers

all_props   = get_all_properties()
demand_list = get_demands()
supply_list = [p for p in all_props if p.get("category") == "supply"]
co_broker   = [p for p in all_props if p.get("category") == "joint"]
matches     = get_matches()
customers   = load_customers()

# ── 헤더 + 유저 정보 ─────────────────────────────────────────────────────────
utype_icon = {"kakao": "💛", "admin": "🔑", "guest": "👤"}.get(
    st.session_state.user_type, "👤"
)
utype_label = {"kakao": "카카오 로그인", "admin": "관리자", "guest": "게스트"}.get(
    st.session_state.user_type, ""
)

col_hdr, col_user = st.columns([5, 1])
with col_hdr:
    st.markdown("""
    <div class="main-header">
      <h1>🏠 AI 예약 자동 매칭 챗봇 부동산플랫폼</h1>
      <p>AI 실거래가 분석 · 사전예약 매칭 · 공동중개 네트워크 · 자동 숏츠 광고</p>
    </div>
    """, unsafe_allow_html=True)
with col_user:
    st.markdown(f"""
    <div style="padding-top:1.2rem;">
      <div class="user-badge">
        {utype_icon} {st.session_state.user_name}
        <span style="font-size:0.72rem;opacity:.7;">({utype_label})</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("로그아웃", key="logout_main"):
        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.session_state.user_type = ""
        st.rerun()

# ── 요약 메트릭 ───────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("📋 총 매물",    len(all_props))
c2.metric("🔵 수요",       len(demand_list))
c3.metric("🟢 공급",       len(supply_list))
c4.metric("🟠 공동중개",   len(co_broker))
c5.metric("🤝 매칭 후보",  len(matches))
c6.metric("👥 고객",       len(customers))

st.markdown('<hr class="gold-line">', unsafe_allow_html=True)

# ── 메뉴 카드  ────────────────────────────────────────────────────────────────
col_a, col_b, col_c, col_d, col_e, col_f = st.columns(6)

menu_items = [
    ("🏠", "매물 접수",    "수요·공급·공동중개<br>매물을 등록합니다.",     col_a),
    ("📊", "AI 저평가 분석", "국토부 실거래가·KB시세<br>저평가 매물 탐지", col_b),
    ("🤝", "AI 자동 매칭",  "수요↔공급 AI 점수화<br>실시간 매칭",          col_c),
    ("👥", "고객 관리",     "고객 정보·그룹관리<br>상담이력 관리",          col_d),
    ("🎬", "숏츠 광고",     "저평가 매물을 유튜브<br>숏츠로 자동 제작",     col_e),
    ("💬", "AI 챗봇",      "24시간 고객 상담<br>예약 자동화",               col_f),
]

for icon, title, desc, col in menu_items:
    with col:
        st.markdown(f"""
        <div class="info-card" style="text-align:center;min-height:110px;">
          <div style="font-size:1.8rem;">{icon}</div>
          <h3 style="font-size:0.9rem;margin:0.3rem 0 0.2rem;">{title}</h3>
          <p style="font-size:0.78rem;">{desc}</p>
        </div>""", unsafe_allow_html=True)

# ── 실시간 AI 매칭 미리보기 ───────────────────────────────────────────────────
if matches:
    st.subheader("🔴 실시간 AI 매칭 상위 후보")
    for m in matches[:3]:
        sc = m.get("score", 0)
        grade_color = "#22c55e" if sc >= 80 else ("#f59e0b" if sc >= 65 else "#94a3b8")
        st.markdown(f"""
        <div style="background:#f0fdf4;border:1.5px solid {grade_color};border-radius:10px;
                    padding:0.7rem 1rem;margin-bottom:0.5rem;">
          🤝 <b>{m.get("demand_name","-")}</b>
          ↔ <b>{m.get("supply_name","-")}</b> &nbsp;|&nbsp;
          {m.get("region","")} / {m.get("type","")} / {m.get("trade","")} &nbsp;|&nbsp;
          매칭 <b style="color:{grade_color};">{sc}%</b>
          &nbsp;<span style="color:{grade_color};font-size:0.8rem;">{m.get("grade","")}</span>
        </div>""", unsafe_allow_html=True)

# ── 카카오 공유 / 앱 링크 ─────────────────────────────────────────────────────
APP_URL = "https://ai-real-estate-app-nvbi9ytwq6gh6tmztd4tpu.streamlit.app"

with st.expander("💛 카카오톡 공유 & 앱 링크", expanded=False):
    st.markdown(f"""
    <div style="background:#fff8cc;border:1px solid #f0e08a;border-radius:12px;padding:1rem 1.2rem;">
      <b>📱 고객에게 공유할 앱 링크</b><br>
      <code style="font-size:0.9rem;">{APP_URL}</code><br><br>
      <span style="font-size:0.85rem;color:#666;">
        카카오톡 채팅창 → 링크 붙여넣기 → 고객이 바로 실행 가능
      </span>
    </div>
    """, unsafe_allow_html=True)
    st.code(APP_URL)

# ── 푸터 ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-box">
  <strong>AI 예약 자동 매칭 챗봇 부동산플랫폼</strong><br>
  운영: <strong>롯데타워앤강남빌딩부동산중개(주)</strong><br>
  개설등록번호 11680-2023-00078 &nbsp;|&nbsp; 사업자등록번호 461-86-02740<br>
  서울특별시 강남구 대치동 938외1, 삼환아르누보2, 507호<br>
  대표전화 <strong>02-578-8285</strong> &nbsp;|&nbsp; 휴대전화 <strong>010-8985-8945</strong>
</div>
""", unsafe_allow_html=True)
