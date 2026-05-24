import streamlit as st
from PIL import Image
import pytesseract
import cv2
import numpy as np
import re

st.title("AI競艇エンジン v7.0")

# --- 1. スクショ入力エリア ---
uploaded_file = st.file_uploader("レース直前情報のスクショをアップロード", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="解析中...", use_column_width=True)
    
    # --- 2. 解析と判定の自動実行 ---
    if st.button("AI解析・判定を実行"):
        with st.spinner('解析中...'):
            img_array = np.array(image.convert('RGB'))
            height, width, _ = img_array.shape
            
            # OCR解析
            crop_img = img_array[int(height*0.2):int(height*0.8), int(width*0.3):int(width*0.6)]
            img_gray = cv2.cvtColor(crop_img, cv2.COLOR_RGB2GRAY)
            text = pytesseract.image_to_string(img_gray, config='--oem 3 --psm 6')
            
            # 数値抽出（6.00〜7.50）
            all_numbers = re.findall(r'\d\.\d{2}', text)
            valid_times = sorted([float(num) for num in all_numbers if 6.00 <= float(num) <= 7.50])
            
            if not valid_times:
                st.error("展示タイムが検出できませんでした。")
            else:
                best_time = valid_times[0]
                st.success(f"【最速タイム】: {best_time}秒")

                # --- 3. ロジック判定 ---
                # ここにトリガー検知などを統合
                st.write("--- 意思決定結果 ---")
                
                # 簡易判定例
                if best_time < 6.50:
                    st.warning("★【勝負レース判定】: 爆速足検知。軸候補です。")
                    # フォーメーション提示
                    st.write("推奨買い目: 1-23-2345")
                else:
                    st.info("★【見送り推奨】: タイムが拮抗しています。")

                # --- 4. 悪魔の代弁者（最終確認） ---
                st.divider()
                st.subheader("👿 悪魔の代弁者：最終確認")
                if st.checkbox("損害（負け）を許容し、勝負を承認する"):
                    st.balloons()
                    st.success("購入承認：健闘を祈ります！")
