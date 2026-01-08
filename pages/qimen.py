import streamlit as st
import datetime
import math
import random
import pandas as pd
import numpy as np

# ==============================================================================
# 🛡️ 紅蓮戰略系統 V10.0 - 愛情軍師版 (Red Lotus System V10.0 Love General)
# ==============================================================================
# 核心架構：奇門複合攻略 / 讀心雷達 / 賭王決策(80元) / 本命全解 / 靈龜
# ==============================================================================

st.set_page_config(page_title="紅蓮戰略 V10.0", page_icon="🔥", layout="wide")

# --- [自定義介面樣式] ---
st.markdown("""
<style>
    .big-font { font-size:22px !important; font-weight: bold; }
    .qimen-box { background-color: #2d3436; color: #fab1a0; padding: 15px; border-radius: 8px; border-left: 5px solid #d63031; }
    .love-alert { background-color: #ffeaa7; color: #d63031; padding: 10px; border-radius: 5px; font-weight: bold; }
    .action-card { background-color: #55efc4; color: #00b894; padding: 10px; border-radius: 5px; font-weight: bold; }
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
    STARS = ["天蓬", "天任", "天沖", "天輔", "天英", "天芮", "天柱", "天心", "天禽"]
    GODS = ["值符", "騰蛇", "太陰", "六合", "白虎", "玄武", "九地", "九天"]
    PALACES = ["坎一宮 (水)", "坤二宮 (土)", "震三宮 (木)", "巽四宮 (木)", "中五宮 (土)", "乾六宮 (金)", "兌七宮 (金)", "艮八宮 (土)", "離九宮 (火)"]

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
    def analyze_love_battle(today):
        """[V10.0 新增] 乙庚落宮複合戰略"""
        seed = today.year + today.month + today.day
        random.seed(seed)
        
        # 1. 隨機分配乙(女)與庚(男)的落宮
        yi_palace_idx = random.randint(0, 8)
        geng_palace_idx = random.randint(0, 8)
        
        # 避免同宮(簡化邏輯，若同宮則視為比和)
        while geng_palace_idx == yi_palace_idx:
             geng_palace_idx = random.randint(0, 8)
             
        yi_palace = RedLotusCore.PALACES[yi_palace_idx]
        geng_palace = RedLotusCore.PALACES[geng_palace_idx]
        
        # 提取五行
        yi_el = yi_palace.split("(")[1][0]
        geng_el = geng_palace.split("(")[1][0]
        
        # 判斷關係
        relations = {
            "木": {"木": "比和", "火": "生", "土": "剋", "金": "被剋", "水": "被生"},
            "火": {"木": "被生", "火": "比和", "土": "生", "金": "剋", "水": "被剋"},
            "土": {"木": "被剋", "火": "被生", "土": "比和", "金": "生", "水": "剋"},
            "金": {"木": "剋", "火": "被剋", "土": "被生", "金": "比和", "水": "生"},
            "水": {"木": "生", "火": "剋", "土": "被剋", "金": "被生", "水": "比和"}
        }
        
        relation_yi_to_geng = relations[yi_el][geng_el] # 女對男的態度
        
        # 戰略建議
        strategy = ""
        score = 50
        
        if relation_yi_to_geng == "生":
            strategy = "❤️ **大吉 (她生你)**：她心裡還有你，想回來。主動一點，給個台階下就能成。"
            score = 90
        elif relation_yi_to_geng == "被生":
            strategy = "💪 **中吉 (你生她)**：你需要多付出、多哄她。現在是贖罪期，展現誠意。"
            score = 70
        elif relation_yi_to_geng == "比和":
            strategy = "🤝 **平 (五行相同)**：像朋友一樣相處。不要急著提複合，先恢復互動。"
            score = 60
        elif relation_yi_to_geng == "剋":
            strategy = "⚡ **凶 (她剋你)**：她現在還在氣頭上，對你有很多不滿。暫時避風頭，不要撞槍口。"
            score = 30
        elif relation_yi_to_geng == "被剋":
            strategy = "🛡️ **小凶 (你剋她)**：她怕你或是有壓力。請放低姿態，不要用命令的口氣。"
            score = 40

        # 六合狀態
        liu_he_door = random.choice(RedLotusCore.DOORS)
        
        # 行為風水
        lucky_colors = {"木": "綠色", "火": "紅色", "土": "黃色", "金": "白色", "水": "黑色"}
        lucky_dir = {"木": "東方", "火": "南方", "土": "原地", "金": "西方", "水": "北方"}
        action_guide = f"穿 **{lucky_colors[geng_el]}** 衣服，面向 **{lucky_dir[yi_el]}** (她的落宮方向) 聯繫。"

        return yi_palace, geng_palace, strategy, score, liu_he_door, action_guide

    @staticmethod
    def analyze_yj_mind(qimen_data, bio_data):
        god = qimen_data['god']
        star = qimen_data['star']
        door = qimen_data['door']
        emo = bio_data['emo']

        forbidden = "無特殊禁忌"
        if "白虎" in god or "驚門" in door: forbidden = "🚫 禁止談錢、禁止催促、禁止批評。"
        elif "玄武" in god or "杜門" in door: forbidden = "🚫 禁止問『妳在哪？』(她需要空間)。"
        elif "天沖" in star or "傷門" in door: forbidden = "🚫 禁止講道理、禁止辯論。"
        elif "騰蛇" in god: forbidden = "🚫 禁止承諾做不到的事。"

        desire = "希望被理解"
        if "休門" in door: desire = "想休息，想被當成小公主寵愛。"
        elif "生門" in door: desire = "想吃好吃的，想要物質滿足。"
        elif "景門" in door: desire = "想出去玩，想被稱讚漂亮。"
        elif "開門" in door: desire = "想聊未來，希望你有上進心。"
        elif "死門" in door: desire = "心情悶，需要無聲的陪伴。"
        
        offering = "熱可可"
        if emo < -20: offering = "高熱量甜點 (巧克力) - 補血。"
        elif "火" in door: offering = "冰拿鐵、微糖綠茶 - 降火。"
        elif "土" in door: offering = "溫熱湯品 - 暖胃。"
        else: offering = "她喜歡的那個 (珍珠奶茶)。"

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
st.sidebar.title("🔥 紅蓮 V10.0 愛情軍師")
st.sidebar.caption("System Status: LOVE GENERAL")
st.sidebar.markdown("---")

menu = st.sidebar.radio("🔰 戰術模組", [
    "🎰 賭王決策系統 (一注80)", 
    "👧 予婕情緒雷達 (讀心版)", 
    "❤️ 舊愛複合 (奇門攻略版)",
    "📈 K線趨勢分析",
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
    m1.metric("建議注數", f"{num_units} 注", f"每注 ${unit_cost}")
    m2.metric("總投入金額", f"${num_units * unit_cost}", f"佔總資金 {(num_units*80/budget)*100:.1f}%")
    m3.metric("預期獲利", f"${num_units * unit_cost * 53}", "倍率 x53") 
    
    if num_units > 5:
        st.warning("⚠️ **重倉攻擊**：信心高，投入大。")
    elif num_units >= 1:
        st.success("✅ **標準戰術**：穩健佈局。")
    else:
        st.info("🛡️ **觀望**：建議暫停或小額測試。")

# ==============================================================================
# 2. 👧 予婕情緒雷達 (讀心版)
# ==============================================================================
elif menu == "👧 予婕情緒雷達 (讀心版)":
    st.title("👧 予婕情緒雷達・讀心指揮官")
    
    yj_birth = datetime.date(1997, 3, 21)
    today = datetime.date.today()
    bio = RedLotusCore.get_biorhythm(yj_birth)
    qimen = RedLotusCore.get_qimen_chart(today, "午")
    forbidden, desire, offering = RedLotusCore.analyze_yj_mind(qimen, bio)
    
    st.markdown(f"""
    <div class="qimen-box">
    <b>Target:</b> Yu-Jie (予婕) | <b>今日命宮:</b> 臨 <span style="color:#ffeaa7;">{qimen['door']}</span> + {qimen['star']}
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("❤️ 生理情緒", f"{bio['emo']:.1f}%", "高" if bio['emo']>0 else "低")
    c2.metric("🔮 奇門運勢", f"{qimen['luck_score']} 分", qimen['god'])
    c3.metric("🧠 理智指數", f"{bio['intel']:.1f}%", "清" if bio['intel']>0 else "亂")
    
    st.subheader("🧠 紅蓮讀心報告")
    st.markdown(f"""<div class="love-alert">💥 今日掃雷 (Forbidden):<br>{forbidden}</div><br>""", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a: st.info(f"**💭 潛意識訴求**：\n{desire}")
    with col_b: st.markdown(f"""<div class="action-card">🎁 最佳供品：<br>{offering}</div>""", unsafe_allow_html=True)

# ==============================================================================
# 3. ❤️ 舊愛複合 (奇門攻略版 - V10.0核心)
# ==============================================================================
elif menu == "❤️ 舊愛複合 (奇門攻略版)":
    st.title("❤️ 舊愛複合・奇門乙庚決戰")
    st.markdown("利用奇門遁甲「乙庚落宮」與「行為風水」制定必勝戰略。")
    
    c1, c2 = st.columns(2)
    my_dob = c1.date_input("你的生日 (庚/男)", datetime.date(1996, 2, 17))
    ex_dob = c2.date_input("她/他的生日 (乙/女)", datetime.date(1997, 3, 21))
    
    if st.button("💘 啟動奇門兵法"):
        # 1. 五行基礎關係
        m_gan, m_el, t_gan, t_el, relation = RedLotusCore.get_element_relation(my_dob, ex_dob)
        
        # 2. 奇門落宮戰略
        yi_p, geng_p, strategy, score, liu_he, action = RedLotusCore.analyze_love_battle(datetime.date.today())
        
        st.divider()
        st.subheader("🔮 戰場掃描 (Battlefield)")
        
        k1, k2, k3 = st.columns(3)
        k1.metric("乙 (她) 落宮", yi_p)
        k2.metric("庚 (你) 落宮", geng_p)
        k3.metric("複合機率", f"{score}%", relation)
        
        st.markdown(f"""
        <div class="detail-card">
        <h4>📜 紅蓮軍師錦囊</h4>
        <b>【戰略判斷】</b>：{strategy} <br><br>
        <b>【六合狀態】</b>：關係宮臨 <b>{liu_he}</b>。<br>
        (若臨開/休/生門為吉，臨死/驚/傷門需小心)
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🏃 行為風水 (Action Feng Shui)")
        st.markdown(f"""
        <div class="action-card">
        🔥 必勝指令：<br>
        {action}
        </div>
        """, unsafe_allow_html=True)
        
        st.caption("* 此戰略基於今日時空能量推演，請把握良機。")

# ==============================================================================
# 4. 📈 K線趨勢分析
# ==============================================================================
elif menu == "📈 K線趨勢分析":
    st.title("📈 K線趨勢分析")
    input_data = st.text_area("輸入近期數字", "34, 25, 24, 11, 07, 34, 28, 05, 12, 34, 25, 07, 07, 11, 24")
    if input_data:
        try:
            data_list = [int(x.strip()) for x in input_data.split(",")]
            df = pd.DataFrame(data_list, columns=["Number"])
            df['MA3'] = df['Number'].rolling(3).mean()
            st.line_chart(df[['Number', 'MA3']])
            if data_list[-1] == 34: st.success("🔥 34 號回彈確立。")
        except: st.error("格式錯誤")

# ==============================================================================
# 5. 👤 本命解析 (詳細全配版)
# ==============================================================================
elif menu == "👤 本命解析 (詳細全配版)":
    st.title("👁️ 本命解析・全知全能")
    b_date = st.date_input("輸入生日", datetime.date(1996, 2, 17))
    if st.button("🔥 啟動解析"):
        gan, zhi = RedLotusCore.get_gan_zhi(b_date)
        color, direction, numbers = RedLotusCore.get_lucky_info(gan)
        details = RedLotusCore.get_detailed_life_reading(gan)
        
        st.divider()
        st.markdown(f"### 🎯 命主：【{gan}{zhi}】日")
        c1, c2 = st.columns(2)
        c1.info(f"**🎨 幸運色**：{color}")
        c2.success(f"**🧭 貴人方位**：{direction}")
        st.markdown(f"**🔢 幸運數**：{numbers}")
        st.markdown("---")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧠 性格", "❤️ 感情", "💼 事業", "💰 投資", "🏥 健康"])
        with tab1: st.write(details['char'])
        with tab2: st.write(details['love'])
        with tab3: st.write(details['career'])
        with tab4: st.write(details['invest'])
        with tab5: st.write(details['health'])

        st.markdown("---")
        st.subheader("🗓️ 十年大運")
        cycles = RedLotusCore.get_decade_luck(b_date)
        for c in cycles: st.write(f"**{c['period']}** : {c['theme']}")

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
    st.subheader("🔥 本期大吉：07、11、24、25、34")

# ==============================================================================
# 7. ⏳ 今日時空 (流日)
# ==============================================================================
elif menu == "⏳ 今日時空 (流日)":
    today = datetime.date.today()
    gan, zhi = RedLotusCore.get_gan_zhi(today)
    st.title(f"⏳ {today}")
    st.metric("今日干支", f"{gan}{zhi} 日")
    el = RedLotusCore.ELEMENTS[gan]
    st.write(f"五行屬 **{el}**。")
    if el == "火": st.success("🔥 火旺！大利 34 號。")
    elif el == "水": st.info("💧 水旺！利 1, 6 尾數。")

st.markdown("---")
st.caption("Powered by Red Lotus System V10.0 | Love General Edition")
