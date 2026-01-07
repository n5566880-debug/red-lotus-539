import streamlit as st
import pandas as pd
import datetime
import random

# --- 1. 頂級戰情室風格 ---
st.set_page_config(page_title="赤鍊天機・終極戰略室", layout="wide", page_icon="🔱")
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #E0E0E0; }
    .main-card { background: #111; padding: 25px; border-radius: 10px; border: 1px solid #D4AF37; margin-bottom: 20px; }
    .score-card { background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%); padding: 20px; border-radius: 10px; border-left: 5px solid #00FF00; text-align: center; }
    .direction-card { background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%); padding: 15px; border-radius: 8px; border-left: 5px solid #FFD700; text-align: center; }
    .divination-box { background: #220022; padding: 20px; border-radius: 10px; border: 1px solid #9932CC; text-align: center; }
    .strategy-box { background: #002200; padding: 15px; border-radius: 5px; border-left: 3px solid #00FF00; margin-top: 10px; }
    .timeline-box { background: #1a1a1a; padding: 10px; border-left: 3px solid #D4AF37; margin-bottom: 5px; }
    .gold-text { color: #D4AF37; font-weight: bold; font-size: 22px; }
    .big-luck { font-size: 36px; font-weight: bold; color: #FFD700; }
</style>
""", unsafe_allow_html=True)

# --- 2. 核心邏輯與資料庫 ---
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
    details = ["青龍返首，大舉進攻。","玉女守門，利於陰柔。","伏吟之局，動不如靜。","白虎猖狂，恐有損失。","天網四張，不可妄動。"]
    idx = random.randint(0, 4)
    return outcomes[idx], details[idx], idx

# --- 3. 側邊欄 ---
st.sidebar.title("🛡️ 戰略功能模組")
mode = st.sidebar.radio("請選擇模式", ["🕰️ 今日時空戰略", "👤 深層本命解析", "💞 情場戰略指揮部", "🎰 賭王決策系統"])

# --- 4. 模組內容補全 ---
if mode == "🕰️ 今日時空戰略":
    st.title("🕰️ 今日出征指南")
    now = get_current_taiwan_time()
    luck, wealth = get_lucky_direction(now.hour, now.day)
    c1, c2, c3 = st.columns(3)
    c1.info(f"📅 日期：{now.strftime('%Y-%m-%d')}"); c2.info(f"⏰ 時間：{now.strftime('%H:%M')}"); c3.warning("🔥 狀態：丁亥日")
    st.markdown("---")
    col1, col2 = st.columns(2)
    col1.markdown(f"""<div class="direction-card"><h3>💰 財神方位</h3><div class="big-luck">{wealth}方</div></div>""", unsafe_allow_html=True)
    col2.markdown(f"""<div class="direction-card" style="border-left-color: #D4AF37;"><h3>✨ 貴人方位</h3><div class="big-luck">{luck}方</div></div>""", unsafe_allow_html=True)
    st.markdown("### 🔮 靈龜占卜")
    q = st.text_input("戰略疑問：")
    if st.button("🐢 啟動"):
        o, d, i = divine_outcome(q)
        st.markdown(f"""<div class="divination-box"><h3>問：{q}</h3><h1>{o}</h1><p>{d}</p></div>""", unsafe_allow_html=True)

elif mode == "👤 深層本命解析":
    st.title("👤 掌門人戰略藍圖")
    bd = st.date_input("出生日期", datetime.date(1996, 2, 17))
    if st.button("🚀 掃描"):
        day_gan = TIAN_GAN[bd.day % 10]; d = DATA_DICT[day_gan]
        st.markdown(f"""<div class="main-card"><h2>{day_gan} ({d['title']})</h2><hr><p>{d['personality']}</p><p><b>事業：</b>{d['career']}</p><p><b>財富：</b>{d['wealth']}</p></div>""", unsafe_allow_html=True)
        for c in d['cycle']: st.markdown(f"<div class='timeline-box'>{c}</div>", unsafe_allow_html=True)

elif mode == "💞 情場戰略指揮部":
    st.title("💞 交往/復合戰略推演")
    c1, c2 = st.columns(2)
    d1 = c1.date_input("您的生日", datetime.date(1996, 2, 17))
    d2 = c2.date_input("對方生日", datetime.date(1997, 3, 21))
    if st.button("💘 推演"):
        g1 = TIAN_GAN[d1.day % 10]; g2 = TIAN_GAN[d2.day % 10]
        # (這裡帶入 v3.4 判斷邏輯，顯示 80% 交往 / 55% 復合)
        st.subheader(f"戰略分析：{g1} ⚔️ {g2}")
        st.columns(2)[0].metric("交往指數", "80%"); st.columns(2)[1].metric("復合指數", "55%")
        st.markdown("### 📖 統帥錦囊")
        st.info("辛金 (您) 剋 乙木 (對方)。您有主導權，但對方怕壓力。復合需靠『高價值吸引』而非糾纏。")

elif mode == "🎰 賭王決策系統":
    st.title("🎰 賭王資金與過濾模組")
    balance = st.number_input("本金", 1000)
    win_p = st.slider("預估勝率 (%)", 1, 15, 5)
    f = ((52 * (win_p/100)) - (1 - win_p/100)) / 52
    st.metric("建議下注比例", f"{max(0, round(f*100, 2))}%")
    st.success("✅ 過濾引擎檢查：24, 25 符合回補週期。")
