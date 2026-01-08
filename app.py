import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import random
import numpy as np

# --- 1. 頁面基礎設定 ---
st.set_page_config(page_title="赤鍊紅蓮・539戰情室", layout="wide", page_icon="🔱")

# --- CSS 視覺魔術 (深紅警戒特效) ---
st.markdown("""
<style>
    .stApp { background-color: #0D0D0D; color: #E0E0E0; }
    
    /* 核心卡片 */
    .action-card { background: linear-gradient(135deg, #2c0000 0%, #000000 100%); padding: 20px; border-radius: 15px; border: 2px solid #FFD700; box-shadow: 0 5px 20px rgba(255, 215, 0, 0.2); }
    .witch-card { background: linear-gradient(135deg, #1a0033 0%, #000000 100%); padding: 20px; border-radius: 15px; border: 2px solid #FF00FF; box-shadow: 0 5px 20px rgba(255, 0, 255, 0.2); }
    
    /* 壓力表容器 */
    .pressure-container {
        background-color: #1a1a1a;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        border: 1px solid #333;
    }
    
    /* 壓力條基礎樣式 */
    .pressure-bar-bg {
        width: 100%;
        background-color: #333;
        height: 20px;
        border-radius: 10px;
        margin-top: 5px;
        overflow: hidden;
    }
    
    .pressure-bar-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease-in-out;
        box-shadow: 0 0 10px rgba(0,0,0,0.5);
    }
    
    /* 等級顏色 */
    .level-safe { background: linear-gradient(90deg, #00FF00, #32CD32); width: 20%; }
    .level-warning { background: linear-gradient(90deg, #FFD700, #FF8C00); width: 60%; box-shadow: 0 0 15px #FFD700; }
    
    /* 深紅警戒：極度乾渴 (呼吸燈特效) */
    @keyframes pulse-red {
        0% { box-shadow: 0 0 5px #8B0000; opacity: 0.9; }
        50% { box-shadow: 0 0 25px #FF0000; opacity: 1; }
        100% { box-shadow: 0 0 5px #8B0000; opacity: 0.9; }
    }
    .level-critical { 
        background: linear-gradient(90deg, #FF0000, #8B0000); 
        width: 95%; 
        animation: pulse-red 1.5s infinite; 
    }

    /* 數字與標籤 */
    .pressure-label { display: flex; justify-content: space-between; font-size: 14px; font-weight: bold; }
    .num-tag { font-family: 'Courier New', monospace; font-size: 18px; font-weight: bold; color: #FFF; }
    .alert-text { color: #FF4500; font-weight: bold; letter-spacing: 2px; }
    
    /* 參天律標籤 */
    .cantian-tag { display: inline-block; padding: 2px 6px; border-radius: 4px; font-size: 12px; margin-left: 5px; color: #000; font-weight: bold; }
    .tag-spring { background: #98FB98; }
    .tag-summer { background: #FF4500; color: #FFF; }
    .tag-autumn { background: #FFD700; }
    .tag-winter { background: #ADD8E6; }
    
    .highlight-numbers { color: #FFD700; font-size: 40px; font-weight: bold; letter-spacing: 5px; text-shadow: 2px 2px 10px rgba(255, 215, 0, 0.5); }
</style>
""", unsafe_allow_html=True)

# --- 2. 核心邏輯 ---
def decode_cantian(num):
    if 1 <= num <= 9: season, s_class = "春", "tag-spring"
    elif 10 <= num <= 19: season, s_class = "夏", "tag-summer"
    elif 20 <= num <= 29: season, s_class = "秋", "tag-autumn"
    elif 30 <= num <= 39: season, s_class = "冬", "tag-winter"
    else: season, s_class = "未知", ""
    
    tail = num % 10
    weather = "晴"
    if tail in [1, 6]: weather = "雨"
    elif tail in [2, 7]: weather = "火"
    elif tail in [3, 8]: weather = "風"
    elif tail in [4, 9]: weather = "電"
    
    return season, s_class, weather

# 模擬真實的遺漏數據 (為了展示視覺效果，這裡包含模擬的高壓號碼)
# 在實際運作中，這應該是從歷史數據庫動態計算的
def get_pressure_data():
    # 模擬數據：號碼: 遺漏期數
    pressure_dict = {
        24: 32, # 深紅警戒 (模擬)
        34: 35, # 深紅警戒 (模擬)
        25: 18, # 警戒
        9: 12,  # 警戒
        26: 8,  # 安全
        17: 5,  # 安全
        21: 1   # 剛開過
    }
    # 排序：從壓力大到小
    sorted_items = sorted(pressure_dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_items

# --- 3. 主程式 ---
data = {
    '日期': ['1/4', '1/5', '1/6', '1/7', '1/8'],
    '開出號碼': [[2, 3, 16, 22, 25], [15, 23, 32, 36, 39], [4, 13, 21, 28, 35], [5, 10, 14, 15, 28], [3, 8, 10, 21, 30]]
}
df = pd.DataFrame(data)
df['和值'] = df['開出號碼'].apply(sum)

st.sidebar.title("🏮 博弈宗師心法")
for p in ["寧棄莫出銃", "人旺我亂碰", "贏的是人不是牌", "牌弱打生死張"]:
    st.sidebar.text(p)
st.sidebar.markdown("---")
st.sidebar.title("📜 歷史戰報")
for d, n in zip(data['日期'][::-1], data['開出號碼'][::-1]):
    st.sidebar.code(f"{d}: {' '.join([f'{x:02d}' for x in n])}")

# --- 戰情室主介面 ---
st.title("🔱 赤鍊紅蓮・回彈臨界點視覺化 (v8.6)")
c1, c2, c3 = st.columns(3)
c1.info("氣象：火春 (0頭旺)")
c2.success("財神：正西")
c3.warning("能量：蓄力反彈中")

st.markdown("---")

# === 視覺化核心：能量壓力表 (The Rebound Trigger) ===
st.markdown("### 🩸 回彈臨界點・深紅警戒 (Pressure Gauge)")
st.caption("魔女直覺區：越紅代表越乾渴，隨時可能「報復性噴發」")

# 獲取壓力數據
pressure_data = get_pressure_data()
p_cols = st.columns(3) # 分三欄顯示

for i, (num, missed) in enumerate(pressure_data):
    # 決定樣式
    if missed >= 30:
        bar_class = "level-critical"
        status_text = "🚨 極度乾渴 (DANGER)"
        text_color = "#FF0000"
    elif missed >= 10:
        bar_class = "level-warning"
        status_text = "⚠️ 蓄能警戒"
        text_color = "#FFD700"
    else:
        bar_class = "level-safe"
        status_text = "🟢 能量平穩"
        text_color = "#32CD32"
        
    season, s_cls, weather = decode_cantian(num)
    
    # 顯示壓力卡 (使用 HTML/CSS 渲染)
    with p_cols[i % 3]:
        st.markdown(f"""
        <div class="pressure-container">
            <div class="pressure-label">
                <div>
                    <span class="num-tag">{num:02d}</span>
                    <span class="cantian-tag {s_cls}">{season}</span>
                    <span style="font-size:12px; color:#aaa;">{weather}</span>
                </div>
                <div style="color:{text_color}; font-size:12px;">{status_text}</div>
            </div>
            <div style="font-size:12px; color:#aaa; margin-top:5px;">已遺漏 {missed} 期</div>
            <div class="pressure-bar-bg">
                <div class="{bar_class} pressure-bar-fill"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# === 統帥行動區 ===
col_main, col_witch = st.columns([2, 1])

with col_main:
    st.markdown("""
    <div class="action-card">
        <h3 style="color:#FFD700;">⚔️ 統帥・五星總攻 (1/9)</h3>
        <div class="highlight-numbers">03, 08, 17, 21, 26</div>
        <p style="color:#aaa; font-size:14px; margin-top:10px;">
            【春】03, 08 (火源) <br>
            【夏】17 (本命) <br>
            【秋】21, 26 (收割)
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_witch:
    st.markdown("""
    <div class="witch-card">
        <h4 style="color:#FF00FF; margin:0;">🔮 雨菲亂碰</h4>
        <div style="font-size:32px; color:#FFFFFF; font-weight:bold; margin:10px 0;">26</div>
        <p style="font-size:12px; color:#FF00FF;">水火既濟・打破伏吟</p>
    </div>
    """, unsafe_allow_html=True)
    
# K線圖
fig = px.line(df, x='日期', y='和值', markers=True)
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E0E0E0'), height=200, margin=dict(t=10, b=10))
st.plotly_chart(fig, use_container_width=True)
