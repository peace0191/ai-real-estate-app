import streamlit as st

def send_vip_alert(vip_list, location, price):

    for vip in vip_list:

import streamlit as st

def send_vip_alert(vip_list, location, price):

    for vip in vip_list:

        name = vip.get("name", "VIP고객")

        message = f"""
🔥 강남 저평가 매물 발견

지역: {location}
가격: {price}

AI 강남부동산 플랫폼에서 확인하세요
"""

        st.success(f"📩 {name} VIP 고객에게 알림 전송")
        message = f"""
🔥 강남 저평가 매물 발견

지역: {location}
가격: {price}

AI 강남부동산 플랫폼에서 확인하세요
"""

        st.success(f"📩 {name} VIP 고객에게 알림 전송")