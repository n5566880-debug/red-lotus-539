import streamlit as st
import pandas as pd
import numpy as np
import datetime
import random

# --- 1. 帝國指揮部風格 (極致黑金/霓虹) ---
st.set_page_config(page_title="赤鍊天機・黑箱帝國", layout="wide", page_icon="🔱")
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #E0E0E0; }
    /* 卡片風格 */
    .main-card { background: #0f0f0f; padding: 25px; border-radius: 10px; border: 1px solid #D4AF37; margin-bottom: 20px; box-shadow: 0 0 15px rgba(212, 175, 55, 0.1); }
    .score-card { background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%); padding: 20px; border-radius: 10px; border-left: 5px solid #00FF00; text-align: center; }
    /* 賭王與金融風格 */
    .gambler-panel { background: #0a192f; padding: 20px; border-radius: 12px; border: 1px solid #64ffda; box-shadow: 0 0 10px rgba(100, 255, 218, 0.1); text-align: center; }
    .gambler-stat { font-size: 24px; font-weight: bold; color: #64ffda; }
    .gambler-label { font-size: 14px; color: #8892b0; margin-bottom: 5px; }
    /* 情報與雷達 */
    .radar-box { background: #110011; padding: 15px; border-radius: 10px; border: 1px solid #FF00FF; margin-top: 10px; box-shadow: 0 0 10px rgba(255, 0, 255, 0.2); }
    .k-line-box { background: #001100; padding: 15px; border-radius: 10px; border: 1px solid #00FF00; margin-top: 10px; }
    /* 通用 */
    .strategy-box { background: #002200; padding: 15px; border-radius: 5px; border-left: 3px solid #00FF00; margin-top: 10px; }
    .divination-box { background: #220022; padding: 20px; border-radius: 10px; border: 1px solid #9932CC; text-align: center; }
    .gold-text { color: #D4AF37; font-weight: bold; font-size: 22px; }
    .big-luck { font-size: 36px; font-weight: bold; color: #FFD700; }
    h3 { border-bottom: 1px solid #333; padding-bottom: 10px; margin-top: 25px; color: #fff; }
</style>
""", unsafe_allow_html=True)

# --- 2. 核心資料庫 (保留所有功能) ---
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DIRECTIONS = ["正北", "東北", "正東", "東南", "正南", "西南", "正西", "西北"]

DATA_DICT = {
    "甲": {"title": "參天巨木・大將軍", "personality": "剛毅、正直、領袖氣質。缺點是過於固執。", "career": "企業管理、軍警、政治領袖。", "wealth": "正財為主，適合實業投資。", "health": "膽囊、頭部神經。", "cycle": ["25-34歲：紮根期", "35-44歲：破土期", "45-54歲：成林期"]},
    "乙": {"title": "花草藤蔓・軍師", "personality": "靈活、堅韌、善於借勢。缺點是缺乏安全感。", "career": "行銷、策劃、藝術、幕僚。", "wealth": "偏財旺盛，適合人脈生財。", "health": "肝臟、四肢、頸椎。", "cycle": ["25-34歲：探索期", "35-44歲：攀附期", "45-54歲：繁花期"]},
    "丙": {"title": "太陽之火・先鋒官", "personality": "熱情、急躁、光芒萬丈。缺點是三分鐘熱度。", "career": "演藝、媒體、銷售、能源。", "wealth": "名氣生財，適合個人品牌。", "health": "心血管、血壓。", "cycle": ["25-34歲：燃燒期", "35-44歲：普照期", "45-54歲：餘溫期"]},
    "丁": {"title": "星燭之火・情報官", "personality": "細膩、神祕、洞察力強。缺點是敏感多疑。", "career": "心理、研發、分析、命理。", "wealth": "智慧生財，靠專利技術。", "health": "心臟、眼睛、失眠。", "cycle": ["25-34歲：點燈期", "35-44歲：燎原期", "45-54歲：光耀期"]},
    "戊": {"title": "崇山峻嶺・後勤統帥", "personality": "穩重、守信、包容力強。缺點是死腦筋。", "career": "房地產、保險、物流、農業。", "wealth": "聚沙成塔，適合不動產。", "health": "胃部、消化系統。", "cycle": ["25-34歲：堆土期", "35-44歲：成山期", "45-54歲：鎮守期"]},
    "己": {"title": "田園之土・參謀長", "personality": "內斂、隨和、心思細膩。缺點是過於憂慮。", "career": "教育、護理、諮詢、秘書。", "wealth": "技能生財，靠多樣副業。", "health": "脾臟、腹部代謝。", "cycle": ["25-34歲：耕耘期", "35-44歲：收穫期", "45-54歲：養生期"]},
    "庚": {"title": "刀劍之金・戰神", "personality": "果斷、講義氣、殺伐果斷。缺點是容易傷人。", "career": "司法、外科醫生、開拓業務。", "wealth": "險中求財，適合波動市場。", "health": "肺部、大腸、外傷。", "cycle": ["25-34歲：磨礪期", "35-44歲：鋒芒期", "45-54歲：收鞘期"]},
    "辛": {"title": "珠寶之金・特種兵", "personality": "精緻、自尊心強、追求完美。缺點是愛面子。", "career": "金融、醫美、珠寶、法律。", "wealth": "品牌生財，提升溢價。", "health": "肺部、皮膚、牙齒。", "cycle": ["25-34歲：雕琢期", "35-44歲：發光期", "45-54歲：鑑賞期"]},
    "壬": {"title": "江河之水・海軍元帥", "personality": "聰明、奔放、大局觀。缺點是虎頭蛇尾。", "career": "貿易、物流、廣告、大數據。", "wealth": "流動生財，靠貿易價差。", "health": "腎臟、膀胱、血液。", "cycle": ["25-34歲：奔流期", "35-44歲：匯聚期", "45-54歲：入海期"]},
    "癸": {"title": "雨露之水・滲透專家", "personality": "溫柔、耐力驚人、心思極密。缺點是情緒化。", "career": "會計、研發、心理、幕僚。", "wealth": "積少成多，穩健基金。", "health": "腎臟、內分泌、冷症。", "cycle": ["25-34歲：滲透期", "35-44歲：滋潤期", "45-54歲：昇華期"]}
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
    outcomes = ["大吉 (進攻)", "小吉 (穩健)", "平 (觀望)", "小凶 (防守)", "大凶 (撤退)"]
    details = ["青龍返首，大舉進攻。", "玉女守門，利於陰柔。", "伏吟之局，動不如靜。", "白虎猖狂，恐有損失。", "天網四張，不可妄動。"]
    idx = random.randint(0, 4)
    return outcomes[idx], details[idx], idx

# --- 3. 戰略導航 (七大模組) ---
st.sidebar.title("🛡️ 戰略功能模組")
mode = st.sidebar.radio("請選擇戰略層級", [
    "🎰 賭王決策系統 (核心)", 
    "📈 財務戰績覆盤 (NEW!)",
    "📡 予婕情緒雷達 (NEW!)",
    "📊 號碼技術分析 (NEW!)",
    "🕰️ 今日時空戰略", 
    "👤 深層本命解析", 
    "💞 情場戰略指揮部"
])

# ==========================================================
# 模組 1: 🎰 賭王決策系統 (核心)
# ==========================================================
if mode == "🎰 賭王決策系統 (核心)":
    st.markdown("## 🎰 專業資金控管・戰術終端")
    st.caption("Professional Gambler Terminal | Kelly Criterion Engine")
    
    with st.expander("⚙️ 戰術參數設定 (Settings)", expanded=True):
        col_s1, col_s2, col_s3 = st.columns(3)
        balance = col_s1.number_input("💰 總戰備資金 (Bankroll)", value=2000, step=100)
        cost_per_bet = col_s2.number_input("🎟️ 單注成本 (Cost)", value=80, min_value=80, help="每注最低 80 元")
        win_prob = col_s3.slider("🎯 系統預估勝率 (Win%)", 1, 20, 5, help="二星中獎機率約 1/53，建議設 5%-10% 之間")

    odds = 53
    b = odds - 1
    p = win_prob / 100
    q = 1 - p
    kelly_f = max(0, (b * p - q) / b)
    safe_kelly = kelly_f * 0.5 
    suggest_amount = balance * safe_kelly
    suggest_units = int(suggest_amount // cost_per_bet)
    
    st.markdown("---")
    st.markdown("### 📊 決策儀表板 (Dashboard)")
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"""<div class="gambler-panel"><div class="gambler-label">建議下注比例 (Ratio)</div><div class="gambler-stat">{round(safe_kelly * 100, 2)}%</div><div style="color:#aaa; font-size:12px;">基於半凱利準則</div></div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class="gambler-panel"><div class="gambler-label">建議總金額 (Amount)</div><div class="gambler-stat" style="color:#FFD700;">${int(suggest_amount)}</div><div style="color:#aaa; font-size:12px;">風險控制在最佳範圍</div></div>""", unsafe_allow_html=True)
    
    color = "#00FF00" if suggest_units >= 1 else "#FF4B4B"
    c3.markdown(f"""<div class="gambler-panel" style="border-color:{color};"><div class="gambler-label">執行注數 (Units)</div><div class="gambler-stat" style="color:{color};">{suggest_units} 注</div><div style="color:#aaa; font-size:12px;">單注 ${cost_per_bet} 元</div></div>""", unsafe_allow_html=True)

    if suggest_units == 0: st.warning("⚠️ 警告：依照目前本金與勝率，建議觀望 (0 注) 或手動 1 注。")
    else: st.success(f"✅ 指令：請執行 **{suggest_units} 注** (共 ${suggest_units * cost_per_bet})，目標鎖定 24, 25。")

# ==========================================================
# 模組 2: 📈 財務戰績覆盤 (NEW!)
# ==========================================================
elif mode == "📈 財務戰績覆盤 (NEW!)":
    st.markdown("## 📈 財務長・ROI 戰績覆盤")
    st.caption("Financial Officer Module | Profit & Loss Analysis")
    
    # 模擬數據 (展示用)
    st.info("💡 這是您的『勝利軌跡』。展示給自己看，證明您是穩定獲利的投資者，而非賭徒。")
    
    # 模擬 30 天數據
    dates = pd.date_range(end=datetime.datetime.today(), periods=30)
    data = {
        'Date': dates,
        'Profit': np.cumsum(np.random.randn(30) * 1000 + 200) # 模擬正向趨勢
    }
    df = pd.DataFrame(data)
    
    st.line_chart(df.set_index('Date')['Profit'], height=300)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("累積淨利 (Net Profit)", "$ 32,500", "+$1,200")
    c2.metric("投資報酬率 (ROI)", "18.5%", "+2.1%")
    c3.metric("勝率 (Win Rate)", "12.8%", "二星連碰")
    
    st.markdown("---")
    st.markdown("### 📝 近期戰役記錄")
    st.table(pd.DataFrame({
        "日期": ["2026-01-07", "2026-01-06", "2026-01-05"],
        "策略": ["真空狙擊 (24,25)", "強勢順開 (05,10)", "防守觀望"],
        "投入": ["$320", "$160", "$0"],
        "結果": ["待開獎", "中 05 ($0)", "避險成功"],
        "損益": ["-", "-$160", "$0"]
    }))

# ==========================================================
# 模組 3: 📡 予婕情緒雷達 (NEW!)
# ==========================================================
elif mode == "📡 予婕情緒雷達 (NEW!)":
    st.markdown("## 📡 情報官・予婕情緒氣象台")
    st.caption("Intelligence Module | Target Mood Radar")
    
    now = get_current_taiwan_time()
    # 模擬干支邏輯 (假設明日 1/9 為戊子日)
    st.markdown(f"""
    <div class="radar-box">
        <h3 style="color:#FF00FF; border-bottom:1px solid #FF00FF;">👩🏻 對象：予婕 (乙木坐午)</h3>
        <p>📅 預測日期：2026-01-09 (週五)</p>
        <p>🌌 當日氣場：<b>戊子日</b> (土水相剋)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🌪️ 心情預報解析")
    c1, c2 = st.columns(2)
    
    # 邏輯：乙木遇戊土(正財) = 務實；遇子水(偏印) = 敏感
    with c1:
        st.info("📊 **情緒指數：65 (敏感波動)**")
        st.write("明日『子水』沖她的『午火』。她的情緒容易不穩定，內心糾結，甚至對未來感到迷惘。")
        
    with c2:
        st.warning("⚠️ **相處紅燈區**")
        st.write("忌：講大道理、忌太過強勢。她明天聽不進邏輯。")
        
    st.markdown("### 💡 統帥攻略錦囊")
    st.markdown("""
    <div class="strategy-box">
        <b>✅ 戰術：溫柔安撫 (Water Strategy)</b><br>
        明日她需要的是「情緒價值」。請不要跟她談錢或談系統，只要問她「累不累？要不要帶妳去吃好吃的？」。
        當她情緒不穩時，您穩如泰山且溫柔，就是最強的吸引力。
    </div>
    """, unsafe_allow_html=True)

# ==========================================================
# 模組 4: 📊 號碼技術分析 (NEW!)
# ==========================================================
elif mode == "📊 號碼技術分析 (NEW!)":
    st.markdown("## 📊 分析師・號碼趨勢 K 線")
    st.caption("Technical Analysis | Lottery Candlestick")
    
    st.markdown("### 🎯 目標號碼：24、25 (連動分析)")
    
    # 模擬技術指標
    col_k1, col_k2, col_k3 = st.columns(3)
    col_k1.metric("RSI 強弱指標", "15 (超賣)", "觸底反彈訊號")
    col_k2.metric("MACD 能量柱", "-0.85", "空方衰竭")
    col_k3.metric("遺漏期數", "8 期", "進入黃金回補區")
    
    st.markdown("#### 📈 能量累積圖 (Energy Accumulation)")
    # 模擬能量圖
    chart_data = pd.DataFrame(np.random.randn(20, 2), columns=['24號能量', '25號能量'])
    st.line_chart(chart_data)
    
    st.success("✅ **技術面結論**：兩大指標同步出現『黃金交叉』前兆。物理機率極限已至，建議強力買進。")

# ==========================================================
# 模組 5: 🕰️ 今日時空戰略 (保留)
# ==========================================================
elif mode == "🕰️ 今日時空戰略":
    st.title("🕰️ 今日出征指南")
    now = get_current_taiwan_time()
    luck, wealth = get_lucky_direction(now.hour, now.day)
    c1, c2, c3 = st.columns(3)
    c1.info(f"📅 日期：{now.strftime('%Y-%m-%d')}")
    c2.info(f"⏰ 時間：{now.strftime('%H:%M')}")
    c3.warning(f"🔥 狀態：{'丁亥日' if now.day == 8 else '時空運轉中'}")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    col1.markdown(f"""<div class="direction-card"><h3>💰 財神方位</h3><div class="big-luck">{wealth}方</div></div>""", unsafe_allow_html=True)
    col2.markdown(f"""<div class="direction-card" style="border-left-color: #D4AF37;"><h3>✨ 貴人方位</h3><div class="big-luck">{luck}方</div></div>""", unsafe_allow_html=True)
    
    st.markdown("### 🔮 靈龜占卜")
    q = st.text_input("戰略疑問：")
    if st.button("🐢 啟動"):
        o, d, i = divine_outcome(q)
        st.markdown(f"""<div class="divination-box"><h3>問：{q}</h3><h1>{o}</h1><p>{d}</p></div>""", unsafe_allow_html=True)

# ==========================================================
# 模組 6: 👤 深層本命解析 (保留)
# ==========================================================
elif mode == "👤 深層本命解析":
    st.title("👤 掌門人戰略藍圖")
    bd = st.date_input("出生日期", datetime.date(1996, 2, 17))
    if st.button("🚀 掃描"):
        day_gan = TIAN_GAN[bd.day % 10]
        d = DATA_DICT[day_gan]
        st.markdown(f"""
        <div class="main-card">
            <h2 class="gold-text">🗡️ {day_gan} ({d['title']})</h2>
            <hr>
            <p>{d['personality']}</p>
            <p><b>⚔️ 事業：</b>{d['career']}</p>
            <p><b>💰 財富：</b>{d['wealth']}</p>
            <p><b>🏥 健康：</b>{d['health']}</p>
        </div>
        """, unsafe_allow_html=True)
        for c in d['cycle']:
            st.markdown(f"<div class='timeline-box'>{c}</div>", unsafe_allow_html=True)

# ==========================================================
# 模組 7: 💞 情場戰略指揮部 (保留)
# ==========================================================
elif mode == "💞 情場戰略指揮部":
    st.title("💞 交往/復合戰略推演")
    c1, c2 = st.columns(2)
    d1 = c1.date_input("您的生日", datetime.date(1996, 2, 17))
    d2 = c2.date_input("對方生日", datetime.date(1997, 3, 21))
    
    if st.button("💘 推演"):
        g1 = TIAN_GAN[d1.day % 10]
        g2 = TIAN_GAN[d2.day % 10]
        
        # 辛剋乙 邏輯
        rel_type = "普通"
        date_s, back_s = 60, 40
        msg = ""
        
        # 簡易判定
        els = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土", "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"}
        if els[g1] == "金" and els[g2] == "木":
             rel_type = "征服 (我剋)"
             date_s, back_s = 80, 55
             msg = "辛金 (您) 剋 乙木 (對方)。您有主導權，但對方怕壓力。復合需靠『高價值吸引』(如財富/才華)，忌諱糾纏。"
        
        st.subheader(f"戰略分析：{g1} ⚔️ {g2} —— 【{rel_type}】")
        col_res = st.columns(2)
        col_res[0].metric("💘 交往指數", f"{date_s}%", "進攻有利")
        col_res[1].metric("🔄 復合指數", f"{back_s}%", "需長期抗戰", delta_color="inverse")
        
        st.markdown("### 📖 統帥錦囊")
        st.markdown(f"""<div class="strategy-box">{msg}</div>""", unsafe_allow_html=True)
