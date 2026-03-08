import streamlit as st
import streamlit.components.v1 as components
import qrcode
from io import BytesIO

from services.share_message_service import build_property_share_data

# ---------------------------------
# 기본 정보
# ---------------------------------
APP_NAME = "AI 예약 자동 매칭 챗봇 부동산플랫폼"
APP_DESC = "AI 실거래가 분석 · 사전예약 매칭 · 공동중개 네트워크 · 자동 숏츠 광고"
APP_URL = "https://ai-real-estate-app-nvbi9ytwq6gh6tmztd4tpu.streamlit.app"
APP_IMAGE = "https://cdn-icons-png.flaticon.com/512/1040/1040230.png"
KAKAO_JS_KEY = "76eaac78ebaf08220bcf6d4b83012e91"

OFFICE = "롯데타워앤강남빌딩부동산중개(주)"
TEL_MAIN = "02-578-8285"
TEL_MOBILE = "010-8985-8945"

# ---------------------------------
# 스타일
# ---------------------------------
st.markdown("""
<style>
.share-card {
    background: #f7f9fc;
    border: 1px solid #e6ebf2;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 16px;
}
.yellow-card {
    background: #fff8cc;
    border: 1px solid #f0e08a;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 16px;
}
.code-title {
    font-weight: 700;
    margin-top: 10px;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------
# 페이지 헤더
# ---------------------------------
st.title("💬 카카오 공유 센터")
st.caption("플랫폼 공유 · QR 생성 · 매물 홍보 문구 자동 생성")

st.markdown("---")

# ---------------------------------
# 1) 기본 플랫폼 공유
# ---------------------------------
st.subheader("1️⃣ 기본 플랫폼 공유")

col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown('<div class="yellow-card">', unsafe_allow_html=True)
    st.write("앱 전체를 카카오톡으로 공유할 수 있습니다.")
    st.code(APP_URL)

    kakao_app_html = f"""
    <script src="https://developers.kakao.com/sdk/js/kakao.js"></script>
    <script>
    function shareKakaoApp() {{
        if (!window.Kakao) {{
            alert("카카오 SDK 로드에 실패했습니다.");
            return;
        }}

        if (!window.Kakao.isInitialized()) {{
            window.Kakao.init('{KAKAO_JS_KEY}');
        }}

        window.Kakao.Share.sendDefault({{
            objectType: 'feed',
            content: {{
                title: '{APP_NAME}',
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

    <button onclick="shareKakaoApp()"
        style="
            background:#FEE500;
            color:#191919;
            border:none;
            padding:14px 22px;
            border-radius:10px;
            font-size:17px;
            font-weight:700;
            cursor:pointer;">
        💛 플랫폼 카카오 공유
    </button>
    """
    components.html(kakao_app_html, height=90)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="share-card">', unsafe_allow_html=True)
    st.write("바로가기 버튼")
    st.link_button("🚀 앱 바로 실행하기", APP_URL)
    st.markdown("")
    st.write("대표 연락처")
    st.write(f"☎ {TEL_MAIN}")
    st.write(f"📱 {TEL_MOBILE}")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------
# 2) QR 코드 공유
# ---------------------------------
st.subheader("2️⃣ QR 코드 공유")

qr_col1, qr_col2 = st.columns([1, 1.3])

with qr_col1:
    qr = qrcode.make(APP_URL)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    st.image(buf.getvalue(), width=220)

with qr_col2:
    st.markdown('<div class="share-card">', unsafe_allow_html=True)
    st.write("QR을 스캔하면 플랫폼으로 바로 접속됩니다.")
    st.code(APP_URL)
    st.write("오픈하우스, 명함, 문자, 블로그, 전단지에 활용하기 좋습니다.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------
# 3) 매물 홍보 문구 자동 생성
# ---------------------------------
st.subheader("3️⃣ 매물 홍보 문구 자동 생성")

st.markdown('<div class="share-card">', unsafe_allow_html=True)

with st.form("property_share_form"):
    c1, c2 = st.columns(2)

    with c1:
        deal_type = st.selectbox("거래 유형", ["매매", "전세", "월세", "단기임대"])
        area_name = st.text_input("지역", "강남구 대치동")
        complex_name = st.text_input("단지명 / 건물명", "예: 개포래미안블레스티지")
        price = st.text_input("가격", "예: 29억")
        monthly_rent = st.text_input("월세", "예: 250만원 (월세 아니면 비워두기)")
        area_size = st.text_input("면적", "예: 84㎡ / 34평")

    with c2:
        floor_info = st.text_input("층 정보", "예: 15층")
        direction = st.text_input("방향", "예: 남향")
        point_1 = st.text_input("핵심 포인트 1", "예: 학군 우수")
        point_2 = st.text_input("핵심 포인트 2", "예: 역세권")
        point_3 = st.text_input("핵심 포인트 3", "예: 즉시 입주 가능")

    submitted = st.form_submit_button("홍보 문구 생성")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------
# 생성 결과
# ---------------------------------
if submitted:
    property_data = {
        "deal_type": deal_type,
        "area_name": area_name,
        "complex_name": complex_name,
        "price": price,
        "monthly_rent": monthly_rent,
        "area_size": area_size,
        "floor_info": floor_info,
        "direction": direction,
        "point_1": point_1,
        "point_2": point_2,
        "point_3": point_3,
        "app_url": APP_URL,
    }

    result = build_property_share_data(property_data)

    st.success("홍보 문구가 생성되었습니다.")

    out1, out2 = st.columns(2)

    with out1:
        st.markdown('<div class="share-card">', unsafe_allow_html=True)
        st.markdown('<div class="code-title">📌 카카오 공유 제목</div>', unsafe_allow_html=True)
        st.code(result["title"])

        st.markdown('<div class="code-title">🟡 카카오 공유 설명</div>', unsafe_allow_html=True)
        st.code(result["description"])

        st.markdown('<div class="code-title">📱 문자(SMS) 발송용 문구</div>', unsafe_allow_html=True)
        st.code(result["sms_message"])
        st.markdown('</div>', unsafe_allow_html=True)

    with out2:
        st.markdown('<div class="share-card">', unsafe_allow_html=True)
        st.markdown('<div class="code-title">📝 블로그 / 단톡방 / 문자 확장 문구</div>', unsafe_allow_html=True)
        st.code(result["blog_text"])
        st.markdown('</div>', unsafe_allow_html=True)

    # 카카오 공유용 문자열 안전 처리
    property_title = (
        result["title"]
        .replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace("\n", " ")
    )
    property_desc = (
        result["description"]
        .replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace("\n", " ")
    )

    st.subheader("4️⃣ 생성된 매물 카카오 공유")

    property_kakao_html = f"""
    <script src="https://developers.kakao.com/sdk/js/kakao.js"></script>
    <script>
    function sharePropertyKakao() {{
        if (!window.Kakao) {{
            alert("카카오 SDK 로드에 실패했습니다.");
            return;
        }}

        if (!window.Kakao.isInitialized()) {{
            window.Kakao.init('{KAKAO_JS_KEY}');
        }}

        window.Kakao.Share.sendDefault({{
            objectType: 'feed',
            content: {{
                title: '{property_title}',
                description: '{property_desc}',
                imageUrl: '{APP_IMAGE}',
                link: {{
                    mobileWebUrl: '{APP_URL}',
                    webUrl: '{APP_URL}'
                }}
            }},
            buttons: [
                {{
                    title: '매물 보러가기',
                    link: {{
                        mobileWebUrl: '{APP_URL}',
                        webUrl: '{APP_URL}'
                    }}
                }}
            ]
        }});
    }}
    </script>

    <button onclick="sharePropertyKakao()"
        style="
            background:#FEE500;
            color:#191919;
            border:none;
            padding:14px 22px;
            border-radius:10px;
            font-size:17px;
            font-weight:700;
            cursor:pointer;">
        🏠 이 매물 카카오 공유
    </button>
    """
    components.html(property_kakao_html, height=90)

    st.markdown("---")

    st.subheader("5️⃣ 활용 안내")
    st.info("""
생성된 문구 활용 방법

1. 카카오 공유 제목 / 설명 → 카카오톡 공유용
2. 문자(SMS) 문구 → 고객 직접 발송용
3. 블로그/단톡방 문구 → 단체방, 블로그, 카페 업로드용
4. 다음 단계에서는 매물접수 데이터와 자동 연결 가능
""")

else:
    st.info("""
아직 매물 홍보 문구를 생성하지 않았습니다.

위 입력란에 매물 정보를 넣고
'홍보 문구 생성' 버튼을 누르면

- 카카오 공유 제목
- 카카오 설명 문구
- 문자 발송 문구
- 블로그 / 단톡방 문구
- 매물 카카오 공유 버튼

이 자동으로 생성됩니다.
""")

st.markdown("---")

# ---------------------------------
# 향후 확장 안내
# ---------------------------------
st.subheader("6️⃣ 다음 자동화 단계")

st.markdown("""
- `01_매물접수.py` 입력값 자동 불러오기
- 매물별 전용 링크 자동 생성
- VIP 고객군별 추천 문구 자동 생성
- 블로그 / 카카오 / 숏츠 문안 동시 생성
- 매물 등록 → 자동 홍보 흐름 연결
""")