import streamlit as st
import datetime
import math
import random
import time

# ==============================================================================
# 🛡️ 紅蓮戰略系統 V4.0 - 終極全配版 (Red Lotus Strategy System Ultimate)
# ==============================================================================
# 版本號：V4.0.0 (Professional)
# 新增功能：日主精準算法 / 複合戰略 / 靈龜問事
# ==============================================================================

# --- [1. 系統初始化] ---
st.set_page_config(
    page_title="紅蓮戰略終端 V4.0",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定義駭客風格 CSS
st.markdown("""
<style>
    .big-font { font-size:24px !important; font-weight: bold; }
    .highlight { color: #ff4b4b; font-weight: bold; }
    .success-text { color: #28a745; font-weight: bold; }
    .stAlert { border-radius: 10px; }
    .stProgress > div > div > div > div { background-color: #ff4b4b; }
</style>
""", unsafe_allow_html=True)

# --- [2. 紅蓮核心運算模組 (Red Lotus Core)] ---

class RedLotusIntelligence:
    """紅蓮核心運算模組 (不依賴外部庫，保證穩定)"""
    
    @staticmethod
    def get_day_master(birth_date):
        """
        [獨家算法] 不需聯網，精準計算八字日主 (天干)
        基準日：1900年1月1日為甲戌日 (甲木)
        """
        base_date = datetime.date(1900, 1, 1)
        days_diff = (birth_date - base_date).days
        # 天干循環：10天一輪 (0:甲, 1:乙, 2:丙, 3:丁, 4:戊, 5:己, 6:庚, 7:辛, 8:壬, 9:癸)
        stem_index = days_diff % 10
        stems = ["甲木 (參天大樹)", "乙木 (花草藤蔓)", "丙火 (太陽之光)", "丁火 (燈燭星火)", "戊土 (高山巨石)", 
                 "己土 (田園沃土)", "庚金 (斧鉞刀劍)", "辛金 (珠寶首飾)", "壬水 (江河大海)", "癸水 (雨露泉水)"]
        return stems[stem_index]

    @staticmethod
    def get_constellation(month, day):
        dates = (20, 19, 21, 20, 21, 21, 23, 23, 23, 24, 22, 22)
        constellations = ("摩羯座", "水瓶座", "雙魚座", "牡羊座", "金牛座", "雙子座", 
                          "巨蟹座", "獅子座", "處女座", "天秤座", "天蠍座", "射手座", "摩羯座")
        if day < dates[month-1]:
            return constellations[month-1]
        else:
            return constellations[month]

    @staticmethod
    def get_life_number(d):
        s = str(d.year) + str(d.month) + str(d.day)
        num = sum(int(c) for c in s)
        while num > 9:
            num = sum(int(c) for c in str(num))
        return num

    @staticmethod
    def calculate_kelly_criterion(win_prob, odds):
        """凱利公式：專業資金控管"""
        b = odds - 1
        p = win_prob
        q = 1 - p
        f = (b * p - q) / b
        return max(f, 0)

    @staticmethod
    def get_biorhythm(birthdate):
        """生物節律：計算體力、情緒、智力週期"""
        today = datetime.date.today()
        delta = (today - birthdate).days
        phy = math.sin(2 * math.pi * delta / 23) * 100
        emo = math.sin(2 * math.pi * delta / 28) * 100
        intel = math.sin(2 * math.pi * delta / 33) * 100
        return {"phy": phy, "emo": emo, "intel": intel}
    
    @staticmethod
    def get_reconciliation_probability(breakup_days, reason_level, contact_level):
        """[獨家] 複合機率演算法"""
        base_score = 60
        # 時間衰減
        if breakup_days < 30: base_score += 20    # 黃金挽回期
        elif breakup_days < 90: base_score += 10
        elif breakup_days > 365: base_score -= 20 # 冷卻過久
        
        # 原因扣分
        base_score -= (reason_level * 10) # 1=小吵, 5=原則性背叛
        
        # 聯繫加分
        base_score += (contact_level * 5) # 0=斷聯, 5=每天聊
        
        return min(max(base_score, 0), 99)

# --- [3. 側邊欄導航] ---
st.sidebar.title("🔥 紅蓮戰略指揮部")
st.sidebar.caption("System V4.0 | Status: ONLINE")
st.sidebar.markdown("---")

user_avatar = st.sidebar.text_input("指揮官代號", "賭王")
menu = st.sidebar.radio("🔰 戰術模組選擇", [
    "🎰 賭王決策系統 (專業版)", 
    "👧 予婕情緒雷達 (生物節律)", 
    "👤 深層本命解析 (性格判斷)",
    "❤️ 舊愛複合戰略部 (新)",
    "🐢 靈龜問事與大吉 (互動版)",
    "⏳ 今日時空戰略 (奇門)",
    "📈 財務戰績覆盤"
])

st.sidebar.markdown("---")
st.sidebar.info(f"📅 系統日期：{datetime.date.today()}\n🌍 地點：台灣 (Taiwan)")

# ==============================================================================
# [模組 1] 🎰 賭王決策系統 (專業版)
# ==============================================================================
if menu == "🎰 賭王決策系統 (專業版)":
    st.title("🎰 專業資金控管・戰術終端")
    st.markdown("### Professional Gambling Strategy System")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        numbers = st.text_input("📍 本期鎖定號碼", "07, 11, 24, 25, 34")
    with col2:
        budget = st.number_input("💰 總戰備資金 (TWD)", min_value=1000, value=2000, step=100)
    with col3:
        risk_level = st.selectbox("⚡ 風險承受等級", ["保守 (Conservative)", "穩健 (Balanced)", "激進 (Aggressive)"])

    with st.expander("⚙️ 進階參數 (凱利公式設定)"):
        c1, c2 = st.columns(2)
        odds = c1.number_input("預估賠率 (Odds)", value=5.0)
        win_prob_input = c2.slider("預估勝率 (Win Probability)", 0.0, 1.0, 0.25)

    st.markdown("### 📊 決策儀表板")
    
    # 凱利運算
    kelly_ratio = RedLotusIntelligence.calculate_kelly_criterion(win_prob_input, odds)
    base_ratio = kelly_ratio * 100
    
    # 風險調整
    if risk_level == "保守 (Conservative)": final_ratio = base_ratio * 0.5
    elif risk_level == "激進 (Aggressive)": final_ratio = base_ratio * 1.5
    else: final_ratio = base_ratio
        
    # 34號加權
    is_core_present = "34" in numbers
    if is_core_present: final_ratio += 2.0
    
    final_ratio = min(max(final_ratio, 1.0), 10.0) # 限制在 1%~10%

    m1, m2, m3 = st.columns(3)
    m1.metric("紅蓮建議下注比例", f"{final_ratio:.2f}%", "+2.0%" if is_core_present else "0%")
    suggested_bet = budget * (final_ratio / 100)
    m2.metric("建議單注金額", f"${suggested_bet:.0f}", "資金調配")
    m3.metric("潛在獲利預估", f"${suggested_bet * (odds - 1):.0f}", "若命中")

    if is_core_present:
        st.success("🔥 **【核心代碼 34】**：偵測到火屬性回彈號碼，強烈建議作為膽號。")
    if final_ratio > 5.0:
        st.warning("⚠️ **高風險提示**：今日建議注碼較大，請謹慎。")

# ==============================================================================
# [模組 2] 👧 予婕情緒雷達 (生物節律)
# ==============================================================================
elif menu == "👧 予婕情緒雷達 (生物節律)":
    st.title("👧 予婕情緒雷達・生物節律分析")
    st.markdown("### Target: Yu-jie (1997/03/21)")
    st.markdown("---")
    
    yj_birthday = datetime.date(1997, 3, 21)
    bio = RedLotusIntelligence.get_biorhythm(yj_birthday)
    
    col1, col2, col3 = st.columns(3)
    
    # 情緒狀態判斷
    emo_status = "平穩"
    if bio['emo'] > 50: emo_status = "😍 心情極佳 (High)"
    elif bio['emo'] < -50: emo_status = "😡 情緒低潮 (Low)"
        
    col1.metric("❤️ 情緒週期", f"{bio['emo']:.1f}%", emo_status)
    col2.metric("⚡ 體力週期", f"{bio['phy']:.1f}%", "精力旺盛" if bio['phy']>0 else "易疲勞")
    col3.metric("🧠 智力週期", f"{bio['intel']:.1f}%", "思緒清晰" if bio['intel']>0 else "反應慢")
    
    st.markdown("#### 🌊 情緒能量條")
    st.progress((bio['emo'] + 100) / 200)
    
    st.subheader("🛡️ 紅蓮生存戰略指南")
    if bio['emo'] < -30:
        st.error("🚨 **紅色警戒**：今日她處於低潮期，易怒且敏感。")
        st.write("👉 **戰術**：1. 閉嘴傾聽 2. 買甜食 3. 不要講道理。")
    elif bio['emo'] > 30:
        st.success("✅ **綠色通道**：今日心情愉悅，適合進攻。")
        st.write("👉 **戰術**：提出約會邀請或購買請求，成功率 +50%。")
    else:
        st.warning("⚠️ **黃色觀察**：情緒一般，請保持正常互動。")

# ==============================================================================
# [模組 3] 👤 深層本命解析 (性格判斷)
# ==============================================================================
elif menu == "👤 深層本命解析 (性格判斷)":
    st.title("👁️ 深層本命解析・識人術")
    st.markdown("輸入生日，系統自動推算日主天干與深層性格。")
    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        target_name = st.text_input("對象代號", "神秘人")
        b_date = st.date_input("出生年月日", datetime.date(1996, 2, 17))
    with c2:
        mode = st.radio("分析模式", ["交友/看透人心", "面試/識人用人"])

    if st.button("🔥 啟動全息解析"):
        # 計算資料
        day_master = RedLotusIntelligence.get_day_master(b_date) # 核心算法
        constellation = RedLotusIntelligence.get_constellation(b_date.month, b_date.day)
        life_num = RedLotusIntelligence.get_life_number(b_date)
        
        st.divider()
        st.subheader(f"🎯 目標鎖定：{target_name}")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("🔮 八字日主 (核心)", day_master.split(" ")[0])
        m2.metric("🌌 星座", constellation)
        m3.metric("🔢 生命靈數", f"{life_num} 號人")
        
        st.markdown("### 📝 深層性格報告")
        st.info(f"**【命格屬性】：{day_master}**")
        
        # 針對五行給出性格描述 (這是你要求的性格判斷)
        element = day_master[0] # 取出甲乙丙丁...
        traits = {
            "甲": "正直不屈，有領袖風範，但也容易固執不知變通。",
            "乙": "性格柔軟靈活，善於適應環境，但有時缺乏主見。",
            "丙": "熱情如火，藏不住秘密，行動力強但脾氣來得快去得快。",
            "丁": "心思細膩，洞察力極強 (如你)，外表溫和內心有火。",
            "戊": "沈穩厚重，重信守諾，反應較慢但值得信賴。",
            "己": "內斂包容，做事有條理，多才多藝但容易多疑。",
            "庚": "剛毅果斷，講義氣，吃軟不吃硬，有破壞力。",
            "辛": "優雅愛面子，重視細節與質感，自尊心極強。",
            "壬": "聰明善變，適應力強，膽大心細但容易任性。",
            "癸": "溫柔內向，心思深沈，耐力極強，善於滲透人心。"
        }
        
        st.write(f"**【性格判斷】**：\n{traits.get(element, '神秘莫測')}")
        
        st.markdown("### 🛡️ 紅蓮戰略建議")
        if mode == "交友/看透人心":
            st.success(f"面對{element}木/火/土/金/水型人，請注意他們的「底線」。例如{element}型人最討厭被欺騙或看輕。")
        else:
            st.warning(f"若用於職場，此人適合放在{'前線開創' if element in ['甲','丙','庚','壬'] else '後勤守成'}的位置。")

# ==============================================================================
# [模組 4] ❤️ 舊愛複合戰略部 (新功能)
# ==============================================================================
elif menu == "❤️ 舊愛複合戰略部 (新)":
    st.title("❤️ 舊愛複合戰略部")
    st.markdown("分析破局原因，計算挽回機率與執行步驟。")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        breakup_days = st.number_input("分手天數 (Days)", min_value=0, value=30)
        reason_level = st.slider("分手原因嚴重度 (1=小吵, 5=背叛/原則問題)", 1, 5, 2)
    with col2:
        contact_level = st.slider("目前互動頻率 (0=斷聯, 5=每天聊)", 0, 5, 1)
        target_mood = st.selectbox("對方目前態度", ["冷淡/封鎖", "像普通朋友", "偶爾曖昧", "憤怒"])
        
    if st.button("💔 計算複合機率"):
        prob = RedLotusIntelligence.get_reconciliation_probability(breakup_days, reason_level, contact_level)
        
        st.divider()
        c1, c2 = st.columns([1, 2])
        c1.metric("複合成功率", f"{prob}%", "動態評估")
        
        with c2:
            st.markdown("### 🛡️ 戰術執行步驟")
            if prob < 30:
                st.error("🚨 **極度困難**：目前對方防禦值極高。建議執行「斷聯冷凍法」30天，先提升自我價值。")
            elif prob < 60:
                st.warning("⚠️ **拉鋸戰**：有機會但不能急。建議以「朋友名義」切入，展示你的改變 (如新造型、新生活)。")
            else:
                st.success("✅ **黃金窗口**：對方餘情未了。建議製造「偶然碰面」或請求小幫忙，快速升溫。")

# ==============================================================================
# [模組 5] 🐢 靈龜問事與大吉 (互動版)
# ==============================================================================
elif menu == "🐢 靈龜問事與大吉 (互動版)":
    st.title("🐢 靈龜問事・吉凶指引")
    st.markdown("靈龜卦象系統。除了號碼，現在你可以問它問題。")
    st.markdown("---")
    
    # --- 1. 靈龜問事 ---
    st.subheader("🗣️ 向靈龜提問")
    question = st.text_input("輸入你想問的事 (例如：這次34號會開嗎？我和她會和好嗎？)")
    
    if st.button("🔮 擲筊/請示"):
        if not question:
            st.warning("請先輸入問題。")
        else:
            answers = ["大吉！放手去做。", "吉，但需謹慎。", "平，等待時機。", "凶，暫時觀望。", "大凶，千萬不可。", "靈龜笑而不語 (時機未到)。"]
            # 簡單模擬隨機回答，可加入更複雜邏輯
            reply = random.choice(answers)
            
            st.info(f"🐢 靈龜回應：**{reply}**")
            if "吉" in reply:
                st.balloons()

    st.markdown("---")

    # --- 2. 本期大吉號碼 ---
    st.subheader("🔥 本期唯一 5 顆大吉")
    st.markdown("""
    <div style="text-align: center; font-size: 42px; font-weight: bold; color: #d63031; background-color: #ffeaa7; padding: 15px; border-radius: 10px;">
    07、11、24、25、34
    </div>
    """, unsafe_allow_html=True)
    
    st.write("""
    * **核心主星**：**34** (火紅回彈)。
    * **靈龜指示**：氣聚神凝，心誠則靈。
    """)

# ==============================================================================
# [模組 6] ⏳ 今日時空戰略 (奇門)
# ==============================================================================
elif menu == "⏳ 今日時空戰略 (奇門)":
    st.title("⏳ 今日時空戰略")
    st.markdown("結合奇門遁甲與流日能量。")
    today = datetime.date.today()
    st.info(f"📅 戰略日期：{today}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🌞 今日格局")
        st.write("* **能量特徵**：火旺之日 (利紅色號碼)。\n* **幸運方位**：正南方。")
    with col2:
        st.markdown("### 🕰️ 最佳時辰")
        st.write("1. **午時 (11-13)**：財氣最旺。\n2. **戌時 (19-21)**：靈感最強。")

# ==============================================================================
# [模組 7] 📈 財務戰績覆盤
# ==============================================================================
elif menu == "📈 財務戰績覆盤":
    st.title("📈 財務戰績覆盤")
    st.markdown("紀錄得失，修正彈道。")
    c1, c2, c3 = st.columns(3)
    c1.metric("本月淨利", "+$12,500", "5.2%")
    c2.metric("勝率", "38.5%", "持平")
    c3.metric("最大回撤", "-$3,200", "安全")
    st.text_area("戰鬥筆記", "34號回彈如預期，持續鎖定...")

# ==============================================================================
# 頁面底部
# ==============================================================================
st.markdown("---")
st.caption("Powered by Red Lotus AI System V4.0 | Commander Access Only")
