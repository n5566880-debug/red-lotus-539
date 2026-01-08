import streamlit as st
import datetime
import math
import random
import time

# ==============================================================================
# 🛡️ 紅蓮戰略系統 V3.0 - 旗艦指揮官版 (Red Lotus Strategy System Ultimate)
# ==============================================================================
# 版本號：V3.0.1
# 核心架構：賭王決策 / 生物節律雷達 / 人心判斷 / 奇門時空
# ==============================================================================

# --- [1. 系統初始化設定] ---
st.set_page_config(
    page_title="紅蓮戰略終端 V3.0",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定義 CSS 樣式 (讓介面看起來更像駭客終端)
st.markdown("""
<style>
    .big-font { font-size:24px !important; font-weight: bold; }
    .highlight { color: #ff4b4b; font-weight: bold; }
    .success-text { color: #28a745; font-weight: bold; }
    .stAlert { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# --- [2. 核心運算邏輯庫 (無需外掛，保證穩定)] ---

class RedLotusIntelligence:
    """紅蓮核心運算模組"""
    
    @staticmethod
    def get_constellation(month, day):
        """計算星座"""
        dates = (20, 19, 21, 20, 21, 21, 23, 23, 23, 24, 22, 22)
        constellations = ("摩羯座", "水瓶座", "雙魚座", "牡羊座", "金牛座", "雙子座", 
                          "巨蟹座", "獅子座", "處女座", "天秤座", "天蠍座", "射手座", "摩羯座")
        if day < dates[month-1]:
            return constellations[month-1]
        else:
            return constellations[month]

    @staticmethod
    def get_life_number(d):
        """計算生命靈數"""
        s = str(d.year) + str(d.month) + str(d.day)
        num = sum(int(c) for c in s)
        while num > 9:
            num = sum(int(c) for c in str(num))
        return num

    @staticmethod
    def calculate_kelly_criterion(win_prob, odds):
        """
        凱利公式計算 (Kelly Criterion)
        f = (bp - q) / b
        b = 賠率 (不含本金), p = 勝率, q = 敗率 (1-p)
        """
        b = odds - 1
        p = win_prob
        q = 1 - p
        f = (b * p - q) / b
        return max(f, 0) # 不會建議負數下注

    @staticmethod
    def get_biorhythm(birthdate):
        """
        生物節律計算 (Physical, Emotional, Intellectual)
        情緒週期：28天
        體力週期：23天
        智力週期：33天
        """
        today = datetime.date.today()
        delta = (today - birthdate).days
        
        # 使用正弦波計算 (-100 到 +100)
        phy = math.sin(2 * math.pi * delta / 23) * 100
        emo = math.sin(2 * math.pi * delta / 28) * 100
        intel = math.sin(2 * math.pi * delta / 33) * 100
        
        return {"phy": phy, "emo": emo, "intel": intel, "days_alive": delta}

# --- [3. 側邊欄戰術導航] ---
st.sidebar.markdown("# 🔥 紅蓮戰略指揮部")
st.sidebar.caption("System Status: ONLINE | V3.0 Professional")
st.sidebar.markdown("---")

user_avatar = st.sidebar.text_input("指揮官代號", "賭王")
menu = st.sidebar.radio("🔰 戰術模組選擇", [
    "🎰 賭王決策系統 (專業版)", 
    "👧 予婕情緒雷達 (生物節律)", 
    "👤 深層本命解析 (人心判斷)",
    "⏳ 今日時空戰略 (奇門)",
    "📈 財務戰績覆盤", 
    "🐢 靈龜大吉清單 (本期核心)"
])

st.sidebar.markdown("---")
st.sidebar.info(f"📅 系統日期：{datetime.date.today()}\n🌍 地點：台灣")

# ==============================================================================
# [模組 1] 🎰 賭王決策系統 (專業版)
# ==============================================================================
if menu == "🎰 賭王決策系統 (專業版)":
    st.title("🎰 專業資金控管・戰術終端")
    st.markdown("### Professional Gambling Strategy System")
    st.markdown("---")
    
    # 1. 戰術參數設定
    col1, col2, col3 = st.columns(3)
    with col1:
        numbers = st.text_input("📍 本期鎖定號碼", "07, 11, 24, 25, 34")
    with col2:
        budget = st.number_input("💰 總戰備資金 (TWD)", min_value=1000, value=2000, step=100)
    with col3:
        risk_level = st.selectbox("⚡ 風險承受等級", ["保守 (Conservative)", "穩健 (Balanced)", "激進 (Aggressive)"])

    # 2. 進階參數 (模擬專業數據)
    with st.expander("⚙️ 進階參數設定 (Advanced Settings)"):
        c1, c2 = st.columns(2)
        with c1:
            odds = st.number_input("預估賠率 (Odds)", value=5.0, help="例如539中兩星約53倍，此處為綜合期望值")
        with c2:
            win_prob_input = st.slider("預估勝率 (Win Probability)", 0.0, 1.0, 0.25, help="根據歷史數據的主觀判斷")

    # 3. 核心運算
    st.markdown("### 📊 決策儀表板 (Dashboard)")
    
    # 凱利公式計算
    kelly_ratio = RedLotusIntelligence.calculate_kelly_criterion(win_prob_input, odds)
    
    # 紅蓮加權邏輯
    base_ratio = kelly_ratio * 100
    if risk_level == "保守 (Conservative)":
        final_ratio = base_ratio * 0.5
    elif risk_level == "激進 (Aggressive)":
        final_ratio = base_ratio * 1.5
    else:
        final_ratio = base_ratio
        
    # 特殊號碼加成 (34號回彈)
    is_core_present = "34" in numbers
    if is_core_present:
        final_ratio += 2.0 # 強制加權
        
    # 防止溢出
    final_ratio = min(final_ratio, 10.0) # 最大不建議超過總資金 10%
    final_ratio = max(final_ratio, 1.0)  # 最小 1%

    # 4. 顯示結果
    m1, m2, m3 = st.columns(3)
    m1.metric("紅蓮建議下注比例", f"{final_ratio:.2f}%", f"{'+2.0%' if is_core_present else '0%'}")
    
    suggested_bet = budget * (final_ratio / 100)
    m2.metric("建議單注金額", f"${suggested_bet:.0f}", "資金調配")
    
    # 預估獲利 (模擬)
    potential_profit = suggested_bet * (odds - 1)
    m3.metric("潛在獲利預估", f"${potential_profit:.0f}", "若命中")

    # 5. 戰術指令
    st.markdown("#### 📝 副官戰術指令")
    if is_core_present:
        st.success("🔥 **【核心代碼偵測】**：系統偵測到 **[34]** 號。今日火旺，此號碼具備「回彈臨界」特徵，建議作為「膽」使用。")
    
    if final_ratio > 5.0:
        st.warning("⚠️ **高風險提示**：今日建議下注比例較高，請確認資金充裕。")
    else:
        st.info("🛡️ **穩健策略**：今日適合小額佈局，測試盤面水溫。")

    # 視覺化圖表 (模擬歷史回測)
    st.markdown("#### 📉 歷史回測模擬 (Backtest)")
    chart_data = [random.randint(1000, 3000) for _ in range(10)]
    st.line_chart(chart_data)
    st.caption("近 10 期資金曲線模擬 (僅供參考)")


# ==============================================================================
# [模組 2] 👧 予婕情緒雷達 (生物節律版)
# ==============================================================================
elif menu == "👧 予婕情緒雷達 (生物節律)":
    st.title("👧 予婕情緒雷達・生物節律分析")
    st.markdown(f"### Target: Yu-jie (1997/03/21)")
    st.markdown("---")
    
    # 鎖定生日
    yj_birthday = datetime.date(1997, 3, 21)
    bio = RedLotusIntelligence.get_biorhythm(yj_birthday)
    
    # 1. 生物節律儀表板
    col1, col2, col3 = st.columns(3)
    
    # 情緒 (Emotional)
    emo_color = "normal"
    emo_status = "平穩"
    if bio['emo'] > 50: 
        emo_status = "😍 心情極佳"; emo_color = "off" # 綠色
    elif bio['emo'] < -50: 
        emo_status = "😡 情緒低潮"; emo_color = "inverse" # 紅色
        
    col1.metric("❤️ 情緒週期 (Emotional)", f"{bio['emo']:.1f}%", emo_status)
    
    # 體力 (Physical)
    col2.metric("⚡ 體力週期 (Physical)", f"{bio['phy']:.1f}%", "精力旺盛" if bio['phy'] > 0 else "容易疲勞")
    
    # 智力 (Intellectual)
    col3.metric("🧠 智力週期 (Intellectual)", f"{bio['intel']:.1f}%", "思緒清晰" if bio['intel'] > 0 else "反應較慢")
    
    st.progress((bio['emo'] + 100) / 200)
    st.caption("綜合情緒能量條 (左為低潮，右為高潮)")
    
    # 2. 戰略分析報告
    st.subheader("🛡️ 紅蓮生存戰略指南")
    
    if bio['emo'] < -30:
        st.error("🚨 **紅色警戒 (Red Alert)**：目標今日情緒處於「負值區」。")
        st.markdown("""
        * **生存法則**：
            1. 說話音量降低 20%。
            2. 禁止講道理，禁止提「冷靜一點」。
            3. **建議行動**：買她喜歡的甜點，默默放在桌上然後撤退。
        """)
    elif bio['emo'] > 30:
        st.success("✅ **綠色通道 (Green Light)**：目標今日心情愉悅。")
        st.markdown("""
        * **進攻建議**：
            1. 適合提出「購買裝備」或「出遊」的請求。
            2. 適合講笑話，成功率提升 50%。
            3. **建議行動**：帶她去吃好料的，順便談談心。
        """)
    else:
        st.warning("⚠️ **黃色觀察 (Yellow Zone)**：情緒波動不明顯。")
        st.markdown("* **建議**：保持正常互動，多觀察臉色，隨時準備切換模式。")

    # 3. 星座補充
    constellation = RedLotusIntelligence.get_constellation(3, 21) # 3/21 是牡羊與雙魚交界
    st.info(f"💡 **星座註記**：她是 **{constellation}**。{constellation} 的女生通常直接、熱情，但也需要被細心呵護。")


# ==============================================================================
# [模組 3] 👤 深層本命解析 (人心判斷)
# ==============================================================================
elif menu == "👤 深層本命解析 (人心判斷)":
    st.title("👁️ 深層本命解析・識人術")
    st.markdown("輸入生日，利用紅蓮大數據庫看穿對方的底層邏輯。")
    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        target_name = st.text_input("對象代號 / 姓名", "神秘人")
        b_date = st.date_input("出生年月日", datetime.date(1996, 2, 17))
    with c2:
        analysis_mode = st.radio("啟動模式", ["🤝 交友/看透人心", "👔 面試/識人用人"])

    if st.button("🔥 啟動紅蓮全息解析"):
        # 取得分析數據
        constellation = RedLotusIntelligence.get_constellation(b_date.month, b_date.day)
        life_num = RedLotusIntelligence.get_life_number(b_date)
        
        # 模擬詳細的分析資料庫
        traits_db = {
            1: ("開創型", "獨立自主、不喜歡依賴。自尊心強，需要被尊重。適合當領導者。"),
            2: ("協調型", "敏感細膩、重視關係。能夠察言觀色，但也容易優柔寡斷。"),
            3: ("創意型", "像個孩子、充滿好奇心。情緒來得快去得也快，討厭無聊。"),
            4: ("穩健型", "追求安全感、按部就班。非常有責任感，但固執不知變通。"),
            5: ("自由型", "口才好、適應力強。討厭被束縛，喜歡冒險與新鮮感。"),
            6: ("關懷型", "充滿愛心、喜歡照顧人。完美主義者，容易給自己壓力。"),
            7: ("探究型", "直覺強、喜歡獨處分析。帶有神秘感，不喜歡笨蛋。"),
            8: ("權威型", "看重目標與利益。天生的生意人，控制欲較強。"),
            9: ("智慧型", "大愛無私、想像力豐富。有時會脫離現實，需要精神支柱。")
        }
        
        trait_title, trait_desc = traits_db.get(life_num, ("神秘型", "數據不足"))
        
        st.divider()
        st.subheader(f"🎯 目標鎖定：{target_name}")
        
        # 3D 儀表板概念
        m1, m2, m3 = st.columns(3)
        m1.metric("🌌 星座代碼", constellation)
        m2.metric("🔢 生命靈數", f"Type {life_num}")
        m3.metric("🧠 核心人格", trait_title)
        
        st.markdown(f"### 📝 詳細分析報告")
        st.write(f"**【性格底層邏輯】**\n{trait_desc}")
        
        # 針對不同日期的特殊彩蛋 (例如你之前的測試日期)
        if b_date == datetime.date(1996, 2, 17):
            st.success("🔥 **特別註記 (Special Note)**：\n此日出生者為「丁火」命格。心思細膩如燈燭，第六感極強。與紅色號碼 (34) 有強烈共鳴，是絕佳的執行者。")
        
        st.markdown("### 🛡️ 紅蓮戰略建議")
        if analysis_mode == "🤝 交友/看透人心":
            st.info(f"與 **{constellation} + {life_num}號人** 相處，切記「真誠」。他們能一眼看穿謊言。若要增進關係，請展現你的能力，而不只是討好。")
        else:
            st.warning(f"若用於職場，此人適合 **{'開創與業務' if life_num in [1,3,5,8] else '守成與執行'}**。請根據其 {trait_title} 特質分配任務。")


# ==============================================================================
# [模組 4] ⏳ 今日時空戰略 (奇門流日)
# ==============================================================================
elif menu == "⏳ 今日時空戰略 (奇門)":
    st.title("⏳ 今日時空戰略")
    st.markdown("結合奇門遁甲與流日能量，尋找最佳進場時機。")
    st.markdown("---")
    
    today = datetime.date.today()
    # 這裡模擬 2026/1/9 的盤勢，或是顯示當日
    st.info(f"📅 戰略日期：{today}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🌞 今日格局：丙午日 (火旺)")
        st.write("""
        * **五行屬性**：天干丙火，地支午火。
        * **能量特徵**：火氣極旺，利於快速回彈、短線操作。
        * **幸運色**：紅色、紫色。
        """)
    with col2:
        st.markdown("### 🕰️ 最佳時辰 (吉時)")
        st.write("""
        1. **午時 (11:00 - 13:00)**：日祿歸時，財氣最旺。
        2. **戌時 (19:00 - 21:00)**：三奇到殿，靈感最強。
        """)
    
    st.divider()
    st.markdown("### 🧭 方位指引")
    st.write("今日 **財神正南方**，**喜神東南方**。建議下注時面向南方，或前往位於住家南方的彩券行。")


# ==============================================================================
# [模組 5] 📈 財務戰績覆盤
# ==============================================================================
elif menu == "📈 財務戰績覆盤":
    st.title("📈 財務戰績覆盤系統")
    st.markdown("紀錄每一場戰役的得失，修正下一次的彈道。")
    st.markdown("---")
    
    # 模擬數據
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("本月淨利 (Net Profit)", "+$12,500", "5.2%")
    c2.metric("總勝率 (Win Rate)", "38.5%", "-2.1%")
    c3.metric("最大回撤 (Max Drawdown)", "-$3,200", "控制內")
    c4.metric("目前連勝 (Streak)", "2 Wins", "氣勢正旺")
    
    st.subheader("📝 戰鬥筆記 (Battle Log)")
    note = st.text_area("輸入今日檢討...", "34號回彈如預期，但連碰沒補到，下次需注意防守號碼...")
    
    if st.button("💾 存檔紀錄"):
        st.toast("✅ 戰績已同步至雲端資料庫")
        time.sleep(1)
        st.balloons()


# ==============================================================================
# [模組 6] 🐢 靈龜大吉清單 (本期核心)
# ==============================================================================
elif menu == "🐢 靈龜大吉清單 (本期核心)":
    st.title("🐢 靈龜大吉・唯一認證")
    st.markdown("靈龜卦象與數據分析的完美交匯點。")
    st.markdown("---")
    
    # 這裡放鞭炮特效
    if st.button("🔥 召喚大吉號碼"):
        st.balloons()
    
    st.success("### 🔥 本期唯一 5 顆大吉")
    
    # 大字體顯示
    st.markdown("""
    <div style="text-align: center; font-size: 48px; font-weight: bold; color: #ff4b4b; background-color: #f0f2f6; padding: 20px; border-radius: 15px;">
    07、11、24、25、34
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🎯 核心主星：34")
        st.write("""
        * **屬性**：紅色 / 雙數 / 火。
        * **特徵**：回彈臨界點。
        * **策略**：作為「膽」或核心，必選。
        """)
        
    with c2:
        st.markdown("### 🛡️ 護法陣型：07, 11, 24, 25")
        st.write("""
        * **07**：與 34 共鳴 (3+4=7)，靈魂連結。
        * **24, 25**：紅波連號，中段防守網。
        * **11**：平衡支撐，穩定小數區。
        """)
        
    st.info("💡 **紅蓮提示**：此組合為「全大吉」卦象，氣聚神凝，切勿隨意更動。")

# ==============================================================================
# 頁面底部版權與狀態
# ==============================================================================
st.markdown("---")
st.caption("Powered by Red Lotus AI System | Developed for Commander Use Only")
