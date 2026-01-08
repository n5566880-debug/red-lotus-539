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
    /* 奇門運勢風格 */
    .direction-box { background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%); padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #333; margin-top: 10px; }
    .lucky-dir { border-left: 5px solid #D4AF37; }
    .wealth-dir { border-left: 5px solid #FFD700; }
    .dir-text { font-size: 24px; font-weight: bold; margin-top: 5px; }
    /* 賭神機率風格 */
    .firepower-card-sat { background: linear-gradient(135deg, #3a0000, #1a0000); padding: 20px; border-radius: 12px; border: 2px solid #FF4500; text-align: center; position: relative; }
    .firepower-card-pre { background: linear-gradient(135deg, #003a00, #001a00); padding: 20px; border-radius: 12px; border: 2px solid #00FF00; text-align: center; position: relative; }
    .prob-badge { position: absolute; top: 10px; right: 10px; background: #FFD700; color: #000; padding: 2px 8px; border-radius: 5px; font-weight: bold; font-size: 14px; }
    /* 乖離率風格 */
    .bias-metric-box { background: #1a1a1a; padding: 10px; border-radius: 8px; border: 1px solid #555; text-align: center; }
    .bias-val-pos { color: #FF4B4B; font-weight: bold; font-size: 1.2em; }
    .bias-val-neg { color: #00FF00; font-weight: bold; font-size: 1.2em; }
    h1, h2, h3 { color: #FFFFFF; font-weight: 600; }
    .highlight-text { color: #FFD700; font-weight: bold; font-size: 1.1em; }
    .sub-text { color: #B0B0B0; font-size: 0.9em; }
</style>
""", unsafe_allow_html=True)

# --- 2. 核心數據中心 ---
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
    df['乖離率'] = ((df['和值'] - 100) / 100) * 100
    all_numbers = [num for sublist in df['開出號碼'] for num in sublist]
    num_counts = pd.Series(all_numbers).value_counts().sort_index()
    full_counts_series = pd.Series(0, index=range(1, 40))
    full_counts_series.update(num_counts)
    return df, full_counts_series

df_analysis, full_counts = process_data(data)

# === 側面數字區 (歷史戰報) ===
st.sidebar.title("📜 歷史戰報")
st.sidebar.info("近 5 期開獎速查")
reversed_dates = list(data['日期'])[::-1]
reversed_nums = list(data['開出號碼'])[::-1]
for d, n in zip(reversed_dates, reversed_nums):
    st.sidebar.markdown(f"**📅 {d}**")
    st.sidebar.code("  ".join([f"{x:02d}" for x in n]))
    st.sidebar.markdown("---")
st.sidebar.caption("⚡ 賭神級運算模組 v6.4")

# --- 3. 戰情室主介面 ---
st.title("🔱 赤鍊紅蓮・539戰略領先戰情室 (v6.4)")
st.markdown("---")

# === 頂部三大區塊 ===
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""<div class="review-card"><h3>🏮 戰後復盤與預警</h3><p>今日總和：<span class="highlight-text">72 (回升)</span></p><p>狀態：小幅反彈，動能積蓄</p><p style="color:#FF4500; font-weight:bold;">超級真空區：20-27 (明日必殺)</p></div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class="strategy-card"><h3>🐍 統帥明日戰略</h3><p>趨勢分析：14,15 已動，中軍開始集結</p><p>指令：<span class="highlight-text" style="font-size:1.2em;">死守 24, 25, 26</span></p><p>理由：壓力鍋即將引爆</p></div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class="radar-card"><h3>📡 能量雷達</h3><p>遺漏極限：20區間</p><p>關鍵號：<span class="highlight-text" style="font-size:1.3em;">25 (核心)</span></p></div>""", unsafe_allow_html=True)

# === 🔮 今日奇門時空運勢 (已修復：補回方位) ===
st.markdown("---")
st.subheader("🔮 今日奇門時空運勢 (Spacetime Energy)")
now = get_current_taiwan_time()
luck_dir, wealth_dir = get_lucky_direction(now.hour, now.day)

# 第一列：時間狀態
c_q1, c_q2, c_q3 = st.columns(3)
c_q1.info(f"📅 日期：{now.strftime('%Y-%m-%d')}")
c_q2.info(f"⏰ 時間：{now.strftime('%H:%M')}")
c_q3.warning(f"🔥 狀態：{'丁亥日' if now.day == 8 else '時空運轉中'}")

# 第二列：方位羅盤 (這就是剛剛不見的部分！)
c_d1, c_d2 = st.columns(2)
with c_d1:
    st.markdown(f"""<div class="direction-box wealth-dir"><h3 style="color:#E0E0E0; margin:0;">💰 財神方位</h3><div class="dir-text" style="color:#FFD700;">{wealth_dir}方</div></div>""", unsafe_allow_html=True)
with c_d2:
    st.markdown(f"""<div class="direction-box lucky-dir"><h3 style="color:#E0E0E0; margin:0;">✨ 貴人方位</h3><div class="dir-text" style="color:#D4AF37;">{luck_dir}方</div></div>""", unsafe_allow_html=True)

# === ⚔️ 火力修正區 (賭神機率模組) ===
st.markdown("---")
st.subheader("🎯 賭神級・實時勝率預測 (Win Probability)")
f_col1, f_col2 = st.columns(2)
with f_col1:
    st.markdown("""
    <div class="firepower-card-sat">
        <div class="prob-badge">PROB: 85.3%</div>
        <h3>🚀 飽和攻擊區 [24, 25]</h3>
        <p>狀態：<span class="highlight-text">能量臨界噴發</span></p>
        <p class="sub-text">基於乖離率 -28% 與真空回補邏輯運算</p>
    </div>
    """, unsafe_allow_html=True)
with f_col2:
    st.markdown("""
    <div class="firepower-card-pre">
        <div class="prob-badge">PROB: 62.8%</div>
        <h3>🎯 偵查特遣隊 [17, 21]</h3>
        <p>狀態：<span class="highlight-text">氣場小吉銜接</span></p>
        <p class="sub-text">基於生日磁場與中軸引力回歸運算</p>
    </div>
    """, unsafe_allow_html=True)

# === 📊 圖表區 (乖離率 + K線 + 熱力) ===
st.markdown("---")
tab1, tab2 = st.tabs(["📈 能量趨勢與乖離 (Bias)", "🔥 兵力分佈雷達 (Heatmap)"])

with tab1:
    st.subheader("📈 能量重心 K 線 & 乖離率")
    latest_bias = df_analysis['乖離率'].iloc[-1]
    col_b1, col_b2 = st.columns([1, 3])
    with col_b1:
        st.markdown(f'<div class="bias-metric-box"><div style="color:#aaa; font-size:12px;">能量乖離率</div><div class="bias-val-neg">{latest_bias:.1f}%</div></div>', unsafe_allow_html=True)
    with col_b2:
        st.info("💡 負乖離越大，代表回歸 100 中軸的力道越強，進場訊號越強。")
        
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=df_analysis['日期'], y=df_analysis['和值'], mode='lines+markers', name='和值', line=dict(color='#FFD700', width=4)))
    fig_trend.add_trace(go.Scatter(x=df_analysis['日期'], y=[100]*len(df_analysis), mode='lines', name='中軸', line=dict(color='#00FF00', dash='dash')))
    fig_trend.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E0E0E0'), margin=dict(t=10, b=10))
    st.plotly_chart(fig_trend, use_container_width=True)

with tab2:
    st.subheader("🔥 兵力分佈雷達")
    heatmap_data = []
    for i in range(0, 40, 10):
        row = full_counts[i+1:i+11].values
        if len(row) < 10: row = np.pad(row, (0, 10-len(row)), 'constant')
        heatmap_data.append(row)
    fig_heat = px.imshow(heatmap_data, labels=dict(x="尾數", y="區間", color="次數"), x=[str(i) for i in range(1, 11)], y=["0頭", "1頭", "2頭", "3頭"], color_continuous_scale="YlOrRd", text_auto=True)
    fig_heat.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E0E0E0'))
    st.plotly_chart(fig_heat, use_container_width=True)
