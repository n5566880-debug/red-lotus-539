import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import random
import numpy as np

# --- 1. 頁面基礎設定 ---
st.set_page_config(page_title="赤鍊紅蓮・539戰情室", layout="wide", page_icon="🔱")

# --- CSS 深度美化 (原版黑金風格) ---
st.markdown("""
<style>
    .stApp { background-color: #0D0D0D; color: #E0E0E0; }
    
    /* 卡片風格 */
    .action-card { background: linear-gradient(135deg, #2c0000 0%, #000000 100%); padding: 20px; border-radius: 15px; border: 2px solid #FFD700; box-shadow: 0 5px 20px rgba(255, 215, 0, 0.2); }
    .witch-card { background: linear-gradient(135deg, #1a0033 0%, #000000 100%); padding: 20px; border-radius: 15px; border: 2px solid #FF00FF; box-shadow: 0 5px 20px rgba(255, 0, 255, 0.2); }
    
    /* 壓力表樣式 */
    .pressure-container { background-color: #1a1a1a; border-radius: 10px; padding: 10px; margin-bottom: 8px; border: 1px solid #333; }
    .pressure-bar-bg { width: 100%; background-color: #333; height: 12px; border-radius: 6px; margin-top: 5px; overflow: hidden; }
    .pressure-bar-fill { height: 100%; border-radius: 6px; box-shadow: 0 0 10px rgba(0,0,0,0.5); }
    
    /* 壓力等級動畫 */
    @keyframes pulse-red { 0% { box-shadow: 0 0 5px #8B0000; opacity: 0.9; } 50% { box-shadow: 0 0 20px #FF0000; opacity: 1; } 100% { box-shadow: 0 0 5px #8B0000; opacity: 0.9; } }
    .level-safe { background: linear-gradient(90deg, #00FF00, #32CD32); width: 25%; }
    .level-warning { background: linear-gradient(90deg, #FFD700, #FF8C00); width: 65%; box-shadow: 0 0 10px #FFD700; }
    .level-critical { background: linear-gradient(90deg, #FF0000, #8B0000); width: 98%; animation: pulse-red 1.2s infinite; }
    
    /* 標籤與文字 */
    .highlight-numbers { color: #FFD700; font-size: 46px; font-weight: bold; letter-spacing: 4px; text-shadow: 2px 2px 10px rgba(255, 215, 0, 0.5); font-family: 'Courier New', monospace; }
    .cantian-tag { display: inline-block; padding: 2px 6px; border-radius: 4px; font-size: 12px; margin: 2px; font-weight: bold; color: #000; }
    .tag-spring { background: #98FB98; } 
    .tag-summer { background: #FF4500; color: #FFF; } 
    .tag-autumn { background: #FFD700; } 
    .tag-winter { background: #ADD8E6; }
    .proverb-text { font-size: 13px; color: #D4AF37; font-style: italic; margin-bottom: 8px; line-height: 1.4; }
    
    /* 圖表區 */
    .bias-metric-box { background: #1a1a1a; padding: 10px; border-radius: 8px; border: 1px solid #555; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- 2. 核心邏輯 ---

def decode_cantian(num):
    # 季節
    if 1 <= num <= 9: season, s_class = "春", "tag-spring"
    elif 10 <= num <= 19: season, s_class = "夏", "tag-summer"
    elif 20 <= num <= 29: season, s_class = "秋", "tag-autumn"
    elif 30 <= num <= 39: season, s_class = "冬", "tag-winter"
    else: season, s_class = "未知", ""
    
    # 氣象
    tail = num % 10
    if tail in [1, 6]: weather, w_icon = "雨", "🌧️"
    elif tail in [2, 7]: weather, w_icon = "火", "🔥"
    elif tail in [3, 8]: weather, w_icon = "風", "🌬️"
    elif tail in [4, 9]: weather, w_icon = "電", "⚡"
    else: weather, w_icon = "晴", "☀️"
    
    return season, s_class, weather, w_icon

def calculate_witch_chaos():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    # 針對 1/12 下週一預測
    target_num = 24
    reason = "25, 26 已開，24 被夾殺形成『真空區』，物理慣性極大機率回補。"
    return target_num, reason, now.strftime("%H:%M:%S")

def get_pressure_data():
    # 1/10 戰後更新數據
    # 11, 25, 34, 38 已開 -> 綠色
    # 24 沒開 -> 紅色警戒
    return [
        (24, 36, "level-critical", "#FF0000", "🚨 極危 (真空補位)"),
        (25, 0, "level-safe", "#32CD32", "🟢 釋放 (已命中)"),
        (11, 0, "level-safe", "#32CD32", "🟢 釋放 (已命中)"),
        (34, 0, "level-safe", "#32CD32", "🟢 釋放 (連莊)"),
        (35, 14, "level-warning", "#FFD700", "⚠️ 蓄能 (34鄰號)"),
        (14, 12, "level-warning", "#FFD700", "⚠️ 蓄能 (4尾效應)")
    ]

# --- 3. 數據準備 (更新至 1/10) ---
data = {
    '日期': ['1/6', '1/7', '1/8', '1/9', '1/10'],
    '開出號碼': [
        [4, 13, 21, 28, 35], 
        [5, 10, 14, 15, 28], 
        [3, 8, 10, 21, 30],
        [1, 12, 14, 22, 34],
        [11, 25, 26, 34, 38]  # 1/10 最新
    ]
}
df = pd.DataFrame(data)
df['和值'] = df['開出號碼'].apply(sum)
all_nums = [n for sub in data['開出號碼'] for n in sub]

# 熱力圖數據
full_counts = pd.Series(all_nums).value_counts().sort_index()
heatmap_data = np.zeros((4, 10))
for i in range(1, 40):
    row = 0 if i < 10 else (1 if i < 20 else (2 if i < 30 else 3))
    col = (i % 10) - 1
    if col == -1: col = 9
    heatmap_data[row, col] = full_counts.get(i, 0)

# --- 4. 側邊欄 ---
st.sidebar.title("🏮 博弈宗師心法")
for p in ["寧棄莫出銃", "人旺我亂碰", "牌衰過三棟", "牌尾吃卡檔", "贏 50 也是贏", "保本為上", "盤勢往大號噴發"]:
    st.sidebar.markdown(f'<div class="proverb-text">{p}</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.title("📜 歷史戰報")
for d, n in zip(data['日期'][::-1], data['開出號碼'][::-1]):
    st.sidebar.code(f"{d}: {' '.join([f'{x:02d}' for x in n])}")

# --- 5. 主戰情室 ---
st.title("🔱 赤鍊紅蓮・終極全配戰情室 (v8.7)")

# 狀態
c1, c2, c3 = st.columns(3)
c1.info("氣象：大號熱 (和值134)")
c2.success("戰果：命中 11, 25 (+50)")
c3.error("能量：24 號真空夾殺")

st.markdown("---")

# === 第一層：深紅警戒壓力表 ===
st.markdown("### 🩸 回彈臨界點 (Pressure Gauge)")
st.caption("魔女直覺區：24 號進入紅色警戒，25 號已釋放")
pres_cols = st.columns(3)
p_data = get_pressure_data()
for i, (num, missed, cls, color, txt) in enumerate(p_data):
    season, s_cls, weather, w_icon = decode_cantian(num)
    with pres_cols[i % 3]:
        st.markdown(f"""
        <div class="pressure-container">
            <div style="display:flex; justify-content:space-between;">
                <div>
                    <span style="font-size:18px; font-weight:bold; color:#FFF;">{num:02d}</span>
                    <span class="cantian-tag {s_cls}">{season}</span>
                    <span style="font-size:12px; color:#aaa;">{w_icon}</span>
                </div>
                <div style="color:{color}; font-size:11px; font-weight:bold;">{txt}</div>
            </div>
            <div class="pressure-bar-bg"><div class="{cls} pressure-bar-fill"></div></div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# === 第二層：核心戰略區 (五星 + 魔女) ===
col_main, col_witch = st.columns([2, 1])
# 下週一戰略：07 (小號), 14 (4尾), 23 (連號前緣), 24 (核心真空), 35 (大號鄰號)
strategy_nums = [7, 14, 23, 24, 35] 

with col_main:
    st.markdown('<div class="action-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color:#FFD700;">⚔️ 統帥・1/12 (一) 五星總攻</h3>', unsafe_allow_html=True)
    st.markdown(f'<div class="highlight-numbers">{", ".join([f"{n:02d}" for n in strategy_nums])}</div>', unsafe_allow_html=True)
    st.markdown('<hr style="border:0.5px solid #444;">', unsafe_allow_html=True)
    
    # 參天律詳細解碼
    cols_decode = st.columns(5)
    for idx, n in enumerate(strategy_nums):
        season, s_cls, weather, w_icon = decode_cantian(n)
        with cols_decode[idx]:
            st.markdown(f"<div style='text-align:center;'><span class='cantian-tag {s_cls}'>{season}</span><br><span style='font-size:20px; color:#FFF;'>{n:02d}</span><br><span style='font-size:12px; color:#aaa;'>{w_icon}</span></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

witch_num, witch_reason, calc_time = calculate_witch_chaos()
season_w, s_cls_w, weather_w, w_icon_w = decode_cantian(witch_num)

with col_witch:
    st.markdown('<div class="witch-card">', unsafe_allow_html=True)
    st.markdown('<h4 style="color:#FF00FF;">🔮 雨菲亂碰</h4>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:40px; color:#FFFFFF; font-weight:bold; margin:5px 0;">{witch_num:02d}</div>', unsafe_allow_html=True)
    st.markdown(f'<span class="cantian-tag {s_cls_w}">{season_w}</span> {w_icon_w}', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:11px; color:#FF00FF; margin-top:5px;">{witch_reason}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# === 第三層：專業圖表區 ===
st.markdown("---")
tab1, tab2, tab3 = st.tabs(["🌪️ 五行能量", "📈 K線趨勢", "🔥 季節熱力"])

with tab1: # 五行
    e_counts = {"Water":0, "Fire":0, "Wood":0, "Metal":0, "Earth":0}
    for n in all_nums:
        d = n % 10
        if d in [1,6]: e_counts["Water"]+=1
        elif d in [2,7]: e_counts["Fire"]+=1
        elif d in [3,8]: e_counts["Wood"]+=1
        elif d in [4,9]: e_counts["Metal"]+=1
        else: e_counts["Earth"]+=1
    colors = {"Water":"#1E90FF", "Fire":"#FF4500", "Wood":"#32CD32", "Metal":"#FFD700", "Earth":"#8B4513"}
    labels = {"Water":"雨(水)", "Fire":"火(火)", "Wood":"風(木)", "Metal":"電(金)", "Earth":"晴(土)"}
    ec_cols = st.columns(5)
    total = sum(e_counts.values())
    for i, (k, col) in enumerate(zip(e_counts.keys(), ec_cols)):
        with col:
            st.markdown(f"<div style='text-align:center; color:{colors[k]}; font-weight:bold;'>{labels[k]}</div>", unsafe_allow_html=True)
            st.progress(e_counts[k]/total if total > 0 else 0)
            st.markdown(f"<div style='text-align:center;'>{e_counts[k]}</div>", unsafe_allow_html=True)

with tab2: # K線 (和值飆高)
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=df['日期'], y=df['和值'], mode='lines+markers', line=dict(color='#FFD700', width=4)))
    fig_trend.add_hline(y=100, line_dash="dash", line_color="#FF0000", annotation_text="高位警戒")
    fig_trend.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E0E0E0'), height=250, margin=dict(t=20, b=20))
    st.plotly_chart(fig_trend, use_container_width=True)

with tab3: # 熱力圖
    fig_heat = px.imshow(heatmap_data, x=["1雨","2火","3風","4電","5晴","6雨","7火","8風","9電","0晴"], 
                         y=["春(0)", "夏(1)", "秋(2)", "冬(3)"], color_continuous_scale="YlOrRd", text_auto=True)
    fig_heat.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E0E0E0'), height=250)
    st.plotly_chart(fig_heat, use_container_width=True)
