import random

# --- 1. 帝國指揮部風格 ---
st.set_page_config(page_title="赤鍊天機・動態狙擊版", layout="wide", page_icon="🔱")
st.set_page_config(page_title="赤鍊天機・完美復刻版", layout="wide", page_icon="🔱")
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #E0E0E0; }
@@ -17,26 +17,108 @@
    .radar-box { background: #110011; padding: 15px; border-radius: 10px; border: 1px solid #FF00FF; margin-top: 10px; box-shadow: 0 0 10px rgba(255, 0, 255, 0.2); }
    .strategy-box { background: #002200; padding: 15px; border-radius: 5px; border-left: 3px solid #00FF00; margin-top: 10px; }
    .divination-box { background: #220022; padding: 20px; border-radius: 10px; border: 1px solid #9932CC; text-align: center; }
    .timeline-box { background: #1a1a1a; padding: 10px; border-left: 3px solid #D4AF37; margin-bottom: 5px; font-size: 14px; }
    .gold-text { color: #D4AF37; font-weight: bold; font-size: 22px; }
    .big-luck { font-size: 36px; font-weight: bold; color: #FFD700; }
    h3 { border-bottom: 1px solid #333; padding-bottom: 10px; margin-top: 25px; color: #fff; }
</style>
""", unsafe_allow_html=True)

# --- 2. 核心資料庫 (不變) ---
# --- 2. 核心資料庫 (已恢復為詳細版) ---
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DIRECTIONS = ["正北", "東北", "正東", "東南", "正南", "西南", "正西", "西北"]

DATA_DICT = {
    "甲": {"title": "參天巨木", "personality": "剛毅正直", "career": "管理、軍警", "wealth": "正財實業", "health": "膽囊、頭部", "cycle": ["25-34歲:紮根", "35-44歲:破土", "45-54歲:成林"]},
    "乙": {"title": "花草藤蔓", "personality": "靈活堅韌", "career": "行銷、策劃", "wealth": "偏財人脈", "health": "肝臟、四肢", "cycle": ["25-34歲:探索", "35-44歲:攀附", "45-54歲:繁花"]},
    "丙": {"title": "太陽之火", "personality": "熱情急躁", "career": "演藝、業務", "wealth": "名氣生財", "health": "心血管", "cycle": ["25-34歲:燃燒", "35-44歲:普照", "45-54歲:餘溫"]},
    "丁": {"title": "星燭之火", "personality": "細膩神祕", "career": "心理、研發", "wealth": "智慧專利", "health": "心臟、眼", "cycle": ["25-34歲:點燈", "35-44歲:燎原", "45-54歲:光耀"]},
    "戊": {"title": "崇山峻嶺", "personality": "穩重固執", "career": "房產、倉儲", "wealth": "積土成山", "health": "胃、消化", "cycle": ["25-34歲:堆土", "35-44歲:成山", "45-54歲:鎮守"]},
    "己": {"title": "田園之土", "personality": "內斂多藝", "career": "教育、秘書", "wealth": "技能副業", "health": "脾、代謝", "cycle": ["25-34歲:耕耘", "35-44歲:收穫", "45-54歲:養生"]},
    "庚": {"title": "刀劍之金", "personality": "果斷義氣", "career": "司法、外科", "wealth": "險中求財", "health": "肺、大腸", "cycle": ["25-34歲:磨礪", "35-44歲:鋒芒", "45-54歲:收鞘"]},
    "辛": {"title": "珠寶之金", "personality": "精緻愛面子", "career": "金融、醫美", "wealth": "品牌溢價", "health": "肺、皮膚", "cycle": ["25-34歲:雕琢", "35-44歲:發光", "45-54歲:鑑賞"]},
    "壬": {"title": "江河之水", "personality": "聰明奔放", "career": "貿易、物流", "wealth": "流動價差", "health": "腎、膀胱", "cycle": ["25-34歲:奔流", "35-44歲:匯聚", "45-54歲:入海"]},
    "癸": {"title": "雨露之水", "personality": "溫柔縝密", "career": "會計、幕僚", "wealth": "積少成多", "health": "腎、內分泌", "cycle": ["25-34歲:滲透", "35-44歲:滋潤", "45-54歲:昇華"]}
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
        "health": "【弱點防禦】：肺部、皮膚、牙齒。皮膚通常較白但也較敏感。",
        "love_script": "挑剔高冷式。重視對方的外表與品味。容易因小事而心裡過不去。",
        "cycle": ["25-34歲：雕琢期，修正缺點，提升自我價值。", "35-44歲：發光期，才華被看見，名利雙收。", "45-54歲：鑑賞期，享受成果，成為圈內名流。", "55-64歲：傳世期，留下經典作品或名聲。"]
    },
    "壬": {
        "title": "江河之水・海軍元帥",
        "personality": "【性格核心】：聰明、奔放、不受拘束。<br>您反應極快，像大江大河一樣流動。有大局觀，能容納各種觀點。但也容易流於善變，虎頭蛇尾。",
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

def get_current_taiwan_time():
@@ -66,12 +148,10 @@ def divine_outcome(question):
])

# ==========================================================
# 模組 1: 🎰 賭王決策系統 (核心 - 動態版)
# 模組 1: 🎰 賭王決策系統 (核心 - 保持動態)
# ==========================================================
if mode == "🎰 賭王決策系統 (核心)":
    st.markdown("## 🎰 專業資金控管・戰術終端")
    
    # 🌟 這裡新增了「目標號碼」輸入框
    target_nums = st.text_input("🎯 輸入本期鎖定號碼 (例如: 24, 25)", "24, 25")

    with st.expander("⚙️ 戰術參數設定", expanded=True):
@@ -94,18 +174,13 @@ def divine_outcome(question):
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"""<div class="gambler-panel"><div class="gambler-label">建議下注比例</div><div class="gambler-stat">{round(safe_kelly * 100, 2)}%</div></div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class="gambler-panel"><div class="gambler-label">建議總金額</div><div class="gambler-stat" style="color:#FFD700;">${int(suggest_amount)}</div></div>""", unsafe_allow_html=True)
    
    color = "#00FF00" if suggest_units >= 1 else "#FF4B4B"
    c3.markdown(f"""<div class="gambler-panel" style="border-color:{color};"><div class="gambler-label">執行注數</div><div class="gambler-stat" style="color:{color};">{suggest_units} 注</div></div>""", unsafe_allow_html=True)

    if suggest_units == 0: 
        st.warning("⚠️ 警告：風險過高，建議觀望或僅下 1 注。")
    else: 
        # 🌟 這裡的指令會自動變更為您輸入的號碼
        st.success(f"✅ 指令：請執行 **{suggest_units} 注** (共 ${suggest_units * cost_per_bet})，目標鎖定 **{target_nums}**。")
    if suggest_units == 0: st.warning("⚠️ 警告：風險過高，建議觀望或僅下 1 注。")
    else: st.success(f"✅ 指令：請執行 **{suggest_units} 注** (共 ${suggest_units * cost_per_bet})，目標鎖定 **{target_nums}**。")

# ==========================================================
# 模組 2: 📈 財務戰績覆盤
# 模組 2: 📈 財務戰績覆盤 (保持不變)
# ==========================================================
elif mode == "📈 財務戰績覆盤":
    st.markdown("## 📈 財務長・ROI 戰績覆盤")
@@ -115,46 +190,62 @@ def divine_outcome(question):
    st.info("💡 這是模擬數據，未來請在此記錄您的真實戰績。")

# ==========================================================
# 模組 3: 📡 予婕情緒雷達
# 模組 3: 📡 予婕情緒雷達 (內容增強)
# ==========================================================
elif mode == "📡 予婕情緒雷達":
    st.markdown("## 📡 情報官・予婕情緒氣象台")
    now = get_current_taiwan_time()
    st.markdown(f"""<div class="radar-box"><h3 style="color:#FF00FF;">👩🏻 對象：予婕 (乙木坐午)</h3><p>📅 日期：{now.strftime('%Y-%m-%d')} (自動運算中...)</p></div>""", unsafe_allow_html=True)
    st.info("📊 **情緒指數：65 (敏感)** | 建議戰術：溫柔安撫，切勿說教。")
    st.markdown("""<div class="strategy-box"><b>✅ 統帥錦囊：</b><br>明日氣場「子午沖」，她情緒不穩。請用美食與陪伴代替講道理。</div>""", unsafe_allow_html=True)
    
    # 這裡的文字我幫您加長、加詳細了
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
# 模組 4: 📊 號碼技術分析 (動態版)
# 模組 4: 📊 號碼技術分析 (保持動態)
# ==========================================================
elif mode == "📊 號碼技術分析":
    st.markdown("## 📊 分析師・號碼趨勢 K 線")
    
    # 🌟 這裡也可以輸入號碼
    target_nums_input = st.text_input("輸入欲分析號碼 (如: 05, 10, 14)", "24, 25")
    
    st.markdown(f"### 🎯 目標號碼：{target_nums_input} (連動分析)")
    
    col_k1, col_k2, col_k3 = st.columns(3)
    col_k1.metric("RSI 指標", "15 (超賣)", "觸底反彈")
    col_k2.metric("MACD 能量", "-0.85", "空方衰竭")
    col_k3.metric("遺漏期數", "8 期", "黃金回補")
    
    st.markdown("#### 📈 能量累積模擬圖")
    
    # 🌟 讓圖表的標籤自動跟著號碼變
    nums_list = target_nums_input.replace("，", ",").split(",")
    # 為了展示效果，產生隨機數據
    chart_data = pd.DataFrame(
        np.random.randn(20, len(nums_list)), 
        columns=[f"{n.strip()}號能量" for n in nums_list]
    )
    chart_data = pd.DataFrame(np.random.randn(20, len(nums_list)), columns=[f"{n.strip()}號能量" for n in nums_list])
    st.line_chart(chart_data)
    
    st.success(f"✅ **技術結論**：號碼組合 **[{target_nums_input}]** 出現技術面買點。")

# ==========================================================
# 模組 5, 6, 7 (保留原貌)
# 模組 5: 🕰️ 今日時空戰略 (保持不變)
# ==========================================================
elif mode == "🕰️ 今日時空戰略":
    st.title("🕰️ 今日出征指南")
@@ -169,17 +260,73 @@ def divine_outcome(question):
    if st.button("🐢 啟動"): 
        o,d,i = divine_outcome(q); st.markdown(f"""<div class="divination-box"><h3>{q}</h3><h1>{o}</h1><p>{d}</p></div>""", unsafe_allow_html=True)

# ==========================================================
# 模組 6: 👤 深層本命解析 (內容恢復詳細版)
# ==========================================================
elif mode == "👤 深層本命解析":
    st.title("👤 掌門人戰略藍圖")
    bd = st.date_input("出生日期", datetime.date(1996, 2, 17))
    if st.button("🚀 掃描"):
        d = DATA_DICT[TIAN_GAN[bd.day % 10]]
        st.markdown(f"""<div class="main-card"><h2 class="gold-text">🗡️ {TIAN_GAN[bd.day % 10]} ({d['title']})</h2><hr><p>{d['personality']}</p><p><b>財富：</b>{d['wealth']}</p></div>""", unsafe_allow_html=True)
        day_gan = TIAN_GAN[bd.day % 10]
        d = DATA_DICT[day_gan]
        # 這裡恢復顯示所有詳細欄位
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
# 模組 7: 💞 情場戰略指揮部 (內容恢復錦囊版)
# ==========================================================
elif mode == "💞 情場戰略指揮部":
    st.title("💞 交往/復合戰略推演")
    c1, c2 = st.columns(2)
    d1 = c1.date_input("您的生日", datetime.date(1996, 2, 17))
    d2 = c2.date_input("對方生日", datetime.date(1997, 3, 21))
    
    if st.button("💘 推演"):
        st.subheader("戰略分析：辛金 ⚔️ 乙木 —— 【征服 (我剋)】")
        st.columns(2)[0].metric("交往指數", "80%"); st.columns(2)[1].metric("復合指數", "55%")
        st.markdown("""<div class="strategy-box">辛金剋乙木。您有主導權，但她怕壓力。請展現高價值，切勿糾纏。</div>""", unsafe_allow_html=True)
        g1 = TIAN_GAN[d1.day % 10]
        g2 = TIAN_GAN[d2.day % 10]
        els = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土", "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"}
        e1, e2 = els[g1], els[g2]
        
        # 這裡恢復完整的邏輯判斷與錦囊
        strategy = []
        date_s, back_s = 50, 50
        rel_type = "普通"
        
        if e1 == e2: 
            date_s, back_s, rel_type = 70, 50, "戰友 (比肩)"
            strategy = ["✅ **共同目標**：一起做事才能維持熱度。", "❌ **忌硬碰硬**：吵架時誰也不讓誰。", "💡 **復合關鍵**：談「合作」不談感情。"]
        elif (e1=="金" and e2=="木") or (e1=="木" and e2=="土") or (e1=="土" and e2=="水") or (e1=="水" and e2=="火") or (e1=="火" and e2=="金"):
             date_s, back_s, rel_type = 80, 55, "征服 (我剋)"
             strategy = [
                 "✅ **霸道主導**：您要展現強勢與自信，對方會因崇拜而跟隨。",
                 "❌ **忌諱猶豫**：如果您優柔寡斷，對方會看不起您。",
                 "💡 **復合關鍵**：必須展現出「我變得更好了」的高價值，重新吸引對方。"
             ]
        elif (e2=="金" and e1=="木") or (e2=="木" and e1=="土") or (e2=="土" and e1=="水") or (e2=="水" and e1=="火") or (e2=="火" and e1=="金"):
            date_s, back_s, rel_type = 60, 30, "磨練 (剋我)"
            strategy = ["✅ **尊重崇拜**：凡事多請教對方意見。", "❌ **忌諱控制**：別想控制對方。", "💡 **復合關鍵**：難度高，需對方主動。"]
        else: # 生我或我生
            date_s, back_s, rel_type = 90, 85, "貴人/付出"
            strategy = ["✅ **溫柔攻勢**：多讚美、多送禮。", "❌ **忌諱計較**：不要計較回報。", "💡 **復合關鍵**：對方容易心軟，低頭就贏。"]
        
        st.subheader(f"戰略分析：{g1} ⚔️ {g2} —— 【{rel_type}】")
        col_res = st.columns(2)
        col_res[0].metric("💘 交往指數", f"{date_s}%", "進攻有利")
        col_res[1].metric("🔄 復合指數", f"{back_s}%", "需長期抗戰", delta_color="inverse")
        
        st.markdown("### 📖 統帥錦囊：相處與攻略")
        for s in strategy:
            st.markdown(f"""<div class="strategy-box">{s}</div>""", unsafe_allow_html=True)
