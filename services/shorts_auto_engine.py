import json
from datetime import datetime


def generate_shorts_script(property_data):

    area = property_data.get("area_name", "")
    complex_name = property_data.get("complex_name", "")
    price = property_data.get("price", "")
    size = property_data.get("area_size", "")
    p1 = property_data.get("point_1", "")
    p2 = property_data.get("point_2", "")
    p3 = property_data.get("point_3", "")

    title = f"{area} {complex_name} 저평가 매물 발견"

    script = f"""
강남 저평가 매물 발견

위치: {area}
단지: {complex_name}
가격: {price}
면적: {size}

✔ {p1}
✔ {p2}
✔ {p3}

AI 강남부동산 플랫폼
"""

    return {
        "title": title,
        "script": script,
        "created": datetime.now().isoformat()
    }


def save_shorts_candidate(data):

    file_path = "data/shorts_candidates.json"

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            old = json.load(f)
    except:
        old = []

    old.append(data)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(old, f, ensure_ascii=False, indent=2)