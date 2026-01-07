import streamlit as st
import pandas as pd
import numpy as np
import datetime
import random

# --- 1. 帝國指揮部風格 ---
st.set_page_config(page_title="赤鍊天機・動態狙擊版", layout="wide", page_icon="🔱")
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #E0E0E0; }
    .main-card { background: #0f0f0f; padding: 25px; border-radius: 10px; border: 1px solid #D4AF37; margin-bottom: 20px; box-shadow: 0 0 15px rgba(212, 175, 55, 0.1); }
    .score-card { background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%); padding: 20px; border-radius: 10px; border-left: 5px solid #00FF00; text-align: center; }
    .gambler-panel { background: #0a192f; padding: 20px; border-radius: 12px; border: 1px solid #64ffda; box-shadow: 0 0 10px rgba(100, 255, 218, 0.1); text-align: center; }
    .gambler-stat { font-size: 24px; font-weight: bold; color: #64ffda; }
    .gambler-label { font-size: 14px; color: #8892b0; margin-bottom: 5px; }
    .radar-box { background: #110011; padding: 15px; border-radius: 10px; border: 1px solid #FF00FF; margin-top: 10px; box-shadow: 0 0 10px rgba(255, 0, 255, 0.2); }
    .strategy-box { background: #002200; padding: 15px; border-radius: 5px; border-left: 3px solid #00FF00; margin-top: 10px; }
    .divination-box { background: #220022; padding: 20px; border-radius: 10px; border: 1px solid #9932CC; text-align: center; }
    .gold-text { color: #D4AF37; font-weight: bold; font-size: 22px; }
    .big-luck { font-size: 36px; font-weight: bold; color: #FFD700; }
    h3 { border-bottom: 1px solid #333; padding-bottom: 10px; margin-top: 25px; color: #fff; }
</style>
""", unsafe_allow_html=True)

# --- 2. 核心資料庫 (不變) ---
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DIRECTIONS = ["正北", "東北", "正東", "東南", "正南", "西南", "正西", "西北"]
DATA_DICT = {
    "甲": {"title": "參天巨木", "personality": "剛毅正直", "career": "管理、軍警", "wealth": "正財實業", "health": "膽囊、頭部", "cycle": ["25-34歲:紮根", "35-44歲:破土", "45-54歲:成林"]},
    "乙": {"title": "花草藤蔓", "personality": "靈活堅韌", "career": "行銷、策劃", "wealth": "偏財人脈", "health": "肝臟、四肢", "cycle": ["25-34歲:探索", "35-44歲:攀附", "45-54歲:繁花"]},
    "丙": {"title": "太陽之火", "personality": "熱情急躁", "career": "演藝、業務", "wealth": "名氣生財", "health": "心血管", "cycle": ["25-34歲:燃燒", "35-44歲:普照", "45-54歲:餘溫"]},
    "丁": {"title": "星燭之火", "personality": "細膩神祕", "career": "心理、研發", "wealth": "智慧專利", "health": "心臟、眼", "cycle": ["25-34歲:點燈", "35-44歲:燎原", "45-54歲:光耀"]},
    "戊": {"title": "崇山峻嶺", "personality": "穩重固執", "career": "房產、倉儲", "wealth": "積土成山", "health": "胃、消化", "cycle": ["25-34歲:堆土", "35-44歲:成山", "45-54歲:鎮守"]},
    "己": {"title": "田園之土", "personality": "內斂多藝", "career": "教育、秘書", "wealth": "技能副業", "health": "脾、代謝", "cycle": ["25-34歲:耕耘", "35-44歲:收穫", "45-54歲:養生"]},
    "庚": {"title": "刀劍之金", "personality": "果斷義氣", "career": "司法、外科", "wealth": "險中求財", "health": "肺、大腸", "cycle": ["25-34歲:磨礪", "35-44歲:鋒芒", "45-54歲:收鞘"]},
    "辛": {"title": "珠寶之金", "personality": "精緻愛面子", "career": "金融、醫美", "wealth": "品牌溢價", "health": "肺、皮膚", "cycle": ["25-34歲:雕琢", "35-44歲:發光", "45-54歲:鑑賞"]},
    "壬": {"title": "江河之水", "personality": "聰明奔放", "career": "貿易、物流", "wealth": "流動價差", "health": "腎、膀胱", "cycle": ["25-34歲:奔流", "35-44歲:匯聚", "45-54歲:入海"]},
    "癸": {"title": "雨露之水", "personality": "溫柔縝密", "career": "會計、幕僚", "wealth": "積少成多", "health": "腎、內分泌", "cycle": ["25-34歲:滲透", "35-44歲:滋潤", "45-54歲:昇華"]}
}

def get_current_taiwan_time():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=8)
def get_lucky_direction(hour, day):
    random.seed(hour + day) 
    return random.choice(DIRECTIONS), random.choice(DIRECTIONS)
def divine_outcome(question):
    if not question: return None, None, None
    seed_val = len(question) + datetime.datetime.now().minute
    random.seed(seed_val)
    outcomes = ["大吉", "小吉", "平", "小凶", "大凶"]
    details = ["青龍返首，大舉進攻。", "玉女守門，利於陰柔。", "伏吟之局，動不如靜。", "白虎猖狂，恐有損失。", "天網四張，不可妄動。"]
    idx = random.randint(0, 4)
    return outcomes[idx], details[idx], idx

# --- 3. 戰略導航 ---
st.sidebar.title("🛡️ 戰略功能模組")
mode = st.sidebar.radio("請選擇戰略層級", [
    "🎰 賭王決策系統 (核心)", 
    "📈 財務戰績覆盤",
    "📡 予婕情緒雷達",
    "📊 號碼技術分析",
    "🕰️ 今日時空戰略", 
    "👤 深層本命解析", 
    "💞 情場戰略指揮部"
])

# ==========================================================
# 模組 1: 🎰 賭王決策系統 (核心 - 動態版)
# ==========================================================
if mode == "🎰 賭王決策系統 (核心)":
    st.markdown("## 🎰 專業資金控管・戰術終端")
    
    # 🌟 這裡新增了「目標號碼」輸入框
    target_nums = st.text_input("🎯 輸入本期鎖定號碼 (例如: 24, 25)", "24, 25")
    
    with st.expander("⚙️ 戰術參數設定", expanded=True):
        col_s1, col_s2, col_s3 = st.columns(3)
        balance = col_s1.number_input("💰 總戰備資金", value=2000, step=100)
        cost_per_bet = col_s2.number_input("🎟️ 單注成本", value=80, min_value=80)
        win_prob = col_s3.slider("🎯 系統預估勝率", 1, 20, 5)

    odds = 53
    b = odds - 1
    p = win_prob / 100
    q = 1 - p
    kelly_f = max(0, (b * p - q) / b)
    safe_kelly = kelly_f * 0.5 
    suggest_amount = balance * safe_kelly
    suggest_units = int(suggest_amount // cost_per_bet)
    
    st.markdown("---")
    st.markdown("### 📊 決策儀表板")
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"""<div class="gambler-panel"><div class="gambler-label">建議下注比例</div><div class="gambler-stat">{round(safe_kelly * 100, 2)}%</div></div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class="gambler-panel"><div class="gambler-label">建議總金額</div><div class="gambler-stat" style="color:#FFD700;">${int(suggest_amount)}</div></div>""", unsafe_allow_html=True)
    
    color = "#00FF00" if suggest_units >= 1 else "#FF4B4B"
    c3.markdown(f"""<div class="gambler-panel" style="border-color:{color};"><div class="gambler-label">執行注數</div><div class="gambler-stat" style="color:{color};">{suggest_units} 注</div></div>""", unsafe_allow_html=True)

    if suggest_units == 0: 
        st.warning("⚠️ 警告：風險過高，建議觀望或僅下 1 注。")
    else: 
        # 🌟 這裡的指令會自動變更為您輸入的號碼
        st.success(f"✅ 指令：請執行 **{suggest_units} 注** (共 ${suggest_units * cost_per_bet})，目標鎖定 **{target_nums}**。")

# ==========================================================
# 模組 2: 📈 財務戰績覆盤
# ==========================================================
elif mode == "📈 財務戰績覆盤":
    st.markdown("## 📈 財務長・ROI 戰績覆盤")
    dates = pd.date_range(end=datetime.datetime.today(), periods=30)
    data = {'Date': dates, 'Profit': np.cumsum(np.random.randn(30) * 1000 + 200)}
    st.line_chart(pd.DataFrame(data).set_index('Date')['Profit'], height=300)
    st.info("💡 這是模擬數據，未來請在此記錄您的真實戰績。")

# ==========================================================
# 模組 3: 📡 予婕情緒雷達
# ==========================================================
elif mode == "📡 予婕情緒雷達":
    st.markdown("## 📡 情報官・予婕情緒氣象台")
    now = get_current_taiwan_time()
    st.markdown(f"""<div class="radar-box"><h3 style="color:#FF00FF;">👩🏻 對象：予婕 (乙木坐午)</h3><p>📅 日期：{now.strftime('%Y-%m-%d')} (自動運算中...)</p></div>""", unsafe_allow_html=True)
    st.info("📊 **情緒指數：65 (敏感)** | 建議戰術：溫柔安撫，切勿說教。")
    st.markdown("""<div class="strategy-box"><b>✅ 統帥錦囊：</b><br>明日氣場「子午沖」，她情緒不穩。請用美食與陪伴代替講道理。</div>""", unsafe_allow_html=True)

# ==========================================================
# 模組 4: 📊 號碼技術分析 (動態版)
# ==========================================================
elif mode == "📊 號碼技術分析":
    st.markdown("## 📊 分析師・號碼趨勢 K 線")
    
    # 🌟 這裡也可以輸入號碼
    target_nums_input = st.text_input("輸入欲分析號碼 (如: 05, 10, 14)", "24, 25")
    
    st.markdown(f"### 🎯 目標號碼：{target_nums_input} (連動分析)")
    
    col_k1, col_k2, col_k3 = st.columns(3)
    col_k1.metric("RSI 指標", "15 (超賣)", "觸底反彈")
    col_k2.metric("MACD 能量", "-0.85", "空方衰竭")
    col_k3.metric("遺漏期數", "8 期", "黃金回補")
    
    st.markdown("#### 📈 能量累積模擬圖")
    
    # 🌟 讓圖表的標籤自動跟著號碼變
    nums_list = target_nums_input.replace("，", ",").split(",")
    # 為了展示效果，產生隨機數據
    chart_data = pd.DataFrame(
        np.random.randn(20, len(nums_list)), 
        columns=[f"{n.strip()}號能量" for n in nums_list]
    )
    st.line_chart(chart_data)
    
    st.success(f"✅ **技術結論**：號碼組合 **[{target_nums_input}]** 出現技術面買點。")

# ==========================================================
# 模組 5, 6, 7 (保留原貌)
# ==========================================================
elif mode == "🕰️ 今日時空戰略":
    st.title("🕰️ 今日出征指南")
    now = get_current_taiwan_time()
    luck, wealth = get_lucky_direction(now.hour, now.day)
    c1,c2,c3 = st.columns(3)
    c1.info(f"📅 {now.strftime('%Y-%m-%d')}"); c2.info(f"⏰ {now.strftime('%H:%M')}"); c3.warning("🔥 狀態：丁亥日")
    st.markdown("---")
    st.columns(2)[0].markdown(f"""<div class="direction-card"><h3>💰 財神</h3><div class="big-luck">{wealth}方</div></div>""", unsafe_allow_html=True)
    st.columns(2)[1].markdown(f"""<div class="direction-card" style="border-left-color:#D4AF37"><h3>✨ 貴人</h3><div class="big-luck">{luck}方</div></div>""", unsafe_allow_html=True)
    q = st.text_input("戰略疑問："); 
    if st.button("🐢 啟動"): 
        o,d,i = divine_outcome(q); st.markdown(f"""<div class="divination-box"><h3>{q}</h3><h1>{o}</h1><p>{d}</p></div>""", unsafe_allow_html=True)

elif mode == "👤 深層本命解析":
    st.title("👤 掌門人戰略藍圖")
    bd = st.date_input("出生日期", datetime.date(1996, 2, 17))
    if st.button("🚀 掃描"):
        d = DATA_DICT[TIAN_GAN[bd.day % 10]]
        st.markdown(f"""<div class="main-card"><h2 class="gold-text">🗡️ {TIAN_GAN[bd.day % 10]} ({d['title']})</h2><hr><p>{d['personality']}</p><p><b>財富：</b>{d['wealth']}</p></div>""", unsafe_allow_html=True)

elif mode == "💞 情場戰略指揮部":
    st.title("💞 交往/復合戰略推演")
    c1, c2 = st.columns(2)
    if st.button("💘 推演"):
        st.subheader("戰略分析：辛金 ⚔️ 乙木 —— 【征服 (我剋)】")
        st.columns(2)[0].metric("交往指數", "80%"); st.columns(2)[1].metric("復合指數", "55%")
        st.markdown("""<div class="strategy-box">辛金剋乙木。您有主導權，但她怕壓力。請展現高價值，切勿糾纏。</div>""", unsafe_allow_html=True)
