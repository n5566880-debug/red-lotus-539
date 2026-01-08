import streamlit as st
import datetime
import math
import random
import pandas as pd
import numpy as np

# ==============================================================================
# 🛡️ 紅蓮戰略系統 V9.0 - 讀心指揮官版 (Red Lotus System V9.0 Mind Reader)
# ==============================================================================
# 核心架構：予婕讀心雷達 / 賭王決策(80元) / 雙人合盤 / 十年大限 / 本命全解
# ==============================================================================

st.set_page_config(page_title="紅蓮戰略 V9.0", page_icon="🔥", layout="wide")

# --- [自定義介面樣式] ---
st.markdown("""
<style>
    .big-font { font-size:22px !important; font-weight: bold; }
    .qimen-box { background-color: #2d3436; color: #fab1a0; padding: 15px; border-radius: 8px; border-left: 5px solid #d63031; }
    .radar-alert { background-color: #ffeaa7; color: #d63031; padding: 10px; border-radius: 5px; font-weight: bold; }
    .offering-box { background-color: #55efc4; color: #00b894; padding: 10px; border-radius: 5px; font-weight: bold; }
    .detail-card { background-color: #fff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 10px; }
    .stProgress > div > div > div > div { background-color: #d63031; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# [核心運算庫] Red Lotus Core Intelligence
# ==============================================================================
class RedLotusCore:
    # 基礎參數
    GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    ELEMENTS = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土", "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"}
    
    # 奇門參數
    DOORS = ["休門 (吉)", "死門 (凶)", "傷門 (凶)", "杜門 (平)", "開門 (吉)", "驚門 (凶)", "生門 (吉)", "景門 (平)"]
    STARS = ["天蓬 (膽大)", "天任 (固執)", "天沖 (急躁)", "天輔 (文雅)", "天英 (愛美)", "天芮 (敏感)", "天柱 (破壞)", "天心 (理智)", "天禽 (尊貴)"]
    GODS = ["值符 (領袖)", "騰蛇 (反覆)", "太陰 (陰私)", "六合 (交際)", "白虎 (壓力)", "玄武 (謊言)", "九地 (沈默)", "九天 (活躍)"]

    @staticmethod
    def get_gan_zhi(date):
        base_date = datetime.date(1900, 1, 1)
        days = (date - base_date).days
        gan_idx = days % 10
        zhi_idx = (days + 10) % 12
        return RedLotusCore.GAN[gan_idx], RedLotusCore.ZHI[zhi_idx]

    @staticmethod
    def get_qimen_chart(date, specific_hour="午"):
        seed = date.year * 10000 + date.month * 100 + date.day
        if specific_hour == "午": seed += 12
        random.seed(seed)
        return {
            "door": random.choice(RedLotusCore.DOORS),
            "star": random.choice(RedLotusCore.STARS),
            "god": random.choice(RedLotusCore.GODS),
            "luck_score": random.randint(40, 95)
        }

    @staticmethod
    def analyze_yj_mind(qimen_data, bio_data):
        """[V9.0 新增] 予婕讀心術演算法"""
        god = qimen_data['god']
        star = qimen_data['star']
        door = qimen_data['door']
        emo = bio_data['emo']

        # 1. 掃雷圖 (禁忌話題)
        forbidden = "無特殊禁忌"
        if "白虎" in god or "驚門" in door: forbidden = "🚫 禁止談錢、禁止催促、禁止批評她的穿著。"
        elif "玄武" in god or "杜門" in door: forbidden = "🚫 禁止問『妳在哪？』、『跟誰？』(她需要空間)。"
        elif "天沖" in star or "傷門" in door: forbidden = "🚫 禁止講道理、禁止辯論、禁止提『冷靜一點』。"
        elif "騰蛇" in god: forbidden = "🚫 禁止承諾做不到的事，她今天特別敏感多疑。"

        # 2. 潛意識訴求
        desire = "希望被理解"
        if "休門" in door: desire = "想休息，想被當成小公主寵愛，不想動腦。"
        elif "生門" in door: desire = "想吃好吃的，想要物質上的滿足 (禮物)。"
        elif "景門" in door: desire = "想出去玩，想拍照，想被稱讚漂亮。"
        elif "開門" in door: desire = "想聊未來，希望你展現上進心。"
        elif "死門" in door: desire = "心情悶，只想一個人靜靜，需要無聲的陪伴。"
        
        # 3. 安撫供品
        offering = "熱可可"
        if emo < -20: offering = "高熱量甜點 (巧克力蛋糕、起司塔) - 補血補心情。"
        elif "火" in door or "天英" in star: offering = "冰拿鐵、微糖綠茶、清爽水果茶 - 降火氣。"
        elif "土" in door: offering = "溫熱的湯品、養生茶 - 暖胃暖心。"
        else: offering = "她喜歡的那個 (你知道的)。"

        return forbidden, desire, offering

    @staticmethod
    def get_element_relation(my_date, target_date):
        my_gan, _ = RedLotusCore.get_gan_zhi(my_date)
        target_gan, _ = RedLotusCore.get_gan_zhi(target_date)
        my_el = RedLotusCore.ELEMENTS[my_gan]
        target_el = RedLotusCore.ELEMENTS[target_gan]
        relations = {
            "木": {"木": "比旺", "火": "我生", "土": "我剋", "金": "剋我", "水": "生我"},
            "火": {"木": "生我", "火": "比旺", "土": "我生", "金": "我剋", "水": "剋我"},
            "土": {"木": "剋我", "火": "生我", "土": "比旺", "金": "我生", "水": "我剋"},
            "金": {"木": "我剋", "火": "剋我", "土": "生我", "金": "比旺", "水": "我生"},
            "水": {"木": "我生", "火": "我剋", "土": "剋我", "金": "生我", "水": "比旺"}
        }
        return my_gan, my_el, target_gan, target_el, relations[my_el][target_el]

    @staticmethod
    def calculate_kelly_criterion(win_prob, odds):
        b = odds - 1
        p = win_prob
        q = 1 - p
        f = (b * p - q) / b if b > 0 else 0
        return max(f, 0)

    @staticmethod
    def get_biorhythm(birthdate):
        today = datetime.date.today()
        delta = (today - birthdate).days
        phy = math.sin(2 * math.pi * delta / 23) * 100
        emo = math.sin(2 * math.pi * delta / 28) * 100
        intel = math.sin(2 * math.pi * delta / 33) * 100
        return {"phy": phy, "emo": emo, "intel": intel}

    @staticmethod
    def get_decade_luck(birth_date):
        start_year = datetime.date.today().year
        element_cycle = ["木運 (啟動)", "火運 (顯化)", "土運 (穩固)", "金運 (變革)", "水運 (潛藏)"]
        seed = birth_date.year % 5 
        cycles = []
        for i in range(5):
            cycles.append({"period": f"{start_year + i*10} ~ {start_year + (i+1)*10 - 1}", "theme": element_cycle[(seed + i) % 5]})
        return cycles

    @staticmethod
    def get_lucky_info(gan):
        el = RedLotusCore.ELEMENTS[gan]
        info = {
            "木": ("綠色、青色", "東方", "3, 8"),
            "火": ("紅色、紫色", "南方", "2, 7"),
            "土": ("黃色、咖啡色", "中央/東北", "0, 5"),
            "金": ("白色、金色", "西方", "4, 9"),
            "水": ("黑色、藍色", "北方", "1, 6")
        }
        return info[el]

    @staticmethod
    def get_detailed_life_reading(gan):
        db = {
            "甲": {"char": "【參天大樹】正直、固執、領袖感。", "love": "大男人/大女人，專一但無趣。", "career": "管理、創業。", "invest": "穩健藍籌股。", "health": "肝膽、頭部。"},
            "乙": {"char": "【花草藤蔓】柔軟、適應力強、依賴。", "love": "黏人、需要呵護。", "career": "業務、幕僚。", "invest": "波段操作。", "health": "頸椎、關節。"},
            "丙": {"char": "【太陽之火】熱情、急躁、無心機。", "love": "主動直接、愛吵架。", "career": "演藝、公關。", "invest": "短線爆發。", "health": "心臟、血壓。"},
            "丁": {"char": "【燈燭之火】細膩、敏感、第六感強。", "love": "慢熱深情、精神契合。", "career": "分析、策劃。", "invest": "策略期權。", "health": "心血管、神經。"},
            "戊": {"char": "【高山之土】沈穩、守信、固執。", "love": "木訥實在、給安全感。", "career": "倉儲、銀行。", "invest": "房地產。", "health": "胃部、肌肉。"},
            "己": {"char": "【田園之土】內斂、多疑、細心。", "love": "被動、細水長流。", "career": "秘書、教育。", "invest": "基金債券。", "health": "脾臟、腹部。"},
            "庚": {"char": "【刀劍之金】剛毅、講義氣、衝動。", "love": "愛恨分明、佔有慾。", "career": "軍警、法務。", "invest": "鋼鐵、大宗。", "health": "肺部、呼吸道。"},
            "辛": {"char": "【珠寶之金】優雅、愛面子、說話毒。", "love": "外貌協會、挑剔。", "career": "設計、金融。", "invest": "精品貴金屬。", "health": "牙齒、骨骼。"},
            "壬": {"char": "【江河之水】聰明、善變、任性。", "love": "多情浪漫、愛自由。", "career": "貿易、旅遊。", "invest": "外匯航運。", "health": "腎臟、膀胱。"},
            "癸": {"char": "【雨露之水】溫柔、深沈、想太多。", "love": "敏感依賴、需確認。", "career": "幕後、玄學。", "invest": "潛力股。", "health": "生殖系統。"}
        }
        return db[gan]

    @staticmethod
    def turtle_divination(question):
        if not question: return None
        seed = int(datetime.datetime.now().timestamp() * 1000)
        random.seed(seed)
        results = [
            ("大吉", "乾卦", "飛龍在天，利見大人。"),
            ("中吉", "離卦", "日麗中天，前途光明。"),
            ("小吉", "震卦", "雷驚百里，有驚無險。"),
            ("平", "兌卦", "朋友講習，多作溝通。"),
            ("凶", "坎卦", "水流潤下，暫時保守。"),
            ("大凶", "困卦", "澤無水，困。靜待時機。")
        ]
        return random.choice(results)

# --- [UI 側邊欄] ---
st.sidebar.title("🔥 紅蓮 V9.0 讀心指揮官")
st.sidebar.caption("System Status: MIND READING")
st.sidebar.markdown("---")

menu = st.sidebar.radio("🔰 戰術模組", [
    "🎰 賭王決策系統 (一注80)", 
    "👧 予婕情緒雷達 (讀心術版)", 
    "📈 K線趨勢分析",
    "❤️ 舊愛複合 (對話攻略)",
    "👤 本命解析 (詳細全配版)",
    "🐢 靈龜問事 (卜卦)",
    "⏳ 今日時空 (流日)"
])

# ==============================================================================
# 1. 🎰 賭王決策系統 (一注80版)
# ==============================================================================
if menu == "🎰 賭王決策系統 (一注80)":
    st.title("🎰 專業資金控管・一注 80")
    st.markdown("---")
    
    c1, c2, c3 = st.columns(3)
    numbers = c1.text_input("📍 鎖定號碼", "07, 11, 24, 25, 34")
    budget = c2.number_input("💰 總預算 (TWD)", value=2000, step=100)
    win_prob = c3.slider("📊 信心指數 (勝率)", 0.1, 0.9, 0.35)
    
    odds = 5.0
    kelly_ratio = RedLotusCore.calculate_kelly_criterion(win_prob, odds)
    base_ratio = kelly_ratio * 100 * 0.8
    
    if "34" in numbers: 
        base_ratio += 5.0
        st.caption("🔥 偵測到 [34] 號，權重提升！")
    
    suggested_total = budget * (base_ratio / 100)
    unit_cost = 80
    num_units = int(suggested_total / unit_cost)
    
    if num_units < 1 and base_ratio > 1: num_units = 1
    
    st.markdown("### 🛡️ 戰術指令")
    m1, m2, m3 = st.columns(3)
    m1.metric("建議注數 (Unit)", f"{num_units} 注", f"每注 ${unit_cost}")
    m2.metric("總投入金額", f"${num_units * unit_cost}", f"佔總資金 {(num_units*80/budget)*100:.1f}%")
    m3.metric("預期獲利 (若中獎)", f"${num_units * unit_cost * 53}", "倍率 x53") 
    
    if num_units > 5:
        st.warning("⚠️ **重倉攻擊**：今日信心高，投入較大。")
    elif num_units >= 1:
        st.success("✅ **標準戰術**：穩健佈局。")
    else:
        st.info("🛡️ **觀望**：風險回報比不佳。")

# ==============================================================================
# 2. 👧 予婕情緒雷達 (讀心術版 - V9.0核心)
# ==============================================================================
elif menu == "👧 予婕情緒雷達 (讀心術版)":
    st.title("👧 予婕情緒雷達・讀心指揮官")
    
    yj_birth = datetime.date(1997, 3, 21)
    today = datetime.date.today()
    bio = RedLotusCore.get_biorhythm(yj_birth)
    qimen = RedLotusCore.get_qimen_chart(today, "午")
    
    # 執行讀心演算法
    forbidden, desire, offering = RedLotusCore.analyze_yj_mind(qimen, bio)
    
    st.markdown(f"""
    <div class="qimen-box">
    <b>Target:</b> Yu-Jie (予婕) | <b>Birthday:</b> 1997/03/21 (午時) <br>
    <b>今日命宮:</b> 臨 <span style="color:#ffeaa7; font-size:18px;">{qimen['door']}</span> + {qimen['star']}
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("❤️ 生理情緒", f"{bio['emo']:.1f}%", "高昂" if bio['emo']>0 else "低落")
    c2.metric("🔮 奇門運勢", f"{qimen['luck_score']} 分", qimen['god'])
    c3.metric("🧠 理智指數", f"{bio['intel']:.1f}%", "清晰" if bio['intel']>0 else "混亂")
    
    st.subheader("🧠 紅蓮讀心報告")
    
    # 1. 禁忌話題
    st.markdown(f"""
    <div class="radar-alert">
    💥 今日掃雷 (Forbidden Topics): <br>
    {forbidden}
    </div>
    <br>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.info(f"**💭 潛意識訴求 (Hidden Desire)**：\n\n{desire}")
    with col_b:
        st.markdown(f"""<div class="offering-box">🎁 最佳安撫供品：<br>{offering}</div>""", unsafe_allow_html=True)

# ==============================================================================
# 3. 📈 K線趨勢分析
# ==============================================================================
elif menu == "📈 K線趨勢分析":
    st.title("📈 K線趨勢分析")
    input_data = st.text_area("輸入近期數字 (逗號分隔)", "34, 25, 24, 11, 07, 34, 28, 05, 12, 34, 25, 07, 07, 11, 24")
    
    if input_data:
        try:
            data_list = [int(x.strip()) for x in input_data.split(",")]
            df = pd.DataFrame(data_list, columns=["Number"])
            df['MA3'] = df['Number'].rolling(3).mean()
            st.line_chart(df[['Number', 'MA3']])
            if data_list[-1] == 34:
                st.success("🔥 **強勢確認**：34 號近期多頭排列，回彈確立。")
        except:
            st.error("格式錯誤")

# ==============================================================================
# 4. ❤️ 舊愛複合 (對話攻略)
# ==============================================================================
elif menu == "❤️ 舊愛複合 (對話攻略)":
    st.title("❤️ 舊愛複合・五行攻略")
    
    c1, c2 = st.columns(2)
    my_dob = c1.date_input("你的生日", datetime.date(1996, 2, 17))
    ex_dob = c2.date_input("對方生日", datetime.date(1997, 3, 21))
    
    if st.button("💔 分析關係"):
        m_gan, m_el, t_gan, t_el, relation = RedLotusCore.get_element_relation(my_dob, ex_dob)
        
        st.divider()
        k1, k2, k3 = st.columns(3)
        k1.metric("你 (日主)", f"{m_gan} {m_el}")
        k2.metric("她 (日主)", f"{t_gan} {t_el}")
        k3.metric("關係", relation)
        
        st.subheader("💬 紅蓮推薦開場白")
        if "生我" in relation:
            st.success("✅ **優勢局**：她心軟。")
            st.write("『最近經過以前我們常去的那家店，突然想起妳愛吃的那個...』")
        elif "我剋" in relation:
            st.info("⚡ **霸氣局**：直接一點。")
            st.write("『夢到妳了。沒什麼事，只想確認妳最近過得好不好。』")
        elif "剋我" in relation:
            st.error("🛑 **逆風局**：姿態要低。")
            st.write("『這件事只有妳最懂，想請教妳一個問題...』")
        else:
            st.warning("🤝 **平局**：像朋友一樣閒聊。")

# ==============================================================================
# 5. 👤 本命解析 (詳細全配版)
# ==============================================================================
elif menu == "👤 本命解析 (詳細全配版)":
    st.title("👁️ 本命解析・全知全能")
    b_date = st.date_input("輸入生日", datetime.date(1996, 2, 17))
    
    if st.button("🔥 啟動全息解析"):
        gan, zhi = RedLotusCore.get_gan_zhi(b_date)
        color, direction, numbers = RedLotusCore.get_lucky_info(gan)
        details = RedLotusCore.get_detailed_life_reading(gan)
        
        st.divider()
        st.markdown(f"### 🎯 命主核心：【{gan}{zhi}】日")
        
        c1, c2 = st.columns(2)
        c1.info(f"**🎨 幸運色**：{color}")
        c2.success(f"**🧭 貴人方位**：{direction}")
        st.markdown(f"**🔢 本命幸運數**：{numbers}")
        st.markdown("---")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧠 性格底牌", "❤️ 感情交友", "💼 事業天賦", "💰 投資理財", "🏥 身體健康"])
        with tab1: st.markdown(f"""<div class="detail-card"><h4>🧠 性格底層邏輯</h4>{details['char']}</div>""", unsafe_allow_html=True)
        with tab2: st.markdown(f"""<div class="detail-card"><h4>❤️ 感情與交友</h4>{details['love']}</div>""", unsafe_allow_html=True)
        with tab3: st.markdown(f"""<div class="detail-card"><h4>💼 適合做什麼</h4>{details['career']}</div>""", unsafe_allow_html=True)
        with tab4: st.markdown(f"""<div class="detail-card"><h4>💰 投資理財方向</h4>{details['invest']}</div>""", unsafe_allow_html=True)
        with tab5: st.markdown(f"""<div class="detail-card"><h4>🏥 身體弱點與保養</h4>{details['health']}</div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("🗓️ 未來十年大運")
        cycles = RedLotusCore.get_decade_luck(b_date)
        for c in cycles:
            st.write(f"**{c['period']}** : {c['theme']}")

# ==============================================================================
# 6. 🐢 靈龜問事 (卜卦)
# ==============================================================================
elif menu == "🐢 靈龜問事 (卜卦)":
    st.title("🐢 靈龜問事")
    q = st.text_input("心中的問題")
    if st.button("🔮 卜卦") and q:
        res = RedLotusCore.turtle_divination(q)
        st.info(f"**卦象：{res[0]} ({res[1]})**")
        st.write(f"籤詩：{res[2]}")
        if "吉" in res[0]: st.balloons()
    
    st.markdown("---")
    st.subheader("🔥 本期唯一 5 顆大吉")
    st.markdown("""<div style="text-align: center; font-size: 36px; font-weight: bold; color: #d63031; background-color: #ffeaa7; padding: 10px; border-radius: 10px;">07、11、24、25、34</div>""", unsafe_allow_html=True)

# ==============================================================================
# 7. ⏳ 今日時空 (流日)
# ==============================================================================
elif menu == "⏳ 今日時空 (流日)":
    today = datetime.date.today()
    gan, zhi = RedLotusCore.get_gan_zhi(today)
    st.title(f"⏳ {today}")
    st.metric("今日干支", f"{gan}{zhi} 日")
    el = RedLotusCore.ELEMENTS[gan]
    st.write(f"今日五行屬 **{el}**。")
    if el == "火": st.success("🔥 火旺！大利 34 號。")
    elif el == "水": st.info("💧 水旺！利 1, 6 尾數。")

st.markdown("---")
st.caption("Powered by Red Lotus System V9.0 | Mind Reader Edition")
