import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re  # これを忘れずに追加しました

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
        
        # 展示タイムの取得ロジック
        times = []
        elements = soup.select(".is-fs18")
        for el in elements:
            text = el.text.strip()
            # 6秒〜7秒台の形式かチェック
            if re.match(r'^[67]\.\d{2}$', text):
                times.append(float(text))
        
        if times:
            best_time = min(times)
            avg_time = sum(times) / len(times)
            
            st.success("データ取得成功！")
            st.metric("最速展示タイム", f"{best_time:.2f}秒")
            st.write(f"平均タイム: {avg_time:.2f}秒")
            
            if best_time < avg_time - 0.1:
                st.warning("★【勝負レース判定】: 爆速足検知。軸候補です！")
            else:
                st.info("★【見送り推奨】: タイムが拮抗しています。")
        else:
            st.error("展示タイムが取得できませんでした（まだ公開前か、サイト構造上の問題です）。")
            st.write("確認用URL:", url)
            
    except Exception as e:
        st.error(f"接続エラー: {e}")
