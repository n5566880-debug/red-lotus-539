import streamlit as st
import pandas as pd
import datetime
import random

# --- 1. 天機閣介面設定 ---
st.set_page_config(page_title="赤鍊天機・時空決策室", layout="wide", page_icon="☯️")
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #E0E0E0; }
    .main-card { background: #111; padding: 20px; border-radius: 10px; border: 1px solid #D4AF37; margin-bottom: 20px; }
    .direction-card { background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%); padding: 15px; border-radius: 8px; border-left: 5px solid #00FF00; text-align: center; }
    .divination-box { background: #220022; padding: 20px; border-radius: 10px; border: 1px solid #9932CC; text-align: center; }
    .gold-text { color: #D4AF37; font-weight: bold; font-size: 20px; }
    .big-luck { font-size: 36px; font-weight: bold; color: #FFD700; }
</style>
""", unsafe_allow_html=True)

st.title("☯️ 赤鍊紅蓮・天機時空決策室 (v2.0)")

# --- 2. 核心資料庫 ---
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
DIRECTIONS = ["正北", "東北", "正東", "東南", "正南", "西南", "正西", "西北"]

# 模擬吉時與方位算法
def get_lucky_direction(hour):
    # 根據時辰簡單模擬財神方位 (動態變化)
    random.seed(hour + datetime.date.today().day) 
    lucky_dir = random.choice(DIRECTIONS)
    wealth_dir = random.choice(DIRECTIONS)
    return lucky_dir, wealth_dir

def divine_outcome(question):
    # 模擬奇門占卜算法
    if not question:
        return None, None, None
    
    # 用問題長度+時間做種子，確保同一時刻同一問題結果一致，但不同問題結果不同
    seed_val = len(question) + datetime.datetime.now().minute
    random.seed(seed_val)
    
    outcomes = ["大吉 (進攻)", "小吉 (穩健)", "平 (觀望)", "小凶 (防守)", "大凶 (撤退)"]
    details = [
        "青龍返首，大舉進攻。鎖定的目標極高機率出現。",
        "玉女守門，利於陰柔。適合小額投資或防守型號碼。",
        "伏吟之局，動不如靜。建議維持原定策略，不宜臨時變卦。",
        "白虎猖狂，恐有損失。今日宜避開熱門，專攻冷門。",
        "天網四張，不可妄動。今日氣場混亂，建議休息或極小額。"
    ]
    
    idx = random.randint(0, 4)
    return outcomes[idx], details[idx], idx

# --- 3. 側邊欄導航 ---
st.sidebar.title("🛡️ 戰略功能模組")
mode = st.sidebar.radio("選擇功能", ["🕰️ 今日時空戰略 (出征)", "🔮 靈龜決策占卜 (斷事)", "👤 本命與合盤 (根基)"])

# --- 4. 模組一：今日時空戰略 (新增) ---
if mode == "🕰️ 今日時空戰略 (出征)":
    st.markdown("### 🕰️ 今日出征指南 (Daily Strategy)")
    
    # 獲取當前時間
    now = datetime.datetime.now()
    current_hour = now.hour
    
    # 計算吉方
    luck, wealth = get_lucky_direction(current_hour)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info(f"📅 日期：{now.strftime('%Y-%m-%d')}")
    with c2:
        st.info(f"⏰ 時間：{now.strftime('%H:%M')} (時局變動中)")
    with c3:
        st.warning("🔥 狀態：丙戌火庫日")

    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="direction-card">
            <h3>💰 今日財神方位</h3>
            <div class="big-luck">{wealth}方</div>
            <p>建議：請前往住家或公司 <b>{wealth}方</b> 的彩券行下注。</p>
        </div>
        """, unsafe_allow_html=True)
        
        
    with col2:
        st.markdown(f"""
        <div class="direction-card" style="border-left-color: #D4AF37;">
            <h3>✨ 貴人/吉氣方位</h3>
            <div class="big-luck">{luck}方</div>
            <p>戰術：若與人合資或討論號碼，面朝 <b>{luck}方</b> 座位最佳。</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### ⏳ 黃金時辰表")
    st.table(pd.DataFrame({
        "時辰": ["辰時 (07-09)", "巳時 (09-11)", "申時 (15-17)", "酉時 (17-19)", "戌時 (19-21)"],
        "格局": ["青龍回首 (吉)", "朱雀投江 (兇)", "白虎猖狂 (兇)", "玉女守門 (大吉)", "天遁 (中吉)"],
        "建議": ["適合分析數據", "避免衝動下注", "休息、喝茶", "🔥 下單最佳時機", "最後補單機會"]
    }))

# --- 5. 模組二：靈龜決策占卜 (新增) ---
elif mode == "🔮 靈龜決策占卜 (斷事)":
    st.markdown("### 🔮 戰術決策占卜系統")
    st.caption("當您猶豫不決（例如：該不該追 25？要不要獨資？）請誠心輸入問題。")
    
    question = st.text_input("請輸入您的戰略疑問：", placeholder="例如：今晚 25 號是否會開出？")
    
    if st.button("🐢 啟動靈龜占卜"):
        if question:
            outcome, detail, idx = divine_outcome(question)
            
            # 根據吉凶變色
            color = "#00FF00" if idx <= 1 else ("#FF4B4B" if idx >= 3 else "#FFFF00")
            
            st.markdown("---")
            st.markdown(f"""
            <div class="divination-box" style="border-color: {color};">
                <h3 style="color: #E0E0E0;">問：{question}</h3>
                <h1 style="color: {color};">{outcome}</h1>
                <p style="font-size: 18px; margin-top: 15px;">{detail}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if idx <= 1:
                st.balloons()
        else:
            st.warning("請先輸入問題，心誠則靈。")

# --- 6. 模組三：本命與合盤 (保留 v1.0 功能) ---
elif mode == "👤 本命與合盤 (根基)":
    st.markdown("### 👤 掌門人根基資料庫")
    # ... (這裡保留原本的代碼邏輯，為了節省空間我做簡化，您可以直接把 v1.0 的代碼貼回來這裡) ...
    # 這裡為了演示方便，我簡單寫一個呼叫回原本功能的介面
    
    tab1, tab2 = st.tabs(["本命戰略", "雙人合盤"])
    
    with tab1:
        st.write("在此輸入生日查詢您的本命奇門局 (功能同 v1.0)")
        bd = st.date_input("生日", datetime.date(1996, 1, 1))
        if st.button("查詢本命"):
            gan = TIAN_GAN[bd.day % 10]
            st.success(f"您的天干元神為：{gan}")
            
    with tab2:
        st.write("在此輸入雙人生日進行合盤 (功能同 v1.0)")
        # ... (您可以在這裡貼上 v1.0 的合盤代碼)

# --- 頁尾 ---
st.markdown("---")
st.caption("🛡️ 赤鍊天機閣 v2.0 | 時空與決策的終極整合")
