import random
import time
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="2026 YUnicorn 루키톤 - 스피드 키워드 서바이벌",
    page_icon="💥",
    layout="centered"
)

# ----------------------------------------------------
# [실시간 공유 데이터베이스]
# ----------------------------------------------------
@st.cache_resource
def get_shared_game_state():
    return {
        "students": [],
        "current_student": "",
        "current_keyword": "",
        "is_active": False,
        "is_exploded": False,
        "start_time": 0,
        "time_limit": 5.0,
        "last_update": time.time()
    }

game_state = get_shared_game_state()

KEYWORDS = [
    "문경 최고의 맛집", "내가 제일 잘하는 기술", "학교 매점 최애 메뉴",
    "요즘 가장 즐겨하는 게임", "나만의 스트레스 해소법", "가지고 싶은 신기술 제품",
    "이번 루키톤에서 내 역할", "멘토님께 궁금한 점", "주말에 주로 하는 것"
]

# CSS 스타일링 (버튼 가독성 완전 고정 & 귀여운 파스텔 스타일)
st.markdown("""
    <style>
    /* 전체 배경 */
    .stApp { background-color: #121212; color: white; }
    .main-title { text-align: center; font-size: 2.2rem; font-weight: bold; color: #FFD166; margin-bottom: 20px; }
    
    /* Expander(접이식 창) 가독성 */
    div[data-testid="stExpander"] { background-color: #1e1e1e !important; border: 2px solid #333 !important; border-radius: 18px !important; }
    div[data-testid="stExpander"] summary { background-color: #2b2b36 !important; color: #FFD166 !important; font-weight: bold !important; font-size: 1.15rem !important; border-radius: 14px !important; }
    
    /* [기본 버튼] - 등록 버튼 등 */
    div.stButton > button {
        background: linear-gradient(135deg, #06D6A0, #118AB2) !important;
        color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        border-radius: 50px !important;
        border: none !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 10px rgba(6, 214, 160, 0.3) !important;
        transition: transform 0.1s ease !important;
    }
    div.stButton > button:hover {
        transform: scale(1.03) !important;
        color: #ffffff !important;
    }
    
    /* [보조 버튼] - 전체 명단 초기화 (분홍/레드) */
    div.stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #FF70A6, #FF5964) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 10px rgba(255, 89, 100, 0.3) !important;
    }
    
    /* [게임 시작 버튼] (크고 또렷한 노란색/주황색) */
    .start-btn button {
        background: linear-gradient(135deg, #FFD166, #FF9F1C) !important;
        color: #121212 !important; /* 검은색 글자 적용 */
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        padding: 18px !important;
        border-radius: 50px !important;
        border: none !important;
        box-shadow: 0 6px 18px rgba(255, 209, 102, 0.4) !important;
    }
    
    /* [패스 버튼] (선명한 민트 그린) */
    .pass-btn button {
        background: linear-gradient(135deg, #06D6A0, #04A777) !important;
        color: #ffffff !important;
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        padding: 18px !important;
        border-radius: 50px !important;
        border: none !important;
        box-shadow: 0 6px 18px rgba(6, 214, 160, 0.4) !important;
    }
    
    /* 카드 스타일 */
    .keyword-card { background-color: #1e1e1e; border-radius: 18px; padding: 20px; text-align: center; font-size: 1.8rem; font-weight: bold; color: #FFD166; border: 2px solid #333; margin-bottom: 20px; }
    .name-card { background-color: #2b2b36; border-radius: 24px; padding: 30px; text-align: center; font-size: 3.5rem; font-weight: bold; color: #FFD166; margin: 20px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    .exploded-card { background-color: #381a1d; border-radius: 24px; padding: 30px; text-align: center; font-size: 3.5rem; font-weight: bold; color: #FF5964; border: 3px solid #FF5964; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🚀 2026 YUnicorn 루키톤<br>스피드 키워드 서바이벌</div>", unsafe_allow_html=True)

# ----------------------------------------------------
# [1] 참가자 이름 입력 및 관리 영역
# ----------------------------------------------------
with st.expander("🙋‍♂️ 참가자 이름 입력 / 명단 확인", expanded=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        new_name = st.text_input("이름 입력", placeholder="본인 이름을 입력하세요", label_visibility="collapsed")
    with col2:
        if st.button("✨ 등록", use_container_width=True):
            if new_name and new_name not in game_state["students"]:
                game_state["students"].append(new_name)
                game_state["last_update"] = time.time()
                st.rerun()
    
    if game_state["students"]:
        st.write(f"**현재 접속 참가자 ({len(game_state['students'])}명):**")
        tags = " ".join([f"`👤 {name}`" for name in game_state["students"]])
        st.markdown(tags)
        
        if st.button("🧹 전체 명단 초기화", type="secondary"):
            game_state["students"] = []
            game_state["is_active"] = False
            game_state["last_update"] = time.time()
            st.rerun()
    else:
        st.info("학생들은 이름을 입력하고 '✨ 등록' 버튼을 눌러주세요!")

st.divider()

# ----------------------------------------------------
# [2] 게임 진행 컨트롤
# ----------------------------------------------------
if not game_state["students"]:
    st.warning("⚠️ 참가자를 1명 이상 등록해 주세요.")
else:
    # 게임 미진행 상태일 때 -> 시작 버튼
    if not game_state["is_active"] or game_state["is_exploded"]:
        st.markdown("<div class='start-btn'>", unsafe_allow_html=True)
        if st.button("🚀 게임 시작 (폭탄 돌리기 시작!)", use_container_width=True):
            game_state["current_student"] = random.choice(game_state["students"])
            game_state["current_keyword"] = random.choice(KEYWORDS)
            game_state["is_active"] = True
            game_state["is_exploded"] = False
            game_state["start_time"] = time.time()
            game_state["last_update"] = time.time()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # 게임 진행 중일 때 -> 다음 사람 패스 버튼
    else:
        st.markdown("<div class='pass-btn'>", unsafe_allow_html=True)
        if st.button("▶️ 외쳤다! 다음 사람에게 패스", use_container_width=True):
            candidates = [s for s in game_state["students"] if s != game_state["current_student"]]
            if not candidates:
                candidates = game_state["students"]
                
            game_state["current_student"] = random.choice(candidates)
            game_state["current_keyword"] = random.choice(KEYWORDS)
            game_state["start_time"] = time.time() # 5초 타이머 리셋
            game_state["last_update"] = time.time()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------
# [3] 화면 연출 및 타이머 처리
# ----------------------------------------------------
if game_state["is_active"]:
    st.markdown(f"<div class='keyword-card'>📌 주제: {game_state['current_keyword']}</div>", unsafe_allow_html=True)
    
    name_placeholder = st.empty()
    name_placeholder.markdown(f"<div class='name-card'>👤 {game_state['current_student']}</div>", unsafe_allow_html=True)
    
    if not game_state["is_exploded"]:
        elapsed = time.time() - game_state["start_time"]
        remaining = max(0.0, game_state["time_limit"] - elapsed)
        ratio = remaining / game_state["time_limit"]
        
        st.progress(int(ratio * 100))
        
        if remaining <= 0:
            game_state["is_exploded"] = True
            game_state["last_update"] = time.time()
            st.rerun()
        else:
            time.sleep(0.1)
            st.rerun()
            
    if game_state["is_exploded"]:
        name_placeholder.markdown(f"<div class='exploded-card'>💥 {game_state['current_student']} 당첨! 💥</div>", unsafe_allow_html=True)

# 대기 상태 시 2초 자동 폴링
if not game_state["is_active"]:
    time.sleep(2)
    st.rerun()