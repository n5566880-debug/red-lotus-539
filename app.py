
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# --- 1. 軍事戰情室風格 ---
st.set_page_config(page_title="赤鍊九五・火力全開版", layout="wide")
st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #050505; border-right: 2px solid #D4AF37; }
    .main-card { background: #111; padding: 20px; border-radius: 10px; border: 1px solid #D4AF37; }
    .fire-power { background: #220000; padding: 15px; border-radius: 8px; border-left: 5px solid #FF4B4B; }
    .precision { background: #001a00; padding: 15px; border-radius: 8px; border-left: 5px solid #00FF00; }
</style>
""", unsafe_allow_html=True)

st.title("⚔️ 赤鍊紅蓮・539 火力配置戰情室 (v5.6)")

# --- 2. 數據核心 ---
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
all_nums = pd.concat([df['N1'], df['N2'], df['N3'], df['N4'], df['N5']])
counts = all_nums.value_counts().reindex(range(1, 40), fill_value=0)

# --- 3. 新增：火力配置建議面板 ---
st.markdown("### 💥 今日火力配置建議 (Firepower Allocation)")
f1, f2 = st.columns(2)
with f1:
    st.markdown("""<div class="fire-power">
        <h4 style='color: #FF4B4B;'>🚀 彈幕覆蓋 (Saturation)</h4>
        <b>方式：地毯式搜索 (二星連碰)</b><br>
        <b>目標陣地</b>：[24, 25, 26] 區間<br>
        <b>說明</b>：針對能量斷層進行小範圍火力壓制，捕捉反彈。
    </div>""", unsafe_allow_html=True)
with f2:
    st.markdown("""<div class="precision">
        <h4 style='color: #00FF00;'>🎯 精準打擊 (Precision)</h4>
        <b>方式：定點斬首 (坐車/獨資)</b><br>
        <b>鎖定座標</b>：[ 25 ]<br>
        <b>說明</b>：命盤氣場最強點，今日奇門陣眼，執行高價值打擊。
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# --- 4. 戰場雙圖 ---
c1, c2 = st.columns([1, 1])
with c1:
    st.subheader("📈 能量重心波段")
    fig_k = go.Figure()
    fig_k.add_trace(go.Scatter(x=df['日期'], y=df['總和'], mode='lines+markers+text', text=df['總和'], textposition="top center", line=dict(color='#D4AF37', width=3)))
    fig_k.update_layout(template="plotly_dark", height=350, margin=dict(l=10, r=10, t=30, b=10), showlegend=False, xaxis=dict(rangeslider=dict(visible=False), type='category'))
    st.plotly_chart(fig_k, use_container_width=True)

with c2:
    st.subheader("🔥 兵力分佈雷達")
    fig_h = go.Figure(go.Bar(x=counts.index, y=counts.values, text=counts.values, textposition='outside', marker_color=counts.values, marker_colorscale='YlOrRd'))
    fig_h.update_layout(template="plotly_dark", height=350, margin=dict(l=10, r=10, t=30, b=10), showlegend=False, xaxis=dict(type='category'))
    st.plotly_chart(fig_h, use_container_width=True)

# --- 5. 側邊欄 ---
with st.sidebar:
    st.header("🛠️ 數據注入")
    n = [st.number_input(f"N{i+1}", 1, 39, 1) for i in range(5)]
    if st.button("🚀 更新戰場數據"):
        st.success("數據載入成功！")
