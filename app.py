import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

st.title("🤖 AI競艇エンジン v7.0【公式データ直結版】")

# 開催地マッピング
jcd_map = {"桐生": "01", "戸田": "02", "江戸川": "03", "平和島": "04", "多摩川": "05", 
           "浜名湖": "06", "蒲郡": "07", "常滑": "08", "津": "09", "三国": "10", 
           "びわこ": "11", "住之江": "12", "尼崎": "13", "鳴門": "14", "丸亀": "15", 
           "児島": "16", "宮島": "17", "徳山": "18", "下関": "19", "若松": "20", 
           "芦屋": "21", "福岡": "22", "唐津": "23", "大村": "24"}

stadium = st.selectbox("開催場を選択", list(jcd_map.keys()))
race_num = st.selectbox("レース番号", range(1, 13))

if st.button("公式データから自動解析を実行"):
    date_str = datetime.now().strftime("%Y%m%d")
    # 出走表ページに一度アクセスして、データJSONのURLを探す（今回は簡易的にAPI直叩きの構成を想定）
    # ※公式サイトのデータ提供形式に基づいたロジック
    url = f"https://www.boatrace.jp/owpc/pc/race/index?rno={race_num}&jcd={jcd_map[stadium]}&hd={date_str}"
    
    try:
        # 簡易版：実際の展示タイム取得には、公式サイトが裏側で呼んでいるJSONを参照するのが最も確実です
        st.info("公式サイトへアクセス中...")
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        
        # 抽出ロジック（公式サイトの特定の隠しデータクラスを狙い撃ち）
        soup = BeautifulSoup(res.text, "html.parser")
        
        # 展示タイムは 'is-fs18' クラスにあります
        times = []
        for el in soup.select(".is-fs18"):
            text = el.text.strip()
            # 6秒台〜7秒台の数値のみを抽出
            if len(text) == 4 and "." in text:
                times.append(float(text))
        
        # 重複を除く（同じ数値の排除）
        times = sorted(list(set(times)))
        
        if times:
            st.success("データ取得成功！")
            st.write(f"取得タイム: {times}")
            
            best_time = min(times)
            st.metric("最速展示タイム", f"{best_time:.2f}秒")
            
            if best_time < 6.50:
                st.warning("★【勝負レース判定】: 爆速足検知！")
            else:
                st.info("★【見送り推奨】")
        else:
            st.error("現在、展示タイムデータが公開されていないか、取得できませんでした。")
            
    except Exception as e:
        st.error(f"システムエラー: {e}")
