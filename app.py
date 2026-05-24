import streamlit as st
import easyocr
import numpy as np
from PIL import Image

st.title("🤖 AI競艇エンジン v8.0【スクショ解析版】")
st.info("出走表の展示タイム列をスクリーンショットして、ここにアップロードしてください。")

# 1. OCRエンジンの初期化（高速化のためキャッシュ）
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])

reader = load_reader()

# 2. 画像アップロード
uploaded_file = st.file_uploader("展示タイムのスクショをアップロード", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # 画像表示
    image = Image.open(uploaded_file)
    st.image(image, caption="解析中の画像", use_container_width=True)
    
    if st.button("解析実行"):
        # 画像をnumpy形式に変換して読み込み
        img_np = np.array(image)
        results = reader.readtext(img_np, detail=0)
        
        # 6秒台〜7秒台の数値を抽出（正規表現）
        import re
        times = [float(t) for t in results if re.match(r'^[67]\.\d{2}$', t)]
        
        if times:
            times = sorted(list(set(times)))
            best_time = min(times)
            avg_time = sum(times) / len(times)
            
            st.success(f"解析成功！: {times}")
            st.metric("最速展示タイム", f"{best_time:.2f}秒")
            
            # AI判定
            if best_time < avg_time - 0.1:
                st.warning("★【勝負レース判定】: 爆速足検知！軸候補です！")
            else:
                st.info("★【見送り推奨】: タイムが拮抗しています。")
        else:
            st.error("数値が読み取れませんでした。タイム列が鮮明に写っているか確認してください。")
