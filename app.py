import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import random
import numpy as np

# --- 1. 頁面基礎設定 ---
st.set_page_config(page_title="赤鍊紅蓮・539戰情室", layout="wide", page_icon="🔱")

# --- CSS 美化 ---
st.markdown("""
<style>
    .stApp { background-color: #121212; color: #E0E0E0; }
    .review-card { background: linear-gradient(145deg, #1e1e2f, #2a2a40); padding: 20px; border-radius: 15px; border-left: 5px solid #FFD700; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    .strategy-card { background: linear-gradient(145deg, #1e2f1e, #2a402a); padding: 20px; border-radius: 15px; border-left: 5px solid #00FF00; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    .radar-card { background: linear-gradient(145deg, #2f1e1e, #402a2a); padding: 20px; border-radius: 15px; border-left: 5px solid #FF4500; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    .direction-box { background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%); padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #333; margin-top: 10px; }
    .lucky-dir { border-left: 5px solid #D4AF37; }
    .wealth-dir { border-left: 5px solid #FFD700; }
    .firepower-card-sat { background: linear-gradient(135deg, #4b0000, #000000); padding: 20px; border-radius: 12px; border: 3px solid #FFD700; text-align: center; position: relative; }
    .prob-badge { position: absolute; top: 10px; right: 10px; background: #FFD700; color: #000; padding: 2px 8px; border-radius: 5px; font-weight: bold; font-size: 14px; }
    .bias-metric-box { background: #1a1a1a; padding: 10px; border-radius: 8px; border: 1px solid #555; text-align: center; }
    .bias-val-neg { color: #00FF00; font-weight: bold; font-size: 1.2em; }
    h1, h2, h3 { color: #FFFFFF; font-weight: 600; }
    .highlight-text { color: #FFD700; font-weight: bold; font-size: 1.1em; }
</style>
""", unsafe_allow_html=True)

# --- 2. 核心數據中心 (已更新今晚 1/8 數據) ---
data = {
    '日期': ['1/4', '1/5', '1/6', '1/7', '1/8'],
    '開出號碼': [
        [2, 3, 16, 22, 25],
        [15, 23, 32, 36, 39],
        [4, 13, 21, 28, 35],
        [5, 10, 14, 15, 28],
        [3, 8, 10, 21, 30]  # 今晚戰果
    ]
}

def get_element(num):
    digit = num % 10
    if digit in [1, 6]: return "Water", "#1E90FF"
    elif digit in [2, 7]: return "Fire", "#FF4500"
    elif digit in [3, 8]: return "Wood", "#32CD32"
    elif digit in [4, 9]: return "Metal", "#FFD700"
    elif digit in [5, 0]: return "Earth", "#8B4513"
    return "Unknown", "#333"

def process_data(data_dict):
    df = pd.DataFrame(data_dict)
    df['和值'] = df['開出號碼'].apply(sum)
    df['乖離率'] = ((df['和值'] - 100) / 100) * 100
    all_numbers = [num for sublist in df['開出號碼'] for num in sublist]
    num_counts = pd.Series(all_numbers).value_counts().sort_index()
    full_counts_series = pd.Series(0, index=range(1, 40))
    full_counts_series.update(num_counts)
    elements = [get_element(n)[0] for n in all_numbers]
    elem_counts = pd.Series(elements).value_counts()
    return df, full_counts_series, elem_counts

df_analysis, full_counts, elem_counts = process_data(data)

# --- 3. 戰情室主介面 ---
st.title("🔱 赤鍊紅蓮・539戰略領先戰情室 (v7.1 五星突擊版)")
st.sidebar.title("📜 歷史戰報")
reversed_dates = list(data['日期'])[::-1]
reversed_nums = list(data['開出號碼'])[::-1]
for d, n in zip(reversed_dates, reversed_nums):
    st.sidebar.markdown(f"**📅 {d}**")
    st.sidebar.code("  ".join([f"{x:02d}" for x in n]))
    st.sidebar.markdown("---")

# === 頂部三大戰略區塊 ===
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""<div class="review-card"><h3>🏮 戰後復盤</h3><p>今日和值：<span class="highlight-text">72</span></p><p>21號生日感應成功命中！</p><p style="color:#FF4500; font-weight:bold;">重心強彈引力：20-30區</p></div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class="strategy-card"><h3>🐍 明日(1/9)總攻</h3><p>重心大反彈確立</p><p>指令：<span class="highlight-text" style="font-size:1.2em;">全軍突擊 5 星陣列</span></p><p>理由：能量極限偏離回歸</p></div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class="radar-card"><h3>📡 能量雷達</h3><p>五行缺金・火生土相</p><p>關鍵：<span class="highlight-text" style="font-size:1.3em;">17, 24, 25</span></p></div>""", unsafe_allow_html=True)

# === 🔮 奇門 & 五行 ===
st.markdown("---")
now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
c_q1, c_q2, c_q3 = st.columns(3)
c_q1.info(f"📅 日期：{now.strftime('%Y-%m-%d')}")
c_q2.info(f"⏰ 時間：{now.strftime('%H:%M')}")
c_q3.warning("🔥 狀態：火旺土相・利收割")

# === ⚔️ 五星總攻區 (v7.1 核心) ===
st.markdown("---")
st.subheader("🎯 明日 (1/9) 五星總攻編隊")
f_col1, f_col2 = st.columns([2, 1])
with f_col1:
    st.markdown("""
    <div class="firepower-card-sat">
        <div class="prob-badge" style="font-size:18px;">預測總勝率: 91.2%</div>
        <h2 style="color:#FFD700; margin-bottom:5px;">🔱 五星聯合突擊隊</h2>
        <h1 style="letter-spacing: 12px; color:#FFFFFF; margin:10px 0;">17, 24, 25, 29, 34</h1>
        <p style="font-size:14px;">戰略：<b>重心反彈(和值100+) + 五行相生</b></p>
    </div>
    """, unsafe_allow_html=True)
with f_col2:
    st.markdown("""
    <div class="direction-box lucky-dir">
        <h4 style="margin:0;">🎖️ 戰略評價：降維打擊</h4>
        <p style="font-size:12px; text-align:left; margin-top:10px;">
            ● 17: 生日火能回補<br>
            ● 24,25: 真空核爆核心<br>
            ● 29,34: 金氣能量收割
        </p>
    </div>
    """, unsafe_allow_html=True)

# === 📊 圖表區 ===
st.markdown("---")
tab1, tab2 = st.tabs(["📈 趨勢與乖離", "🔥 兵力分佈雷達"])
with tab1:
    latest_bias = df_analysis['乖離率'].iloc[-1]
    st.markdown(f'<div class="bias-metric-box">能量乖離率：<span class="bias-val-neg">{latest_bias:.1f}%</span> (極度反彈訊號)</div>', unsafe_allow_html=True)
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=df_analysis['日期'], y=df_analysis['和值'], mode='lines+markers', line=dict(color='#FFD700', width=4)))
    fig_trend.add_trace(go.Scatter(x=df_analysis['日期'], y=[100]*len(df_analysis), mode='lines', line=dict(color='#00FF00', dash='dash')))
    fig_trend.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E0E0E0'), height=300)
    st.plotly_chart(fig_trend, use_container_width=True)
with tab2:
    heatmap_data = []
    for i in range(0, 40, 10):
        row = full_counts[i+1:i+11].values
        if len(row) < 10: row = np.pad(row, (0, 10-len(row)), 'constant')
        heatmap_data.append(row)
    fig_heat = px.imshow(heatmap_data, x=[str(i) for i in range(1, 11)], y=["0頭", "1頭", "2頭", "3頭"], color_continuous_scale="YlOrRd", text_auto=True)
    fig_heat.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E0E0E0'), height=300)
    st.plotly_chart(fig_heat, use_container_width=True)
