import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# --- 1. 介面與金庫風格 ---
st.set_page_config(page_title="赤鍊九五・雙圖並聯版", layout="wide")
st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 2px solid #D4AF37; }
    .main-card { background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%); padding: 25px; border-radius: 15px; border: 1px solid #D4AF37; margin-bottom: 20px; }
    .fortune-card { background: #2d1b00; padding: 15px; border-radius: 10px; border-left: 5px solid #D4AF37; }
</style>
""", unsafe_allow_html=True)

st.title("🔱 赤鍊紅蓮・539 雙圖並聯戰情室 (v5.2)")

# --- 2. 數據核心 (30期真實數據) ---
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
all_nums = pd.concat([df['N1'], df['N2'], df['N3'], df['N4'], df['N5']])
counts = all_nums.value_counts().reindex(range(1, 40), fill_value=0)

# --- 3. 頂部看板 ---
st.markdown(f"""<div class="main-card"><div style='display: flex; justify-content: space-between;'>
<div style='width: 33%;'> <h3 style='color: #D4AF37; margin:0;'>🏮 丙戌日奇門局</h3><p style='font-size:14px;'>生門鎖定：<b>25</b><br>大數反彈機率：<b>極高</b></p> </div>
<div style='width: 33%; border-left: 1px solid #333; padding-left: 15px;'> <h3 style='color: #00FF00; margin:0;'>🐉 掌門運勢</h3><p style='font-size:14px;'>庚申金旺：<b>適合重兵佈署</b><br>狀態：騰蛇化龍</p> </div>
<div style='width: 33%; border-left: 1px solid #333; padding-left: 15px;'> <h3 style='color: #FF4B4B; margin:0;'>📊 指令狀態</h3><p style='font-size:14px;'>當前建議：<b>全力突擊 20 區間</b><br>真空期：2 期未開</p> </div>
</div></div>""", unsafe_allow_html=True)

# --- 4. 雙圖並聯區域 ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📈 能量趨勢 K 線")
    fig_k = go.Figure()
    fig_k.add_trace(go.Scatter(x=df['日期'], y=df['總和'], mode='lines+markers', line=dict(color='#D4AF37', width=3), name='總和趨勢'))
    fig_k.add_trace(go.Scatter(x=df['日期'], y=df['MA5'], line=dict(color='gray', width=1, dash='dash'), name='5日均線'))
    fig_k.update_layout(template="plotly_dark", height=350, margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
    st.plotly_chart(fig_k, use_container_width=True)

with col_right:
    st.subheader("🔥 號碼熱力分佈")
    fig_h = go.Figure(go.Bar(x=counts.index, y=counts.values, marker_color=counts.values, marker_colorscale='YlOrRd'))
    fig_h.update_layout(template="plotly_dark", height=350, margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
    st.plotly_chart(fig_h, use_container_width=True)

# --- 5. 戰術詳細建議 ---
c1, c2 = st.columns(2)
with c1:
    st.markdown("""<div class="fortune-card"><h4>🎯 攻勢陣容</h4><b>主攻</b>：24, 25, 26<br><b>奇兵</b>：31 | <b>守備</b>：07</div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="fortune-card" style='border-left-color: #FF4B4B;'><h4>⚠️ 操盤注意</h4>避開 01, 02 連號回踩。鎖定 20 區間真空回填。</div>""", unsafe_allow_html=True)

# --- 6. 側邊欄 ---
with st.sidebar:
    st.header("🛠️ 數據注入")
    new_date = st.date_input("開獎日期")
    n = [st.number_input(f"N{i+1}", 1, 39, 1) for i in range(5)]
    if st.button("🚀 注入最新號碼"):
        st.success("數據載入成功！")
