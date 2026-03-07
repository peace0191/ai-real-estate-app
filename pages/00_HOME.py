import streamlit as st
import streamlit.components.v1 as components
from io import BytesIO

try:
    import qrcode
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False

# ---------------------------------
# 기본 정보
# ---------------------------------
APP_TITLE = "AI 예약 자동 매칭 챗봇 부동산플랫폼"
APP_SUBTITLE = "AI 실거래가 분석 · 사전예약 매칭 · 공동중개 네트워크 · 자동 숏츠 광고"
APP_DESC = "AI가 추천하는 프리미엄 매물과 상담 예약 서비스를 확인해보세요."
APP_URL = "https://ai5788285.streamlit.app"
APP_IMAGE = "https://ai5788285.streamlit.app/favicon.png"
KAKAO_JS_KEY = "76eaac78ebaf08220bcf6d4b83012e91"

OFFICE = "롯데타워앤강남빌딩부동산중개(주)"
TEL_MAIN = "02-578-8285"
TEL_MOBILE = "010-8985-8945"
REG_NO = "11680-2023-00078"
BIZ_NO = "461-86-02740"
ADDRESS = "서울특별시 강남구 대치동 938외1 삼환아르누보2 507호"

# ---------------------------------
# 스타일
# ---------------------------------
st.markdown("""
<style>
.home-card {
    background: #f7f9fc;
    border: 1px solid #e6ebf2;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 14px;
}
.metric-card {
    background: white;
    border: 1px solid #e6ebf2;
    border-radius: 16px;
    padding: 18px;
    text-align: center;
    min-height: 150px;
}
.kakao-box {
    background: #fff8cc;
    border: 1px solid #f0e08a;
    border-radius: 14px;
    padding: 18px;
}
.small-muted {
    color: #6b7280;
    font-size: 0.92rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------
# 헤더
# ---------------------------------
st.title("🏠 AI 예약 자동 매칭 챗봇 부동산플랫폼")
st.caption(APP_SUBTITLE)

col1, col2 = st.columns([1.6, 1])

with col1:
    st.markdown(f"""
<div class="home-card">
    <h3 style="margin-top:0;">{OFFICE}</h3>
    <p><b>대표전화</b> : {TEL_MAIN} / {TEL_MOBILE}</p>
    <p><b>등록번호</b> : {REG_NO}</p>
    <p><b>사업자등록번호</b> : {BIZ_NO}</p>
    <p><b>주소</b> : {ADDRESS}</p>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div class="home-card">
    <h4 style="margin-top:0;">📌 핵심 기능</h4>
    <p>• AI 매물 추천</p>
    <p>• 상담 예약 자동 매칭</p>
    <p>• 카카오 공유 · QR 홍보</p>
    <p>• 관리자 검수 · 운영 관리</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------
# 기능 요약
# ---------------------------------
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown("""
<div class="metric-card">
    <h3>📋</h3>
    <h4>매물 접수</h4>
    <p class="small-muted">신규 매물 등록 및 관리</p>
</div>
""", unsafe_allow_html=True)

with m2:
    st.markdown("""
<div class="metric-card">
    <h3>📊</h3>
    <h4>AI 저평가 분석</h4>
    <p class="small-muted">실거래가 · 비교 · 추천 분석</p>
</div>
""", unsafe_allow_html=True)

with m3:
    st.markdown("""
<div class="metric-card">
    <h3>🤝</h3>
    <h4>실시간 매칭</h4>
    <p class="small-muted">수요자-공급자 연결</p>
</div>
""", unsafe_allow_html=True)

with m4:
    st.markdown("""
<div class="metric-card">
    <h3>💬</h3>
    <h4>카카오 공유</h4>
    <p class="small-muted">링크 · QR · 홍보 자동화</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------
# 카카오 공유 / 링크 / QR
# ---------------------------------
st.subheader("💛 카카오 · 링크 · QR 공유")

left, right = st.columns([1.3, 1])

with left:
    st.markdown('<div class="kakao-box">', unsafe_allow_html=True)
    st.write("아래 버튼으로 플랫폼 주소를 카카오톡으로 바로 공유할 수 있습니다.")

    kakao_share_html = f"""
    <script src="https://developers.kakao.com/sdk/js/kakao.js"></script>
    <script>
    if (!window.Kakao.isInitialized()) {{
        window.Kakao.init('{KAKAO_JS_KEY}');
    }}

    function shareKakao() {{
        window.Kakao.Share.sendDefault({{
            objectType: 'feed',
            content: {{
                title: '{APP_TITLE}',
                description: '{APP_DESC}',
                imageUrl: '{APP_IMAGE}',
                link: {{
                    mobileWebUrl: '{APP_URL}',
                    webUrl: '{APP_URL}'
                }}
            }},
            buttons: [
                {{
                    title: '플랫폼 바로가기',
                    link: {{
                        mobileWebUrl: '{APP_URL}',
                        webUrl: '{APP_URL}'
                    }}
                }}
            ]
        }});
    }}
    </script>

    <button onclick="shareKakao()"
        style="
            background:#FEE500;
            color:#191919;
            border:none;
            padding:12px 18px;
            border-radius:10px;
            font-size:16px;
            font-weight:700;
            cursor:pointer;">
        💬 카카오톡 공유하기
    </button>
    """
    components.html(kakao_share_html, height=80)

    st.markdown("**🔗 플랫폼 주소**")
    st.code(APP_URL)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown("#### 📱 QR 코드")
    if QR_AVAILABLE:
        qr = qrcode.make(APP_URL)
        buf = BytesIO()
        qr.save(buf, format="PNG")
        st.image(buf.getvalue(), width=220)
    else:
        st.warning("QR 코드 라이브러리가 없어 QR을 표시하지 못했습니다.")
        st.code("pip install qrcode[pil]")

st.markdown("---")

# ---------------------------------
# 빠른 실행
# ---------------------------------
st.subheader("🚀 빠른 이용 안내")

g1, g2 = st.columns(2)

with g1:
    st.markdown("""
<div class="home-card">
    <h4 style="margin-top:0;">사용 순서</h4>
    <p>1. 매물 접수</p>
    <p>2. AI 저평가 분석</p>
    <p>3. 실시간 매칭 관리</p>
    <p>4. 관리자 검수</p>
    <p>5. 카카오 공유 및 홍보</p>
</div>
""", unsafe_allow_html=True)

with g2:
    st.markdown("""
<div class="home-card">
    <h4 style="margin-top:0;">운영 팁</h4>
    <p>• 홈 화면에서 바로 카카오 공유 가능</p>
    <p>• 실제 운영 주소와 localhost 모두 등록 완료</p>
    <p>• 카카오 로그인 리다이렉트 URI는 현재 불필요</p>
    <p>• 추후 매물 상세 페이지 공유로 확장 가능</p>
</div>
""", unsafe_allow_html=True)