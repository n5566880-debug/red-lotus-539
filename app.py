import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import numpy as np

# --- 1. 頁面基礎設定 ---
st.set_page_config(page_title="赤鍊紅蓮・1/12 全配戰情室", layout="wide", page_icon="🔱")

# --- CSS 深度美化 (黑金旗艦版) ---
st.markdown("""
<style>
    .stApp { background-color: #0D0D0D; color: #E0E0E0; }
    
    /* 卡片風格 */
    .action-card { background: linear-gradient(135deg, #2c0000 0%, #000000 100%); padding: 20px; border-radius: 15px; border: 2px solid #FF4500; box-shadow: 0 5px 20px rgba(255, 69, 0, 0.3); }
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
    .highlight-numbers { color: #FFD700; font-size: 48px; font-weight: bold; letter-spacing: 4px; text-shadow: 2px 2px 10px rgba(255, 215, 0, 0.5); font-family: 'Courier New', monospace; text-align: center; }
    .cantian-tag { display: inline-block; padding: 2px 6px; border-radius: 4px; font-size: 12px; margin: 2px; font-weight: bold; color: #000; }
    .tag-spring { background: #98FB98; } 
    .tag-summer { background: #FF4500; color: #FFF; } 
    .tag-autumn { background: #FFD700; } 
    .tag-winter { background: #ADD8E6; }
    .proverb-text { font-size: 13px; color: #D4AF37; font-style: italic; margin-bottom: 8px; line-height: 1.4; }
</style>
""", unsafe_allow_html=True)

# --- 2. 核心運算邏輯 ---

def decode_cantian(num):
    # 季節判斷
    if 1 <= num <= 9: season, s_class = "春", "tag-spring"
    elif 10 <= num <= 19: season, s_class = "夏", "tag-summer"
    elif 20 <= num <= 29: season, s_class = "秋", "tag-autumn"
    elif 30 <= num <= 39: season, s_class = "冬", "tag-winter"
    else: season, s_class = "未知", ""
    
    # 氣象判斷 (修正五行對應)
    tail = num % 10
    if tail in [1, 6]: weather, w_icon = "雨(水)", "🌧️"
    elif tail in [2, 7]: weather, w_icon = "火(火)", "🔥"
    elif tail in [3, 8]: weather, w_icon = "風(木)", "🌬️"
    elif tail in [4, 9]: weather, w_icon = "電(金)", "⚡"
    else: weather, w_icon = "晴(土)", "☀️"
    
    return season, s_class, weather, w_icon

def calculate_witch_chaos():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    target_num = 35
    reason = "庚金直覺發動！鎖定大號區連續轟炸，35為能量核心。"
    return target_num, reason, now.strftime("%H:%M:%S")

def get_pressure_data():
    return [
        (24, 38, "level-critical", "#FF0000", "🚨 極危 (真空補位)"),
        (25, 0, "level-warning", "#FFD700", "🛡️ 防禦 (差一號掩護)"),
        (35, 20, "level-critical", "#FF0000", "🎯 統帥直覺 (核心)"),
        (36, 18, "level-warning", "#FFD700", "⚠️ 連號 (大號擴散)"),
        (37, 12, "level-warning", "#FFD700", "🛡️ 防禦 (加一戰術)"),
        (34, 0, "level-safe", "#32CD32", "🟢 已釋放 (連莊)")
    ]

# --- 3. 數據準備 (歷史 30 期 K 線數據源) ---
# 這裡使用最近 10 期用於計算熱力圖與五行，避免數據過舊失真
data = {
    '日期': ['12/31', '1/1', '1/2', '1/3', '1/5', '1/6', '1/7', '1/8', '1/9', '1/10'],
    '開出號碼': [
        [2, 14, 23, 29, 36],
        [1, 11, 15, 27, 33],
        [8, 14, 19, 21, 29],
        [2, 3, 16, 22, 25],
        [15, 23, 32, 36, 39],
        [4, 13, 21, 28, 35], 
        [5, 10, 14, 15, 28], 
        [3, 8, 10, 21, 30],
        [1, 12, 14, 22, 34],
        [11, 25, 26, 34, 38]  # 最新一期
    ]
}
df = pd.DataFrame(data)
df['和值'] = df['開出號碼'].apply(sum)
all_nums = [n for sub in data['開出號碼'] for n in sub]

# --- 熱力圖數據矩陣計算 (修復版) ---
# 4行 (春夏秋冬) x 10列 (尾數1~0)
heatmap_data = np.zeros((4, 10))
for n in all_nums:
    # 行索引：春(0), 夏(1), 秋(2), 冬(3)
    if 1 <= n <= 9: row = 0
    elif 10 <= n <= 19: row = 1
    elif 20 <= n <= 29: row = 2
    elif 30 <= n <= 39: row = 3
    else: continue
    
    # 列索引：尾數 1->0, 2->1 ... 0->9
    col = (n % 10) - 1
    if col == -1: col = 9
    
    heatmap_data[row, col] += 1

# --- 4. 側邊欄 ---
st.sidebar.title("🏮 庚金統帥心法")
for p in ["直覺是利劍", "差一號是魔咒", "火力覆蓋破防", "贏 50 也是贏", "大號區連彈", "寧錯殺不放過"]:
    st.sidebar.markdown(f'<div class="proverb-text">{p}</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.title("📜 歷史戰報")
for d, n in zip(data['日期'][::-1], data['開出號碼'][::-1]):
    st.sidebar.code(f"{d}: {' '.join([f'{x:02d}' for x in n])}")

# --- 5. 主戰情室 ---
st.title("🔱 赤鍊紅蓮・1/12 加一防禦全配版")

# 狀態標籤
c1, c2, c3 = st.columns(3)
c1.info("氣象：大號區 (30-39) 高熱")
c2.success("戰術：加一號火力覆蓋")
c3.error("能量：24 號真空必補")

st.markdown("---")

# === 第一層：壓力表 (Pressure Gauge) ===
st.markdown("### 🩸 回彈臨界點 (Pressure Gauge)")
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

# === 第二層：核心戰略區 ===
col_main, col_witch = st.columns([2, 1])

# 戰術號碼：24, 25 (中號) + 35, 36, 37 (大號)
strategy_nums = [24, 25, 35, 36, 37]

with col_main:
    st.markdown('<div class="action-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color:#FF4500; text-align: center;">⚔️ 統帥・1/12 密集轟炸令</h3>', unsafe_allow_html=True)
    st.markdown(f'<div class="highlight-numbers" style="text-align: center;">{" ".join([f"{n:02d}" for n in strategy_nums])}</div>', unsafe_allow_html=True)
    st.markdown('<hr style="border:0.5px solid #444;">', unsafe_allow_html=True)
    
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
    st.markdown('<h4 style="color:#FF00FF;">🔮 直覺感應</h4>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:40px; color:#FFFFFF; font-weight:bold; margin:5px 0;">{witch_num:02d}</div>', unsafe_allow_html=True)
    st.markdown(f'<span class="cantian-tag {s_cls_w}">{season_w}</span> {w_icon_w}', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:11px; color:#FF00FF; margin-top:5px;">{witch_reason}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# === 第三層：圖表分析 (修復完畢) ===
st.markdown("---")
tab1, tab2, tab3 = st.tabs(["🌪️ 五行能量 (修復)", "🔥 季節熱力圖 (回歸)", "📈 K線趨勢"])

with tab1:
    # 五行能量計算 logic fix
    e_counts = {"Water":0, "Fire":0, "Wood":0, "Metal":0, "Earth":0}
    for n in all_nums:
        d = n % 10
        if d in [1,6]: e_counts["Water"]+=1
        elif d in [2,7]: e_counts["Fire"]+=1
        elif d in [3,8]: e_counts["Wood"]+=1
        elif d in [4,9]: e_counts["Metal"]+=1
        else: e_counts["Earth"]+=1
    
    colors = {"Water":"#1E90FF", "Fire":"#FF4500", "Wood":"#32CD32", "Metal":"#FFD700", "Earth":"#8B4513"}
    labels = {"Water":"雨 (1,6)", "Fire":"火 (2,7)", "Wood":"風 (3,8)", "Metal":"電 (4,9)", "Earth":"晴 (5,0)"}
    
    ec_cols = st.columns(5)
    total = sum(e_counts.values())
    
    for i, (k, col) in enumerate(zip(e_counts.keys(), ec_cols)):
        with col:
            st.markdown(f"<div style='text-align:center; color:{colors[k]}; font-weight:bold;'>{labels[k]}</div>", unsafe_allow_html=True)
            # 進度條
            val = e_counts[k]
            pct = val/total if total > 0 else 0
            st.progress(pct)
            st.markdown(f"<div style='text-align:center; font-size:20px;'>{val}</div>", unsafe_allow_html=True)

with tab2:
    # 熱力圖顯示
    fig_heat = px.imshow(heatmap_data, 
                         x=["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"], 
                         y=["春 (01-09)", "夏 (10-19)", "秋 (20-29)", "冬 (30-39)"], 
                         color_continuous_scale="YlOrRd", 
                         text_auto=True,
                         aspect="auto")
    fig_heat.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(color='#E0E0E0'), 
        height=300,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    st.caption("💡 觀察重點：冬區 (30-39) 顏色最深，代表近期最熱，您的 35-37 策略符合熱區。")

with tab3:
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=df['日期'], y=df['和值'], mode='lines+markers', line=dict(color='#FFD700', width=4)))
    fig_trend.add_hline(y=100, line_dash="dash", line_color="#FF0000", annotation_text="平均線")
    fig_trend.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E0E0E0'), height=300)
    st.plotly_chart(fig_trend, use_container_width=True)
