import streamlit as st
from PIL import Image

st.title("AI競艇エンジン v7.0")

uploaded_file = st.file_uploader("レース直前情報のスクショをアップロード", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="解析対象の画像", use_column_width=True)
    
    if st.button("展示タイムを解析する"):
        st.write("解析中...")
        st.info("ここに解析結果が表示されるように今後拡張します！")
