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
    
    if st.button("展示タイムを解析する"):
        with st.spinner('解析中...'):
            img_array = np.array(image.convert('RGB'))
            height, width, _ = img_array.shape
            
            # 【調整済】縦画面用：中央付近のタイム列を狙って切り抜き
            # 横幅(width)の 30%〜60% の範囲を切り抜きます
            crop_img = img_array[int(height*0.2):int(height*0.8), int(width*0.3):int(width*0.6)]
            img_gray = cv2.cvtColor(crop_img, cv2.COLOR_RGB2GRAY)
            
            # OCR実行（数字認識に特化）
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(img_gray, config=custom_config)
            
            # 競艇の展示タイム（6.00〜7.50の範囲）のみを抽出するロジック
            all_numbers = re.findall(r'\d\.\d{2}', text)
            valid_times = []
            for num in all_numbers:
                val = float(num)
                if 6.00 <= val <= 7.50:
                    valid_times.append(val)
            
            st.write("### --- 解析結果 ---")
            if valid_times:
                # 重複を削除して昇順に並べる（速い順）
                unique_times = sorted(list(set(valid_times)))
                for time in unique_times:
                    st.success(f"検出タイム: {time}")
            else:
                st.warning("展示タイムが見つかりませんでした。")
                st.text("もし何も出ない場合は、設定の範囲（width*0.3:0.6）を少しずらしてみてください。")
