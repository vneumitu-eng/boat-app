import streamlit as st
from PIL import Image
import pytesseract
import cv2
import numpy as np

st.title("AI競艇エンジン v7.0")

uploaded_file = st.file_uploader("レース直前情報のスクショをアップロード", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    # 画像を開く
    image = Image.open(uploaded_file)
    st.image(image, caption="解析対象の画像", use_column_width=True)
    
    if st.button("展示タイムを解析する"):
        st.write("解析中...")
        
        # 画像をOpenCV形式に変換
        img_array = np.array(image.convert('RGB'))
        img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # OCRで文字を読み取る
        try:
            text = pytesseract.image_to_string(img_gray, lang='jpn') # 日本語モード
            st.write("--- 解析結果 ---")
            st.text(text)
        except Exception as e:
            st.error(f"解析中にエラーが発生しました: {e}")
            st.info("※初回はツールの準備に少し時間がかかることがあります")
