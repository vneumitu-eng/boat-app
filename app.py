import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- 1. 設定・マッピング ---
st.set_page_config(page_title="AI競艇エンジン v7.0", layout="wide")
st.title("🤖 AI競艇エンジン v7.0【完全自動版】")

jcd_map = {"桐生": "01", "戸田": "02", "江戸川": "03", "平和島": "04", "多摩川": "05", 
           "浜名湖": "06", "蒲郡": "07", "常滑": "08", "津": "09", "三国": "10", 
           "びわこ": "11", "住之江": "12", "尼崎": "13", "鳴門": "14", "丸亀": "15", 
           "児島": "16", "宮島": "17", "徳山": "18", "下関": "19", "若松": "20", 
           "芦屋": "21", "福岡": "22", "唐津": "23", "大村": "24"}

# --- 2. 入力UI ---
col1, col2 = st.columns(2)
with col1:
    stadium = st.selectbox("開催場を選択", list(jcd_map.keys()))
with col2:
    race_num = st.selectbox("レース番号", range(1, 13))

# --- 3. メイン処理 ---
if st.button("🚀 公式サイトから自動解析を実行"):
    date_str = datetime.now().strftime("%Y%m%d")
    url = f"https://www.boatrace.jp/owpc/pc/race/index?rno={race_num}&jcd={jcd_map[stadium]}&hd={date_str}"
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        
        # 展示タイム抽出 (.is-fs18 にタイムが格納されている)
        time_elements = soup.select(".is-fs18")
        times = [float(t.text.strip()) for t in time_elements if "." in t.text and 6.0 <= float(t.text.strip()) <= 7.5]
        
        if not times:
            st.error("展示タイムが取得できませんでした。レース前か通信エラーの可能性があります。")
        else:
            # 判定ロジック適用
            best_time = min(times)
            avg_time = sum(times) / len(times)
            
            st.subheader("📊 解析結果")
            st.metric("最速展示タイム", f"{best_time:.2f}秒")
            st.write(f"平均タイム: {avg_time:.2f}秒")
            
            # AIロジック判定
            if best_time < avg_time - 0.1:
                st.warning("★【勝負レース判定】: 爆速足検知。軸候補です！")
                st.write("推奨買い目: 1-23-2345 (6点固定)")
            else:
                st.info("★【見送り推奨】: タイムが拮抗しています。")
                
            # 悪魔の代弁者（損切可視化）
            st.divider()
            st.subheader("👿 悪魔の代弁者：最終確認")
            if st.checkbox("損害（負け）を許容し、勝負を承認する"):
                st.balloons()
                st.success("購入承認：健闘を祈ります！")
                
    except Exception as e:
        st.error(f"システムエラー: {e}")
