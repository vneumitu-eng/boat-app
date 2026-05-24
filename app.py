import streamlit as st
import pytesseract
from PIL import Image
import re
import numpy as np

st.title("🤖 AI競艇エンジン v8.2【自動買い目提案版】")

uploaded_file = st.file_uploader("直前情報のスクショをアップロード", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="解析画像", use_container_width=True)
    
    if st.button("買い目を解析・生成"):
        text = pytesseract.image_to_string(image, config='--psm 6')
        
        # タイムを抽出（展示タイムは枠番の並び順で取得）
        # 枠番 1〜6 に対応するタイムを見つけるロジック
        times = re.findall(r'[67]\.\d{2}', text)
        times = [float(t) for t in times]
        
        if len(times) >= 6:
            # 1枠から6枠までのタイムリスト
            boat_times = times[:6]
            best_idx = np.argmin(boat_times) + 1 # 最速の艇番号
            best_val = min(boat_times)
            
            st.success(f"最速艇: {best_idx}号艇 ({best_val}秒)")
            
            # 買い目ロジック
            st.subheader("💡 推奨買い目")
            if best_idx == 1:
                st.write(f"**【イン鉄板】** 1-23-全")
            elif best_idx == 2:
                st.write(f"**【2号艇強襲】** 2-13-1345")
            else:
                st.write(f"**【波乱期待】** {best_idx}-1-全, {best_idx}-{best_idx+1}-1")
                
            st.info("※これは展示データのみに基づいた機械的な推奨です。オッズを確認して勝負してください！")
        else:
            st.error("6艇分のタイムが読み取れませんでした。画像を切り抜いて再度お試しください。")
