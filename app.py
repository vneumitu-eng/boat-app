import streamlit as st
import pandas as pd
from datetime import datetime

st.title("🤖 AI競艇エンジン v8.0【確実データ入力版】")

st.info("現在、自動スクレイピングで接続制限が発生しています。最も安定して解析を行うため、公式サイトの出走表をコピーして貼り付けてください。")

# 1. データ入力欄（スクレイピングを使わず、コピー＆ペーストで取得する）
# これが「究極の安定」です。
data_input = st.text_area("出走表の展示タイム列をコピーして貼り付けてください（例: 6.78, 6.72, 6.80...）")

if st.button("解析実行"):
    if data_input:
        # 入力されたテキストから数値を抽出
        import re
        times = [float(t) for t in re.findall(r'\d\.\d{2}', data_input)]
        
        if times:
            best_time = min(times)
            avg_time = sum(times) / len(times)
            
            st.success(f"データ取得成功！: {times}")
            st.metric("最速展示タイム", f"{best_time:.2f}秒")
            
            if best_time < avg_time - 0.1:
                st.warning("★【勝負レース判定】: 爆速足検知！軸候補です！")
            else:
                st.info("★【見送り推奨】: タイムが拮抗しています。")
        else:
            st.error("数値が見つかりません。形式を確認してください。")
    else:
        st.warning("データが入力されていません。")
