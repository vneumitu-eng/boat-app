import streamlit as st
from PIL import Image
import pytesseract
import cv2
import numpy as np
import re

st.title("AI競艇エンジン v7.0")

uploaded_file = st.file_uploader("レース直前情報のスクショをアップロード", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="解析対象の画像", use_column_width=True)
    
    if st.button("展示タイムを解析して予想する"):
        with st.spinner('解析中...'):
            img_array = np.array(image.convert('RGB'))
            height, width, _ = img_array.shape
            
            # 解析エリアの切り抜き
            crop_img = img_array[int(height*0.2):int(height*0.8), int(width*0.3):int(width*0.6)]
            img_gray = cv2.cvtColor(crop_img, cv2.COLOR_RGB2GRAY)
            
            # OCR実行
            text = pytesseract.image_to_string(img_gray, config='--oem 3 --psm 6')
            
            # 数値抽出
            all_numbers = re.findall(r'\d\.\d{2}', text)
            valid_times = sorted([float(num) for num in all_numbers if 6.00 <= float(num) <= 7.50])
            
            st.write("### --- AI予想レポート ---")
            if valid_times:
                best_time = valid_times[0]
                st.success(f"【最速タイム】: {best_time}秒")
                
                # 予想ロジック：平均タイムとの比較
                avg_time = sum(valid_times) / len(valid_times)
                st.write(f"平均タイム: {avg_time:.2f}秒")
                
                if best_time < avg_time - 0.1:
                    st.warning("★AIの判定: このレースは最速タイムの艇が突出しています。軸に最適です！")
                else:
                    st.info("AIの判定: タイムが拮抗しています。混戦模様です。")
            else:
                st.warning("タイムが正常に読み取れませんでした。")
