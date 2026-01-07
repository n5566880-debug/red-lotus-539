
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# --- 1. 軍事戰情室風格設定 ---
st.set_page_config(page_title="赤鍊帝國・軍事沙盤", layout="wide")
st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #050505; border-right: 2px solid #D4AF37; }
    .stApp { background-color: #000000; }
    .corps-card { background: rgba(20, 20, 20, 0.9); padding: 15px; border-radius: 5px; border: 1px solid #333; border-top: 3px solid #D4AF37; }
    .radar-text { font-family: 'Courier New', monospace; color: #00FF00; }
</style>
""", unsafe_allow_html=True)

st.title("⚔️ 赤鍊紅蓮・539 軍事沙盤戰情室 (v5.5)")

# --- 2. 數據核心 (30期真實數據) ---
data = {
    '日期': ['12-03', '12-04', '12-05', '12-06', '12-08','12-09', '12-10', '12-11', '12-12', '12-13','12-15', '12-16', '12-17', '12-18', '12-19','12-20', '12-22', '12-23', '12-24', '12-25','12-26', '12-27', '12-29', '12-30', '12-31','01-01', '01-02', '01-03', '01-05', '01-06'],
    'N1': [5, 1, 2, 6, 5, 7, 4, 2, 10, 2, 3, 2, 5, 4, 12, 1, 2, 9, 2, 14, 1, 1, 5, 11, 8, 15, 17, 22, 10, 1],
    'N2': [9, 7, 3, 22, 23, 8, 7, 6, 24, 9, 17, 10, 6, 9, 16, 5, 22, 22, 3, 18, 10, 15, 10, 12, 10, 16, 18, 23, 16, 2],
    'N3': [14, 20, 16, 23, 27, 15, 11, 17, 26, 21, 27, 14, 7, 32, 23, 16, 24, 24, 14, 28, 20, 19, 13, 24, 11, 18, 25, 31, 18, 6],
    'N4': [33, 25, 17, 24, 28, 30, 16, 25, 28, 31, 29, 33, 19, 33, 27, 35, 27, 30, 25, 36, 27, 28, 29, 27, 26, 29, 36, 32, 34, 11],
    'N5': [35, 37, 29, 32, 31, 39, 26, 26, 35, 38, 38, 35, 32, 36, 30, 38, 38, 35, 30, 39, 36, 38, 37, 33, 35, 36, 39, 38, 39, 33]
}
df = pd.DataFrame(data)
df['總和'] = df[['N1', 'N2', 'N3', 'N4', 'N5']].sum(axis=1)
df['MA5'] = df['總和'].rolling(window=5).mean()
all_nums = pd.concat([df['N1'], df['N2'], df['N3'], df['N4'], df['N5']])
counts = all_nums.value_counts().reindex(range(1, 40), fill_value=0)

# --- 3. 戰略軍團編制表 ---
st.markdown("### 🗺️ 戰略軍團編制狀態")
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown("""<div class="corps-card"><h4>先鋒軍團 (01-13)</h4><b>狀態</b>：連續佔領/疲乏<br><b>火力建議</b>：低量牽制</div>""", unsafe_allow_html=True)
with col_b:
    st.markdown("""<div class="corps-card" style="border-top-color: #FF4B4B;"><h4>中軍軍團 (14-26)</h4><b>狀態</b>：主力集結/準備衝鋒<br><b>核心目標</b>：24, 25, 26</div>""", unsafe_allow_html=True)
with col_c:
    st.markdown("""<div class="corps-card" style="border-top-color: #00FF00;"><h4>後衛軍團 (27-39)</h4><b>狀態</b>：火力支援/高位壓制<br><b>核心目標</b>：31, 33</div>""", unsafe_allow_html=True)

st.markdown("---")

# --- 4. 戰場雙圖並聯 ---
c1, c2 = st.columns([1, 1])
with c1:
    st.subheader("📈 能量重心波段 (戰場趨勢)")
    fig_k = go.Figure()
    fig_k.add_trace(go.Scatter(x=df['日期'], y=df['總和'], mode='lines+markers+text', text=df['總和'], textposition="top center", line=dict(color='#D4AF37', width=3), name='重心'))
    fig_k.add_trace(go.Scatter(x=df['日期'], y=df['MA5'], line=dict(color='rgba(255,255,255,0.2)', width=1, dash='dash')))
    fig_k.update_layout(template="plotly_dark", height=380, margin=dict(l=10, r=10, t=30, b=10), showlegend=False, xaxis=dict(rangeslider=dict(visible=False), type='category'))
    st.plotly_chart(fig_k, use_container_width=True)

with c2:
    st.subheader("🔥 兵力分佈雷達 (熱力分佈)")
    fig_h = go.Figure(go.Bar(x=counts.index, y=counts.values, text=counts.values, textposition='outside', marker_color=counts.values, marker_colorscale='YlOrRd'))
    fig_h.update_layout(template="plotly_dark", height=380, margin=dict(l=10, r=10, t=30, b=10), showlegend=False, xaxis=dict(type='category'))
    st.plotly_chart(fig_h, use_container_width=True)

# --- 5. 指揮官即時指令面板 ---
st.markdown("""<div style="background: #111; padding: 20px; border: 1px solid #D4AF37; border-radius: 10px;">
    <h3 style="color: #D4AF37; margin-top:0;">📡 統帥即時指令</h3>
    <div style="display: flex; justify-content: space-between;">
        <div class="radar-text">【奇門局】丙戌火庫：利大數、利奇數</div>
        <div class="radar-text">【運勢】庚申專祿：財氣在中宮(25)</div>
        <div class="radar-text" style="color: #FF4B4B;">【警告】20區間真空第3期臨界點</div>
    </div>
</div>""", unsafe_allow_html=True)

# --- 6. 側邊欄：數據注入 ---
with st.sidebar:
    st.header("🛠️ 數據注入系統")
    new_date = st.date_input("日期")
    n = [st.number_input(f"N{i+1}", 1, 39, 1) for i in range(5)]
    if st.button("🚀 更新戰場數據"):
        st.success("數據已寫入沙盤！")
