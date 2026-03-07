import streamlit as st
from services.property_store import save_property, push_alert

st.set_page_config(page_title="매물 접수", layout="wide")

# CSS
st.markdown("""
<style>
  .page-title{background:linear-gradient(135deg,#0A1F44,#1E3A6E);padding:1.5rem 2rem;border-radius:12px;
    border-bottom:3px solid #D4AF37;margin-bottom:1.5rem;}
  .page-title h2{color:#D4AF37;margin:0;font-size:1.6rem;}
  .page-title p{color:#b0c4de;margin:0.3rem 0 0;font-size:0.9rem;}
  .section-header{background:#eef2ff;border-left:4px solid #0A1F44;padding:0.7rem 1rem;
    border-radius:0 8px 8px 0;margin:1.2rem 0 0.8rem;}
  .upload-guide{background:#fffbeb;border:1px solid #fbbf24;border-radius:8px;
    padding:0.8rem 1rem;font-size:0.85rem;color:#92400e;}
  .tag-customer{display:inline-block;padding:3px 10px;border-radius:999px;
    background:#dbeafe;color:#1d4ed8;font-weight:700;font-size:0.8rem;}
  .tag-broker{display:inline-block;padding:3px 10px;border-radius:999px;
    background:#dcfce7;color:#166534;font-weight:700;font-size:0.8rem;}
  .footer-box{background:#0A1F44;color:#b0c4de;border-radius:12px;padding:1rem 1.5rem;
    font-size:0.75rem;line-height:1.8;border-top:3px solid #D4AF37;margin-top:2rem;}
  .footer-box strong{color:#D4AF37;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-title">
  <h2>🏠 매물 접수 (수요 / 공급 / 공동중개)</h2>
  <p>수요·공급·공동중개 매물을 등록합니다. 필수 사진(공간별 2장) 및 30초 이하 영상 업로드가 필요합니다.</p>
</div>
""", unsafe_allow_html=True)

# ── 1. 기본 정보 ────────────────────────────────────────────────
st.markdown('<div class="section-header"><b>① 기본 정보</b></div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    submitter_type = st.radio("접수 주체", ["고객", "중개업자"], horizontal=True)
    deal_side      = st.radio("수요 / 공급", ["수요", "공급"], horizontal=True)
    property_type  = st.selectbox("매물 유형", ["아파트", "주상복합", "오피스텔", "상가", "빌라", "기타"])

with c2:
    trade_type    = st.selectbox("거래 유형", ["매매", "전세", "월세", "단기임대"])
    region        = st.selectbox("지역", ["강남구 대치동", "강남구 개포동", "강남구 역삼동",
                                         "송파구 신천동", "성수동", "용산구 한남동", "기타"])
    address       = st.text_input("상세 주소 (단지명·동·호)")

with c3:
    client_name = st.text_input("고객명 / 접수자명")
    phone       = st.text_input("연락처")
    co_broker   = st.checkbox("공동중개 매물")

c4, c5, c6 = st.columns(3)
with c4:
    price        = st.text_input("매매가 / 보증금 (만원)")
    monthly_rent = st.text_input("월세 (만원, 해당시)")
with c5:
    area_exclusive = st.text_input("전용면적 (㎡)")
    area_supply    = st.text_input("공급면적 (㎡)")
with c6:
    floor_info = st.text_input("층수")
    room_count = st.number_input("방 수", 1, 10, 3)
    bath_count = st.number_input("욕실 수", 1, 5, 1)

verified = st.checkbox("✅ 실매물 확인 완료")

# ── 2. 공간별 사진 업로드 ──────────────────────────────────────
st.markdown('<div class="section-header"><b>② 공간별 표준 사진 업로드 (필수)</b></div>', unsafe_allow_html=True)

st.markdown("""
<div class="upload-guide">
  📸 <b>촬영 기준</b>: 각 공간은 반드시 <b>문 → 창 방향</b> 1장, <b>창 → 문 방향</b> 1장으로 최소 2장 업로드해 주세요.<br>
  밝고 흔들림 없이 촬영하며, 필수 공간 사진이 누락되면 매물 등록이 완료되지 않습니다.
</div>
""", unsafe_allow_html=True)

spaces = ["거실", "주방", "방1", "방2", "욕실", "현관", "발코니·전망"]
upload_status = {}

cols_per_row = 3
space_chunks = [spaces[i:i+cols_per_row] for i in range(0, len(spaces), cols_per_row)]

for chunk in space_chunks:
    cols = st.columns(cols_per_row)
    for idx, space in enumerate(chunk):
        with cols[idx]:
            with st.expander(f"📸 {space}", expanded=False):
                p1 = st.file_uploader(f"{space} 문→창", type=["jpg","jpeg","png"], key=f"{space}_a")
                p2 = st.file_uploader(f"{space} 창→문", type=["jpg","jpeg","png"], key=f"{space}_b")
                ok = p1 is not None and p2 is not None
                upload_status[space] = ok
                if ok:
                    st.success("완료 ✓")
                else:
                    st.warning("2장 필요")

# ── 3. 영상 업로드 ─────────────────────────────────────────────
st.markdown('<div class="section-header"><b>③ 30초 이하 매물 영상 업로드 (필수)</b></div>', unsafe_allow_html=True)

video_file    = st.file_uploader("매물 영상 (mp4/mov, 30초 이하)", type=["mp4","mov"])
video_confirm = st.checkbox("영상 길이 30초 이하 확인")

# ── 4. 접수 상태 점검 ─────────────────────────────────────────
st.markdown('<div class="section-header"><b>④ 접수 상태 자동 점검</b></div>', unsafe_allow_html=True)

missing = [s for s, ok in upload_status.items() if not ok]
if missing:
    st.error("필수 사진 누락 공간: " + ", ".join(missing))
else:
    st.success("모든 필수 공간 사진 업로드 완료 ✓")

if video_file is None:
    st.warning("매물 영상이 업로드되지 않았습니다.")
elif not video_confirm:
    st.warning("영상 길이 확인 체크가 필요합니다.")
else:
    st.success("매물 영상 업로드 완료 ✓")

can_submit = (len(missing) == 0 and video_file is not None and video_confirm
              and client_name and address)

st.divider()

budget_field = price  # 수요일 때 예산으로도 사용

if can_submit:
    if st.button("✅ 매물 접수 완료", use_container_width=True, type="primary"):
        item = {
            "submitter_type": submitter_type,
            "deal_side":      deal_side,
            "property_type":  property_type,
            "trade_type":     trade_type,
            "region":         region,
            "address":        address,
            "client_name":    client_name,
            "phone":          phone,
            "co_broker":      co_broker,
            "price":          price,
            "budget":         price,
            "monthly_rent":   monthly_rent,
            "area":           area_exclusive,
            "floor":          floor_info,
            "rooms":          room_count,
            "verified":       verified,
            "video_uploaded": True,
            "missing_spaces": [],
        }
        save_property(item)
        push_alert("신규 매물 접수",
                   f"{client_name}님 {property_type}({region}) 접수완료 — 관리자 검수 대기",
                   "info")
        st.balloons()
        st.success(f"✅ 매물 접수 완료! {client_name}님의 {region} {property_type} 매물이 등록되었습니다.")
else:
    st.button("✅ 매물 접수 완료", disabled=True, use_container_width=True)
    st.caption("필수 정보(이름·주소·사진·영상)를 모두 입력 및 업로드해야 접수가 완료됩니다.")

st.markdown("""
<div class="footer-box">
  <strong>AI 예약 자동 매칭 챗봇 부동산플랫폼</strong> | 운영: <strong>롯데타워앤강남빌딩부동산중개(주)</strong><br>
  개설등록번호 11680-2023-00078 | 사업자등록번호 461-86-02740<br>
  서울 강남구 대치동 938외1, 삼환아르누보2, 507호 | <strong>02-578-8285</strong> / 010-8985-8945
</div>
""", unsafe_allow_html=True)
