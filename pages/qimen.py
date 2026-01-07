import streamlit as st
import pandas as pd
import datetime
import random

# --- 1. 介面設定 ---
st.set_page_config(page_title="赤鍊天機・深度戰略室", layout="wide", page_icon="☯️")
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #E0E0E0; }
    .main-card { background: #111; padding: 25px; border-radius: 10px; border: 1px solid #D4AF37; margin-bottom: 20px; }
    .score-card { background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%); padding: 20px; border-radius: 10px; border-left: 5px solid #00FF00; text-align: center; }
    .bad-score { border-left: 5px solid #FF4B4B; }
    .timeline-box { background: #222; padding: 15px; border-radius: 5px; margin-bottom: 10px; border-left: 3px solid #D4AF37; }
    .gold-text { color: #D4AF37; font-weight: bold; font-size: 22px; }
    h3 { border-bottom: 1px solid #333; padding-bottom: 10px; margin-top: 20px; }
</style>
""", unsafe_allow_html=True)

st.title("☯️ 赤鍊紅蓮・深度命理戰略室 (v3.0)")

# --- 2. 深度資料庫 (天干戰略屬性) ---
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 模擬資料：真實排盤需萬年曆，此處以天干特性進行深度模擬
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

# --- 3. 側邊欄導航 ---
st.sidebar.title("🛡️ 戰略功能模組")
mode = st.sidebar.radio("請選擇戰略層級", ["👤 深度本命解析 (戰略藍圖)", "💞 高階合盤分析 (戰友識別)", "🕰️ 時空決策 (v2.0保留)"])

# --- 4. 模組一：深度本命解析 ---
if mode == "👤 深度本命解析 (戰略藍圖)":
    st.markdown("### 👤 掌門人・人生戰略藍圖")
    
    col1, col2 = st.columns(2)
    with col1:
        birth_date = st.date_input("請輸入您的生辰", datetime.date(1996, 1, 1))
    
    if st.button("🚀 啟動深度掃描"):
        # 簡易模擬：以日期尾數模擬日干 (真實需萬年曆)
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

# --- 5. 模組二：高階合盤分析 ---
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
        
        # 模擬合盤邏輯
        # 這裡使用簡易的五行生剋賦分
        elements = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土", "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"}
        e1, e2 = elements[gan1], elements[gan2]
        
        # 基礎分
        love_score = 60
        biz_score = 60
        relation_type = "普通"
        
        # 判斷邏輯
        if e1 == e2: # 比旺
            love_score = 75
            biz_score = 90
            relation_type = "戰友 (比肩)"
            desc = "你們像是照鏡子，性格相似。事業上是最佳拍檔，但感情上容易互不相讓，缺乏互補的激情。"
        elif (e1=="木" and e2=="火") or (e1=="火" and e2=="土") or (e1=="土" and e2=="金") or (e1=="金" and e2=="水") or (e1=="水" and e2=="木"): # 我生
            love_score = 85
            biz_score = 70
            relation_type = "付出 (食傷)"
            desc = "您非常寵愛對方，願意為對方付出。對方能激發您的靈感。感情甜蜜，但事業上您會比較累。"
        elif (e2=="木" and e1=="火") or (e2=="火" and e1=="土") or (e2=="土" and e1=="金") or (e2=="金" and e1=="水") or (e2=="水" and e1=="木"): # 生我
            love_score = 95
            biz_score = 85
            relation_type = "貴人 (印星)"
            desc = "對方是您的超級大貴人！無論事業還是感情，對方都能無條件支持您、滋潤您。請好好珍惜。"
        elif (e1=="木" and e2=="土") or (e1=="火" and e2=="金") or (e1=="土" and e2=="水") or (e1=="金" and e2=="木") or (e1=="水" and e2=="火"): # 我剋
            love_score = 70
            biz_score = 80
            relation_type = "征服 (財星)"
            desc = "您能掌控對方。對方在您面前比較聽話。事業上對方是您的下屬或資產，感情上您佔主導權。"
        else: # 剋我
            love_score = 50
            biz_score = 60
            relation_type = "磨練 (官殺)"
            desc = "對方氣場壓制您。這是一段有壓力的關係。事業上對方能督促您進步，但感情上您會感到壓抑。"

        st.markdown("---")
        
        # 顯示儀表板
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.markdown(f"""
            <div class="score-card" style="border-color: {'#00FF00' if love_score >= 80 else '#FF4B4B'};">
                <h3>❤️ 感情速配指數</h3>
                <h1 style="font-size: 48px; margin:0;">{love_score}%</h1>
                <p>類型：{relation_type}</p>
            </div>
            """, unsafe_allow_html=True)
        with col_res2:
            st.markdown(f"""
            <div class="score-card" style="border-color: {'#00FF00' if biz_score >= 80 else '#FF4B4B'};">
                <h3>💼 事業互補指數</h3>
                <h1 style="font-size: 48px; margin:0;">{biz_score}%</h1>
                <p>戰力評估：{desc}</p>
            </div>
            """, unsafe_allow_html=True)
            
        st.info(f"📋 戰略總評：{gan1} (您) ⚔️ {gan2} (對方)")

# --- 6. 模組三：保留 v2.0 的時空決策 ---
elif mode == "🕰️ 時空決策 (v2.0保留)":
    # 為了節省篇幅，這裡保留 v2.0 的代碼邏輯，或者您需要我再貼一次完整的包含 v2.0 功能的代碼？
    st.markdown("### 🕰️ 今日時空戰略 (Daily Strategy)")
    st.info("💡 此模組功能與 v2.0 相同，提供每日財神方位與靈龜占卜。")
    # ... (若需要完整代碼可再次請求)

# --- 頁尾 ---
st.markdown("---")
st.caption("🛡️ 赤鍊天機閣 v3.0 | 深度命理戰略系統")
