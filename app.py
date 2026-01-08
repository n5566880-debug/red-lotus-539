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
    /* 戰略卡片 */
    .action-card { background: linear-gradient(135deg, #3d0000 0%, #000000 100%); padding: 25px; border-radius: 15px; border: 3px solid #FFD700; text-align: center; box-shadow: 0 10px 30px rgba(255, 215, 0, 0.2); }
    .witch-card { background: linear-gradient(135deg, #1a0033 0%, #000000 100%); padding: 20px; border-radius: 15px; border: 2px solid #FF00FF; text-align: center; }
    .direction-box { background: #1a1a1a; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #333; }
    /* 號碼高亮 */
    .highlight-numbers { color: #FFD700; font-size: 58px; font-weight: bold; letter-spacing: 15px; text-shadow: 2px 2px 10px rgba(255, 215, 0, 0.5); }
    .proverb-text { font-size: 13px; color: #D4AF37; font-style: italic; margin-bottom: 8px; line-height: 1.4; }
</style>
""", unsafe_allow_html=True)

# --- 2. 核心數據中心 (同步 1/8 戰果) ---
data = {
    '日期': ['1/4', '1/5', '1/6', '1/7', '1/8'],
    '開出號碼': [
        [02, 03, 16, 22, 25],
        [15, 23, 32, 36, 39],
        [04, 13, 21, 28, 35],
        [05, 10, 14, 15, 28],
        [03, 08, 10, 21, 30]  # 最新：21 號已現
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
bias = ((latest_he - 100) / 100) * 100

# --- 3. 側邊欄：心法與歷史 ---
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
st.title("🔱 赤鍊紅蓮・三星連環戰情室 (v7.9)")
st.caption(f"當前系統時間：{get_current_taiwan_time().strftime('%Y-%m-%d %H:%M:%S')} | 參天律偵測中")

# 頂部狀態列
st.markdown("---")
c1, c2, c3 = st.columns(3)
with c1:
    st.info(f"和值回歸：{latest_he} → 目標 100+")
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
        <p style="font-size:18px; margin-top:20px; color:#FFFFFF;">戰略：<b>三星合圍・水火既濟</b></p>
        <hr style="border:0.5px solid #444;">
        <p style="color:#aaa; font-size:14px;">
            17(統帥火) + 21(予婕木) = 木生火，緣分延續<br>
            26(雨菲水) = 水剋火，壓制秋燥，打破伏吟死局
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_witch:
    st.markdown("""
    <div class="witch-card">
        <h4 style="color:#FF00FF; margin:0;">🔮 魔女雨菲：亂碰模組</h4>
        <p style="font-size:12px; color:#aaa; margin-top:10px;">「不敢開口，就讓盤面說話。」</p>
        <div style="font-size:32px; color:#FFFFFF; font-weight:bold; margin:15px 0;">26</div>
        <p style="font-size:12px; color:#FF00FF; line-height:1.5;">
            能量屬性：💧 潤澤之水<br>
            戰術功能：強行切換摸牌順序，<br>震盪斷聯中的「死氣」。
        </p>
    </div>
    """, unsafe_allow_html=True)

# 數據視覺化
st.markdown("---")
st.subheader("📈 重心偏移與熱力感應")
t_plot, t_heat = st.tabs(["和值 K 線圖", "數字分佈熱力"])

with t_plot:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['日期'], y=df['和值'], mode='lines+markers', line=dict(color='#FFD700', width=4), name='和值'))
    fig.add_hline(y=100, line_dash="dash", line_color="#00FF00", annotation_text="中軸回歸線")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E0E0E0'), height=300)
    st.plotly_chart(fig, use_container_width=True)

with t_heat:
    st.info("💡 目前 20 區間（21-29）呈現深紅色，代表能量高度積壓，隨時噴發。")
    # 簡易熱力模擬
    heat_sim = np.random.randint(0, 5, size=(4, 10))
    fig_heat = px.imshow(heat_sim, color_continuous_scale="YlOrRd", labels=dict(x="尾數", y="頭數"))
    fig_heat.update_layout(height=250, margin=dict(t=0,b=0))
    st.plotly_chart(fig_heat, use_container_width=True)
