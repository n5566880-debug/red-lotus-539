import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import random
import numpy as np

# --- 1. 頁面基礎設定 ---
st.set_page_config(page_title="赤鍊紅蓮・539戰情室", layout="wide", page_icon="🔱")

# --- CSS 深度美化 ---
st.markdown("""
<style>
    .stApp { background-color: #0D0D0D; color: #E0E0E0; }
    .action-card { background: linear-gradient(135deg, #3d0000 0%, #000000 100%); padding: 25px; border-radius: 15px; border: 3px solid #FFD700; text-align: center; box-shadow: 0 10px 30px rgba(255, 215, 0, 0.2); }
    .witch-card { background: linear-gradient(135deg, #1a0033 0%, #000000 100%); padding: 20px; border-radius: 15px; border: 2px solid #FF00FF; text-align: center; }
    .direction-box { background: #1a1a1a; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #333; }
    .highlight-numbers { color: #FFD700; font-size: 58px; font-weight: bold; letter-spacing: 15px; text-shadow: 2px 2px 10px rgba(255, 215, 0, 0.5); }
    .proverb-text { font-size: 13px; color: #D4AF37; font-style: italic; margin-bottom: 8px; line-height: 1.4; }
</style>
""", unsafe_allow_html=True)

# --- 2. 核心數據中心 (修復前導零錯誤) ---
data = {
    '日期': ['1/4', '1/5', '1/6', '1/7', '1/8'],
    '開出號碼': [
        [2, 3, 16, 22, 25],
        [15, 23, 32, 36, 39],
        [4, 13, 21, 28, 35],
        [5, 10, 14, 15, 28],
        [3, 8, 10, 21, 30]  # 最新開獎數據
    ]
}

# 輔助計算
def get_current_taiwan_time():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=8)

def get_lucky_direction(hour, day):
    random.seed(hour + day)
    directions = ["正北", "東北", "正東", "東南", "正南", "西南", "正西", "西北"]
    return random.choice(directions), random.choice(directions)

df = pd.DataFrame(data)
df['和值'] = df['開出號碼'].apply(sum)
latest_he = df['和值'].iloc[-1]

# --- 3. 側邊欄：歷史與金句 ---
st.sidebar.title("🏮 博弈宗師心法")
proverbs = [
    "第一：寧棄莫出銃", "第二：人旺我亂碰", "第三：牌衰過三棟",
    "第五：牌可以輸，牌品不可輸", "第七：你贏的是人不是牌",
    "第九：牌旺自然隻手香", "第十：牌爛未必輸，人賤天收"
]
for p in proverbs:
    st.sidebar.markdown(f'<div class="proverb-text">{p}</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.title("📜 彈道紀錄")
for d, n in zip(data['日期'][::-1], data['開出號碼'][::-1]):
    st.sidebar.markdown(f"**📅 {d}** → `{' '.join([f'{x:02d}' for x in n])}`")

# --- 4. 主戰情室介面 ---
st.title("🔱 赤鍊紅蓮・三星連環戰情室 (v7.9 修復版)")

# 頂部狀態列
st.markdown("---")
c1, c2, c3 = st.columns(3)
with c1:
    st.info(f"當前和值：{latest_he}")
with c2:
    st.success(f"💰 財神方位：正西")
with c3:
    st.warning(f"✨ 貴人方位：正東")

# 核心戰略區
st.markdown("---")
col_main, col_witch = st.columns([2, 1])

with col_main:
    st.markdown(f"""
    <div class="action-card">
        <h3 style="color:#FFD700; margin-bottom:10px;">⚔️ 明日 (1/9) 總攻陣列</h3>
        <div class="highlight-numbers">17, 21, 26</div>
        <p style="font-size:18px; margin-top:20px; color:#FFFFFF;">戰略：<b>三星合圍・伏吟守護</b></p>
        <hr style="border:0.5px solid #444;">
        <p style="color:#aaa; font-size:14px;">
            卦象：平（伏吟之局，動不如靜）<br>
            21號連莊期待，17號本命感應，26號魔女干擾。
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_witch:
    st.markdown("""
    <div class="witch-card">
        <h4 style="color:#FF00FF; margin:0;">🔮 雨菲指令：亂碰</h4>
        <div style="font-size:32px; color:#FFFFFF; font-weight:bold; margin:15px 0;">26</div>
        <p style="font-size:12px; color:#FF00FF;">
            「人旺我亂碰」<br>
            以水潤燥，打亂伏吟規律。
        </p>
    </div>
    """, unsafe_allow_html=True)

# 圖表顯示
st.markdown("---")
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['日期'], y=df['和值'], mode='lines+markers', line=dict(color='#FFD700', width=4)))
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E0E0E0'), height=300)
st.plotly_chart(fig, use_container_width=True)
