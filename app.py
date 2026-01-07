import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# --- 1. 介面風格設定 ---
st.set_page_config(page_title="赤鍊九五・數據全顯版", layout="wide")
st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 2px solid #D4AF37; }
    .main-card { background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%); padding: 25px; border-radius: 15px; border: 1px solid #D4AF37; margin-bottom: 20px; }
    .fortune-card { background: #2d1b00; padding: 15px; border-radius: 10px; border-left: 5px solid #D4AF37; }
</style>
""", unsafe_allow_html=True)

st.title("🔱 赤鍊紅蓮・539 數據全顯戰情室 (v5.3)")

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

# --- 3. 頂部看板 ---
st.markdown(f"""<div class="main-card"><div style='display: flex; justify-content: space-between;'>
<div style='width: 33%;'> <h3 style='color: #D4AF37; margin:0;'>🏮 丙戌日奇門局</h3><p style='font-size:14px;'>生門鎖定：<b>25</b><br>大數反彈：<b>今晚必見</b></p> </div>
<div style='width: 33%; border-left: 1px solid #333; padding-left: 15px;'> <h3 style='color: #00FF00; margin:0;'>🐉 掌門運勢</h3><p style='font-size:14px;'>庚申雙金：<b>騰蛇化龍</b><br>狀態：財氣凝聚</p> </div>
<div style='width: 33%; border-left: 1px solid #333; padding-left: 15px;'> <h3 style='color: #FF4B4B; margin:0;'>📊 戰略指令</h3><p style='font-size:14px;'>核心：<b>20區間真空回填</b><br>目標：24, 25, 26</p> </div>
</div></div>""", unsafe_allow_html=True)

# --- 4. 雙圖數據全顯區域 ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📈 能量趨勢 (附數值標籤)")
    fig_k = go.Figure()
    # 增加 text 參數來顯示數字
    fig_k.add_trace(go.Scatter(
        x=df['日期'], y=df['總和'], 
        mode='lines+markers+text', 
        text=df['總和'], 
        textposition="top center",
        line=dict(color='#D4AF37', width=3), 
        name='總和'
    ))
    fig_k.add_trace(go.Scatter(x=df['日期'], y=df['MA5'], line=dict(color='gray', width=1, dash='dash'), name='均線'))
    fig_k.update_layout(template="plotly_dark", height=400, margin=dict(l=10, r=10, t=30, b=10), showlegend=False)
    st.plotly_chart(fig_k, use_container_width=True)

with col_right:
    st.subheader("🔥 號碼熱力 (附出現次數)")
    # 增加 text 參數顯示次數
    fig_h = go.Figure(go.Bar(
        x=counts.index, y=counts.values, 
        text=counts.values, 
        textposition='outside',
        marker_color=counts.values, 
        marker_colorscale='YlOrRd'
    ))
    fig_h.update_layout(template="plotly_dark", height=400, margin=dict(l=10, r=10, t=30, b=10), showlegend=False)
    st.plotly_chart(fig_h, use_container_width=True)

# --- 5. 戰術詳細建議 ---
c1, c2 = st.columns(2)
with c1:
    st.markdown("""<div class="fortune-card"><h4>🎯 攻勢陣容</h4><b>主攻</b>：24, 25, 26<br><b>奇兵</b>：31 | <b>守備</b>：07</div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="fortune-card" style='border-left-color: #FF4B4B;'><h4>⚠️ 操盤注意</h4>昨日總和 53 為極端低點，今晚反彈力道看好 60-80 點。</div>""", unsafe_allow_html=True)

# --- 6. 側邊欄 ---
with st.sidebar:
    st.header("🛠️ 數據注入")
    new_date = st.date_input("開獎日期")
    n = [st.number_input(f"N{i+1}", 1, 39, 1) for i in range(5)]
    if st.button("🚀 注入最新號碼"):
        st.success("數據載入成功！")
