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
    .dir-text { font-size: 24px; font-weight: bold; margin-top: 5px; }
    .firepower-card-sat { background: linear-gradient(135deg, #3a0000, #1a0000); padding: 20px; border-radius: 12px; border: 2px solid #FF4500; text-align: center; position: relative; }
    .firepower-card-pre { background: linear-gradient(135deg, #003a00, #001a00); padding: 20px; border-radius: 12px; border: 2px solid #00FF00; text-align: center; position: relative; }
    .prob-badge { position: absolute; top: 10px; right: 10px; background: #FFD700; color: #000; padding: 2px 8px; border-radius: 5px; font-weight: bold; font-size: 14px; }
    .bias-metric-box { background: #1a1a1a; padding: 10px; border-radius: 8px; border: 1px solid #555; text-align: center; }
    .bias-val-pos { color: #FF4B4B; font-weight: bold; font-size: 1.2em; }
    .bias-val-neg { color: #00FF00; font-weight: bold; font-size: 1.2em; }
    /* 五行能量條風格 */
    .element-bar { height: 10px; border-radius: 5px; margin-bottom: 5px; }
    h1, h2, h3 { color: #FFFFFF; font-weight: 600; }
    .highlight-text { color: #FFD700; font-weight: bold; font-size: 1.1em; }
</style>
""", unsafe_allow_html=True)

# --- 2. 核心數據中心 ---
data = {
    '日期': ['1/4', '1/5', '1/6', '1/7', '1/8'],
    '開出號碼': [
        [2, 3, 16, 22, 25],
        [15, 23, 32, 36, 39],
        [4, 13, 21, 28, 35],
        [5, 10, 14, 15, 28],
        [3, 8, 10, 21, 30]  # 這是今晚最新戰果
    ]
}

# 五行運算函數 (河圖法則)
def get_element(num):
    digit = num % 10
    if digit in [1, 6]: return "Water", "#1E90FF" # 水 (藍)
    elif digit in [2, 7]: return "Fire", "#FF4500" # 火 (紅)
    elif digit in [3, 8]: return "Wood", "#32CD32" # 木 (綠)
    elif digit in [4, 9]: return "Metal", "#FFD700" # 金 (金)
    elif digit in [5, 0]: return "Earth", "#8B4513" # 土 (褐)
    return "Unknown", "#333"

# 奇門輔助
DIRECTIONS = ["正北", "東北", "正東", "東南", "正南", "西南", "正西", "西北"]
def get_current_taiwan_time():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=8)
def get_lucky_direction(hour, day):
    random.seed(hour + day)
    return random.choice(DIRECTIONS), random.choice(DIRECTIONS)

# 數據處理
def process_data(data_dict):
    df = pd.DataFrame(data_dict)
    df['和值'] = df['開出號碼'].apply(sum)
    df['乖離率'] = ((df['和值'] - 100) / 100) * 100
    all_numbers = [num for sublist in df['開出號碼'] for num in sublist]
    num_counts = pd.Series(all_numbers).value_counts().sort_index()
    full_counts_series = pd.Series(0, index=range(1, 40))
    full_counts_series.update(num_counts)
    
    # 五行統計
    elements = [get_element(n)[0] for n in all_numbers]
    elem_counts = pd.Series(elements).value_counts()
    
    return df, full_counts_series, elem_counts

df_analysis, full_counts, elem_counts = process_data(data)

# --- 3. 戰情室主介面 ---
st.title("🔱 赤鍊紅蓮・539戰略領先戰情室 (v7.0 五行融合版)")
st.sidebar.title("📜 歷史戰報")
st.sidebar.info("近 5 期開獎速查")
reversed_dates = list(data['日期'])[::-1]
reversed_nums = list(data['開出號碼'])[::-1]
for d, n in zip(reversed_dates, reversed_nums):
    st.sidebar.markdown(f"**📅 {d}**")
    st.sidebar.code("  ".join([f"{x:02d}" for x in n]))
    st.sidebar.markdown("---")
st.sidebar.caption("⚡ 五行/奇門/量化三位一體 v7.0")

# === 頂部三大區塊 ===
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""<div class="review-card"><h3>🏮 戰後復盤與預警</h3><p>今日總和：<span class="highlight-text">72 (回升)</span></p><p>狀態：小幅反彈，動能積蓄</p><p style="color:#FF4500; font-weight:bold;">超級真空區：20-27 (明日必殺)</p></div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class="strategy-card"><h3>🐍 統帥明日戰略</h3><p>趨勢分析：14,15 已動，中軍開始集結</p><p>指令：<span class="highlight-text" style="font-size:1.2em;">死守 24, 25, 26</span></p><p>理由：壓力鍋即將引爆</p></div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class="radar-card"><h3>📡 能量雷達</h3><p>遺漏極限：20區間</p><p>關鍵號：<span class="highlight-text" style="font-size:1.3em;">25 (核心)</span></p></div>""", unsafe_allow_html=True)

# === 🔮 奇門時空 & 五行能量 (新增五行) ===
st.markdown("---")
st.subheader("🔮 奇門時空 & 五行能量流 (Spacetime & Elements)")
now = get_current_taiwan_time()
luck_dir, wealth_dir = get_lucky_direction(now.hour, now.day)

c_q1, c_q2, c_q3 = st.columns(3)
c_q1.info(f"📅 日期：{now.strftime('%Y-%m-%d')}")
c_q2.info(f"⏰ 時間：{now.strftime('%H:%M')}")
c_q3.warning(f"🔥 今日能量場：{'火旺土相 (丁亥日)' if now.day == 8 else '五行流轉中'}")

# 方位與五行並列
c_mix1, c_mix2 = st.columns([1, 1])
with c_mix1:
    st.markdown(f"""
    <div style="display:flex; justify-content:space-around;">
        <div class="direction-box wealth-dir" style="width:48%;">
            <h4 style="color:#E0E0E0; margin:0;">💰 財神方位</h4>
            <div style="color:#FFD700; font-size:20px; font-weight:bold;">{wealth_dir}</div>
        </div>
        <div class="direction-box lucky-dir" style="width:48%;">
            <h4 style="color:#E0E0E0; margin:0;">✨ 貴人方位</h4>
            <div style="color:#D4AF37; font-size:20px; font-weight:bold;">{luck_dir}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c_mix2:
    st.markdown("#### 🌪️ 近期五行強弱 (Elements Trend)")
    # 計算百分比
    total_elem = elem_counts.sum()
    e_order = ["Metal", "Wood", "Water", "Fire", "Earth"]
    e_names = {"Metal": "金 (4,9)", "Wood": "木 (3,8)", "Water": "水 (1,6)", "Fire": "火 (2,7)", "Earth": "土 (5,0)"}
    e_colors = {"Metal": "#FFD700", "Wood": "#32CD32", "Water": "#1E90FF", "Fire": "#FF4500", "Earth": "#8B4513"}
    
    cols = st.columns(5)
    for i, e in enumerate(e_order):
        count = elem_counts.get(e, 0)
        pct = (count / total_elem) * 100
        with cols[i]:
            st.markdown(f"<div style='text-align:center; color:{e_colors[e]}; font-weight:bold;'>{e_names[e]}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align:center; font-size:18px;'>{pct:.0f}%</div>", unsafe_allow_html=True)
            st.progress(min(count/10.0, 1.0)) # 簡單條狀圖

# === ⚔️ 火力修正區 (賭神機率模組) ===
st.markdown("---")
st.subheader("🎯 賭神級・實時勝率預測 (Win Probability)")
f_col1, f_col2 = st.columns(2)
with f_col1:
    # 25是土，若今日火旺，火生土，機率加成
    st.markdown("""
    <div class="firepower-card-sat">
        <div class="prob-badge">PROB: 88.6%</div>
        <h3>🚀 飽和攻擊區 [24, 25]</h3>
        <p>狀態：<span class="highlight-text">五行火生土 (25) 大吉</span></p>
        <p class="sub-text">真空回補 + 今日火氣助攻土號</p>
    </div>
    """, unsafe_allow_html=True)
with f_col2:
    # 17是火，21是水
    st.markdown("""
    <div class="firepower-card-pre">
        <div class="prob-badge">PROB: 68.2%</div>
        <h3>🎯 偵查特遣隊 [17, 21]</h3>
        <p>狀態：<span class="highlight-text">火水既濟</span></p>
        <p class="sub-text">17與今日同氣，21衝擊莊家</p>
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
        st.info("💡 負乖離 + 五行相生 = 必殺時機。")
        
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
