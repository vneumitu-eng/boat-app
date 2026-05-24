import streamlit as st
import google.generativeai as genai
from PIL import Image

# APIキーの設定
api_key = st.secrets.get("GOOGLE_API_KEY") 
genai.configure(api_key=api_key)

st.title("🤖 競艇・直前解析エンジン v10.0")

uploaded_file = st.file_uploader("直前情報のスクショをアップロード", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="解析画像", use_container_width=True)
    
    if st.button("買い目を解析"):
        with st.spinner("AIが解析中..."):
            # Geminiモデルの呼び出し
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = "この競艇の直前情報から、各艇の展示タイムを読み取り、最速艇を軸にした推奨買い目を提案して。"
            response = model.generate_content([prompt, image])
            
            st.subheader("💡 解析結果")
            st.write(response.text)
