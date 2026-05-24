import streamlit as st
from PIL import Image
import pytesseract
import cv2
import numpy as np

st.title("AI競艇エンジン v7.0")

uploaded_file = st.file_uploader("レース直前情報のスクショをアップロード", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="解析対象の画像", use_column_width=True)
    
    if st.button("展示タイムを解析する"):
        with st.spinner('解析中...'):
            # 画像を配列に変換
            img_array = np.array(image.convert('RGB'))
            height, width, _ = img_array.shape
            
            # 【重要】画像の真ん中あたり（展示タイムがあるエリア）を切り抜く
            # 縦30%から70%の範囲に絞ることで精度を上げます
            crop_img = img_array[int(height*0.3):int(height*0.7), 0:width]
            
            # モノクロ化して読み取りやすくする
            img_gray = cv2.cvtColor(crop_img, cv2.COLOR_RGB2GRAY)
            
            # OCR設定：数字と小数点のみを許可して抽出
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789.'
            text = pytesseract.image_to_string(img_gray, config=custom_config)
            
            # 空行を除去して数字リストを表示
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            st.write("### --- 解析された数値 ---")
            if lines:
                for line in lines:
                    st.text(line)
            else:
                st.warning("数字を検出できませんでした。画像を明るくして再試行してください。")

# 解析の仕組みを可視化
st.info("※解析精度を上げるには、画像の『展示タイム』部分を大きく映して撮影してください。")
