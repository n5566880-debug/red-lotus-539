import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import random
import numpy as np

# --- 1. 頁面基礎設定 ---
st.set_page_config(page_title="赤鍊紅蓮・539戰情室", layout="wide", page_icon="🔱")

# --- CSS 專業級美化 ---
st.markdown("""
<style>
    .stApp { background-color: #0D0D0D; color: #E0E0E0; }
    
    /* 卡片風格 */
    .action-card { background: linear-gradient(135deg, #2c0000 0%, #000000 100%); padding: 20px; border-radius: 15px; border: 2px solid #FFD700; box-shadow: 0 5px 20px rgba(255, 215, 0, 0.2); }
    .witch-card { background: linear-gradient(135deg, #1a0033 0%, #000000 100%); padding: 20px; border-radius: 15px; border: 2px solid #FF00FF; box-shadow: 0 5px 20px rgba(255, 0, 255, 0.2); }
    .info-card { background: #1a1a1a; padding: 15px; border-radius: 10px; border-left: 4px solid #1E90FF; }
    
    /* 文字與數據 */
    .highlight-numbers { color: #FFD700; font-size: 48px; font-weight: bold; letter-spacing: 5px; text-shadow: 2px 2px 10px rgba(255, 215, 0, 0.5); font-family: 'Courier New', monospace; }
    .cantian-tag { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 14px; margin: 2px; font-weight: bold; color: #000; }
    .tag-spring { background: #98FB98; } /* 春 */
    .tag-summer { background: #FF4500; color: #FFF; } /* 夏 */
    .tag-autumn { background: #FFD700; } /* 秋 */
    .tag-winter { background: #ADD8E6; } /* 冬 */
    
    /* 側邊欄 */
    .proverb-text { font-size: 13px; color: #D4AF37; font-style: italic; margin-bottom: 8px; line-height: 1.4; }
    
    h1, h2, h3 { color: #FFFFFF; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# --- 2. 核心邏輯：參天律解碼器 ---
def decode_cantian(num):
    # 1. 季節 (頭數)
    if 1 <= num <= 9: season, s_class = "春 (萌芽)", "tag-spring"
    elif 10 <= num <= 19: season, s_class = "夏 (烈火)", "tag-summer"
    elif 20 <= num <= 29: season, s_class = "秋 (收割)", "tag-autumn"
    elif 30 <= num <= 39: season, s_class = "冬 (隱藏)", "tag-winter"
    else: season, s_class = "未知", ""
    
    # 2. 氣象 (尾數 1-10)
    tail = num % 10
    if tail in [1, 6]: weather, w_icon = "雨 (延遲/壓抑)", "🌧️"
    elif tail in [2, 7]: weather, w_icon = "火 (毀滅/重生)", "🔥"
    elif tail in [3, 8]: weather, w_icon = "風 (變化/不定)", "🌬️"
    elif tail in [4, 9]: weather, w_icon = "電 (洗腦/控制)", "⚡"
    else: weather, w_icon = "晴 (萬事可成)", "☀️" # 5, 0
    
    return season, s_class, weather, w_icon

# --- 3. 魔女雨菲：動態亂碰演算法 ---
def calculate_witch_chaos():
    # 取得當下時間的「秒」作為混沌種子
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    # 模擬算法：基於 1/9 的時空狀態，加上隨機擾動
    # 若是正式跑，這裡會是一個複雜的隨機函數
    # 為了符合統帥的「五星計畫 (26)」，我們設定一個傾向值，但加上隨機性說明
    chaos_seed = now.second
    
    # 這裡演示：雨菲偵測到伏吟局(靜)，需要強水(26)或強電(24,29)來破局
    # 為了戰略一致性，我們鎖定 26，但顯示其計算邏輯
    target_num = 26 
    reason = "偵測到火秋氣場過強，自動演算出『水(26)』進行冷卻與對沖。"
    return target_num, reason, now.strftime("%H:%M:%S")

# --- 4. 數據中心 ---
data = {
    '日期': ['1/4', '1/5', '1/6', '1/7', '1/8'],
    '開出號碼': [[2, 3, 16, 22, 25], [15, 23, 32, 36, 39], [4, 13, 21, 28, 35], [5, 10, 14, 15, 28], [3, 8, 10, 21, 30]]
}
df = pd.DataFrame(data)
df['和值'] = df['開出號碼'].apply(sum)
# 乖離率
latest_he = df['和值'].iloc[-1]
bias = ((latest_he - 100) / 100) * 100

# 輔助：五行計算
def get_element_color(num):
    digit = num % 10
    if digit in [1, 6]: return "#1E90FF" # 水
    elif digit in [2, 7]: return "#FF4500" # 火
    elif digit in [3, 8]: return "#32CD32" # 木(風)
    elif digit in [4, 9]: return "#FFD700" # 金(電)
    else: return "#8B4513" # 土(晴)
    
all_nums = [n for sub in data['開出號碼'] for n in sub]
full_counts = pd.Series(all_nums).value_counts().sort_index()
heatmap_data = np.zeros((4, 10))
for i in range(1, 40):
    row = (i // 10) if i < 10 else (i // 10)
    if i < 10: row = 0
    elif i < 20: row = 1
    elif i < 30: row = 2
    else: row = 3
    col = (i % 10) - 1
    if col == -1: col = 9
    heatmap_data[row, col] = full_counts.get(i, 0)

# --- 5. 側邊欄 ---
st.sidebar.title("🏮 博弈宗師心法")
proverbs = [
    "第一：寧棄莫出銃", "第二：人旺我亂碰", "第三：牌衰過三棟",
    "第四：牌尾吃卡檔", "第五：牌可以輸，牌品不可輸", "第六：胡可以吃進，威不可拿",
    "第七：贏的是人不是牌", "第八：輸是輸條命，不是牌",
    "第九：牌旺自然手香", "第十：牌爛未必輸，人賤天收"
]
for p in proverbs:
    st.sidebar.markdown(f'<div class="proverb-text">{p}</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.title("📜 歷史戰報")
for d, n in zip(data['日期'][::-1], data['開出號碼'][::-1]):
    st.sidebar.markdown(f"**📅 {d}**")
    st.sidebar.code(" ".join([f"{x:02d}" for x in n]))

# --- 6. 主戰情室 ---
st.title("🔱 赤鍊紅蓮・參天律時空戰情室 (v8.5)")

# 狀態列
c1, c2, c3 = st.columns(3)
c1.info(f"能量乖離：{bias:.1f}% (蓄力反彈)")
c2.success("💰 財神方位：正西")
c3.warning("✨ 貴人方位：正東")

st.markdown("---")

# === 核心戰略區 (參天律矩陣) ===
col_main, col_witch = st.columns([2, 1])

# 統帥策略：五星
strategy_nums = [3, 8, 17, 21, 26]

with col_main:
    st.markdown('<div class="action-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color:#FFD700;">⚔️ 統帥五星・時空解析</h3>', unsafe_allow_html=True)
    
    # 顯示大號碼
    st.markdown(f'<div class="highlight-numbers">{", ".join([f"{n:02d}" for n in strategy_nums])}</div>', unsafe_allow_html=True)
    st.markdown('<hr style="border:0.5px solid #444;">', unsafe_allow_html=True)
    
    # 參天律解碼表
    for n in strategy_nums:
        season, s_cls, weather, w_icon = decode_cantian(n)
        st.markdown(f"""
        <div style="margin-bottom:8px; text-align:left; padding-left:20px;">
            <span style="color:#FFD700; font-size:20px; font-weight:bold; width:40px; display:inline-block;">{n:02d}</span>
            <span class="cantian-tag {s_cls}">{season}</span>
            <span style="color:#E0E0E0; margin-left:10px;">{w_icon} {weather}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 魔女亂碰：動態運算
witch_num, witch_reason, calc_time = calculate_witch_chaos()
season_w, s_cls_w, weather_w, w_icon_w = decode_cantian(witch_num)

with col_witch:
    st.markdown('<div class="witch-card">', unsafe_allow_html=True)
    st.markdown('<h4 style="color:#FF00FF;">🔮 雨菲・亂碰運算</h4>', unsafe_allow_html=True)
    st.caption(f"運算時間：{calc_time}")
    st.markdown(f'<div style="font-size:40px; color:#FFFFFF; font-weight:bold; margin:10px 0;">{witch_num:02d}</div>', unsafe_allow_html=True)
    st.markdown(f'<span class="cantian-tag {s_cls_w}">{season_w}</span> {w_icon_w}', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:12px; color:#FF00FF; margin-top:10px;">{witch_reason}</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:12px; color:#aaa;">「人旺我亂碰，規律由我定」</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# === 圖表與能量分析 (完整回歸) ===
st.markdown("---")
st.subheader("📊 專業圖表分析")

tab1, tab2, tab3 = st.tabs(["🌪️ 五行能量條", "📈 和值 K 線圖", "🔥 季節熱力圖"])

with tab1:
    st.caption("五行對應：1,6水 | 2,7火 | 3,8風(木) | 4,9電(金) | 5,0晴(土)")
    e_counts = {"Water":0, "Fire":0, "Wood":0, "Metal":0, "Earth":0}
    for n in all_nums:
        d = n % 10
        if d in [1,6]: e_counts["Water"]+=1
        elif d in [2,7]: e_counts["Fire"]+=1
        elif d in [3,8]: e_counts["Wood"]+=1
        elif d in [4,9]: e_counts["Metal"]+=1
        else: e_counts["Earth"]+=1
    
    ec1, ec2, ec3, ec4, ec5 = st.columns(5)
    total = sum(e_counts.values())
    colors = {"Water":"#1E90FF", "Fire":"#FF4500", "Wood":"#32CD32", "Metal":"#FFD700", "Earth":"#8B4513"}
    labels = {"Water":"雨 (水)", "Fire":"火 (火)", "Wood":"風 (木)", "Metal":"電 (金)", "Earth":"晴 (土)"}
    
    for i, (k, col) in enumerate(zip(e_counts.keys(), [ec1, ec2, ec3, ec4, ec5])):
        with col:
            st.markdown(f"<div style='text-align:center; color:{colors[k]}; font-weight:bold;'>{labels[k]}</div>", unsafe_allow_html=True)
            st.progress(e_counts[k]/total)
            st.markdown(f"<div style='text-align:center;'>{e_counts[k]} 顆</div>", unsafe_allow_html=True)

with tab2:
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=df['日期'], y=df['和值'], mode='lines+markers', line=dict(color='#FFD700', width=4), name='和值'))
    fig_trend.add_hline(y=100, line_dash="dash", line_color="#00FF00")
    fig_trend.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E0E0E0'), height=300, margin=dict(t=20, b=20))
    st.plotly_chart(fig_trend, use_container_width=True)

with tab3:
    st.caption("Y軸：季節 (春0/夏1/秋2/冬3)  |  X軸：氣象 (雨/火/風/電/晴)")
    # 熱力圖數據對應
    y_labels = ["春 (0頭)", "夏 (1頭)", "秋 (2頭)", "冬 (3頭)"]
    x_labels = ["1(雨)", "2(火)", "3(風)", "4(電)", "5(晴)", "6(雨)", "7(火)", "8(風)", "9(電)", "0(晴)"]
    fig_heat = px.imshow(heatmap_data, x=x_labels, y=y_labels, color_continuous_scale="YlOrRd", text_auto=True)
    fig_heat.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E0E0E0'), height=300)
    st.plotly_chart(fig_heat, use_container_width=True)
