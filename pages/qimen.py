import streamlit as st
import pandas as pd
import datetime
import plotly.graph_objects as go

# --- 1. 天機閣介面設定 ---
st.set_page_config(page_title="赤鍊天機・奇門戰略室", layout="wide", page_icon="☯️")
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #E0E0E0; }
    .main-card { background: #111; padding: 20px; border-radius: 10px; border: 1px solid #D4AF37; margin-bottom: 20px; }
    .grid-box { background: #1a1a1a; padding: 15px; border-radius: 5px; border: 1px solid #333; text-align: center; }
    .lucky { color: #00FF00; font-weight: bold; }
    .warning { color: #FF4B4B; font-weight: bold; }
    .gold-text { color: #D4AF37; font-weight: bold; font-size: 18px; }
</style>
""", unsafe_allow_html=True)

st.title("☯️ 赤鍊紅蓮・奇門遁甲天機閣 (v1.0)")

# --- 2. 核心資料庫 (天干地支與奇門屬性) ---
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 簡易排盤模擬算法 (正式版需引入天文庫)
def get_gan_zhi(year):
    # 簡單計算年干支 (模擬)
    idx = (year - 4) % 60
    gan_idx = idx % 10
    zhi_idx = idx % 12
    return TIAN_GAN[gan_idx], DI_ZHI[zhi_idx]

def analyze_character(gan):
    # 天干性格映射
    traits = {
        "甲": "領袖氣質、剛直、不怒自威 (大將軍)",
        "乙": "靈活、善於謀略、適應力強 (軍師)",
        "丙": "熱情、急躁、影響力大 (先鋒官)",
        "丁": "細膩、神祕、洞察力強 (情報官)",
        "戊": "穩重、守信、包容力強 (後勤官)",
        "己": "策劃、內斂、善於協調 (參謀)",
        "庚": "剛毅、果斷、肅殺之氣 (戰神)",
        "辛": "精緻、變革、好勝心強 (特種兵)",
        "壬": "智謀、流動、善變 (海軍統帥)",
        "癸": "陰柔、滲透、耐力極強 (刺客)"
    }
    return traits.get(gan, "未知")

def analyze_compatibility(gan1, gan2):
    # 簡單的天干相生相剋矩陣
    elements = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土", "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"}
    e1, e2 = elements[gan1], elements[gan2]
    
    relation = "平淡"
    score = 60
    desc = "普通關係"
    
    # 五行生剋邏輯
    if e1 == e2:
        relation = "比旺 (戰友關係)"
        score = 80
        desc = "你們性格相似，適合共同作戰，但也容易固執己見。"
    elif (e1=="木" and e2=="火") or (e1=="火" and e2=="土") or (e1=="土" and e2=="金") or (e1=="金" and e2=="水") or (e1=="水" and e2=="木"):
        relation = "我生 (付出關係)"
        score = 75
        desc = "您對對方有助益，您是他的貴人，但他可能比較依賴您。"
    elif (e2=="木" and e1=="火") or (e2=="火" and e1=="土") or (e2=="土" and e1=="金") or (e2=="金" and e1=="水") or (e2=="水" and e1=="木"):
        relation = "生我 (被愛關係)"
        score = 90
        desc = "對方天生旺您，是您的超級貴人，能給您帶來資源。"
    else:
        relation = "相剋 (磨練關係)"
        score = 50
        desc = "氣場不合，容易產生摩擦。對方可能是來修練您的心性的。"
        
    return relation, score, desc

# --- 3. 側邊欄控制 ---
st.sidebar.title("🛠️ 天機排盤設定")
mode = st.sidebar.radio("選擇功能模式", ["👤 本命戰略分析", "💞 雙人合盤系統"])

# --- 4. 模式一：本命戰略分析 ---
if mode == "👤 本命戰略分析":
    st.markdown("### 👤 掌門人本命戰略盤")
    
    col1, col2 = st.columns(2)
    with col1:
        birth_date = st.date_input("請輸入您的生辰", datetime.date(1996, 1, 1))
        birth_time = st.time_input("出生時間", datetime.time(12, 0))
    
    if st.button("🚀 啟動排盤"):
        # 簡易模擬：以日干代表命主 (這裡用日期尾數模擬，真實需要萬年曆)
        simulated_day_gan = TIAN_GAN[birth_date.day % 10] 
        year_gan = TIAN_GAN[(birth_date.year - 4) % 10]
        
        # --- A. 命盤核心展示 ---
        st.markdown(f"""
        <div class="main-card">
            <h2 class="gold-text">🗡️ 命主代號：{simulated_day_gan} (年命：{year_gan})</h2>
            <p><b>【元神屬性】</b>：{analyze_character(simulated_day_gan)}</p>
            <p><b>【當前大限】</b>：30-39歲 (事業變革期)</p>
            <p><b>【戰略優勢】</b>：直覺敏銳、決策果斷。</p>
            <p><b>【潛在弱點】</b>：容易急躁，需防背後小人。</p>
        </div>
        """, unsafe_allow_html=True)
        
        # --- B. 奇門九宮模擬圖 ---
        st.subheader("🔮 本命奇門九宮局")
        g1, g2, g3 = st.columns(3)
        g4, g5, g6 = st.columns(3)
        g7, g8, g9 = st.columns(3)
        
        # 模擬九宮數據
        grids = [
            {"pos": "巽四宮", "men": "杜門", "star": "天輔", "god": "六合"},
            {"pos": "離九宮", "men": "景門", "star": "天英", "god": "騰蛇"},
            {"pos": "坤二宮", "men": "死門", "star": "天芮", "god": "太陰"},
            {"pos": "震三宮", "men": "傷門", "star": "天沖", "god": "九天"},
            {"pos": "中五宮", "men": "寄宮", "star": "天禽", "god": "值符"},
            {"pos": "兌七宮", "men": "驚門", "star": "天柱", "god": "白虎"},
            {"pos": "艮八宮", "men": "生門", "star": "天任", "god": "玄武"},
            {"pos": "坎一宮", "men": "休門", "star": "天蓬", "god": "九地"},
            {"pos": "乾六宮", "men": "開門", "star": "天心", "god": "值符"}
        ]
        
        cols = [g1, g2, g3, g4, g5, g6, g7, g8, g9]
        for i, col in enumerate(cols):
            data = grids[i]
            border_color = "#D4AF37" if data['men'] in ["生門", "開門", "休門"] else "#333"
            bg_color = "#222" if i != 4 else "#330000" # 中宮深色
            with col:
                st.markdown(f"""
                <div style="background:{bg_color}; padding:10px; border:1px solid {border_color}; border-radius:5px; text-align:center;">
                    <small style="color:#888;">{data['pos']}</small><br>
                    <b style="color:#FFD700;">{data['god']}</b><br>
                    <span style="color:#FFF;">{data['star']}</span><br>
                    <b style="color:{'#00FF00' if data['men'] in ['生門','開門'] else '#FF4B4B'}; font-size:18px;">{data['men']}</b>
                </div>
                """, unsafe_allow_html=True)

# --- 5. 模式二：雙人合盤系統 ---
elif mode == "💞 雙人合盤系統":
    st.markdown("### 💞 戰略夥伴/伴侶 合盤分析")
    
    c1, c2 = st.columns(2)
    with c1:
        st.info("👤 您的資料")
        d1 = st.date_input("您的生日", datetime.date(1996, 1, 1))
    with c2:
        st.info("👥 對方資料")
        d2 = st.date_input("對方生日", datetime.date(2001, 1, 1))
        
    if st.button("💘 開始合盤解析"):
        gan1 = TIAN_GAN[d1.day % 10]
        gan2 = TIAN_GAN[d2.day % 10]
        
        relation, score, desc = analyze_compatibility(gan1, gan2)
        
        st.markdown("---")
        st.markdown(f"""
        <div class="main-card" style="text-align: center;">
            <h2 style="color: #D4AF37;">合盤結果：{score} 分</h2>
            <h3 style="color: {'#00FF00' if score >= 80 else '#FF4B4B'};">{relation}</h3>
            <p style="font-size: 18px;">{gan1} (您) ⚔️ {gan2} (對方)</p>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("💡 戰略相處建議")
        if score >= 80:
            st.success("✅ **最佳策略**：你們是天作之合，適合共同創業或組建家庭。對方能補足您的短板。")
        elif score >= 60:
            st.warning("⚠️ **中庸策略**：需要多溝通。您可能會覺得對方有點依賴您，或是您需要多照顧對方情緒。")
        else:
            st.error("🛑 **防禦策略**：氣場容易衝突。建議保持適當距離，或是透過第三方（如屬土/金的朋友）來調和。")

# --- 6. 頁尾 ---
st.markdown("---")
st.caption("🛡️ 赤鍊天機閣 v1.0 | 統帥專用戰略排盤")
