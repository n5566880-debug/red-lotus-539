import streamlit as st
import pandas as pd
import numpy as np
import datetime
import random
from lunar_python import Lunar, Solar  # 引入八字核心庫

# --- 1. 帝國指揮部風格 ---
st.set_page_config(page_title="赤鍊天機・完美復刻版", layout="wide", page_icon="🔱")
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
    .timeline-box { background: #1a1a1a; padding: 10px; border-left: 3px solid #D4AF37; margin-bottom: 5px; font-size: 14px; }
    .human-card { background: #0c141c; padding: 20px; border-radius: 8px; border: 1px solid #3498db; margin-bottom: 15px; }
    .gold-text { color: #D4AF37; font-weight: bold; font-size: 22px; }
    .big-luck { font-size: 36px; font-weight: bold; color: #FFD700; }
    h3 { border-bottom: 1px solid #333; padding-bottom: 10px; margin-top: 25px; color: #fff; }
</style>
""", unsafe_allow_html=True)

# --- 2. 核心資料庫 & 工具函數 ---
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DIRECTIONS = ["正北", "東北", "正東", "東南", "正南", "西南", "正西", "西北"]

# 舊版靜態資料庫 (保留用於快速查詢)
DATA_DICT = {
    "甲": {"title": "參天巨木・大將軍", "personality": "剛毅、正直、不輕易低頭。", "career": "管理、建築、領袖。", "wealth": "正財為主，資歷生財。", "health": "頭部、膽囊。", "love_script": "霸道總裁式。", "cycle": ["25-34歲：紮根期", "35-44歲：破土期"]},
    "乙": {"title": "花草藤蔓・軍師", "personality": "靈活、堅韌、善於借勢。", "career": "行銷、設計、幕僚。", "wealth": "偏財旺，靠人脈賺錢。", "health": "肝臟、頸椎。", "love_script": "纏綿依賴式。", "cycle": ["25-34歲：探索期", "35-44歲：攀附期"]},
    "丙": {"title": "太陽之火・先鋒官", "personality": "熱情、急躁、光芒萬丈。", "career": "演藝、業務、能源。", "wealth": "名氣生財。", "health": "心血管、血壓。", "love_script": "烈火乾柴式。", "cycle": ["25-34歲：燃燒期", "35-44歲：普照期"]},
    "丁": {"title": "星燭之火・情報官", "personality": "細膩、神祕、洞察力強。", "career": "諮商、命理、研發。", "wealth": "智慧生財，專利技術。", "health": "心臟、眼睛。", "love_script": "悶騷深情式。", "cycle": ["25-34歲：點燈期", "35-44歲：燎原期"]},
    "戊": {"title": "崇山峻嶺・後勤統帥", "personality": "穩重、守信、固執。", "career": "房產、金融、倉儲。", "wealth": "聚沙成塔，不動產。", "health": "胃部、背肌。", "love_script": "木訥忠誠式。", "cycle": ["25-34歲：堆土期", "35-44歲：成山期"]},
    "己": {"title": "田園之土・參謀長", "personality": "內斂、多才、心思深。", "career": "秘書、護理、教育。", "wealth": "技能生財，副業。", "health": "脾臟、代謝。", "love_script": "含蓄糾結式。", "cycle": ["25-34歲：耕耘期", "35-44歲：收穫期"]},
    "庚": {"title": "刀劍之金・戰神", "personality": "剛毅、果斷、好勝。", "career": "軍警、外科、重工。", "wealth": "險中求財。", "health": "大腸、骨骼。", "love_script": "愛恨分明式。", "cycle": ["25-34歲：磨礪期", "35-44歲：鋒芒期"]},
    "辛": {"title": "珠寶之金・特種兵", "personality": "精緻、愛面子、口才好。", "career": "金融、珠寶、法律。", "wealth": "品牌生財，高溢價。", "health": "肺部、皮膚。", "love_script": "挑剔高冷式。", "cycle": ["25-34歲：雕琢期", "35-44歲：發光期"]},
    "壬": {"title": "江河之水・海軍元帥", "personality": "聰明、奔放、善變。", "career": "貿易、物流、網路。", "wealth": "流動生財，賺價差。", "health": "腎臟、膀胱。", "love_script": "風流瀟灑式。", "cycle": ["25-34歲：奔流期", "35-44歲：匯聚期"]},
    "癸": {"title": "雨露之水・滲透專家", "personality": "溫柔、內向、耐力強。", "career": "心理、會計、玄學。", "wealth": "積少成多。", "health": "腎臟、足冷。", "love_script": "靈魂伴侶式。", "cycle": ["25-34歲：滲透期", "35-44歲：滋潤期"]}
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

# --- 新增：人心判斷邏輯 (Lunar Python) ---
def get_human_profile(birth_date, mode):
    solar = Solar.fromYmd(birth_date.year, birth_date.month, birth_date.day)
    lunar = solar.getLunar()
    ba_zi = lunar.getEightChar()
    day_master = ba_zi.getDayGan()  # 日干
    day_master_wuxing = ba_zi.getDayWuXing() # 五行
    
    # 動態生成分析內容
    base_trait = DATA_DICT.get(day_master, {}).get('personality', '數據不足')
    
    analysis = ""
    strategy = ""
    
    if mode == "交友/看透人心":
        analysis = f"🌀 **本性掃描**：此人日主為【{day_master}{day_master_wuxing}】。<br>底層邏輯：{base_trait}"
        if day_master_wuxing == "火":
            analysis += "<br>💡 **相處重點**：他們要的是「認同感」與「舞台」。不可當眾給他難堪，誇他就對了。"
        elif day_master_wuxing == "木":
            analysis += "<br>💡 **相處重點**：他們吃軟不吃硬。展現你的上進心，他們會把你當自己人。"
        elif day_master_wuxing == "土":
            analysis += "<br>💡 **相處重點**：誠信第一。不要耍小聰明，他們反應雖慢但心裡有數。"
        elif day_master_wuxing == "金":
            analysis += "<br>💡 **相處重點**：講義氣、乾脆俐落。不要拖泥帶水，直接說重點。"
        elif day_master_wuxing == "水":
            analysis += "<br>💡 **相處重點**：給予空間。他們討厭被束縛，你要比他更有趣才能吸引他。"
        
        strategy = "【紅蓮交友指令】：觀察對方的眼神。若閃爍不定（水），則多聽少說；若直視不避（火/金），則強勢主導話題。"

    elif mode == "面試/識人用人":
        analysis = f"🛡️ **職能掃描** (日主：{day_master}{day_master_wuxing})：<br>"
        if day_master_wuxing in ["木", "火"]:
            analysis += "✅ **適合位置**：前鋒、業務、開拓者、公關。<br>⚠️ **風險係數**：高。容易因為情緒波動而影響決策，需配備冷靜的副手。"
        elif day_master_wuxing in ["金", "水"]:
            analysis += "✅ **適合位置**：財務、策略、研發、技術核心。<br>⚠️ **風險係數**：中。心思較深，需定期確認忠誠度，避免帶走資源。"
        else: # 土
            analysis += "✅ **適合位置**：行政、倉管、後勤、守成者。<br>⚠️ **風險係數**：低。但缺乏變通，不適合處理突發危機。"
            
        strategy = f"【紅蓮用人指令】：若今日為您的「貴人日」，此人可用；若相沖，則建議僅作短期專案配合。"

    return {
        "day_master": f"{day_master}{day_master_wuxing}",
        "zodiac": lunar.getAnimal(),
        "constellation": solar.getXingZuo(),
        "text": analysis,
        "strategy": strategy,
        "lunar_date": lunar.toString()
    }

# --- 3. 戰略導航 ---
st.sidebar.title("🛡️ 戰略功能模組")
mode = st.sidebar.radio("請選擇戰略層級", [
    "🎰 賭王決策系統 (核心)", 
    "📈 財務戰績覆盤",
    "📡 予婕情緒雷達",
    "📊 號碼技術分析",
    "🕰️ 今日時空戰略", 
    "👤 深層本命解析", 
    "💞 情場戰略指揮部",
    "👁️ 人心判斷系統 (詳細版)"  # 新增選項
])

# ==========================================================
# 模組 1: 🎰 賭王決策系統 (核心)
# ==========================================================
if mode == "🎰 賭王決策系統 (核心)":
    st.markdown("## 🎰 專業資金控管・戰術終端")
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
    if suggest_units == 0: st.warning("⚠️ 警告：風險過高，建議觀望或僅下 1 注。")
    else: st.success(f"✅ 指令：請執行 **{suggest_units} 注** (共 ${suggest_units * cost_per_bet})，目標鎖定 **{target_nums}**。")

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
    
    st.markdown(f"""
    <div class="radar-box">
        <h3 style="color:#FF00FF;">👩🏻 對象：予婕 (乙木坐午)</h3>
        <p>📅 監測日期：{now.strftime('%Y-%m-%d')} (自動運算中...)</p>
        <p>🌌 氣場干支：<b>戊子日</b> (土水相剋，子午相沖)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🌪️ 心情深度解析")
    c1, c2 = st.columns(2)
    with c1:
        st.info("📊 **情緒指數：65 (敏感波動期)**")
        st.write("明日『子水』強勢沖擊她的『午火』。午火代表她的面子與急躁，子水代表深沉的思考與不安。")
        st.write("這意味著：**她明天內心戲很多，容易對未來感到迷惘，甚至突然發脾氣掩飾不安。**")
        
    with c2:
        st.warning("⚠️ **相處紅燈區 (禁忌)**")
        st.write("❌ **忌講道理**：她的『火』被水澆熄，講邏輯她聽不進去。")
        st.write("❌ **忌太強勢**：不要在這個時候展現您的控制欲，她會覺得壓力山大而逃避。")
        
    st.markdown("### 💡 統帥攻略錦囊")
    st.markdown("""
    <div class="strategy-box">
        <b>✅ 戰術：溫柔的黃金港灣 (Water Strategy)</b><br>
        1. <b>投食戰術</b>：子午沖最怕餓，帶她去吃好吃的，或點外送給她。<br>
        2. <b>傾聽不語</b>：如果她抱怨，您只要點頭說「我也覺得是這樣」，千萬別給解決方案。<br>
        3. <b>穩定輸出</b>：讓她看到您情緒很穩，她會像在海上抓到浮木一樣依賴您。
    </div>
    """, unsafe_allow_html=True)

# ==========================================================
# 模組 4: 📊 號碼技術分析
# ==========================================================
elif mode == "📊 號碼技術分析":
    st.markdown("## 📊 分析師・號碼趨勢 K 線")
    target_nums_input = st.text_input("輸入欲分析號碼 (如: 05, 10, 14)", "24, 25")
    st.markdown(f"### 🎯 目標號碼：{target_nums_input} (連動分析)")
    col_k1, col_k2, col_k3 = st.columns(3)
    col_k1.metric("RSI 指標", "15 (超賣)", "觸底反彈")
    col_k2.metric("MACD 能量", "-0.85", "空方衰竭")
    col_k3.metric("遺漏期數", "8 期", "黃金回補")
    st.markdown("#### 📈 能量累積模擬圖")
    nums_list = target_nums_input.replace("，", ",").split(",")
    chart_data = pd.DataFrame(np.random.randn(20, len(nums_list)), columns=[f"{n.strip()}號能量" for n in nums_list])
    st.line_chart(chart_data)
    st.success(f"✅ **技術結論**：號碼組合 **[{target_nums_input}]** 出現技術面買點。")

# ==========================================================
# 模組 5: 🕰️ 今日時空戰略
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

# ==========================================================
# 模組 6: 👤 深層本命解析 (舊版)
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
            <h3>🧠 性格深層掃描</h3>{d['personality']}
            <h3>⚔️ 事業與戰場</h3>{d['career']}
            <h3>💰 財富戰略</h3>{d['wealth']}
            <h3>🏥 健康罩門</h3>{d['health']}
            <h3>💘 感情劇本</h3>{d['love_script']}
        </div>
        """, unsafe_allow_html=True)
        st.subheader("📅 十年大限運勢")
        for c in d['cycle']:
            st.markdown(f"<div class='timeline-box'>{c}</div>", unsafe_allow_html=True)

# ==========================================================
# 模組 7: 💞 情場戰略指揮部
# ==========================================================
elif mode == "💞 情場戰略指揮部":
    st.title("💞 交往/復合戰略推演")
    c1, c2 = st.columns(2)
    d1 = c1.date_input("您的生日", datetime.date(1996, 2, 17))
    d2 = c2.date_input("對方生日", datetime.date(1997, 3, 21))
    
    if st.button("💘 推演"):
        g1 = TIAN_GAN[d1.day % 10]
        g2 = TIAN_GAN[d2.day % 10]
        els = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土", "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"}
        e1, e2 = els[g1], els[g2]
        
        strategy = []
        date_s, back_s = 50, 50
        rel_type = "普通"
        
        if e1 == e2: 
            date_s, back_s, rel_type = 70, 50, "戰友 (比肩)"
            strategy = ["✅ **共同目標**：一起做事才能維持熱度。", "❌ **忌硬碰硬**：吵架時誰也不讓誰。", "💡 **復合關鍵**：談「合作」不談感情。"]
        elif (e1=="金" and e2=="木") or (e1=="木" and e2=="土") or (e1=="土" and e2=="水") or (e1=="水" and e2=="火") or (e1=="火" and e2=="金"):
             date_s, back_s, rel_type = 80, 55, "征服 (我剋)"
             strategy = ["✅ **霸道主導**：您要展現強勢與自信，對方會因崇拜而跟隨。", "❌ **忌諱猶豫**：如果您優柔寡斷，對方會看不起您。", "💡 **復合關鍵**：必須展現出「我變得更好了」的高價值，重新吸引對方。"]
        elif (e2=="金" and e1=="木") or (e2=="木" and e1=="土") or (e2=="土" and e1=="水") or (e2=="水" and e1=="火") or (e2=="火" and e1=="金"):
            date_s, back_s, rel_type = 60, 30, "磨練 (剋我)"
            strategy = ["✅ **尊重崇拜**：凡事多請教對方意見。", "❌ **忌諱控制**：別想控制對方。", "💡 **復合關鍵**：難度高，需對方主動。"]
        else:
            date_s, back_s, rel_type = 90, 85, "貴人/付出"
            strategy = ["✅ **溫柔攻勢**：多讚美、多送禮。", "❌ **忌諱計較**：不要計較回報。", "💡 **復合關鍵**：對方容易心軟，低頭就贏。"]
        
        st.subheader(f"戰略分析：{g1} ⚔️ {g2} —— 【{rel_type}】")
        col_res = st.columns(2)
        col_res[0].metric("💘 交往指數", f"{date_s}%", "進攻有利")
        col_res[1].metric("🔄 復合指數", f"{back_s}%", "需長期抗戰", delta_color="inverse")
        
        st.markdown("### 📖 統帥錦囊：相處與攻略")
        for s in strategy:
            st.markdown(f"""<div class="strategy-box">{s}</div>""", unsafe_allow_html=True)

# ==========================================================
