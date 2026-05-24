import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

st.title("🤖 AI競艇エンジン v7.0【完全自動版】")

# 開催地マッピング
jcd_map = {"桐生": "01", "戸田": "02", "江戸川": "03", "平和島": "04", "多摩川": "05", 
           "浜名湖": "06", "蒲郡": "07", "常滑": "08", "津": "09", "三国": "10", 
           "びわこ": "11", "住之江": "12", "尼崎": "13", "鳴門": "14", "丸亀": "15", 
           "児島": "16", "宮島": "17", "徳山": "18", "下関": "19", "若松": "20", 
           "芦屋": "21", "福岡": "22", "唐津": "23", "大村": "24"}

stadium = st.selectbox("開催場を選択", list(jcd_map.keys()))
race_num = st.selectbox("レース番号", range(1, 13))

if st.button("公式サイトからデータ取得・解析"):
    date_str = datetime.now().strftime("%Y%m%d")
    url = f"https://www.boatrace.jp/owpc/pc/race/index?rno={race_num}&jcd={jcd_map[stadium]}&hd={date_str}"
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        
        # --- 改善点: 公式サイトのテーブル構造から直接抽出 ---
        # 展示タイムは「is-number」または「is-fs18」などが含まれるセルにあります
        times = []
        # すべてのセルを走査し、6.xx ~ 7.xx の形式を探す
        for td in soup.find_all("td"):
            text = td.text.strip()
            if re.match(r'^[67]\.\d{2}$', text):
                times.append(float(text))
        
        # 重複削除（同じタイムが複数選手いた場合など）
        times = sorted(list(set(times)))
        
        if times:
            best_time = min(times)
            avg_time = sum(times) / len(times)
            
            st.success("データ取得成功！")
            st.metric("最速展示タイム", f"{best_time:.2f}秒")
            
            if best_time < 6.50:
                st.warning("★【勝負レース判定】: 爆速足検知。軸候補です！")
            else:
                st.info("★【見送り推奨】: タイムが拮抗しています。")
        else:
            st.error("展示タイムがHTML内に見つかりません。")
            st.write("もし公式サイトに表示されているのに取れない場合は、まだデータが確定していないか、公式サイトの仕様変更の可能性があります。")
            
    except Exception as e:
        st.error(f"接続エラー: {e}")
