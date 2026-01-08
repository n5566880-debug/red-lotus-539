import streamlit as st
import datetime
import math
import random
import pandas as pd
import numpy as np

# ==============================================================================
# 🛡️ 紅蓮戰略系統 V8.0 - 全知全能指揮官版 (Red Lotus System V8.0 Omniscient)
# ==============================================================================
# 核心架構：奇門遁甲 / 賭王決策(80元) / 雙人合盤 / 十年大限 / 全方位本命解析
# ==============================================================================

st.set_page_config(page_title="紅蓮戰略 V8.0", page_icon="🔥", layout="wide")

# --- [自定義軍事風格介面] ---
st.markdown("""
<style>
    .big-font { font-size:22px !important; font-weight: bold; }
    .qimen-box { background-color: #2d3436; color: #fab1a0; padding: 15px; border-radius: 8px; border-left: 5px solid #d63031; }
    .metric-box { background-color: #f1f2f6; padding: 15px; border-radius: 8px; border-left: 5px solid #0984e3; }
    .luck-cycle { background-color: #dfe6e9; color: #2d3436; padding: 10px; border-radius: 5px; margin-bottom: 5px; }
    .detail-card { background-color: #fff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 10px; }
    .stProgress > div > div > div > div { background-color: #d63031; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# [核心運算庫] Red Lotus Core Intelligence
# ==============================================================================
class RedLotusCore:
    # 基礎天干地支
    GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    ELEMENTS = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土", "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"}
    
    # 奇門參數
    DOORS = ["休門 (吉)", "死門 (凶)", "傷門 (凶)", "杜門 (平)", "開門 (吉)", "驚門 (凶)", "生門 (吉)", "景門 (平)"]
    STARS = ["天蓬 (大盜)", "天任 (富翁)", "天沖 (武士)", "天輔 (文曲)", "天英 (烈火)", "天芮 (病符)", "天柱 (破軍)", "天心 (名醫)", "天禽 (領袖)"]
    GODS = ["值符 (領袖)", "騰蛇 (詐欺)", "太陰 (陰佑)", "六合 (婚姻)", "白虎 (血光)", "玄武 (小人)", "九地 (潛藏)", "九天 (顯揚)"]

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
        """[V8.0 新增] 全方位詳細本命解析資料庫"""
        db = {
            "甲": {
                "char": "【參天大樹】正直嚴肅，有領袖氣質，不怒自威。缺點是容易固執，不知變通，吃軟不吃硬。",
                "love": "感情專一但缺乏浪漫。喜歡有能力、聽話的伴侶。大男人/大女人主義較重。",
                "career": "適合創業、管理、公職。你是天生的主管，不喜歡被人管。適合做實業。",
                "invest": "【穩健增長型】適合長期持有的藍籌股、房地產。忌短線投機。",
                "health": "注意【肝膽】、神經系統、頭部。容易因為壓力大而頭痛或失眠。"
            },
            "乙": {
                "char": "【花草藤蔓】性格柔軟靈活，適應力極強。善於迂迴溝通，不喜歡正面衝突。缺點是有時缺乏主見。",
                "love": "溫柔體貼，黏人。喜歡被呵護的感覺。容易在感情中委曲求全。",
                "career": "適合業務、策劃、藝術、幕僚。你擅長借力使力，適合團隊合作。",
                "invest": "【靈活操作型】適合波段操作、文化產業、醫療相關標的。",
                "health": "注意【肝臟】、頸椎、四肢關節。容易有筋骨痠痛的問題。"
            },
            "丙": {
                "char": "【太陽之火】熱情奔放，藏不住秘密。行動力強，急躁但無心機，脾氣來得快去得快。",
                "love": "主動直接，喜歡就會大聲說出來。喜歡陽光、開朗的對象。感情中容易爭吵但很快和好。",
                "career": "適合演藝、銷售、公關、餐飲。需要舞台和掌聲的工作。",
                "invest": "【短線爆發型】適合科技股、能源股、加密貨幣。直覺強，但忌貪心。",
                "health": "注意【心臟】、血壓、小腸、眼睛。容易上火發炎。"
            },
            "丁": {
                "char": "【燈燭之火】心思細膩，洞察力極強 (如你)。外表溫和，內心有火。第六感神準，善於謀略。",
                "love": "慢熱深情，一旦愛上就很執著。重視精神契合，不喜歡粗魯的人。",
                "career": "適合心理諮詢、命理、分析師、研發。需要用腦和直覺的工作。",
                "invest": "【策略分析型】適合技術分析、期貨、選擇權。擅長捕捉趨勢轉折。",
                "health": "注意【心血管】、眼睛視力、焦慮。容易因為想太多而神經衰弱。"
            },
            "戊": {
                "char": "【高山之土】沈穩厚重，重信守諾。反應較慢但非常可靠。缺點是固執，不喜歡改變。",
                "love": "被動木訥，不懂浪漫但很實在。給伴侶極大的安全感。喜歡顧家的對象。",
                "career": "適合倉儲、保險、銀行、房地產、農業。需要信用和穩定的工作。",
                "invest": "【資產累積型】最適合房地產、定存、儲蓄險。只做看得到的投資。",
                "health": "注意【胃部】、消化系統、肌肉。容易有胃病或肥胖問題。"
            },
            "己": {
                "char": "【田園之土】內斂包容，多才多藝。做事有條理，細心。缺點是容易多疑，心防較重。",
                "love": "細水長流，會照顧人。感情中比較被動，需要對方先示好。",
                "career": "適合秘書、護理、教育、會計。需要耐心和細心的工作。",
                "invest": "【穩健防守型】適合基金、債券、傳統產業。風險厭惡者。",
                "health": "注意【脾臟】、腹部、代謝系統。容易有腸胃不適。"
            },
            "庚": {
                "char": "【刀劍之金】剛毅果斷，講義氣。吃軟不吃硬，有話直說。缺點是容易得罪人，破壞力強。",
                "love": "愛恨分明，喜歡強者。感情中佔有慾強，不喜歡拖泥帶水。",
                "career": "適合軍警、法務、工程師、外科醫生。需要決斷力和技術的工作。",
                "invest": "【積極進攻型】適合鋼鐵、硬體設施、大宗商品。敢於槓桿操作。",
                "health": "注意【肺部】、呼吸系統、大腸、皮膚。容易過敏或咳嗽。"
            },
            "辛": {
                "char": "【珠寶之金】優雅愛面子，重視質感。口才好，說話帶刺。自尊心極強，受不得委屈。",
                "love": "重視外表和品味。喜歡有氣質、能帶出門的對象。感情中比較挑剔。",
                "career": "適合設計、精品、外交、律師、金融。需要形象和口才的工作。",
                "invest": "【精準操作型】適合貴金屬、珠寶、醫美、高端消費股。",
                "health": "注意【呼吸道】、牙齒、骨骼。體質通常較敏感。"
            },
            "壬": {
                "char": "【江河之水】聰明靈活，善變奔放。風趣幽默，人緣好。缺點是任性，不喜歡被管束。",
                "love": "多情浪漫，桃花旺。喜歡新鮮感，不喜歡太黏的關係。",
                "career": "適合貿易、運輸、旅遊、業務、創意。需要流動和變化的工作。",
                "invest": "【趨勢投機型】適合外匯、航運、跨境電商。流動性強的資產。",
                "health": "注意【腎臟】、膀胱、泌尿系統、血液循環。"
            },
            "癸": {
                "char": "【雨露之水】溫柔內向，心思深沈。耐力極強，善於滲透人心。容易情緒內耗，想很多。",
                "love": "敏感細膩，容易受傷。需要大量的愛和確認。感情中比較依賴。",
                "career": "適合幕後、策劃、研究、玄學、心理。適合靜態用腦的工作。",
                "invest": "【靈感直覺型】適合冷門股、潛力股。擅長挖掘被低估的價值。",
                "health": "注意【腎氣】、生殖系統、耳朵、水腫。容易有婦科/男科隱疾。"
            }
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
st.sidebar.title("🔥 紅蓮 V8.0 全知全能")
st.sidebar.caption("System Status: OMNISCIENT")
st.sidebar.markdown("---")

menu = st.sidebar.radio("🔰 戰術模組", [
    "🎰 賭王決策系統 (一注80)", 
    "👧 予婕情緒雷達 (奇門)", 
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
    
    # 凱利公式計算
    odds = 5.0 # 期望賠率
    kelly_ratio = RedLotusCore.calculate_kelly_criterion(win_prob, odds)
    base_ratio = kelly_ratio * 100 * 0.8 # 風控係數
    
    # 核心號碼加權
    if "34" in numbers: 
        base_ratio += 5.0
        st.caption("🔥 偵測到 [34] 號，權重提升！")
    
    # 計算具體注數 (一注80)
    suggested_total = budget * (base_ratio / 100)
    unit_cost = 80
    num_units = int(suggested_total / unit_cost)
    
    if num_units < 1 and base_ratio > 1: num_units = 1
    
    st.markdown("### 🛡️ 戰術指令")
    m1, m2, m3 = st.columns(3)
    
    m1.metric("建議注數 (Unit)", f"{num_units} 注", f"每注 ${unit_cost}")
    m2.metric("總投入金額", f"${num_units * unit_cost}", f"佔總資金 {(num_units*80/budget)*100:.1f}%")
    m3.metric("預期獲利 (若中獎)", f"${num_units * unit_cost * 53}", "倍率 x53") 
    
    st.markdown("---")
    if num_units > 5:
        st.warning("⚠️ **重倉攻擊**：今日信心高，投入較大，請確認資金風險。")
    elif num_units >= 1:
        st.success("✅ **標準戰術**：依計畫執行，穩健佈局。")
    else:
        st.info("🛡️ **觀望**：今日風險回報比不佳，建議暫停或僅下一注測試。")

# ==============================================================================
# 2. 👧 予婕情緒雷達 (奇門回歸版)
# ==============================================================================
elif menu == "👧 予婕情緒雷達 (奇門)":
    st.title("👧 予婕情緒雷達・奇門天眼")
    
    yj_birth = datetime.date(1997, 3, 21)
    today = datetime.date.today()
    bio = RedLotusCore.get_biorhythm(yj_birth)
    qimen = RedLotusCore.get_qimen_chart(today, "午")
    
    st.markdown(f"""
    <div class="qimen-box">
    <b>Target:</b> Yu-Jie (予婕) | <b>Birthday:</b> 1997/03/21 (午時) <br>
    <b>今日奇門命宮:</b> 臨 <span style="color:#ffeaa7; font-size:18px;">{qimen['door']}</span> + {qimen['star']}
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("❤️ 生理情緒", f"{bio['emo']:.1f}%", "高昂" if bio['emo']>0 else "低落")
    c2.metric("🔮 奇門運勢", f"{qimen['luck_score']} 分", qimen['god'])
    c3.metric("🧠 理智指數", f"{bio['intel']:.1f}%", "清晰" if bio['intel']>0 else "混亂")
    
    st.subheader("🛡️ 紅蓮戰略分析")
    
    if "吉" in qimen['door'] and bio['emo'] > -20:
        st.success(f"🔥 **絕佳機會**：今日臨 **{qimen['door']}** (吉門)，且情緒穩定。適合求複合、約會。")
    elif "凶" in qimen['door'] or bio['emo'] < -40:
        st.error(f"🚨 **紅色警戒**：今日臨 **{qimen['door']}** (凶門)，又逢情緒低潮。請保持安靜。")
    else:
        st.warning(f"⚠️ **變數極大**：情緒普通，臨 {qimen['door']}。建議先試探水溫。")

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
            st.caption("藍線：開出號碼 | 紅線：3期平均線")
            
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
            st.success("✅ **優勢局**：她心軟。適合打溫情牌。")
            st.write("『最近經過以前我們常去的那家店，突然想起妳愛吃的那個...』")
        elif "我剋" in relation:
            st.info("⚡ **霸氣局**：直接一點。")
            st.write("『夢到妳了。沒什麼事，只想確認妳最近過得好不好。』")
        elif "剋我" in relation:
            st.error("🛑 **逆風局**：姿態要低，請教問題開場。")
            st.write("『這件事只有妳最懂，想請教妳一個問題...』")
        else:
            st.warning("🤝 **平局**：像朋友一樣閒聊。")

# ==============================================================================
# 5. 👤 本命解析 (詳細全配版)
# ==============================================================================
elif menu == "👤 本命解析 (詳細全配版)":
    st.title("👁️ 本命解析・全知全能")
    st.markdown("針對性格、身體、交友、事業、投資的全方位深度掃描。")
    
    b_date = st.date_input("輸入生日", datetime.date(1996, 2, 17))
    
    if st.button("🔥 啟動全息解析"):
        gan, zhi = RedLotusCore.get_gan_zhi(b_date)
        color, direction, numbers = RedLotusCore.get_lucky_info(gan)
        details = RedLotusCore.get_detailed_life_reading(gan)
        
        st.divider()
        st.markdown(f"### 🎯 命主核心：【{gan}{zhi}】日")
        
        # 幸運參數
        c1, c2 = st.columns(2)
        c1.info(f"**🎨 幸運色**：{color}")
        c2.success(f"**🧭 貴人方位**：{direction}")
        
        st.markdown("---")
        
        # 深度解析卡片 (Tabs)
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧠 性格底牌", "❤️ 感情交友", "💼 事業天賦", "💰 投資理財", "🏥 身體健康"])
        
        with tab1:
            st.markdown(f"""<div class="detail-card"><h4>🧠 性格底層邏輯</h4>{details['char']}</div>""", unsafe_allow_html=True)
        with tab2:
            st.markdown(f"""<div class="detail-card"><h4>❤️ 感情與交友</h4>{details['love']}</div>""", unsafe_allow_html=True)
        with tab3:
            st.markdown(f"""<div class="detail-card"><h4>💼 適合做什麼</h4>{details['career']}</div>""", unsafe_allow_html=True)
        with tab4:
            st.markdown(f"""<div class="detail-card"><h4>💰 投資理財方向</h4>{details['invest']}</div>""", unsafe_allow_html=True)
        with tab5:
            st.markdown(f"""<div class="detail-card"><h4>🏥 身體弱點與保養</h4>{details['health']}</div>""", unsafe_allow_html=True)
            st.caption("*以上為命理分析，身體不適請務必就醫。")

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
st.caption("Powered by Red Lotus System V8.0 | Omniscient Commander")
