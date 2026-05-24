import streamlit as st
from PIL import Image

st.title("AI競艇エンジン v7.0")

# 1. 写真をアップロードする機能
uploaded_file = st.file_uploader("レース直前情報のスクショをアップロード", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    # 2. アップロードされた画像を表示
    image = Image.open(uploaded_file)
    st.image(image, caption="解析対象の画像", use_column_width=True)
    
    # 3. 解析ボタン
    if st.button("展示タイムを解析する"):
        st.write("解析中...（※今はまだ骨組みです）")
        st.info("ここに解析結果が表示されるように今後拡張します！")