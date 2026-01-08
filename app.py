import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import random
import numpy as np

# --- 1. 頁面基礎設定 ---
st.set_page_config(page_title="赤鍊紅蓮・539戰情室", layout="wide", page_icon="🔱")

# --- CSS 美化 (全配版風格) ---
st.markdown("""
<style>
    .stApp { background-color: #121212; color: #E0E0E0; }
    /* 頂部戰略卡 */
    .review-card { background: linear-gradient(145deg, #1e1e2f, #2a2a40); padding: 20px; border-radius: 15px; border-left: 5px solid #FFD700; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    .strategy-card { background: linear-gradient(145deg, #1e2f1e, #2a402a); padding: 20px; border-radius: 15px; border-left: 5px solid #00FF00; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    .radar-card { background: linear-gradient(145deg, #2f1e1e, #402a2a); padding: 20px; border-radius: 15px; border-left: 5px solid #FF4500; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    
    /* 奇門方位與五行 */
    .direction-box { background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%); padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #333; height: 100%; display: flex; flex-direction: column; justify-content: center; }
    .lucky-dir { border-left: 5px solid #D4AF37; }
    .wealth-dir { border-left: 5px solid #FFD700; }
    .dir-text { font-size: 24px; font-weight: bold; margin-top: 5px; }

    /* 戰略核心區 (Action Zone) */
    .action-card { background: linear-gradient(135deg, #4b0000, #000000); padding: 20px; border-radius: 12px; border: 3px solid #FFD700; text-align: center; position: relative; }
    .monitor-card { background: linear-gradient(135deg, #001a33, #000000); padding: 20px; border-radius: 12px; border: 1px solid #1E90FF; text-align: center; position: relative; }
    .prob-badge { position: absolute; top: 10px; right: 10px; background: #FFD700; color: #000; padding: 2px 8px; border-radius: 5px; font-weight: bold; font-size: 14px; }
    
    /* 乖離率指標 */
    .bias-metric-box { background: #1a1a1a; padding: 10px; border-radius: 8px; border: 1px solid #555; text-align: center; }
    .bias-val-neg { color: #00FF00; font-weight: bold; font-size: 1.2em; }
    
    h1, h2, h3 { color: #FFFFFF; font-weight: 600; }
    .highlight-text { color: #FFD700; font-weight: bold; font-size: 1.1em; }
</style>
""", unsafe_allow_html=True)

# --- 2. 核心數據中心 (包含 1/8 最新戰果) ---
data = {
    '日期': ['1/4', '1/5', '1/6', '1/7', '1/8'],
    '開出號碼': [
        [2, 3, 16, 22, 25],
        [15, 23, 32, 36, 39],
        [4, 13, 21, 28, 35],
        [5, 10, 14, 15, 28],
        [3, 8, 10, 21, 30]  # 最新開獎
    ]
}

# 輔助函數群
DIRECTIONS = ["正北", "東北", "正東", "東南", "正南", "西南", "正西", "西北"]
def get_current_taiwan_time():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=8)
def get_lucky_direction(hour, day):
    random.seed(hour + day)
    return random.choice(DIRECTIONS), random.choice(DIRECTIONS)

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
st.title("🔱 赤鍊紅蓮・539戰略領先戰情室 (v7.4 完整帝國版)")
st.sidebar.title("📜 歷史戰報")
reversed_dates = list(data['日期'])[::-1]
reversed_nums = list(data['開出號碼'])[::-1]
for d, n in zip(reversed_dates, reversed_nums):
    st.sidebar.markdown(f"**📅 {d}**")
    st.sidebar.code("  ".join([f"{x:02d}" for x in n]))
    st.sidebar.markdown("---")
st.sidebar.caption("⚡ 五行/奇門/量化/伏吟策略 全整合")

# === 頂部三大戰略區塊 ===
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""<div class="review-card"><h3>🏮 戰後復盤</h3><p>今日和值：<span class="highlight-text">72 (連兩期極低)</span></p><p>狀態：21號已開，緣分啟動</p><p style="color:#FF4500; font-weight:bold;">警示：和值面臨極限反彈</p></div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class="strategy-card"><h3>🐍 明日(1/9)指令</h3><p>奇門格局：<b>伏吟 (動不如靜)</b></p><p>決策：<span class="highlight-text" style="font-size:1.1em;">死守本命 17, 21</span></p><p>理由：順應伏吟，不擴大戰線</p></div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class="radar-card"><h3>📡 能量雷達</h3><p>金系真空・土相生金</p><p>潛在爆發：<span class="highlight-text" style="font-size:1.3em;">24, 25, 34</span></p><p style="font-size:12px; color:#aaa;">(作為背景監控，暫不主攻)</p></div>""", unsafe_allow_html=True)

# === 🔮 奇門時空方位 & 五行能量流 ===
st.markdown("---")
st.subheader("🔮 奇門時空方位 & 五行能量流")
now = get_current_taiwan_time()
luck_dir, wealth_dir = get_lucky_direction(now.hour, now.day)

# 第一列：方位羅盤 (完整回歸)
c_dir1, c_dir2, c_dir3 = st.columns([1, 1, 1])
with c_dir1:
    st.info(f"📅 日期：{now.strftime('%Y-%m-%d')}\n\n⏰ 時間：{now.strftime('%H:%M')}")
    st.warning("🔥 伏吟局：利於連莊，重複，防守")
with c_dir2:
    st.markdown(f"""<div class="direction-box wealth-dir"><h4 style="margin:0;color:#aaa;">💰 財神方位</h4><div class="dir-text" style="color:#FFD700;">{wealth_dir}</div></div>""", unsafe_allow_html=True)
with c_dir3:
    st.markdown(f"""<div class="direction-box lucky-dir"><h4 style="margin:0;color:#aaa;">✨ 貴人方位</h4><div class="dir-text" style="color:#D4AF37;">{luck_dir}</div></div>""", unsafe_allow_html=True)

# 第二列：五行能量條
st.markdown("#### 🌪️ 五行元素動態 (Element Status)")
e_order = ["Metal", "Wood", "Water", "Fire", "Earth"]
e_names = {"Metal": "金 (4,9)", "Wood": "木 (3,8)", "Water": "水 (1,6)", "Fire": "火 (2,7)", "Earth": "土 (5,0)"}
e_colors = {"Metal": "#FFD700", "Wood": "#32CD32", "Water": "#1E90FF", "Fire": "#FF4500", "Earth": "#8B4513"}
total_elem = elem_counts.sum()
e_cols = st.columns(5)
for i, e in enumerate(e_order):
    count = elem_counts.get(e, 0)
    pct = (count / total_elem) * 100
    with e_cols[i]:
        st.markdown(f"<div style='text-align:center; color:{e_colors[e]}; font-size:14px;'>{e_names[e]}</div>", unsafe_allow_html=True)
        st.progress(min(count/10.0, 1.0))
        st.markdown(f"<div style='text-align:center; font-size:12px;'>{pct:.0f}%</div>", unsafe_allow_html=True)

# === ⚔️ 統帥核心戰略區 (Action Zone) ===
st.markdown("---")
st.subheader("🎯 統帥核心戰略區 (Commander's Action)")
f_col1, f_col2 = st.columns([2, 1])

# 左側：您的執行指令
with f_col1:
    st.markdown("""
    <div class="action-card">
        <div class="prob-badge">執行確認</div>
        <h2 style="color:#FFD700; margin-bottom:5px;">🔱 統帥專屬陣列</h2>
        <h1 style="letter-spacing: 12px; color:#FFFFFF; margin:15px 0;">17, 21</h1>
        <p style="font-size:16px; color:#E0E0E0;">戰略邏輯：<b>本命守護 + 伏吟連莊</b></p>
        <p style="font-size:14px; color:#aaa;">(21已開，能量延續；17火接力，靜待感應)</p>
    </div>
    """, unsafe_allow_html=True)

# 右側：全局監控 (原本的5星，現在作為背景情報)
with f_col2:
    st.markdown("""
    <div class="monitor-card">
        <h4 style="color:#1E90FF; margin:0;">📡 全局趨勢監控</h4>
        <p style="font-size:12px; color:#aaa; margin-top:5px;">若重心反彈，以下為高危區：</p>
        <h2 style="color:#FFFFFF; margin:5px 0;">24, 25, 34</h2>
        <p style="font-size:12px; color:#B0B0B0;">狀態：真空極限・五行缺金</p>
        <hr style="border:0.5px solid #333;">
        <p style="font-size:12px; color:#FF4500;">統帥批示：<b>暫不擴張，僅作監控</b></p>
    </div>
    """, unsafe_allow_html=True)

# === 📊 數據圖表區 (完整回歸) ===
st.markdown("---")
tab1, tab2 = st.tabs(["📈 能量趨勢與乖離 (Bias)", "🔥 兵力分佈雷達 (Heatmap)"])
with tab1:
    latest_bias = df_analysis['乖離率'].iloc[-1]
    st.markdown(f'<div class="bias-metric-box">目前能量乖離率：<span class="bias-val-neg">{latest_bias:.1f}%</span> (報復性反彈蓄力中)</div>', unsafe_allow_html=True)
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=df_analysis['日期'], y=df_analysis['和值'], mode='lines+markers', line=dict(color='#FFD700', width=4)))
    fig_trend.add_trace(go.Scatter(x=df_analysis['日期'], y=[100]*len(df_analysis), mode='lines', line=dict(color='#00FF00', dash='dash')))
    fig_trend.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E0E0E0'), height=250)
    st.plotly_chart(fig_trend, use_container_width=True)
with tab2:
    heatmap_data = []
    for i in range(0, 40, 10):
        row = full_counts[i+1:i+11].values
        if len(row) < 10: row = np.pad(row, (0, 10-len(row)), 'constant')
        heatmap_data.append(row)
    fig_heat = px.imshow(heatmap_data, x=[str(i) for i in range(1, 11)], y=["0頭", "1頭", "2頭", "3頭"], color_continuous_scale="YlOrRd", text_auto=True)
    fig_heat.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E0E0E0'), height=250)
    st.plotly_chart(fig_heat, use_container_width=True)
