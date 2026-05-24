import streamlit as st
from PIL import Image
import pytesseract
import cv2
import numpy as np
import re # 追加：文字列解析のため

st.title("AI競艇エンジン v7.0")

uploaded_file = st.file_uploader("レース直前情報のスクショをアップロード", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="解析対象の画像", use_column_width=True)
    
    if st.button("展示タイムを解析する"):
        with st.spinner('解析中...'):
            img_array = np.array(image.convert('RGB'))
            height, width, _ = img_array.shape
            
            # 画像の中央付近にエリアを絞る
            crop_img = img_array[int(height*0.3):int(height*0.7), 0:width]
            img_gray = cv2.cvtColor(crop_img, cv2.COLOR_RGB2GRAY)
            
            # OCR実行
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(img_gray, config=custom_config)
            
            st.write("### --- 抽出された展示タイム候補 ---")
            
            # 【重要】正規表現を使って「X.XX」という形式の数字だけを抽出する
            # 小数点を含む数字を探すためのフィルターです
            found_times = re.findall(r'\d\.\d{2}', text)
            
            if found_times:
                # 重複を削除して表示
                unique_times = sorted(list(set(found_times)))
                for time in unique_times:
                    st.success(f"検出タイム: {time}")
            else:
                st.warning("展示タイムが見つかりませんでした。別の範囲を切り抜く必要があります。")
                st.warning("数字を検出できませんでした。画像を明るくして再試行してください。")

# 解析の仕組みを可視化
st.info("※解析精度を上げるには、画像の『展示タイム』部分を大きく映して撮影してください。")
