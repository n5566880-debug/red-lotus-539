import streamlit as st
import pandas as pd
import datetime
import random

# --- 1. 戰情室風格設定 ---
st.set_page_config(page_title="赤鍊天機・情場戰略室", layout="wide", page_icon="☯️")
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #E0E0E0; }
    .main-card { background: #111; padding: 25px; border-radius: 10px; border: 1px solid #D4AF37; margin-bottom: 20px; }
    .score-card { background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%); padding: 15px; border-radius: 10px; border-left: 5px solid #00FF00; text-align: center; }
    .love-card { background: #220022; padding: 15px; border-radius: 10px; border: 1px solid #FF69B4; margin-top: 10px; }
    .strategy-box { background: #002200; padding: 15px; border-radius: 5px; border-left: 3px solid #00FF00; margin-top: 10px; }
    .direction-card { background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%); padding: 15px; border-radius: 8px; border-left: 5px solid #FFD700; text-align: center; }
    .divination-box { background: #220022; padding: 20px; border-radius: 10px; border: 1px solid #9932CC; text-align: center; }
    .timeline-box { background: #1a1a1a; padding: 10px; border-left: 3px solid #D4AF37; margin-bottom: 5px; font-size: 14px; }
    .gold-text { color: #D4AF37; font-weight: bold; font-size: 22px; }
    .big-luck { font-size: 36px; font-weight: bold; color: #FFD700; }
    h3 { border-bottom: 1px solid #333; padding-bottom: 10px; margin-top: 25px; color: #fff; }
</style>
""", unsafe_allow_html=True)

st.title("☯️ 赤鍊紅蓮・情場戰略指揮部 (v3.4)")

# --- 2. 核心資料庫 ---
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DIRECTIONS = ["正北", "東北", "正東", "東南", "正南", "西南", "正西", "西北"]

# [深度解析字典]
DATA_DICT = {
    "甲": {
        "title": "參天巨木・大將軍",
        "personality": "【性格核心】：剛毅、正直、不輕易低頭。<br>您是天生的棟樑，不喜歡依附別人。外表嚴肅，內心仁慈。但缺點是「寧折不彎」，容易因為太過固執而錯失轉彎的機會。",
        "career": "【適合戰場】：企業管理、建築營造、軍警、政治領袖。<br>【戰術風格】：您適合打「陣地戰」。建立制度、帶領團隊，一步步擴張版圖，不適合投機取巧。",
        "wealth": "【財富戰略】：正財為主。您的財富來自於「資歷」與「實業」。不宜過度沉迷短線博弈，房地產或長線績優股是最佳金庫。",
        "health": "【弱點防禦】：頭部神經、膽囊、毛髮。壓力大時容易偏頭痛或脫髮。",
        "love_script": "霸道總裁式。您喜歡保護對方，但也希望對方絕對忠誠。吵架時絕不先低頭。",
        "cycle": ["25-34歲：紮根期，如大樹向下生長，辛苦但累積實力。", "35-44歲：破土期，事業開始嶄露頭角，掌握權力。", "45-54歲：成林期，建立自己的勢力範圍，財富大增。", "55-64歲：巨木期，成為行業權威，受人景仰。"]
    },
    "乙": {
        "title": "花草藤蔓・軍師",
        "personality": "【性格核心】：靈活、堅韌、適應力極強。<br>您不像甲木那樣硬碰硬，您懂得「借勢」。看似柔弱，其實生命力最強。您是談判高手，擅長以退為進。",
        "career": "【適合戰場】：行銷企劃、藝術設計、教育培訓、幕僚。<br>【戰術風格】：您適合打「游擊戰」。利用資訊落差與人脈賺錢，避免正面衝突。",
        "wealth": "【財富戰略】：偏財旺盛。您對市場敏銳，適合投資、合夥。但要小心耳根子軟，容易被朋友借錢不還。",
        "health": "【弱點防禦】：肝臟、頸椎、四肢神經。需注意筋骨痠痛與睡眠品質。",
        "love_script": "纏綿依賴式。您需要大量的安全感與陪伴。擅長用溫柔攻勢融化對方。",
        "cycle": ["25-34歲：探索期，嘗試多種可能性，累積人脈。", "35-44歲：攀附期，找到強力的合作夥伴(貴人)，借力使力。", "45-54歲：繁花期，名聲遠播，靠智慧與人脈賺錢。", "55-64歲：收穫期，桃李滿天下，享受人情紅利。"]
    },
    "丙": {
        "title": "太陽之火・先鋒官",
        "personality": "【性格核心】：熱情、急躁、光芒萬丈。<br>您心直口快，藏不住秘密。您是人群的焦點，充滿感染力。但容易三分鐘熱度，脾氣來得快去得也快。",
        "career": "【適合戰場】：演藝娛樂、媒體廣告、業務銷售、能源。<br>【戰術風格】：您適合打「閃電戰」。在短時間內衝高聲量或業績，不適合需要極度耐心的工作。",
        "wealth": "【財富戰略】：名氣生財。只要名聲越大，錢就越多。適合經營個人品牌。花錢大手大腳，需強迫儲蓄。",
        "health": "【弱點防禦】：心血管、血壓、小腸。激動時需注意血壓飆升。",
        "love_script": "烈火乾柴式。愛的時候轟轟烈烈，昭告天下。但若對方冷淡，您會瞬間熄火離開。",
        "cycle": ["25-34歲：燃燒期，精力最旺盛，容易年少成名。", "35-44歲：普照期，影響力擴大，開始帶領團隊。", "45-54歲：餘溫期，轉向傳承或教育，受人尊敬。", "55-64歲：夕陽期，地位崇高，享受榮譽。"]
    },
    "丁": {
        "title": "星燭之火・情報官",
        "personality": "【性格核心】：細膩、神祕、洞察力強。<br>外表溫和，內心火熱。您有很強的第六感，能注意到別人忽略的細節。善於謀略，是最好的幕後推手。",
        "career": "【適合戰場】：心理諮商、宗教命理、科技研發、分析師。<br>【戰術風格】：您適合打「精準打擊」。不打沒把握的仗，收集完情報才出手。",
        "wealth": "【財富戰略】：智慧生財。靠專利、技術、內線消息賺錢。適合投資波動大但具未來性的標的。",
        "health": "【弱點防禦】：心臟、眼睛、焦慮失眠。用腦過度容易神經衰弱。",
        "love_script": "悶騷深情式。暗戀時間長，一旦愛上就非常執著。在感情中比較敏感多疑。",
        "cycle": ["25-34歲：點燈期，在專業領域默默耕耘，累積口碑。", "35-44歲：燎原期，機會一到，實力瞬間爆發。", "45-54歲：光耀期，成為行業內的權威專家。", "55-64歲：傳燈期，培養接班人，退居幕後。"]
    },
    "戊": {
        "title": "崇山峻嶺・後勤統帥",
        "personality": "【性格核心】：穩重、守信、固執。<br>您像山一樣給人安全感。做事按部就班，不喜歡變動。包容力強，但一旦被踩到底線，爆發起來很恐怖。",
        "career": "【適合戰場】：房地產、金融保險、倉儲物流、農業。<br>【戰術風格】：您適合打「防禦戰」。先求不敗，再求勝。擅長守成與累積資產。",
        "wealth": "【財富戰略】：聚沙成塔。適合不動產投資、定存、儲蓄險。不適合高風險的虛擬貨幣。",
        "health": "【弱點防禦】：胃部、消化系統、背部肌肉。容易有胃食道逆流或發胖問題。",
        "love_script": "木訥忠誠式。不懂浪漫，但會把薪水上繳。用實際行動（買房、煮飯）表達愛意。",
        "cycle": ["25-34歲：堆土期，累積資產與信用，進度較慢。", "35-44歲：成山期，信譽變現，事業基礎穩固。", "45-54歲：鎮守期，坐享其成，以守代攻。", "55-64歲：不動期，資產豐厚，享受安穩退休。"]
    },
    "己": {
        "title": "田園之土・參謀長",
        "personality": "【性格核心】：內斂、多才多藝、心思深。<br>您比較隨和，善於協調人際關係。肚子裡有很多計畫，但不會輕易說出來。適應力比戊土強，懂得變通。",
        "career": "【適合戰場】：秘書行政、護理、教育、仲介顧問。<br>【戰術風格】：您適合打「滲透戰」。潤物細無聲，慢慢改變局勢，解決複雜的人際問題。",
        "wealth": "【財富戰略】：技能生財。靠多樣化的才藝或副業賺錢。適合分散風險的投資組合。",
        "health": "【弱點防禦】：脾臟、腹部、代謝系統。需注意飲食衛生與代謝症候群。",
        "love_script": "含蓄糾結式。容易陷入三角關係或暗戀。需要對方主動帶領。",
        "cycle": ["25-34歲：耕耘期，學習技能，培養耐心。", "35-44歲：收穫期，之前的佈局開始獲利，生活富足。", "45-54歲：養生期，注重生活品質，投資穩健。", "55-64歲：歸園期，享受家庭生活，含飴弄孫。"]
    },
    "庚": {
        "title": "刀劍之金・戰神",
        "personality": "【性格核心】：剛毅、果斷、好勝心強。<br>您講義氣，好打抱不平。像一把鋒利的劍，越挫越勇。說話直接，容易傷人而不自知。天生適合競爭。",
        "career": "【適合戰場】：軍警司法、外科醫生、鋼鐵重工、開拓業務。<br>【戰術風格】：您適合打「攻堅戰」。解決最棘手的問題，開拓新市場，殺伐果斷。",
        "wealth": "【財富戰略】：險中求財。敢於重押，適合波動大的市場。要小心大起大落。",
        "health": "【弱點防禦】：大腸、肺部、骨骼斷裂。容易有外傷或呼吸道過敏。",
        "love_script": "愛恨分明式。喜歡強者，不喜歡黏人。分手後絕不回頭。",
        "cycle": ["25-34歲：磨礪期，經歷挫折與挑戰，越磨越利。", "35-44歲：鋒芒期，事業達到巔峰，戰無不勝。", "45-54歲：收鞘期，轉向管理，傳授戰鬥經驗。", "55-64歲：鑄劍期，成為精神領袖，地位穩固。"]
    },
    "辛": {
        "title": "珠寶之金・特種兵",
        "personality": "【性格核心】：精緻、自尊心強、愛面子。<br>您思維敏捷，說話犀利。追求完美，對生活品質有高要求。外表光鮮，內心堅韌，比庚金更能忍受壓力。",
        "career": "【適合戰場】：金融證券、珠寶設計、法律、精密科技、醫美。<br>【戰術風格】：您適合打「特種作戰」。依靠高度專業與美感取勝，講究細節。",
        "wealth": "【財富戰略】：品牌生財。靠個人形象與專業度賺取高溢價。適合投資黃金、精品。",
        "health": "【弱點防禦】：肺部、牙齒、皮膚過敏。皮膚通常較白但也較敏感。",
        "love_script": "挑剔高冷式。重視對方的外表與品味。容易因小事而心裡過不去。",
        "cycle": ["25-34歲：雕琢期，修正缺點，提升自我價值。", "35-44歲：發光期，才華被看見，名利雙收。", "45-54歲：鑑賞期，享受成果，成為圈內名流。", "55-64歲：傳世期，留下經典作品或名聲。"]
    },
    "壬": {
        "title": "江河之水・海軍元帥",
        "personality": "【性格核心】：聰明、奔放、不受拘束。<br>您反應極快，像大江大河一樣流動。有大局觀，能容納各種觀點，但也容易流於善變，虎頭蛇尾。",
        "career": "【適合戰場】：國際貿易、物流運輸、旅遊、網際網路、大數據。<br>【戰術風格】：您適合打「流動戰」。在快速變化的環境中獲利，整合資源。",
        "wealth": "【財富戰略】：流動生財。錢要流動才會多，適合貿易、轉手賺價差。不適合把錢鎖死。",
        "health": "【弱點防禦】：腎臟、膀胱、泌尿系統。需注意水腫與生殖系統保養。",
        "love_script": "風流瀟灑式。異性緣極好，不喜歡被承諾束縛。像抓不住的風。",
        "cycle": ["25-34歲：奔流期，四處闖蕩，累積閱歷。", "35-44歲：匯聚期，資源整合，事業做大。", "45-54歲：入海期，格局宏大，掌握跨國或跨領域資源。", "55-64歲：調節期，掌控資源分配，呼風喚雨。"]
    },
    "癸": {
        "title": "雨露之水・滲透專家",
        "personality": "【性格核心】：溫柔、內向、心思極密。<br>您像水氣一樣無孔不入，耐力驚人。雖然不張揚，但往往是笑到最後的人。容易多愁善感，想太多。",
        "career": "【適合戰場】：心理諮詢、幕僚策劃、會計、化學、玄學。<br>【戰術風格】：您適合打「潛伏戰」。以柔克剛，等待最佳時機，用最小力氣擊倒對手。",
        "wealth": "【財富戰略】：積少成多。精打細算，每一分錢都花在刀口上。適合穩健型基金。",
        "health": "【弱點防禦】：腎臟、足部冷、血液循環。容易手腳冰冷或內分泌失調。",
        "love_script": "靈魂伴侶式。渴望精神契合，情感豐富細膩。容易陷入單戀。",
        "cycle": ["25-34歲：滲透期，在基層累積人脈，不顯山露水。", "35-44歲：滋潤期，成為團隊不可或缺的核心。", "45-54歲：昇華期，靠智慧與資歷獲得地位。", "55-64歲：雲雨期，德高望重，潤澤後輩。"]
    }
}

# [時空決策算法]
def get_current_taiwan_time():
    utc_now = datetime.datetime.utcnow()
    taiwan_time = utc_now + datetime.timedelta(hours=8)
    return taiwan_time

def get_lucky_direction(hour, day):
    random.seed(hour + day) 
    lucky_dir = random.choice(DIRECTIONS)
    wealth_dir = random.choice(DIRECTIONS)
    return lucky_dir, wealth_dir

def divine_outcome(question):
    if not question: return None, None, None
    seed_val = len(question) + datetime.datetime.now().minute
    random.seed(seed_val)
    outcomes = ["大吉 (進攻)", "小吉 (穩健)", "平 (觀望)", "小凶 (防守)", "大凶 (撤退)"]
    details = [
        "青龍返首，大舉進攻。鎖定的目標極高機率出現。",
        "玉女守門，利於陰柔。適合小額投資或防守型號碼。",
        "伏吟之局，動不如靜。建議維持原定策略，不宜臨時變卦。",
        "白虎猖狂，恐有損失。今日宜避開熱門，專攻冷門。",
        "天網四張，不可妄動。今日氣場混亂，建議休息或極小額。"
    ]
    idx = random.randint(0, 4)
    return outcomes[idx], details[idx], idx

# --- 3. 側邊欄導航 ---
st.sidebar.title("🛡️ 戰略功能模組")
mode = st.sidebar.radio("請選擇戰略層級", ["🕰️ 今日時空戰略 (出征)", "👤 深層本命解析 (戰略藍圖)", "💞 情場戰略指揮部 (合盤)"])

# --- 4. 模組一：今日時空戰略 ---
if mode == "🕰️ 今日時空戰略 (出征)":
    st.markdown("### 🕰️ 今日出征指南 (Daily Strategy)")
    now = get_current_taiwan_time()
    luck, wealth = get_lucky_direction(now.hour, now.day)
    date_str = now.strftime('%Y-%m-%d')
    nongli = "丁亥日 (火弱/水旺)" if now.day == 8 else "丙戌火庫日" 
    
    c1, c2, c3 = st.columns(3)
    c1.info(f"📅 日期：{date_str}"); c2.info(f"⏰ 時間：{now.strftime('%H:%M')}"); c3.warning(f"🔥 狀態：{nongli}")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    col1.markdown(f"""<div class="direction-card"><h3>💰 今日財神方位</h3><div class="big-luck">{wealth}方</div><p>建議：請前往住家或公司 <b>{wealth}方</b> 的彩券行下注。</p></div>""", unsafe_allow_html=True)
    col2.markdown(f"""<div class="direction-card" style="border-left-color: #D4AF37;"><h3>✨ 貴人/吉氣方位</h3><div class="big-luck">{luck}方</div><p>戰術：若與人合資或討論號碼，面朝 <b>{luck}方</b> 座位最佳。</p></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🔮 靈龜決策占卜系統")
    q = st.text_input("戰略疑問：", placeholder="例如：今晚 25 號是否會開出？")
    if st.button("🐢 啟動靈龜占卜"):
        if q:
            o, d, i = divine_outcome(q)
            color = "#00FF00" if i <= 1 else ("#FF4B4B" if i >= 3 else "#FFFF00")
            st.markdown(f"""<div class="divination-box" style="border-color: {color};"><h3 style="color:#E0E0E0;">問：{q}</h3><h1 style="color:{color};">{o}</h1><p style="font-size:18px;margin-top:15px;">{d}</p></div>""", unsafe_allow_html=True)
            if i <= 1: st.balloons()
        else: st.warning("請先輸入問題。")

# --- 5. 模組二：深層本命解析 ---
elif mode == "👤 深層本命解析 (戰略藍圖)":
    st.markdown("### 👤 掌門人・五維戰略藍圖")
    col1, col2 = st.columns(2)
    with col1:
        birth_date = st.date_input("生辰", datetime.date(1996, 1, 1))
    with col2:
        birth_month = st.selectbox("出生月份", range(1, 13))

    if st.button("🚀 啟動深度掃描"):
        day_gan = TIAN_GAN[birth_date.day % 10]
        d = DATA_DICT[day_gan]
        
        energy_level = 50
        if day_gan in ['甲','乙'] and birth_month in [1,2,3]: energy_level = 85
        elif day_gan in ['丙','丁'] and birth_month in [4,5,6]: energy_level = 90
        elif day_gan in ['庚','辛'] and birth_month in [7,8,9]: energy_level = 85
        elif day_gan in ['壬','癸'] and birth_month in [10,11,12]: energy_level = 90
        else: energy_level = 40
        
        energy_desc = "身強 (適合開拓/主導)" if energy_level >= 70 else "身弱 (適合策略/合夥)"
        
        st.markdown(f"""
        <div class="main-card">
            <h2 class="gold-text">🗡️ 命主代號：{day_gan} ({d['title']})</h2>
            <div style='background:#333; height:10px; border-radius:5px; margin-top:10px;'>
                <div style='background:#00FF00; width:{energy_level}%; height:100%; border-radius:5px;'></div>
            </div>
            <p>能量指數：{energy_level}/100 | 判定：<b>{energy_desc}</b></p>
            <hr style="border-top: 1px solid #333;">
            <h3>🧠 性格深層掃描</h3>{d['personality']}
            <h3>⚔️ 事業與戰場</h3>{d['career']}
            <h3>💰 財富戰略</h3>{d['wealth']}
            <h3>🏥 健康罩門</h3>{d['health']}
            <h3>💘 感情劇本</h3>{d['love_script']}
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("📅 十年大限運勢")
        for cycle in d['cycle']:
            st.markdown(f"""<div class="timeline-box">{cycle}</div>""", unsafe_allow_html=True)

# --- 6. 模組三：情場戰略指揮部 (全面升級) ---
elif mode == "💞 情場戰略指揮部 (合盤)":
    st.markdown("### 💞 戰友/伴侶/復合 綜合戰略盤")
    c1, c2 = st.columns(2)
    with c1:
        st.info("👤 您的資料")
        d1 = st.date_input("您的生日", datetime.date(1996, 1, 1))
    with c2:
        st.info("👥 對方資料")
        d2 = st.date_input("對方生日", datetime.date(2001, 1, 1))
        
    if st.button("💘 啟動戰略推演"):
        g1 = TIAN_GAN[d1.day % 10]
        g2 = TIAN_GAN[d2.day % 10]
        
        # 簡易五行關係
        els = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土", "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"}
        e1, e2 = els[g1], els[g2]
        
        # 初始化變數
        date_score = 60 # 交往指數
        back_score = 40 # 復合指數
        relation_type = "普通"
        strategy = [] # 錦囊
        
        # 邏輯核心
        if e1 == e2: 
            date_score, back_score = 70, 50
            relation_type = "戰友 (比肩)"
            strategy = [
                "✅ **共同目標**：你們像朋友一樣，需要一起做某件事（創業、旅遊）才能維持熱度。",
                "❌ **忌諱硬碰硬**：吵架時兩人都很硬，復合難度高，除非一方先給台階。",
                "💡 **復合關鍵**：不要談感情，改談「合作」或「幫忙」，藉口接近。"
            ]
        elif (e1=="木" and e2=="火") or (e1=="火" and e2=="土") or (e1=="土" and e2=="金") or (e1=="金" and e2=="水") or (e1=="水" and e2=="木"):
            date_score, back_score = 85, 60
            relation_type = "付出 (我生)"
            strategy = [
                "✅ **寵愛攻勢**：您是付出方，對方很吃您這一套。多讚美、多送禮。",
                "❌ **忌諱計較**：不要計較誰付出的多，一旦計較，關係就崩塌。",
                "💡 **復合關鍵**：對方其實很依賴您的好。只要您展現出「我還是在等你」，對方容易心軟。"
            ]
        elif (e2=="木" and e1=="火") or (e2=="火" and e1=="土") or (e2=="土" and e1=="金") or (e2=="金" and e1=="水") or (e2=="水" and e1=="木"):
            date_score, back_score = 95, 90
            relation_type = "貴人 (生我)"
            strategy = [
                "✅ **示弱撒嬌**：對方天生想照顧您。您越示弱，對方越愛您。",
                "❌ **忌諱逞強**：不要拒絕對方的好意，讓對方覺得被需要。",
                "💡 **復合關鍵**：這段關係復合率最高！只要您肯低頭認錯，對方通常會原諒。"
            ]
        elif (e1=="木" and e2=="土") or (e1=="火" and e2=="金") or (e1=="土" and e2=="水") or (e1=="金" and e2=="木") or (e1=="水" and e2=="火"):
            date_score, back_score = 80, 55
            relation_type = "征服 (我剋)"
            strategy = [
                "✅ **霸道主導**：您要展現強勢與自信，對方會因崇拜而跟隨。",
                "❌ **忌諱猶豫**：如果您優柔寡斷，對方會看不起您。",
                "💡 **復合關鍵**：必須展現出「我變得更好了」的高價值，重新吸引對方。"
            ]
        else:
            date_score, back_score = 60, 30
            relation_type = "磨練 (剋我)"
            strategy = [
                "✅ **尊重崇拜**：對方氣場強，喜歡被尊重。凡事多請教對方意見。",
                "❌ **忌諱控制**：千萬別想控制對方，您控制不了的。",
                "💡 **復合關鍵**：難度高。除非對方主動回頭，否則您的追求會變成壓力。"
            ]

        st.markdown("---")
        st.subheader(f"📋 戰略總評：{g1} (您) ⚔️ {g2} (對方) —— 【{relation_type}】")
        
        c_a, c_b = st.columns(2)
        with c_a:
            st.markdown(f"""
            <div class="score-card" style="border-color:{'#FF69B4' if date_score>=80 else '#aaa'}">
                <h3>💘 交往/追求指數</h3>
                <h1 style="margin:0; font-size:42px;">{date_score}%</h1>
                <p>進攻建議：{'大膽出擊' if date_score>=80 else '步步為營'}</p>
            </div>
            """, unsafe_allow_html=True)
        with c_b:
            st.markdown(f"""
            <div class="score-card" style="border-color:{'#00FF00' if back_score>=80 else '#FF4B4B'}">
                <h3>🔄 復合/挽回指數</h3>
                <h1 style="margin:0; font-size:42px;">{back_score}%</h1>
                <p>難度評估：{'容易心軟' if back_score>=80 else ('需要長期抗戰' if back_score>=50 else '建議放下')}</p>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("### 📖 統帥錦囊：相處與攻略")
        for s in strategy:
            st.markdown(f"""<div class="strategy-box" style="border-left-color: #D4AF37;">{s}</div>""", unsafe_allow_html=True)

# --- 頁尾 ---
st.markdown("---")
st.caption("🛡️ 赤鍊天機閣 v3.4 | 情場戰略指揮部")
