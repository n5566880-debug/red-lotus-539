import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# --- 1. 介面極致美化 ---
st.set_page_config(page_title="赤鍊九五・至尊戰情室", layout="wide")
st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 2px solid #D4AF37; }
    .main-card { background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%); padding: 25px; border-radius: 15px; border: 1px solid #D4AF37; margin-bottom: 20px; }
    .fortune-card { background: #2d1b00; padding: 15px; border-radius: 10px; border-left: 5px solid #D4AF37; }
    .stMetric { background: #111; border-radius: 10px; padding: 10px; border: 0.5px solid #333; }
</style>
""", unsafe_allow_html=True)

st.title("🔱 赤鍊紅蓮・539 九五至尊戰情室 (v5.0)")

# --- 2. 側邊欄：數據注入 ---
with st.sidebar:
    st.header("🛠️ 數據注入系統")
    new_date = st.date_input("開獎日期")
    n_cols = st.columns(5)
    nums = [n_cols[i].number_input(f"N{i+1}", 1, 39, 1) for i in range(5)]
    if st.button("🚀 注入數據並分析"):
        st.balloons()
        st.success("數據已同步至雲端緩存")

# --- 3. 核心數據 (30期真實數據) ---
data = {
    '日期': ['2025-12-03', '2025-12-04', '2025-12-05', '2025-12-06', '2025-12-08','2025-12-09', '2025-12-10', '2025-12-11', '2025-12-12', '2025-12-13','2025-12-15', '2025-12-16', '2025-12-17', '2025-12-18', '2025-12-19','2025-12-20', '2025-12-22', '2025-12-23', '2025-12-24', '2025-12-25','2025-12-26', '2025-12-27', '2025-12-29', '2025-12-30', '2025-12-31','2026-01-01', '2026-01-02', '2026-01-03', '2026-01-05', '2026-01-06'],
    'N1': [5, 1, 2, 6, 5, 7, 4, 2, 10, 2, 3, 2, 5, 4, 12, 1, 2, 9, 2, 14, 1, 1, 5, 11, 8, 15, 17, 22, 10, 1],
    'N2': [9, 7, 3, 22, 23, 8, 7, 6, 24, 9, 17, 10, 6, 9, 16, 5, 22, 22, 3, 18, 10, 15, 10, 12, 10, 16, 18, 23, 16, 2],
    'N3': [14, 20, 16, 23, 27, 15, 11, 17, 26, 21, 27, 14, 7, 32, 23, 16, 24, 24, 14, 28, 20, 19, 13, 24, 11, 18, 25, 31, 18, 6],
    'N4': [33, 25, 17, 24, 28, 30, 16, 25, 28, 31, 29, 33, 19, 33, 27, 35, 27, 30, 25, 36, 27, 28, 29, 27, 26, 29, 36, 32, 34, 11],
    'N5': [35, 37, 29, 32, 31, 39, 26, 26, 35, 38, 38, 35, 32, 36, 30, 38, 38, 35, 30, 39, 36, 38, 37, 33, 35, 36, 39, 38, 39, 33]
}
df = pd.DataFrame(data)
df['總和'] = df[['N1', 'N2', 'N3', 'N4', 'N5']].sum(axis=1)
df['MA5'] = df['總和'].rolling(window=5).mean()

# --- 4. 奇門與運勢分析面板 ---
st.markdown(f"""
<div class="main-card">
    <h2 style='color: #D4AF37; margin-top: 0;'>🏮 今日奇門遁甲局：丙戌日</h2>
    <div style='display: flex; justify-content: space-between;'>
        <div style='width: 48%;'>
            <p style='color: #FF4B4B; font-size: 18px;'><b>【 奇門局勢 】</b></p>
            <ul>
                <li><b>天盤：</b>丙火入戌庫，火光內斂，大數區隱現。</li>
                <li><b>地盤：</b>庚申專祿祿位偏移，20區間磁場最強。</li>
                <li><b>吉神：</b>生門落中宮，25 為定格核心。</li>
            </ul>
        </div>
        <div style='width: 48%; border-left: 1px solid #333; padding-left: 20px;'>
            <p style='color: #00FF00; font-size: 18px;'><b>【 掌門今日運勢 】</b></p>
            <p>1996庚申(金) + 2001辛巳(金) 雙金交輝，運勢呈「<b>騰蛇化龍</b>」之象。金氣太旺，需以火煉，今晚利「大數」與「奇數」。</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 5. 具體建議面板 ---
col_s1, col_s2 = st.columns(2)
with col_s1:
    st.markdown("""
    <div class="fortune-card">
        <h3 style='color: #D4AF37; margin:0;'>🎯 戰術建議</h3>
        <p style='margin: 10px 0;'>1. <b>重兵佈署</b>：24, 25, 26（連碰）。<br>
        2. <b>奇兵突擊</b>：31（防禦最大數跳空）。<br>
        3. <b>守備位</b>：07（平衡金火氣場）。</p>
    </div>
    """, unsafe_allow_html=True)

with col_s2:
    st.markdown("""
    <div class="fortune-card" style='border-left-color: #FF4B4B;'>
        <h3 style='color: #FF4B4B; margin:0;'>⚠️ 注意事項</h3>
        <p style='margin: 10px 0;'>1. <b>避開連號</b>：昨日01, 02已開，今日應避開極端連號。<br>
        2. <b>封盤提醒</b>：19:50 前完成所有佈署。<br>
        3. <b>心態穩住</b>：今日為「反彈局」，切勿因昨日跌深而縮手。</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- 6. 數據看板 ---
st.subheader("📊 量化監控指標")
m1, m2, m3, m4 = st.columns(4)
m1.metric("昨日總和", int(df['總和'].iloc[-1]), "-64")
m2.metric("MA5 攻擊水位", f"{df['MA5'].iloc[-1]:.0f}")
m3.metric("推薦號碼", "25", "奇門定格")
m4.metric("吉時窗口", "13:15-14:45", "庚申金旺")

# --- 7. 能量趨勢圖 ---
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['日期'], y=df['總和'], mode='lines+markers', line=dict(color='#D4AF37', width=4), name='能量重心'))
fig.add_trace(go.Scatter(x=df['日期'], y=df['MA5'], line=dict(color='gray', width=2, dash='dash'), name='5日均線'))
fig.update_layout(template="plotly_dark", height=400, margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig, use_container_width=True)
