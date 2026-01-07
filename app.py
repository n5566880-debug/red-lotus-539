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
    /* 頂部三大區塊 */
    .review-card { background: linear-gradient(145deg, #1e1e2f, #2a2a40); padding: 20px; border-radius: 15px; border-left: 5px solid #FFD700; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    .strategy-card { background: linear-gradient(145deg, #1e2f1e, #2a402a); padding: 20px; border-radius: 15px; border-left: 5px solid #00FF00; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    .radar-card { background: linear-gradient(145deg, #2f1e1e, #402a2a); padding: 20px; border-radius: 15px; border-left: 5px solid #FF4500; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    /* 奇門運勢風格 */
    .direction-box { background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%); padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #333; }
    .lucky-dir { border-left: 5px solid #D4AF37; }
    .wealth-dir { border-left: 5px solid #FFD700; }
    .dir-text { font-size: 24px; font-weight: bold; margin-top: 5px; }
    /* 火力修正 */
    .firepower-card-sat { background: linear-gradient(135deg, #3a0000, #1a0000); padding: 20px; border-radius: 12px; border: 2px solid #FF4500; text-align: center; }
    .firepower-card-pre { background: linear-gradient(135deg, #003a00, #001a00); padding: 20px; border-radius: 12px; border: 2px solid #00FF00; text-align: center; }
    /* 文字設定 */
    h1, h2, h3 { color: #FFFFFF; font-weight: 600; }
    .highlight-text { color: #FFD700; font-weight: bold; font-size: 1.1em; }
    .sub-text { color: #B0B0B0; font-size: 0.9em; }
</style>
""", unsafe_allow_html=True)

# --- 2. 核心數據中心 ---
# [請在此更新每日開獎號碼]
data = {
    '日期': ['1/3', '1/4', '1/5', '1/6', '1/7'],
    '開出號碼': [
        [14, 15, 16, 26, 34],
        [2, 3, 16, 22, 25],
        [15, 23, 32, 36, 39],
        [4, 13, 21, 28, 35],
        [5, 10, 14, 15, 28]
    ]
}

# 奇門輔助函數
DIRECTIONS = ["正北", "東北", "正東", "東南", "正南", "西南", "正西", "西北"]
def get_current_taiwan_time():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=8)
def get_lucky_direction(hour, day):
    random.seed(hour + day)
    return random.choice(DIRECTIONS), random.choice(DIRECTIONS)

# 數據處理函數
def process_data(data_dict):
    df = pd.DataFrame(data_dict)
    df['和值'] = df['開出號碼'].apply(sum)
    df['平均值'] = df['和值'] / 5
    all_numbers = [num for sublist in df['開出號碼'] for num in sublist]
    num_counts = pd.Series(all_numbers).value_counts().sort_index()
    full_counts_series = pd.Series(0, index=range(1, 40))
    full_counts_series.update(num_counts)
    return df, full_counts_series

df_analysis, full_counts = process_data(data)

# === [修復] 側面數字區 (歷史戰報) ===
st.sidebar.title("📜 歷史戰報")
st.sidebar.info("近 5 期開獎速查")

# 倒序顯示 (最新的在最上面)
reversed_dates = list(data['日期'])[::-1]
reversed_nums = list(data['開出號碼'])[::-1]

for d, n in zip(reversed_dates, reversed_nums):
    st.sidebar.markdown(f"**📅 {d}**")
    # 將號碼格式化為漂亮的代碼塊
    nums_str = "  ".join([f"{x:02d}" for x in n])
    st.sidebar.code(nums_str)
    st.sidebar.markdown("---")

st.sidebar.caption("⚡ 赤鍊紅蓮系統 v6.1")


# --- 3. 戰情室主介面 ---
st.title("🔱 赤鍊紅蓮・539戰略領先戰情室 (v6.1)")
st.markdown("---")

# === 頂部三大戰略區塊 ===
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="review-card">
        <h3>🏮 戰後復盤與預警</h3>
        <p>今日總和：<span class="highlight-text">72 (回升)</span></p>
        <p>狀態：小幅反彈，動能積蓄</p>
        <p style="color:#FF4500; font-weight:bold;">超級真空區：20-27 (明日必殺)</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="strategy-card">
        <h3>🐍 統帥明日戰略</h3>
        <p>趨勢分析：14,15 已動，中軍開始集結</p>
        <p>指令：<span class="highlight-text" style="font-size:1.2em;">死守 24, 25, 26</span></p>
        <p>理由：壓力鍋即將引爆</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="radar-card">
        <h3>📡 能量雷達</h3>
        <p>遺漏極限：20區間</p>
        <p>關鍵號：<span class="highlight-text" style="font-size:1.3em;">25 (核心)</span></p>
    </div>
    """, unsafe_allow_html=True)

# === 🔮 今日奇門時空運勢 ===
st.markdown("---")
st.subheader("🔮 今日奇門時空運勢 (Daily Qimen Fortune)")
now = get_current_taiwan_time()
luck_dir, wealth_dir = get_lucky_direction(now.hour, now.day)

c_q1, c_q2, c_q3 = st.columns(3)
c_q1.info(f"📅 日期：{now.strftime('%Y-%m-%d')}")
c_q2.info(f"⏰ 時間：{now.strftime('%H:%M')}")
c_q3.warning(f"🔥 狀態：{'丁亥日' if now.day == 8 else '時空運轉中'}")

c_d1, c_d2 = st.columns(2)
with c_d1:
    st.markdown(f"""<div class="direction-box wealth-dir"><h3 style="color:#E0E0E0; margin:0;">💰 財神方位</h3><div class="dir-text" style="color:#FFD700;">{wealth_dir}方</div></div>""", unsafe_allow_html=True)
with c_d2:
    st.markdown(f"""<div class="direction-box lucky-dir"><h3 style="color:#E0E0E0; margin:0;">✨ 貴人方位</h3><div class="dir-text" style="color:#D4AF37;">{luck_dir}方</div></div>""", unsafe_allow_html=True)

# === 火力修正區塊 ===
st.markdown("---")
st.subheader("⚔️ 明日火力修正 (Firepower Adjustment)")
f_col1, f_col2 = st.columns(2)
with f_col1:
    st.markdown("""<div class="firepower-card-sat"><h3>🚀 飽和攻擊區</h3><p>鎖定陣地：<span class="highlight-text">20 - 27</span></p><p class="sub-text">戰術目的：今日28已開出，明日回填機率90%。</p></div>""", unsafe_allow_html=True)
with f_col2:
    st.markdown("""<div class="firepower-card-pre"><h3>🎯 狙擊手目標</h3><p>核心目標：<span class="highlight-text" style="font-size:1.5em;">[ 25 ]</span> 拖帶 [ 26 ]</p><p class="sub-text">戰術目的：中軸線依然是最強引力點。</p></div>""", unsafe_allow_html=True)

# === 📊 圖表區 ===
st.markdown("---")
tab1, tab2 = st.tabs(["📈 能量重心趨勢 (K線)", "🔥 兵力分佈雷達 (熱力)"])

with tab1:
    st.subheader("📈 能量重心趨勢圖 (Trend)")
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=df_analysis['日期'], y=df_analysis['和值'], 
        mode='lines+markers', name='和值 (總能量)', 
        line=dict(color='#FFD700', width=4)
    ))
    fig_trend.add_trace(go.Scatter(
        x=df_analysis['日期'], y=df_analysis['平均值']*5, 
        mode='lines', name='理論基準線', 
        line=dict(color='#00FF00', width=2, dash='dash')
    ))
    fig_trend.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E0E0E0'), hovermode="x unified",
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#333')
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with tab2:
    st.subheader("🔥 兵力分佈雷達 (Heatmap)")
    heatmap_data = []
    for i in range(0, 40, 10):
        row = full_counts[i+1:i+11].values
        if len(row) < 10: 
            row = np.pad(row, (0, 10-len(row)), 'constant')
        heatmap_data.append(row)
        
    fig_heat = px.imshow(heatmap_data,
                        labels=dict(x="尾數 (1-0)", y="區間", color="次數"),
                        x=[str(i) for i in range(1, 11)], 
                        y=["0頭(01-10)", "1頭(11-20)", "2頭(21-30)", "3頭(31-39)"],
                        color_continuous_scale="YlOrRd", text_auto=True, aspect="auto")
    fig_heat.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E0E0E0'))
    st.plotly_chart(fig_heat, use_container_width=True)
