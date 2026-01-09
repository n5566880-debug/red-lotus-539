import streamlit as st
import datetime
import math
import random
import pandas as pd
import numpy as np

# ==============================================================================
# 🛡️ 紅蓮戰略系統 V11.0 - 慣性修正版 (Red Lotus V11.0 Inertia Correction)
# ==============================================================================
# 核心戰略：利用 22 號出現修正 24/25 機率 / 賭王一注80 / 舊愛奇門 / 本命全解
# ==============================================================================

st.set_page_config(page_title="紅蓮戰略 V11.0", page_icon="🔥", layout="wide")

# --- [軍事介面樣式] ---
st.markdown("""
<style>
    .big-font { font-size:22px !important; font-weight: bold; }
    .qimen-box { background-color: #2d3436; color: #fab1a0; padding: 15px; border-radius: 8px; border-left: 5px solid #d63031; }
    .correction-box { background-color: #74b9ff; color: #2d3436; padding: 15px; border-radius: 8px; border-left: 5px solid #0984e3; }
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
    DOORS = ["休門", "死門", "傷門", "杜門", "開門", "驚門", "生門", "景門"]
    STARS = ["天蓬", "天任", "天沖", "天輔", "天英", "天芮", "天柱", "天心", "天禽"]
    GODS = ["值符", "騰蛇", "太陰", "六合", "白虎", "玄武", "九地", "九天"]
    PALACES = ["坎一宮(水)", "坤二宮(土)", "震三宮(木)", "巽四宮(木)", "中五宮(土)", "乾六宮(金)", "兌七宮(金)", "艮八宮(土)", "離九宮(火)"]

    @staticmethod
    def get_gan_zhi(date):
        base_date = datetime.date(1900, 1, 1)
        days = (date - base_date).days
        gan_idx = days % 10
        zhi_idx = (days + 10) % 12
        return RedLotusCore.GAN[gan_idx], RedLotusCore.ZHI[zhi_idx]

    @staticmethod
    def analyze_inertia_correction(last_draw_nums, target_nums):
        """[V11.0 新增] 慣性修正演算法：根據上期號碼調整本期權重"""
        correction_score = 0
        analysis_log = []
        
        # 1. 鄰號拖曳效應 (Drag Effect)
        # 邏輯：22 出現，對 23, 24 (偶數連動) 有拖曳力
        if 22 in last_draw_nums:
            if 24 in target_nums:
                correction_score += 15
                analysis_log.append("🔹 **22 號前導確認**：偶數慣性啟動，24 號回補機率提升 (+15%)。")
            if 23 in target_nums:
                correction_score += 10
                analysis_log.append("🔹 **22 號鄰號效應**：23 號作為中間號，熱度上升。")

        # 2. 34 號回彈餘波 (Rebound Aftershock)
        # 邏輯：34 已開，通常會帶動 24 (同尾數) 或 35
        if 34 in last_draw_nums:
            if 24 in target_nums:
                correction_score += 20
                analysis_log.append("🔥 **34 號同尾共鳴**：4 尾數能量開啟，強力支撐 24 號 (+20%)。")
            if 25 in target_nums:
                correction_score += 10
                analysis_log.append("🔸 **34 號斜連動**：高位號碼回落，有利於 25 號填補空缺。")

        # 3. 隔期回補 (Gap Fill)
        # 邏輯：25 沒開，累積了未能釋放的勢能
        if 25 in target_nums and 25 not in last_draw_nums:
            analysis_log.append("⏳ **25 號勢能累積**：未開出視為蓄力，下期爆發係數增加。")

        return correction_score, analysis_log

    @staticmethod
    def analyze_love_battle(today):
        seed = today.year + today.month + today.day
        random.seed(seed)
        yi_idx = random.randint(0, 8)
        geng_idx = random.randint(0, 8)
        while geng_idx == yi_idx: geng_idx = random.randint(0, 8)
        
        yi_p = RedLotusCore.PALACES[yi_idx]
        geng_p = RedLotusCore.PALACES[geng_idx]
        yi_el = yi_p.split("(")[1][0]
        geng_el = geng_p.split("(")[1][0]
        
        relations = {
            "木": {"木": "比和", "火": "生", "土": "剋", "金": "被剋", "水": "被生"},
            "火": {"木": "被生", "火": "比和", "土": "生", "金": "剋", "水": "被剋"},
            "土": {"木": "被剋", "火": "被生", "土": "比和", "金": "生", "水": "剋"},
            "金": {"木": "剋", "火": "被剋", "土": "被生", "金": "比和", "水": "生"},
            "水": {"木": "生", "火": "剋", "土": "被剋", "金": "被生", "水": "比和"}
        }
        rel = relations[yi_el][geng_el]
        
        strat = "平局"
        if rel == "生": strat = "❤️ 大吉 (她生你)：她想回來，主動點。"
        elif rel == "被生": strat = "💪 中吉 (你生她)：多哄她，展現誠意。"
        elif rel == "剋": strat = "⚡ 凶 (她剋你)：她在生氣，避風頭。"
        elif rel == "被剋": strat = "🛡️ 小凶 (你剋她)：她怕你，放低姿態。"
        
        lucky_colors = {"木": "綠", "火": "紅", "土": "黃", "金": "白", "水": "黑"}
        action = f"穿{lucky_colors[geng_el]}衣，向{yi_p[:2]}方聯繫。"
        
        return yi_p, geng_p, strat, rel, action

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
    def analyze_yj_mind(qimen, bio):
        god = qimen['god']
        door = qimen['door']
        emo = bio['emo']
        
        forbidden = "無特殊禁忌"
        if "白虎" in god: forbidden = "🚫 禁止談錢、催促。"
        elif "玄武" in god: forbidden = "🚫 禁止查勤。"
        elif "傷門" in door: forbidden = "🚫 禁止講道理。"
        
        desire = "求關注"
        if "休門" in door: desire = "想休息，當小公主。"
        elif "生門" in door: desire = "想吃美食，收禮物。"
        
        offering = "熱飲"
        if emo < -20: offering = "甜點 (補血)。"
        elif "火" in door: offering = "冰飲 (降火)。"
        
        return forbidden, desire, offering

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
    def get_gan_zhi(date):
        base_date = datetime.date(1900, 1, 1)
        days = (date - base_date).days
        gan_idx = days % 10
        zhi_idx = (days + 10) % 12
        return RedLotusCore.GAN[gan_idx], RedLotusCore.ZHI[zhi_idx]
        
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
    def get_lucky_info(gan):
        el = RedLotusCore.ELEMENTS[gan]
        info = {
            "木": ("綠/青", "東", "3,8"), "火": ("紅/紫", "南", "2,7"),
            "土": ("黃/咖", "中/東北", "0,5"), "金": ("白/金", "西", "4,9"),
            "水": ("黑/藍", "北", "1,6")
        }
        return info[el]

    @staticmethod
    def get_detailed_life_reading(gan):
        db = {
            "甲": {"char": "領袖、固執", "love": "大男人/女人", "career": "管理", "invest": "藍籌股", "health": "肝"},
            "乙": {"char": "柔軟、適應", "love": "黏人", "career": "業務", "invest": "波段", "health": "頸椎"},
            "丙": {"char": "熱情、急躁", "love": "主動", "career": "演藝", "invest": "短線", "health": "心臟"},
            "丁": {"char": "細膩、第六感", "love": "深情", "career": "分析", "invest": "策略", "health": "心血管"},
            "戊": {"char": "沈穩、木訥", "love": "給安全感", "career": "倉儲", "invest": "房產", "health": "胃"},
            "己": {"char": "內斂、多疑", "love": "細水長流", "career": "秘書", "invest": "基金", "health": "脾"},
            "庚": {"char": "剛毅、衝動", "love": "愛恨分明", "career": "軍警", "invest": "鋼鐵", "health": "肺"},
            "辛": {"char": "優雅、挑剔", "love": "外貌協會", "career": "設計", "invest": "精品", "health": "牙"},
            "壬": {"char": "聰明、善變", "love": "多情", "career": "貿易", "invest": "外匯", "health": "腎"},
            "癸": {"char": "溫柔、深沈", "love": "依賴", "career": "玄學", "invest": "潛力股", "health": "生殖"}
        }
        return db[gan]
        
    @staticmethod
    def get_decade_luck(birth_date):
        start = datetime.date.today().year
        els = ["木運(啟動)", "火運(顯化)", "土運(穩固)", "金運(變革)", "水運(潛藏)"]
        seed = birth_date.year % 5
        return [{"period": f"{start+i*10}~{start+(i+1)*10-1}", "theme": els[(seed+i)%5]} for i in range(5)]

    @staticmethod
    def turtle_divination(q):
        if not q: return None
        random.seed(len(q) + datetime.datetime.now().microsecond)
        res = [("大吉", "乾", "飛龍在天"), ("中吉", "離", "前途光明"), ("小吉", "震", "有驚無險"),
               ("平", "兌", "多溝通"), ("凶", "坎", "保守"), ("大凶", "困", "靜待")]
        return random.choice(res)

# --- [UI 側邊欄] ---
st.sidebar.title("🔥 紅蓮 V11.0 慣性修正")
st.sidebar.caption("Status: RE-CALIBRATING...")
st.sidebar.markdown("---")

menu = st.sidebar.radio("🔰 戰術模組", [
    "🎰 賭王決策系統 (鄰號修正版)", 
    "❤️ 舊愛複合 (奇門攻略)", 
    "👧 予婕情緒雷達 (讀心)", 
    "📈 K線趨勢分析",
    "👤 本命解析 (全配版)",
    "🐢 靈龜問事 (卜卦)",
    "⏳ 今日時空 (流日)"
])

# ==============================================================================
# 1. 🎰 賭王決策系統 (鄰號修正版 - V11.0 核心)
# ==============================================================================
if menu == "🎰 賭王決策系統 (鄰號修正版)":
    st.title("🎰 專業資金控管・慣性修正")
    st.markdown("### Inertia Correction System")
    st.markdown("---")
    
    # 1. 輸入區
    c1, c2 = st.columns(2)
    last_draw_input = c1.text_input("📍 上期開出號碼 (修正參數)", "01, 12, 14, 22, 34")
    target_input = c2.text_input("🎯 本期鎖定目標", "24, 25, 07, 11")
    
    c3, c4 = st.columns(2)
    budget = c3.number_input("💰 總預算 (TWD)", value=2000, step=100)
    win_prob = c4.slider("📊 信心指數", 0.1, 0.9, 0.40) # 信心提升，因為有修正

    # 2. 數據處理
    try:
        last_draw = [int(x.strip()) for x in last_draw_input.split(",")]
        target_nums = [int(x.strip()) for x in target_input.split(",")]
        
        # 3. 執行修正演算法
        correction_score, logs = RedLotusCore.analyze_inertia_correction(last_draw, target_nums)
        
        # 4. 凱利公式 + 修正
        odds = 5.0
        kelly_ratio = RedLotusCore.calculate_kelly_criterion(win_prob, odds)
        base_ratio = kelly_ratio * 100 * 0.8 # 基礎風控
        
        # 疊加修正權重
        final_ratio = base_ratio + (correction_score / 10)
        
        # 5. 計算注數
        unit_cost = 80
        suggested_total = budget * (final_ratio / 100)
        num_units = int(suggested_total / unit_cost)
        if num_units < 1 and final_ratio > 1: num_units = 1
        
        # 6. 顯示結果
        st.subheader("🛡️ 修正後戰略指令")
        
        # 顯示修正日誌
        st.markdown(f"""
        <div class="correction-box">
        <b>⚙️ 矩陣校準日誌：</b><br>
        {"<br>".join(logs)}
        </div>
        <br>
        """, unsafe_allow_html=True)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("建議注數", f"{num_units} 注", f"權重修正 +{correction_score}%")
        m2.metric("總投入", f"${num_units * unit_cost}", f"佔比 {(num_units*80/budget)*100:.1f}%")
        m3.metric("目標核心", "24, 25", "強力回補")
        
        if correction_score > 20:
            st.success("🔥 **強力進攻信號**：鄰號與同尾數雙重共鳴，建議加碼佈局。")
        else:
            st.info("✅ **標準戰術**：依修正後的權重執行。")
            
    except:
        st.error("⚠️ 請輸入正確的數字格式 (用逗號分隔)")

# ==============================================================================
# 2. ❤️ 舊愛複合 (奇門攻略)
# ==============================================================================
elif menu == "❤️ 舊愛複合 (奇門攻略)":
    st.title("❤️ 舊愛複合・乙庚決戰")
    c1, c2 = st.columns(2)
    my_dob = c1.date_input("你的生日", datetime.date(1996, 2, 17))
    ex_dob = c2.date_input("她/他的生日", datetime.date(1997, 3, 21))
    
    if st.button("💘 分析戰局"):
        m_gan, m_el, t_gan, t_el, rel_ele = RedLotusCore.get_element_relation(my_dob, ex_dob)
        yi_p, geng_p, strat, rel_qimen, action = RedLotusCore.analyze_love_battle(datetime.date.today())
        
        st.divider()
        k1, k2, k3 = st.columns(3)
        k1.metric("乙(她) 落宮", yi_p)
        k2.metric("庚(你) 落宮", geng_p)
        k3.metric("戰略判定", rel_qimen)
        
        st.markdown(f"""<div class="qimen-box"><b>📜 紅蓮軍師錦囊：</b><br>{strat}</div>""", unsafe_allow_html=True)
        st.markdown(f"**🏃 行為風水：** {action}")

# ==============================================================================
# 3. 👧 予婕情緒雷達 (讀心)
# ==============================================================================
elif menu == "👧 予婕情緒雷達 (讀心)":
    st.title("👧 予婕情緒雷達")
    yj_birth = datetime.date(1997, 3, 21)
    bio = RedLotusCore.get_biorhythm(yj_birth)
    qimen = RedLotusCore.get_qimen_chart(datetime.date.today())
    forbidden, desire, offering = RedLotusCore.analyze_yj_mind(qimen, bio)
    
    st.markdown(f"""<div class="qimen-box"><b>Target:</b> Yu-Jie (予婕) | <b>命宮:</b> {qimen['door']} + {qimen['star']}</div>""", unsafe_allow_html=True)
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("❤️ 生理情緒", f"{bio['emo']:.1f}%")
    c2.metric("🔮 運勢", f"{qimen['luck_score']}分")
    c3.metric("🧠 理智", f"{bio['intel']:.1f}%")
    
    col_a, col_b = st.columns(2)
    with col_a: st.info(f"**💭 潛意識訴求**：\n{desire}")
    with col_b: st.warning(f"**💥 掃雷禁忌**：\n{forbidden}")

# ==============================================================================
# 4. 📈 K線趨勢分析
# ==============================================================================
elif menu == "📈 K線趨勢分析":
    st.title("📈 K線趨勢分析")
    input_data = st.text_area("輸入近期數字", "34, 25, 24, 11, 07, 34, 28, 05, 12, 34, 25, 07, 07, 11, 24")
    if input_data:
        try:
            data = [int(x.strip()) for x in input_data.split(",")]
            df = pd.DataFrame(data, columns=["Number"])
            df['MA3'] = df['Number'].rolling(3).mean()
            st.line_chart(df)
            if data[-1] == 34: st.success("🔥 34 號確立回彈。")
        except: st.error("格式錯誤")

# ==============================================================================
# 5. 👤 本命解析 (全配版)
# ==============================================================================
elif menu == "👤 本命解析 (全配版)":
    st.title("👁️ 本命解析")
    b_date = st.date_input("輸入生日", datetime.date(1996, 2, 17))
    if st.button("🔥 解析"):
        gan, zhi = RedLotusCore.get_gan_zhi(b_date)
        color, direct, nums = RedLotusCore.get_lucky_info(gan)
        det = RedLotusCore.get_detailed_life_reading(gan)
        
        st.divider()
        st.markdown(f"### 🎯 命主：【{gan}{zhi}】日")
        c1, c2 = st.columns(2)
        c1.info(f"🎨 {color}")
        c2.success(f"🧭 {direct}")
        st.markdown("---")
        t1, t2, t3, t4, t5 = st.tabs(["🧠 性格", "❤️ 感情", "💼 事業", "💰 投資", "🏥 健康"])
        with t1: st.write(det['char'])
        with t2: st.write(det['love'])
        with t3: st.write(det['career'])
        with t4: st.write(det['invest'])
        with t5: st.write(det['health'])
        
        st.subheader("🗓️ 十年大運")
        for c in RedLotusCore.get_decade_luck(b_date): st.write(f"**{c['period']}**: {c['theme']}")

# ==============================================================================
# 6. 🐢 靈龜問事 (卜卦)
# ==============================================================================
elif menu == "🐢 靈龜問事 (卜卦)":
    st.title("🐢 靈龜問事")
    q = st.text_input("問題")
    if st.button("🔮") and q:
        res = RedLotusCore.turtle_divination(q)
        st.info(f"**{res[0]}** ({res[1]}): {res[2]}")
        if "吉" in res[0]: st.balloons()

# ==============================================================================
# 7. ⏳ 今日時空 (流日)
# ==============================================================================
elif menu == "⏳ 今日時空 (流日)":
    today = datetime.date.today()
    gan, zhi = RedLotusCore.get_gan_zhi(today)
    st.title(f"⏳ {today}")
    st.metric("干支", f"{gan}{zhi}日")
    el = RedLotusCore.ELEMENTS[gan]
    st.write(f"五行屬 **{el}**")
    if el == "火": st.success("🔥 火旺利 34")

st.markdown("---")
st.caption("Powered by Red Lotus System V11.0 | Inertia Correction")
