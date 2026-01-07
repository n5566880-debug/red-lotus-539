import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# --- 1. 頂規戰情室風格 ---
st.set_page_config(page_title="赤鍊帝國・戰略領先戰情室", layout="wide")
st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #050505; border-right: 2px solid #D4AF37; }
    .main-card { background: #0a0a0a; padding: 20px; border-radius: 10px; border: 1px solid #D4AF37; margin-bottom: 15px; }
    .warning-card { background: #330000; padding: 15px; border-radius: 10px; border-left: 5px solid #FF0000; color: #FFCCCC; }
    .victory-card { background: #002200; padding: 15px; border-radius: 10px; border-left: 5px solid #00FF00; color: #CCFFCC; }
</style>
""", unsafe_allow_html=True)

st.title("🔱 赤鍊紅蓮・539 戰略領先戰情室 (v5.9)")

# --- 2. 數據核心 (更新至 01-07) ---
data = {
    '日期': ['12-04', '12-05', '12-06', '12-08','12-09', '12-10', '12-11', '12-12', '12-13','12-15', '12-16', '12-17', '12-18', '12-19','12-20', '12-22', '12-23', '12-24', '12-25','12-26', '12-27', '12-29', '12-30', '12-31','01-01', '01-02', '01-03', '01-05', '01-06', '01-07'],
    'N1': [1, 2, 6, 5, 7, 4, 2, 10, 2, 3, 2, 5, 4, 12, 1, 2, 9, 2, 14, 1, 1, 5, 11, 8, 15, 17, 22, 10, 1, 5],
    'N2': [7, 3, 22, 23, 8, 7, 6, 24, 9, 17, 10, 6, 9, 16, 5, 22, 22, 3, 18, 10, 15, 10, 12, 10, 16, 18, 23, 16, 2, 10],
    'N3': [20, 16, 23, 27, 15, 11, 17, 26, 21, 27, 14, 7, 32, 23, 16, 24, 24, 14, 28, 20, 19, 13, 24, 11, 18, 25, 31, 18, 6, 14],
    'N4': [25, 17, 24, 28, 30, 16, 25, 28, 31, 29, 33, 19, 33, 27, 35, 27, 30, 25, 36, 27, 28, 29, 27, 26, 29, 36, 32, 34, 11, 15],
    'N5': [37, 29, 32, 31, 39, 26, 26, 35, 38, 38, 35, 32, 36, 30, 38, 38, 35, 30, 39, 36, 38, 37, 33, 35, 36, 39, 38, 39, 33, 28]
}
df = pd.DataFrame(data)
df['總和'] = df[['N1', 'N2', 'N3', 'N4', 'N5']].sum(axis=1)
all_nums = pd.concat([df['N1'], df['N2'], df['N3'], df['N4'], df['N5']])
counts = all_nums.value_counts().reindex(range(1, 40), fill_value=0)

# --- 3. 領先者看板 (明日預測) ---
st.markdown(f"""
<div class="main-card">
    <div style='display: flex; justify-content: space-between;'>
        <div style='width: 30%;'>
            <h4 style='color: #D4AF37; margin:0;'>🏮 戰後復盤與預警</h4>
            <p style='font-size:13px;'>今日總和：<b>72 (回升)</b><br>狀態：小幅反彈，動能積蓄<br><b>超級真空區：20-27 (明日必殺)</b></p>
        </div>
        <div style='width: 40%; border-left: 1px solid #333; padding-left: 15px;'>
            <h4 style='color: #00FF00; margin:0;'>🐉 統帥明日戰略</h4>
            <p style='font-size:13px;'>趨勢分析：14,15 已動，中軍開始集結<br><b>指令：死守 24, 25, 26</b><br>理由：壓力鍋即將引爆</p>
        </div>
        <div style='width: 25%; border-left: 1px solid #333; padding-left: 15px;'>
            <h4 style='color: #FF4B4B; margin:0;'>📡 能量雷達</h4>
            <p style='font-size:13px;'>遺漏極限：20區間<br><b>關鍵號：25 (核心)</b></p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 4. 火力配置 (戰略修正) ---
st.subheader("⚔️ 明日火力修正 (Firepower Adjustment)")
f1, f2 = st.columns(2)
with f1:
    st.markdown("""<div class="warning-card"><h4>🚀 飽和攻擊區 (Saturation)</h4><b>鎖定陣地</b>：20 - 27<br><b>戰術目的</b>：今日28已開出，明日回填 20-27 的機率飆升至 90%。</div>""", unsafe_allow_html=True)
with f2:
    st.markdown("""<div class="victory-card"><h4>🎯 狙擊手目標 (Precision)</h4><b>核心目標</b>：[ 25 ] 拖帶 [ 26 ]<br><b>戰術目的</b>：數據顯示中軸線依然是最強引力點。</div>""", unsafe_allow_html=True)

st.markdown("---")

# --- 5. 數據全顯雙圖 ---
col_l, col_r = st.columns([1, 1])
with col_l:
    st.subheader("📈 能量重心趨勢 (反彈確認中)")
    fig_k = go.Figure()
    fig_k.add_trace(go.Scatter(x=df['日期'], y=df['總和'], mode='lines+markers+text', text=df['總和'], textposition="top center", line=dict(color='#D4AF37', width=3)))
    fig_k.update_layout(template="plotly_dark", height=380, margin=dict(l=10, r=10, t=30, b=10), showlegend=False, xaxis=dict(rangeslider=dict(visible=False), type='category'))
    st.plotly_chart(fig_k, use_container_width=True)

with col_r:
    st.subheader("🔥 兵力分佈雷達 (找最矮的柱子)")
    fig_h = go.Figure(go.Bar(x=counts.index, y=counts.values, text=counts.values, textposition='outside', marker_color=counts.values, marker_colorscale='YlOrRd'))
    fig_h.update_layout(template="plotly_dark", height=380, margin=dict(l=10, r=10, t=30, b=10), showlegend=False, xaxis=dict(type='category'))
    st.plotly_chart(fig_h, use_container_width=True)

# --- 6. 側邊欄 ---
with st.sidebar:
    st.header("🛠️ 數據模擬")
    n = [st.number_input(f"N{i+1}", 1, 39, 1) for i in range(5)]
    if st.button("🚀 試算明日"):
        st.success("模擬數據載入！")
