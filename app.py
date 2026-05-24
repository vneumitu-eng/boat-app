import streamlit as st

st.title("AI競艇エンジン v7.0：判定エンジン")

# 1. データ入力（OCRと手入力の併用）
st.subheader("レース状況を入力")
is_f_held = st.checkbox("1号艇がF持ち")
is_bad_weather = st.checkbox("波高5cm以上・安定板")
display_odds = st.number_input("3連単本線オッズ", min_value=1.0, value=5.0)
total_funds = st.number_input("現在の軍資金", value=20000)

# 2. 【見フォルダ】判定
if is_f_held or is_bad_weather:
    st.error("【警告】見送り（ケン）対象です。資金を温存してください。")
else:
    st.success("【判定】検討可能。ロジックを続行します。")
    
    # 3. 資金配分計算（仮想オッズベース）
    grade = st.selectbox("開催グレード", ["SG/G1", "一般戦"])
    margin = 0.3 if grade == "SG/G1" else 0.8
    virtual_odds = display_odds - margin
    
    if virtual_odds < 4.0:
        st.warning("仮想オッズが低すぎます（勝負不可）。")
    else:
        st.write(f"計算用仮想オッズ: {virtual_odds:.2f}")
        st.write(f"推奨投資額: {int(total_funds * 0.5)}円 (総資金の50%)")
# --- 紐選定・フォーメーション自動スイッチ ---
def get_formation(is_2course_collapse):
    if is_2course_collapse:
        # 2コース自滅展開（1-34-2345）
        return ["1-3-2", "1-3-4", "1-3-5", "1-4-2", "1-4-3", "1-4-5"]
    else:
        # 通常展開（1-23-2345）
        return ["1-2-3", "1-2-4", "1-2-5", "1-3-2", "1-3-4", "1-3-5"]

# --- 悪魔の代弁者（損切可視化）---
def show_devils_advocate(total_investment):
    st.sidebar.warning("👿 悪魔の代弁者：最終確認")
    st.sidebar.write(f"もし1号艇が飛んだ場合、あなたは {total_investment}円 を失います。")
    if st.sidebar.checkbox("損害を許容し、勝負を承認する"):
        return True
    return False
