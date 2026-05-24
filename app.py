import streamlit as st
import pytesseract
from PIL import Image
import re

st.title("🤖 競艇・直前解析エンジン v9.1")

uploaded_file = st.file_uploader("直前情報のスクショをアップロード", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="解析画像", use_container_width=True)
    
    if st.button("買い目を解析"):
        # 画像からテキストを読み取る（Tesseractがクラウドにある前提）
        text = pytesseract.image_to_string(image)
        # 数値（6.xxなど）を抽出
        times = [float(t) for t in re.findall(r'[67]\.\d{2}', text)]
        
        if len(times) >= 6:
            # 最速艇の特定
            best_idx = times.index(min(times)) + 1
            
            st.subheader("💡 解析結果")
            st.write(f"最速艇: {best_idx}号艇 ({min(times)}秒)")
            
            # ロジックに基づいた買い目提案
            st.subheader("🎯 推奨買い目")
            if best_idx == 1:
                st.write("1-23-全")
            elif best_idx == 2:
                st.write("2-1-3, 2-5-1, 2-1-5")
            else:
                st.write(f"{best_idx}-1-全, {best_idx}-{best_idx+1}-1")
        else:
            st.error("タイムが読み取れませんでした。スクショを『直前情報』タブの文字がはっきり見える状態で撮り直してください。")
