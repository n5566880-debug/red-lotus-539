import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# --- 1. 介面與金庫風格 ---
st.set_page_config(page_title="赤鍊九五・金庫終極版", layout="wide")
st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 2px solid #D4AF37; }
    .main-card { background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%); padding: 25px; border-radius: 15px; border: 1px solid #D4AF37; margin-bottom: 20px; }
    .fortune-card { background: #2d1b00; padding: 15px; border-radius: 10px; border-left: 5px solid #D4AF37; }
    .heatmap-box { background: #111; padding: 10px; border-radius: 10px; border: 1px solid #444; }
</style>
""", unsafe_allow_html=True)

st.title("🔱 赤鍊紅蓮・539 金庫終極戰情室 (v5.1)")

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
all_nums = pd.concat([df['N1'], df['N2'], df['N3'], df['N4'], df['N5']])
counts = all_nums.value_counts().reindex(range(1, 40), fill_value=0)

# --- 3. 奇門運勢與戰術頂部看板 ---
st.markdown(f"""
<div class="main-card">
    <div style='display: flex; justify-content: space-between;'>
        <div style='width: 30%;'>
            <h3 style='color: #D4AF37; margin-top: 0;'>🏮 丙戌日奇門局</h3>
            <p style='font-size: 14px;'>生門中宮：鎖定 <b>25</b><br>天盤丙火：利 <b>大數奇數</b><br>地盤專祿：20區間反彈</p>
        </div>
        <div style='width: 35%; border-left: 1px solid #333; padding-left: 15px;'>
            <h3 style='color: #00FF00; margin-top: 0;'>🐉 掌門運勢</h3>
            <p style='font-size: 14px;'>庚申金氣：<b>極旺</b><br>戰鬥建議：<b>宜守中帶攻</b><br>今日狀態：騰蛇化龍(利偏財)</p>
        </div>
        <div style='width: 30%; border-left: 1px solid #333; padding-left: 15px;'>
            <h3 style='color: #FF4B4B; margin-top: 0;'>⏱️ 吉時倒數</h3>
            <p style='font-size: 20px;'><b>封盤前最後衝刺</b></p>
            <p style='font-size: 12px;'>吉時：13:15-14:45 已過，進入暗合局。</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 4. 具體建議與注意事項 ---
c1, c2 = st.columns(2)
with c1:
    st.markdown("""<div class="fortune-card"><h4>🎯 戰術建議</h4>1. 進攻連碰：<b>24, 25, 26</b><br>2. 奇兵定位：<b>31</b><br>3. 防守防線：<b>07</b></div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="fortune-card" style='border-left-color: #FF4B4B;'><h4>⚠️ 注意事項</h4>1. 避開連號：01, 02 剛開，暫避連號。<br>2. 回填規律：20區間連斷2期必回填。</div>""", unsafe_allow_html=True)

st.markdown("---")

# --- 5. 號碼熱力分佈圖 (新增！) ---
st.subheader("🔥 30期冷熱號碼雷達")
fig_heat = px.bar(x=counts.index, y=counts.values, labels={'x':'號碼', 'y':'出現次數'}, color=counts.values, color_continuous_scale='YlOrRd')
fig_heat.update_layout(template="plotly_dark", height=300, margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig_heat, use_container_width=True)

# --- 6. 數據看板與趨勢 ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("昨日總和", 53, "-64")
m2.metric("推薦號碼", "25", "奇門定格")
m3.metric("真空預警", "20-29區間", "高機率")
m4.metric("金庫狀態", "準備噴發", "極限壓縮")

# --- 7. 側邊欄：數據注入 ---
with st.sidebar:
    st.header("🛠️ 數據注入")
    new_date = st.date_input("日期")
    n = [st.number_input(f"N{i+1}", 1, 39, 1) for i in range(5)]
    if st.button("🚀 注入數據"):
        st.success("成功！")
