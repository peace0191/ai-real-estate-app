import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="카카오톡 공유", layout="centered")

APP_URL = "https://ai-real-estate-app-nvbi9ytwq6gh6tmztd4tpu.streamlit.app"

# CSS
st.markdown("""
<style>
  [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0A1F44 0%, #1E3A6E 50%, #0d2856 100%) !important;
  }
  [data-testid="stSidebar"] { background: linear-gradient(180deg,#0A1F44,#1E2F5B); }
  [data-testid="stSidebar"] * { color: #f8f8f8 !important; }
</style>
""", unsafe_allow_html=True)

# 카카오 공유 HTML 컴포넌트
html_code = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap" rel="stylesheet">
  <style>
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{
      font-family: 'Noto Sans KR', sans-serif;
      background: transparent;
      padding: 0;
    }}
    .card {{
      background: rgba(255,255,255,0.97);
      border-radius: 24px;
      overflow: hidden;
      box-shadow: 0 20px 60px rgba(0,0,0,0.3);
      max-width: 480px;
      margin: 0 auto;
    }}
    .header {{
      background: linear-gradient(135deg, #0A1F44, #1E3A6E);
      padding: 28px 24px 20px;
      border-bottom: 3px solid #D4AF37;
      text-align: center;
    }}
    .header .logo {{ font-size: 2.5rem; margin-bottom: 6px; }}
    .header h1 {{ color: #D4AF37; font-size: 1.15rem; font-weight: 900; line-height: 1.4; margin-bottom: 5px; }}
    .header p {{ color: #b0c4de; font-size: 0.78rem; }}
    .badge-row {{ display:flex; gap:6px; justify-content:center; margin-top:12px; flex-wrap:wrap; }}
    .badge {{
      background: rgba(212,175,55,0.15);
      border: 1px solid #D4AF37;
      color: #D4AF37;
      padding: 3px 10px;
      border-radius: 999px;
      font-size: 0.7rem;
      font-weight: 700;
    }}
    .body {{ padding: 24px; }}
    .sec-title {{ font-size:0.72rem; font-weight:700; color:#888; letter-spacing:1px; text-transform:uppercase; margin-bottom:10px; }}
    .link-box {{
      background: #f0f4ff;
      border: 2px solid #c7d4f5;
      border-radius: 10px;
      padding: 12px 14px;
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 16px;
    }}
    .link-text {{ flex:1; font-size:0.72rem; color:#1d3a8a; word-break:break-all; font-weight:600; }}
    .copy-btn {{
      background: #0A1F44; color: white; border: none;
      padding: 7px 12px; border-radius: 7px; cursor: pointer;
      font-size: 0.7rem; font-weight: 700; white-space: nowrap;
      transition: background 0.2s;
    }}
    .copy-btn:hover {{ background: #1E3A6E; }}
    .copy-btn.done {{ background: #22c55e; }}
    .btn {{
      display: flex; align-items: center; justify-content: center;
      gap: 10px; width: 100%; padding: 14px;
      border-radius: 12px; border: none; cursor: pointer;
      font-family: 'Noto Sans KR', sans-serif;
      font-size: 0.95rem; font-weight: 700;
      transition: transform 0.15s, box-shadow 0.15s;
      text-decoration: none;
      margin-bottom: 10px;
    }}
    .btn:active {{ transform: scale(0.97); }}
    .btn-kakao {{ background: #FEE500; color: #3C1E1E; box-shadow: 0 4px 14px rgba(254,229,0,0.4); }}
    .btn-kakao:hover {{ box-shadow: 0 6px 22px rgba(254,229,0,0.6); transform:translateY(-1px); }}
    .btn-open {{
      background: linear-gradient(135deg, #0A1F44, #1E3A6E); color: white;
      box-shadow: 0 4px 14px rgba(10,31,68,0.3);
    }}
    .btn-open:hover {{ box-shadow: 0 6px 22px rgba(10,31,68,0.5); transform:translateY(-1px); }}
    .btn-sms {{
      background: #f0fdf4; color: #166534;
      border: 2px solid #bbf7d0; box-shadow: none;
    }}
    .btn-sms:hover {{ background: #dcfce7; }}
    .divider {{ border:none; border-top:1px solid #e8edf5; margin:18px 0; }}
    .features {{ display:grid; grid-template-columns:1fr 1fr; gap:7px; margin-bottom:18px; }}
    .feat {{
      background: #f8fafc; border: 1px solid #e2e8f0;
      border-radius: 9px; padding: 9px 11px;
      font-size: 0.76rem; color: #334155;
    }}
    .feat .ic {{ font-size:1rem; display:block; margin-bottom:2px; }}
    .qr-section {{ text-align: center; }}
    #qrcode {{
      display: inline-block; padding:14px;
      background: white; border: 2px solid #dde3ef;
      border-radius: 14px; margin: 10px auto;
      box-shadow: 0 4px 12px rgba(0,0,0,0.07);
    }}
    .qr-cap {{ font-size:0.72rem; color:#888; margin-top:6px; }}
    .co-info {{
      background: #0A1F44; color: #b0c4de;
      border-radius: 11px; padding: 13px 15px;
      font-size: 0.72rem; line-height: 1.9; margin-top:4px;
    }}
    .co-info strong {{ color: #D4AF37; }}
    .toast {{
      position: fixed; bottom:24px; left:50%;
      transform: translateX(-50%) translateY(70px);
      background: #1e293b; color: white;
      padding: 10px 22px; border-radius: 999px;
      font-size: 0.82rem; font-weight: 700;
      box-shadow: 0 8px 24px rgba(0,0,0,0.3);
      transition: transform 0.3s ease; z-index: 999;
      white-space: nowrap;
    }}
    .toast.show {{ transform: translateX(-50%) translateY(0); }}
  </style>
</head>
<body>
<div class="card">
  <div class="header">
    <div class="logo">🏠</div>
    <h1>AI 예약 자동 매칭 챗봇<br>부동산플랫폼</h1>
    <p>롯데타워앤강남빌딩부동산중개(주)</p>
    <div class="badge-row">
      <span class="badge">AI 매칭</span>
      <span class="badge">저평가 분석</span>
      <span class="badge">24시간 챗봇</span>
      <span class="badge">숏츠 광고</span>
    </div>
  </div>
  <div class="body">
    <div class="sec-title">🔗 앱 링크</div>
    <div class="link-box">
      <div class="link-text">{APP_URL}</div>
      <button class="copy-btn" id="cpBtn" onclick="doCopy()">복사</button>
    </div>

    <button class="btn btn-kakao" onclick="shareKakao()">
      💬&nbsp; 카카오톡으로 공유하기
    </button>
    <a class="btn btn-open" href="{APP_URL}" target="_blank">
      ▶&nbsp; 앱 바로 실행하기
    </a>
    <a class="btn btn-sms"
       href="sms:?body=AI 부동산 플랫폼 바로 실행 → {APP_URL}">
      📱&nbsp; 문자(SMS)로 공유하기
    </a>

    <hr class="divider">

    <div class="sec-title">📋 주요 기능</div>
    <div class="features">
      <div class="feat"><span class="ic">🏠</span>매물 접수</div>
      <div class="feat"><span class="ic">📊</span>AI 저평가 분석</div>
      <div class="feat"><span class="ic">🤝</span>AI 자동 매칭</div>
      <div class="feat"><span class="ic">🎬</span>숏츠 광고</div>
      <div class="feat"><span class="ic">🤖</span>AI 챗봇 상담</div>
      <div class="feat"><span class="ic">🔔</span>알림 관리</div>
    </div>

    <hr class="divider">

    <div class="qr-section">
      <div class="sec-title">📷 QR 코드</div>
      <div id="qrcode"></div>
      <p class="qr-cap">📸 카메라로 스캔하면 앱이 바로 열립니다</p>
    </div>

    <hr class="divider">

    <div class="co-info">
      🏢 <strong>롯데타워앤강남빌딩부동산중개(주)</strong><br>
      개설등록번호: 11680-2023-00078 | 사업자등록번호: 461-86-02740<br>
      서울 강남구 대치동 938외1, 삼환아르누보2, 507호<br>
      ☎ <strong>02-578-8285</strong> &nbsp;/&nbsp; 📱 <strong>010-8985-8945</strong>
    </div>
  </div>
</div>

<div class="toast" id="toast">✅ 복사되었습니다!</div>

<script>
const URL = "{APP_URL}";

// QR 코드 생성
new QRCode(document.getElementById("qrcode"), {{
  text: URL, width: 150, height: 150,
  colorDark: "#0A1F44", colorLight: "#ffffff",
  correctLevel: QRCode.CorrectLevel.H
}});

// 링크 복사
function doClick(text,toastMsg={{}}){{}};
function doClick(){{}}
function doCopy() {{
  navigator.clipboard.writeText(URL).then(() => {{
    const b = document.getElementById("cpBtn");
    b.textContent = "✓ 복사됨"; b.classList.add("done");
    showToast("✅ 링크가 복사되었습니다!");
    setTimeout(() => {{ b.textContent="복사"; b.classList.remove("done"); }}, 2500);
  }}).catch(() => {{
    const t = document.createElement("textarea");
    t.value = URL; document.body.appendChild(t);
    t.select(); document.execCommand("copy");
    document.body.removeChild(t);
    showToast("✅ 링크가 복사되었습니다!");
  }});
}}

function showToast(msg) {{
  const t = document.getElementById("toast");
  t.textContent = msg; t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 2500);
}}

// 카카오톡 공유
function shareKakao() {{
  const ua = navigator.userAgent;
  const isMobile = /Android|iPhone|iPad|iPod/i.test(ua);
  const msg = "🏠 AI 부동산 플랫폼\\n\\n▶ 바로 실행하기:\\n" + URL +
              "\\n\\n롯데타워앤강남빌딩부동산중개(주)\\n☎ 02-578-8285";

  if (isMobile) {{
    // 모바일: 카카오톡 앱 스킴으로 직접 오픈
    window.location.href = "kakaotalk://msg/send?text=" + encodeURIComponent(msg);
    setTimeout(() => {{
      if (!document.hidden) openKakaoWeb(msg);
    }}, 1800);
  }} else {{
    openKakaoWeb(msg);
  }}
}}

function openKakaoWeb(msg) {{
  // PC: 카카오톡 웹 공유 또는 클립보드 복사 안내
  const encoded = encodeURIComponent(msg || URL);
  showToast("💬 카카오톡을 열고 링크를 붙여넣기 하세요!");
  navigator.clipboard.writeText(URL).catch(()={{}});
}}
</script>
</body>
</html>
"""

# Streamlit 컴포넌트로 렌더링
components.html(html_code, height=1000, scrolling=False)
