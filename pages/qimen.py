
import streamlit as st
import pandas as pd
import datetime
import random

# --- 1. 介面設定 ---
st.set_page_config(page_title="赤鍊天機・全功能戰略室", layout="wide", page_icon="☯️")
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #E0E0E0; }
    .main-card { background: #111; padding: 25px; border-radius: 10px; border: 1px solid #D4AF37; margin-bottom: 20px; }
    .score-card { background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%); padding: 20px; border-radius: 10px; border-left: 5px solid #00FF00; text-align: center; }
    .direction-card { background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%); padding: 15px; border-radius: 8px; border-left: 5px solid #FFD700; text-align: center; }
    .divination-box { background: #220022; padding: 20px; border-radius: 10px; border: 1px solid #9932CC; text-align: center; }
    .timeline-box { background: #222; padding: 15px; border-radius: 5px; margin-bottom: 10px; border-left: 3px solid #D4AF37; }
    .gold-text { color: #D4AF37; font-weight: bold; font-size: 22px; }
    .big-luck { font-size: 36px; font-weight: bold; color: #FFD700; }
    h3 { border-bottom: 1px solid #333; padding-bottom: 10px; margin-top: 20px; }
</style>
""", unsafe_allow_html=True)

st.title("☯️ 赤鍊紅蓮・全功能命理戰略室 (v3.1)")

# --- 2. 核心資料庫 (深度解析 + 時空算法) ---
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DIRECTIONS = ["正北", "東北", "正東", "東南", "正南", "西南", "正西", "西北"]

# [深度解析資料庫]
DATA_DICT = {
    "甲": {
        "title": "參天巨木・大將軍",
        "personality": "您天生具備領袖氣質，剛直不屈，不怒自威。您不喜歡彎彎繞繞，做事直來直往。在群體中，您往往是那個扛責任的大哥/大姊。缺點是容易過於固執，不願妥協。",
        "career": "【適合戰場】：管理、創業、政治、建築、實業。<br>【戰略風格】：正面突破。您適合帶領團隊打硬仗，不適合做幕後或需要極度圓滑的工作。",
        "love": "感情上您比較強勢，喜歡照顧對方，但也希望對方服從。您需要一個能以柔克剛的伴侶（如土/水型人）。",
        "cycle": ["25-34歲：紮根期，如大樹向下生長，辛苦但累積實力。", "35-44歲：破土期，事業開始嶄露頭角，掌握權力。", "45-54歲：成林期，建立自己的勢力範圍，財富大增。"]
    },
    "乙": {
        "title": "花草藤蔓・軍師",
        "personality": "您身段柔軟，適應力極強。不像甲木那樣硬碰硬，您懂得繞道而行，達成目的。您心思細膩，善於察言觀色，是天生的談判專家。",
        "career": "【適合戰場】：企劃、藝術、教育、行銷、幕僚。<br>【戰略風格】：迂迴包抄。您擅長用最小的資源換取最大的勝利，適合智取。",
        "love": "您在感情中比較依賴，像藤蔓一樣纏繞對方。您溫柔體貼，但也容易缺乏安全感，需要對方不斷的肯定。",
        "cycle": ["25-34歲：探索期，嘗試多種可能性，累積人脈。", "35-44歲：攀附期，找到強力的合作夥伴(貴人)，借力使力。", "45-54歲：繁花期，名聲遠播，靠智慧與人脈賺錢。"]
    },
    "丙": {
        "title": "太陽之火・先鋒官",
        "personality": "您熱情如火，藏不住話，情緒來得快去得也快。您是人群中的焦點，充滿感染力。做事風風火火，講義氣，但有時因為太急躁而得罪人。",
        "career": "【適合戰場】：演藝、媒體、銷售、餐飲、能源。<br>【戰略風格】：火力壓制。您適合打閃電戰，在短時間內衝高業績或知名度。",
        "love": "您的愛是轟轟烈烈的，喜歡一個人會昭告天下。但熱度難以持久，需要對方不斷給您新鮮感。",
        "cycle": ["25-34歲：燃燒期，精力最旺盛，容易年少成名。", "35-44歲：普照期，影響力擴大，開始帶領團隊。", "45-54歲：餘溫期，轉向傳承或教育，受人尊敬。"]
    },
    "丁": {
        "title": "星燭之火・情報官",
        "personality": "您外表溫和，內心火熱。心思極度細膩，第六感強，能注意到別人忽略的細節。您神祕而有魅力，善於謀略，是最好的幕後推手。",
        "career": "【適合戰場】：心理、宗教、研究、設計、科技。<br>【戰略風格】：精準打擊。您不打沒把握的仗，擅長收集情報後一擊必殺。",
        "love": "您慢熱而深情，喜歡心靈契合的伴侶。一旦愛上，會默默付出，是典型的「悶騷」型。",
        "cycle": ["25-34歲：點燈期，在專業領域默默耕耘，累積口碑。", "35-44歲：燎原期，機會一到，實力瞬間爆發。", "45-54歲：光耀期，成為行業內的權威專家。"]
    },
    "戊": {
        "title": "崇山峻嶺・後勤統帥",
        "personality": "您穩重如山，給人強烈的安全感。守信用，包容力強，不輕易改變立場。雖然反應可能不快，但決策極為紮實，是團隊的定海神針。",
        "career": "【適合戰場】：房地產、金融、保險、倉儲、農業。<br>【戰略風格】：陣地戰。您適合守成與累積，不適合高風險的投機。",
        "love": "您不懂浪漫，但絕對忠誠。您的愛是透過實際行動（如買房、存錢）來表現的。",
        "cycle": ["25-34歲：堆土期，累積資產與信用，進度較慢。", "35-44歲：成山期，信譽變現，事業基礎穩固。", "45-54歲：鎮守期，坐享其成，以守代攻。"]
    },
    "己": {
        "title": "田園之土・參謀長",
        "personality": "您內斂含蓄，多才多藝。不像戊土那麼嚴肅，您比較隨和，善於協調人際關係。您心裡有很多盤算，但不會輕易表露，城府較深。",
        "career": "【適合戰場】：秘書、護理、教育、顧問、仲介。<br>【戰略風格】：滲透戰。您擅長潤物細無聲，慢慢改變局勢。",
        "love": "您在感情中比較被動，容易暗戀或陷入糾結。您需要一個能主動帶領您的伴侶。",
        "cycle": ["25-34歲：耕耘期，學習技能，培養耐心。", "35-44歲：收穫期，之前的佈局開始獲利，生活富足。", "45-54歲：養生期，注重生活品質，投資穩健。"]
    },
    "庚": {
        "title": "刀劍之金・戰神",
        "personality": "您剛毅果斷，講義氣，好打抱不平。您像一把鋒利的劍，越挫越勇。說話直接，容易傷人而不自知。天生適合競爭激烈的環境。",
        "career": "【適合戰場】：軍警、司法、鋼鐵、外科醫生、高科技。<br>【戰略風格】：斬首行動。您解決問題快狠準，是天生的開拓者。",
        "love": "您的感情觀是愛恨分明，絕不拖泥帶水。喜歡強者，不喜歡黏人的伴侶。",
        "cycle": ["25-34歲：磨礪期，經歷挫折與挑戰，越磨越利。", "35-44歲：鋒芒期，事業達到巔峰，戰無不勝。", "45-54歲：收鞘期，轉向管理，傳授戰鬥經驗。"]
    },
    "辛": {
        "title": "珠寶之金・特種兵",
        "personality": "您外表光鮮亮麗，自尊心極強。思維敏捷，說話犀利。您追求完美，對生活品質有高要求。雖然不如庚金粗曠，但內心的堅韌度不輸任何人。",
        "career": "【適合戰場】：金融、珠寶、法律、精密儀器、美業。<br>【戰略風格】：精細操作。您適合需要高度專業與美感的工作。",
        "love": "您在感情中比較挑剔，重視對方的外表與品味。容易因小事而心裡不平衡。",
        "cycle": ["25-34歲：雕琢期，修正缺點，提升自我價值。", "35-44歲：發光期，才華被看見，名利雙收。", "45-54歲：鑑賞期，享受成果，成為圈內名流。"]
    },
    "壬": {
        "title": "江河之水・海軍元帥",
        "personality": "您聰明絕頂，反應快，喜歡自由，不喜歡被拘束。您像大江大河一樣，能容納各種觀點，但也容易流於善變。您的適應力與爆發力都是一流的。",
        "career": "【適合戰場】：貿易、物流、旅遊、廣告、網際網路。<br>【戰略風格】：流動戰。您適合變化快速、需要大局觀的行業。",
        "love": "您風流倜儻，異性緣極好。但不喜歡被承諾束縛，像抓不住的風。",
        "cycle": ["25-34歲：奔流期，四處闖蕩，累積閱歷。", "35-44歲：匯聚期，資源整合，事業做大。", "45-54歲：入海期，格局宏大，掌握跨國或跨領域資源。"]
    },
    "癸": {
        "title": "雨露之水・滲透專家",
        "personality": "您溫柔內向，心思極度縝密。您像水氣一樣無孔不入，耐力驚人。雖然不張揚，但往往是笑到最後的人。容易多愁善感，情緒化。",
        "career": "【適合戰場】：心理、命理、幕僚、會計、化學。<br>【戰略風格】：潛伏戰。您擅長以退為進，等待最佳時機。",
        "love": "您渴望靈魂伴侶，情感豐富細膩。容易陷入單戀或三角關係。",
        "cycle": ["25-34歲：滲透期，在基層累積人脈，不顯山露水。", "35-44歲：滋潤期，成為團隊不可或缺的核心。", "45-54歲：昇華期，靠智慧與資歷獲得地位。"]
    }
}

# [時空決策算法]
def get_lucky_direction(hour):
    random.seed(hour + datetime.date.today().day) 
    lucky_dir = random.choice(DIRECTIONS)
    wealth_dir = random.choice(DIRECTIONS)
    return lucky_dir, wealth_dir

def divine_outcome(question):
    if not question:
        return None, None, None
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
mode = st.sidebar.radio("請選擇戰略層級", ["🕰️ 今日時空戰略 (出征)", "👤 深度本命解析 (戰略藍圖)", "💞 高階合盤分析 (戰友識別)"])

# --- 4. 模組一：今日時空戰略 (已修復完整代碼) ---
if mode == "🕰️ 今日時空戰略 (出征)":
    st.markdown("### 🕰️ 今日出征指南 (Daily Strategy)")
    
    # 獲取當前時間
    now = datetime.datetime.now()
    current_hour = now.hour
    
    # 計算吉方
    luck, wealth = get_lucky_direction(current_hour)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info(f"📅 日期：{now.strftime('%Y-%m-%d')}")
    with c2:
        st.info(f"⏰ 時間：{now.strftime('%H:%M')} (時局變動中)")
    with c3:
        st.warning("🔥 狀態：丙戌火庫日")

    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="direction-card">
            <h3>💰 今日財神方位</h3>
            <div class="big-luck">{wealth}方</div>
            <p>建議：請前往住家或公司 <b>{wealth}方</b> 的彩券行下注。</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="direction-card" style="border-left-color: #D4AF37;">
            <h3>✨ 貴人/吉氣方位</h3>
            <div class="big-luck">{luck}方</div>
            <p>戰術：若與人合資或討論號碼，面朝 <b>{luck}方</b> 座位最佳。</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🔮 靈龜決策占卜系統")
    st.caption("當您猶豫不決（例如：該不該追 25？要不要獨資？）請誠心輸入問題。")
    
    question = st.text_input("請輸入您的戰略疑問：", placeholder="例如：今晚 25 號是否會開出？")
    
    if st.button("🐢 啟動靈龜占卜"):
        if question:
            outcome, detail, idx = divine_outcome(question)
            color = "#00FF00" if idx <= 1 else ("#FF4B4B" if idx >= 3 else "#FFFF00")
            
            st.markdown(f"""
            <div class="divination-box" style="border-color: {color};">
                <h3 style="color: #E0E0E0;">問：{question}</h3>
                <h1 style="color: {color};">{outcome}</h1>
                <p style="font-size: 18px; margin-top: 15px;">{detail}</p>
            </div>
            """, unsafe_allow_html=True)
            if idx <= 1:
                st.balloons()
        else:
            st.warning("請先輸入問題，心誠則靈。")

# --- 5. 模組二：深度本命解析 ---
elif mode == "👤 深度本命解析 (戰略藍圖)":
    st.markdown("### 👤 掌門人・人生戰略藍圖")
    col1, col2 = st.columns(2)
    with col1:
        birth_date = st.date_input("請輸入您的生辰", datetime.date(1996, 1, 1))
    
    if st.button("🚀 啟動深度掃描"):
        day_gan_sim = TIAN_GAN[birth_date.day % 10]
        data = DATA_DICT[day_gan_sim]
        
        st.markdown(f"""
        <div class="main-card">
            <h2 class="gold-text">🗡️ 命主代號：{day_gan_sim} ({data['title']})</h2>
            <hr style="border-top: 1px solid #333;">
            <h3>🧠 性格深層掃描</h3>
            <p>{data['personality']}</p>
            <h3>⚔️ 事業與戰場</h3>
            <p>{data['career']}</p>
            <h3>💘 感情戰略</h3>
            <p>{data['love']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("📅 十年大限運勢 (戰略推演)")
        for cycle in data['cycle']:
            st.markdown(f"""<div class="timeline-box">{cycle}</div>""", unsafe_allow_html=True)

# --- 6. 模組三：高階合盤分析 ---
elif mode == "💞 高階合盤分析 (戰友識別)":
    st.markdown("### 💞 戰略夥伴/伴侶 速配指數儀表板")
    c1, c2 = st.columns(2)
    with c1:
        st.info("👤 您的資料")
        d1 = st.date_input("您的生日", datetime.date(1996, 1, 1))
    with c2:
        st.info("👥 對方資料")
        d2 = st.date_input("對方生日", datetime.date(2001, 1, 1))
        
    if st.button("💘 啟動速配計算"):
        gan1 = TIAN_GAN[d1.day % 10]
        gan2 = TIAN_GAN[d2.day % 10]
        
        elements = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土", "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"}
        e1, e2 = elements[gan1], elements[gan2]
        
        love_score = 60
        biz_score = 60
        relation_type = "普通"
        desc = "關係一般"
        
        if e1 == e2: 
            love_score, biz_score, relation_type, desc = 75, 90, "戰友 (比肩)", "你們性格相似，事業上是最佳拍檔，但感情容易互不相讓。"
        elif (e1=="木" and e2=="火") or (e1=="火" and e2=="土") or (e1=="土" and e2=="金") or (e1=="金" and e2=="水") or (e1=="水" and e2=="木"):
            love_score, biz_score, relation_type, desc = 85, 70, "付出 (食傷)", "您寵愛對方，對方激發您的靈感。感情甜蜜，事業您較累。"
        elif (e2=="木" and e1=="火") or (e2=="火" and e1=="土") or (e2=="土" and e1=="金") or (e2=="金" and e1=="水") or (e2=="水" and e1=="木"):
            love_score, biz_score, relation_type, desc = 95, 85, "貴人 (印星)", "對方是超級貴人！無論事業感情都滋潤您。請珍惜。"
        elif (e1=="木" and e2=="土") or (e1=="火" and e2=="金") or (e1=="土" and e2=="水") or (e1=="金" and e2=="木") or (e1=="水" and e2=="火"):
            love_score, biz_score, relation_type, desc = 70, 80, "征服 (財星)", "您掌控對方。事業上對方是您的資產，感情上您主導。"
        else:
            love_score, biz_score, relation_type, desc = 50, 60, "磨練 (官殺)", "對方氣場壓制您。事業上督促您，感情上您會感到壓力。"

        st.markdown("---")
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.markdown(f"""<div class="score-card" style="border-color: {'#00FF00' if love_score >= 80 else '#FF4B4B'};"><h3>❤️ 感情速配指數</h3><h1 style="font-size: 48px; margin:0;">{love_score}%</h1><p>類型：{relation_type}</p></div>""", unsafe_allow_html=True)
        with col_res2:
            st.markdown(f"""<div class="score-card" style="border-color: {'#00FF00' if biz_score >= 80 else '#FF4B4B'};"><h3>💼 事業互補指數</h3><h1 style="font-size: 48px; margin:0;">{biz_score}%</h1><p>評估：{desc}</p></div>""", unsafe_allow_html=True)
            
        st.info(f"📋 戰略總評：{gan1} (您) ⚔️ {gan2} (對方)")

# --- 頁尾 ---
st.markdown("---")
st.caption("🛡️ 赤鍊天機閣 v3.1 | 全功能修復版")
