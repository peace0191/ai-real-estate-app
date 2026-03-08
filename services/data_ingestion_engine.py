"""
데이터 통합 엔진
국토부 실거래가(공공API) + KB 시세 + 내부/CSV 매물 병합
"""

import os
import pandas as pd

PROPERTY_COLS = ["apt", "region", "price", "kb_price", "size",
                 "floor", "deal_type", "school_score", "demand", "development"]


def _normalize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    rename = {"name": "apt", "complex_name": "apt",
               "area_name": "region", "area": "region"}
    df = df.rename(columns=rename)
    for col in PROPERTY_COLS:
        if col not in df.columns:
            df[col] = ""
    df["price"]    = pd.to_numeric(df["price"],    errors="coerce").fillna(0)
    df["kb_price"] = pd.to_numeric(df["kb_price"], errors="coerce").fillna(df["price"])
    df["size"]     = pd.to_numeric(
        df["size"].astype(str).str.extract(r"(\d+\.?\d*)")[0], errors="coerce").fillna(0)
    df["floor"]    = pd.to_numeric(
        df["floor"].astype(str).str.extract(r"(\d+)")[0], errors="coerce").fillna(0)
    df["school_score"] = pd.to_numeric(df["school_score"], errors="coerce").fillna(7)
    df["demand"]       = pd.to_numeric(df["demand"],       errors="coerce").fillna(7)
    df["development"]  = df["development"].astype(bool)
    return df


def load_internal_properties() -> pd.DataFrame:
    data = [
        # 교육 프리미엄
        {"apt":"래미안블레스티지",        "region":"대치동",  "price":29,"kb_price":31,"size":84,"floor":15,"deal_type":"매매","school_score":10,"demand":9,"development":True},
        {"apt":"디에이치퍼스트아이파크",   "region":"개포동",  "price":31,"kb_price":33,"size":84,"floor":18,"deal_type":"매매","school_score":9, "demand":9,"development":True},
        {"apt":"역삼 레전드힐스(전세)",    "region":"역삼동",  "price":18,"kb_price":19,"size":59,"floor":8, "deal_type":"전세","school_score":8, "demand":8,"development":False},
        {"apt":"대치 삼환아르누보(월세)",  "region":"대치동",  "price":5, "kb_price":5.5,"size":84,"floor":5,"deal_type":"월세","school_score":10,"demand":9,"development":False},
        # 럭셔리 주거
        {"apt":"시그니엘 레지던스",        "region":"잠실동",  "price":70,"kb_price":75,"size":150,"floor":42,"deal_type":"매매","school_score":8,"demand":10,"development":True},
        {"apt":"한남더힐",                 "region":"한남동",  "price":85,"kb_price":90,"size":200,"floor":10,"deal_type":"매매","school_score":8,"demand":9, "development":True},
        {"apt":"아크로서울포레스트",       "region":"성수동",  "price":55,"kb_price":58,"size":114,"floor":30,"deal_type":"매매","school_score":7,"demand":9, "development":True},
        # 한강벨트 투자
        {"apt":"트리마제",                 "region":"성수동",  "price":37,"kb_price":39,"size":84,"floor":25,"deal_type":"매매","school_score":7,"demand":9,"development":True},
        {"apt":"잠실 리센츠",              "region":"잠실동",  "price":23,"kb_price":25,"size":84,"floor":12,"deal_type":"매매","school_score":8,"demand":8,"development":True},
        {"apt":"용산 파크타워",            "region":"용산동",  "price":40,"kb_price":42,"size":84,"floor":20,"deal_type":"매매","school_score":7,"demand":8,"development":True},
    ]
    return _normalize(pd.DataFrame(data))


def merge_sources(internal: pd.DataFrame, uploaded=None) -> pd.DataFrame:
    frames = [_normalize(internal)]
    if uploaded is not None and not uploaded.empty:
        frames.append(_normalize(uploaded))
    merged = pd.concat(frames, ignore_index=True)
    merged = merged.drop_duplicates(subset=["apt","region","price","deal_type"], keep="last")
    return merged
