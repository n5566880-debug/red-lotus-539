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
    .stApp { background-color: #0D0D0D; color: #E0E0E0; }
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
    .action-card { background: linear-gradient(135deg, #4b0000, #000000); padding: 25px; border-radius: 12px; border: 3px solid #FFD700; text-align: center; position: relative; }
    .witch-card { background: linear-gradient(135deg, #2b004b, #000000); padding: 20px; border-radius: 12px; border: 2px solid #FF00FF; text-align: center; position: relative; }
    .prob-badge { position: absolute; top: 10px; right: 10px; background: #FFD700; color: #000; padding: 2px 8px; border-radius: 5px; font-weight: bold; font-size: 14px; }
    
    /* 乖離率指標 */
    .bias-metric-box { background: #1a1a1a; padding: 10px; border-radius: 8px; border: 1px solid #555; text-align: center; }
    .bias-val-neg { color: #00FF00; font-weight: bold; font-size: 1.2em; }
    
    .highlight-numbers { color: #FFD700; font-size: 50px; font-weight: bold; letter-spacing: 10px; text-shadow: 2px 2px 10px rgba(255, 215, 0, 0.5); }
    .proverb-text { font-size: 13px; color: #D4AF37; font-style: italic; margin-bottom: 8px; line-height: 1.4; }
    h1, h2, h3 { color: #FFFFFF; font-weight: 600; }
    .highlight-text { color: #FFD700; font-weight: bold; font-size: 1.1em; }
</style>
""", unsafe_allow_html=True)

# --- 2. 核心數據中心 (修復語法錯誤) ---
data = {
    '日期': ['1/4', '1/5', '1/6', '1/7', '1/8'],
    '開出號碼': [
        [2, 3, 16, 22, 25],
        [15, 23, 32, 36, 39],
        [4, 13, 21, 28, 35],
        [5, 10, 14, 15, 28],
        [3, 8, 10, 21, 30]
    ]
}

# 輔助函數群 (找回五行運算)
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

# --- 3. 側邊欄 (戰報 + 十大金句) ---
st.sidebar.title("🏮 博弈宗師心法")
proverbs = [
    "第一：寧棄莫出銃", "第二：人旺我亂碰", "第三：牌衰過三棟",
    "第四：牌尾吃卡檔", "第五：牌可以輸，牌品不可輸", "第六：胡可以吃進，威不可以拿進",
    "第七：你贏的是人不是牌", "第八：輸也是輸條命，更加不是牌",
    "第九：牌旺自然隻手香", "第十：牌爛未必輸，人賤天收"
]
for p in proverbs:
    st.sidebar.markdown(f'<div class="proverb-text">{p}</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.title("📜 歷史戰報")
for d, n in zip(data['日期'][::-1], data['開出號碼'][::-1]):
    st.sidebar.markdown(f"**📅 {d}** → `{' '.join([f'{x:02d}' for x in n])}`")

# --- 4. 主介面內容 ---
st.title("🔱 赤鍊紅蓮・539戰略領先戰情室 (v8.0 完全體)")

# 頂部三大戰略
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""<div class="review-card"><h3>🏮 戰後復盤</h3><p>和值：<span class="highlight-text">72</span> (連兩期極低)</p><p>21號命中，伏吟局確立</p><p style="color:#FF4500; font-weight:bold;">警示：能量嚴重右偏蓄勢</p></div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class="strategy-card"><h3>🐍 明日(1/9)指令</h3><p>參天律：<b>伏吟 (動不如靜)</b></p><p>決策：<span class="highlight-text" style="font-size:1.1em;">三星合圍 (17, 21, 26)</span></p><p>狀態：順勢防禦，魔女亂碰</p></div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class="radar-card"><h3>📡 能量監控</h3><p>金土真空・待爆發</p><p>關注：<span class="highlight-text" style="font-size:1.3em;">24, 25, 34</span></p></div>""", unsafe_allow_html=True)

# 奇門與五行 (完整回歸)
st.markdown("---")
st.subheader("🔮 奇門時空方位 & 五行能量流")
now = get_current_taiwan_time()
luck_dir, wealth_dir = get_lucky_direction(now.hour, now.day)
c_dir1, c_dir2, c_dir3 = st.columns([1, 1, 1])
with c_dir1:
    st.info(f"📅 {now.strftime('%Y-%m-%d')} | ⏰ {now.strftime('%H:%M')}")
    st.warning("🔥 伏吟：利連莊，利防守")
with c_dir2:
    st.markdown(f"""<div class="direction-box wealth-dir"><h4 style="margin:0;color:#aaa;">💰 財神方位</h4><div class="dir-text" style="color:#FFD700;">{wealth_dir}</div></div>""", unsafe_allow_html=True)
with c_dir3:
    st.markdown(f"""<div class="direction-box lucky-dir"><h4 style="margin:0;color:#aaa;">✨ 貴人方位</h4><div class="dir-text" style="color:#D4AF37;">{luck_dir}</div></div>""", unsafe_allow_html=True)

# 五行能量條 (Process Bar 回歸)
st.markdown("#### 🌪️ 近期五行元素佔比")
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

# 核心行動區 (三星 + 魔女)
st.markdown("---")
f_col1, f_col2 = st.columns([2, 1])
with f_col1:
    st.markdown("""
    <div class="action-card">
        <div class="prob-badge">執行中</div>
        <h3 style="color:#FFD700; margin-bottom:10px;">⚔️ 統帥・三星陣列</h3>
        <div class="highlight-numbers">17, 21, 26</div>
        <p style="font-size:16px; color:#E0E0E0; margin-top:15px;">戰術：<b>本命火 + 予婕木 + 魔女水</b></p>
        <p style="font-size:14px; color:#aaa;">水火既濟，打破火秋肅殺</p>
    </div>
    """, unsafe_allow_html=True)
with f_col2:
    st.markdown("""
    <div class="witch-card">
        <h4 style="color:#FF00FF; margin:0;">🔮 雨菲・亂碰指令</h4>
        <div style="font-size:32px; color:#FFFFFF; font-weight:bold; margin:10px 0;">26</div>
        <p style="font-size:12px; color:#FF00FF;">
            「人旺我亂碰」<br>
            以水潤燥，強制干擾。
        </p>
    </div>
    """, unsafe_allow_html=True)

# 完整圖表區 (Heatmap + K-Line 回歸)
st.markdown("---")
tab1, tab2 = st.tabs(["📈 能量趨勢與乖離", "🔥 兵力分佈雷達"])
with tab1:
    latest_bias = df_analysis['乖離率'].iloc[-1]
    st.markdown(f'<div class="bias-metric-box">目前能量乖離率：<span class="bias-val-neg">{latest_bias:.1f}%</span></div>', unsafe_allow_html=True)
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
