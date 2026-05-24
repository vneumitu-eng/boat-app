import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

st.title("🤖 AI競艇エンジン v7.0【実戦直結版】")

# 開催地マッピング（艇国データバンクのコードに合わせる）
# 艇国データバンクのIDに合わせて定義
jcd_map = {"桐生": "01", "戸田": "02", "江戸川": "03", "平和島": "04", "多摩川": "05", 
           "浜名湖": "06", "蒲郡": "07", "常滑": "08", "津": "09", "三国": "10", 
           "びわこ": "11", "住之江": "12", "尼崎": "13", "鳴門": "14", "丸亀": "15", 
           "児島": "16", "宮島": "17", "徳山": "18", "下関": "19", "若松": "20", 
           "芦屋": "21", "福岡": "22", "唐津": "23", "大村": "24"}

stadium = st.selectbox("開催場を選択", list(jcd_map.keys()))
race_num = st.selectbox("レース番号", range(1, 13))

if st.button("データバンクから自動解析を実行"):
    # 今日の日付
    d = datetime.now()
    # 艇国データバンクのURL形式
    url = f"https://www.teikoku-db.net/race/index.php?y={d.year}&m={d.month}&d={d.day}&j={jcd_map[stadium]}&r={race_num}"
    
    try:
        st.info(f"解析中: {url}")
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        res.encoding = res.apparent_encoding
        soup = BeautifulSoup(res.text, "html.parser")
        
        # 艇国データバンクの構造から展示タイムを抽出
        # タイムはテーブル内の数値として確実に入っています
        times = []
        for td in soup.find_all("td"):
            text = td.text.strip()
            if re.match(r'^[67]\.\d{2}$', text):
                times.append(float(text))
        
        # 重複削除
        times = sorted(list(set(times)))
        
        if times:
            best_time = min(times)
            avg_time = sum(times) / len(times)
            
            st.success("データ取得成功！")
            st.metric("最速展示タイム", f"{best_time:.2f}秒")
            
            # AI判定エンジン
            if best_time < avg_time - 0.1:
                st.warning("★【勝負レース判定】: 爆速足検知！")
                st.write("推奨買い目: 1-23-2345")
            else:
                st.info("★【見送り推奨】: タイムが拮抗しています。")
                
            st.divider()
            if st.checkbox("損害を許容し、勝負を承認する"):
                st.balloons()
                st.success("購入承認：健闘を祈ります！")
        else:
            st.error("展示タイムが見つかりませんでした。")
            st.write("サイト上の表示を確認してください:", url)
            
    except Exception as e:
        st.error(f"システムエラー: {e}")
