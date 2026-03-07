import streamlit as st
from services.property_store import get_all_properties, save_reviewed_item, push_alert, get_shorts_candidates

st.set_page_config(page_title="관리자 검수", layout="wide")

st.markdown("""
<style>
  .page-title{background:linear-gradient(135deg,#0A1F44,#1E3A6E);padding:1.5rem 2rem;
    border-radius:12px;border-bottom:3px solid #D4AF37;margin-bottom:1.5rem;}
  .page-title h2{color:#D4AF37;margin:0;} .page-title p{color:#b0c4de;margin:0.3rem 0 0;}
  .biz-card{background:#0A1F44;color:#D4AF37;border-radius:10px;padding:1rem 1.5rem;
    font-size:0.82rem;line-height:1.9;margin-bottom:1.5rem;}
  .footer-box{background:#0A1F44;color:#b0c4de;border-radius:12px;padding:1rem 1.5rem;
    font-size:0.75rem;line-height:1.8;border-top:3px solid #D4AF37;margin-top:2rem;}
  .footer-box strong{color:#D4AF37;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-title">
  <h2>🛡 관리자 매물 검수창</h2>
  <p>필수 사진·영상 확인, 광고 가능 여부 및 숏츠 제작 대상을 관리합니다.</p>
</div>
""", unsafe_allow_html=True)

# 운영사 정보 카드
st.markdown("""
<div class="biz-card">
  🏢 <b>운영사 정보</b><br>
  롯데타워앤강남빌딩부동산중개(주) &nbsp;|&nbsp; 개설등록번호 11680-2023-00078 &nbsp;|&nbsp;
  사업자등록번호 461-86-02740<br>
  서울특별시 강남구 대치동 938외1, 삼환아르누보2, 507호 &nbsp;|&nbsp;
  대표전화 02-578-8285 &nbsp;/&nbsp; 010-8985-8945
</div>
""", unsafe_allow_html=True)

items      = get_all_properties()
shorts_cands = get_shorts_candidates()

tab1, tab2 = st.tabs(["📋 매물 검수 목록", "🎬 숏츠 제작 대상"])

with tab1:
    if not items:
        st.info("접수된 매물이 없습니다.")
    else:
        st.caption(f"총 {len(items)}건 매물 접수됨")
        for idx, item in enumerate(items):
            with st.expander(
                f"#{idx+1}  {item.get('client_name','-')} | {item.get('region','-')} "
                f"{item.get('property_type','-')} | {item.get('trade_type','-')} | {item.get('price','-')}만원",
                expanded=False
            ):
                cl, cr = st.columns([3, 2])
                with cl:
                    st.write(f"**접수주체**: {item.get('submitter_type','-')} &nbsp;|&nbsp; **수요/공급**: {item.get('deal_side','-')}")
                    st.write(f"**주소**: {item.get('address','-')}")
                    st.write(f"**면적**: {item.get('area','-')}㎡ &nbsp;|&nbsp; **층**: {item.get('floor','-')}")
                    st.write(f"**공동중개**: {'예' if item.get('co_broker') else '아니오'} &nbsp;|&nbsp; **실매물 확인**: {'완료' if item.get('verified') else '미확인'}")
                    if item.get("missing_spaces"):
                        st.error("필수 사진 누락: " + ", ".join(item["missing_spaces"]))
                    else:
                        st.success("필수 공간 사진 충족 ✓")
                    if item.get("video_uploaded"):
                        st.success("영상 업로드 완료 ✓")
                    else:
                        st.warning("영상 미업로드")

                with cr:
                    status = st.selectbox("검수 상태", ["검수대기","보완요청","검수완료","광고가능"],
                                          key=f"st_{idx}")
                    underval = st.checkbox("저평가 추천 후보", key=f"uv_{idx}")
                    shorts   = st.checkbox("숏츠 제작 가능",   key=f"sh_{idx}",
                                           value=item.get("video_uploaded", False))
                    memo = st.text_area("관리자 메모", key=f"memo_{idx}", height=80)

                    if st.button("💾 검수 저장", key=f"save_{idx}", use_container_width=True):
                        rev = item.copy()
                        rev.update({"review_status": status, "undervalued_candidate": underval,
                                    "shorts_ready": shorts, "admin_memo": memo})
                        save_reviewed_item(rev)
                        level = "success" if status == "광고가능" else ("warning" if status == "보완요청" else "info")
                        push_alert(f"검수: {status}", f"{item.get('client_name','-')} — {status}", level)
                        st.success("저장 완료!")

with tab2:
    if not shorts_cands:
        st.info("아직 숏츠 제작 후보가 없습니다. [AI 저평가 분석] 탭에서 등록하세요.")
    else:
        st.caption(f"숏츠 제작 후보 {len(shorts_cands)}건")
        for sc in shorts_cands:
            rate  = sc.get("undervalue_rate", 0)
            label = sc.get("label", "")
            color = "#f97316" if rate >= 10 else "#22c55e"
            st.markdown(f"""
            <div style="border:2px solid {color};border-radius:12px;padding:1rem;margin-bottom:0.8rem;
                 background:{'#fff7ed' if rate>=10 else '#f0fdf4'}">
              <b>{sc.get("name","-")}</b> &nbsp;
              <span style="color:{color};font-weight:700">{label} | 저평가율 {rate:.1f}%</span><br>
              <span style="font-size:0.88rem">
                지역: {sc.get("region","-")} | 유형: {sc.get("property_type","-")} |
                매물가: {sc.get("listing_price",0):,}만원 | AI기준가: {sc.get("ai_ref_price",0):,}만원
              </span>
            </div>""", unsafe_allow_html=True)

st.markdown("""
<div class="footer-box">
  <strong>AI 예약 자동 매칭 챗봇 부동산플랫폼</strong> | 운영: <strong>롯데타워앤강남빌딩부동산중개(주)</strong><br>
  개설등록번호 11680-2023-00078 | 사업자등록번호 461-86-02740<br>
  서울 강남구 대치동 938외1, 삼환아르누보2, 507호 | <strong>02-578-8285</strong> / 010-8985-8945
</div>
""", unsafe_allow_html=True)
