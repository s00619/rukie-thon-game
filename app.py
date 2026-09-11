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
        "last_update": time.time()  # 상태 변경 감지용 타임스탬프
    }

game_state = get_shared_game_state()

KEYWORDS = [
    "문경 최고의 맛집", "내가 제일 잘하는 기술", "학교 매점 최애 메뉴",
    "요즘 가장 즐겨하는 게임", "나만의 스트레스 해소법", "가지고 싶은 신기술 제품",
    "이번 루키톤에서 내 역할", "멘토님께 궁금한 점", "주말에 주로 하는 것"
]

# CSS 스타일링
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    .main-title { text-align: center; font-size: 2.2rem; font-weight: bold; color: #FFD166; margin-bottom: 20px; }
    
    /* Expander */
    div[data-testid="stExpander"] { background-color: #1e1e1e !important; border: 2px solid #333 !important; border-radius: 15px !important; }
    div[data-testid="stExpander"] summary { background-color: #2b2b36 !important; color: #FFD166 !important; font-weight: bold !important; font-size: 1.15rem !important; }
    
    /* 큰 시작 버튼 전용 스타일 */
    .start-btn button {
        background-color: #06D6A0 !important;
        color: #121212 !important;
        font-size: 1.5rem !important;
        font-weight: bold !important;
        padding: 18px !important;
        border-radius: 15px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(6, 214, 160, 0.4) !important;
    }
    
    /* 카드 스타일 */
    .keyword-card { background-color: #1e1e1e; border-radius: 15px; padding: 20px; text-align: center; font-size: 1.8rem; font-weight: bold; color: #06D6A0; border: 2px solid #333; margin-bottom: 20px; }
    .name-card { background-color: #2b2b36; border-radius: 20px; padding: 30px; text-align: center; font-size: 3.5rem; font-weight: bold; color: #FFD166; margin: 20px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    .exploded-card { background-color: #381a1d; border-radius: 20px; padding: 30px; text-align: center; font-size: 3.5rem; font-weight: bold; color: #FF5964; border: 3px solid #FF5964; }
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
# [2] 메인 게임 시작 및 진행 버튼 (방장/진행자용)
# ----------------------------------------------------
st.markdown("<div class='start-btn'>", unsafe_allow_html=True)
if not game_state["students"]:
    st.warning("⚠️ 참가자를 1명 이상 등록하면 시작 버튼이 활성화됩니다.")
else:
    if st.button("🔥 게임 시작 / 다음 폭탄 전달 (START / NEXT)", use_container_width=True):
        game_state["current_student"] = random.choice(game_state["students"])
        game_state["current_keyword"] = random.choice(KEYWORDS)
        game_state["is_active"] = True
        game_state["is_exploded"] = False
        game_state["last_update"] = time.time()  # 상태 업데이트
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------
# [3] 게임 플레이 연출 및 실시간 자동 동기화
# ----------------------------------------------------
if game_state["is_active"]:
    st.markdown(f"<div class='keyword-card'>📌 주제: {game_state['current_keyword']}</div>", unsafe_allow_html=True)
    
    name_placeholder = st.empty()
    name_placeholder.markdown(f"<div class='name-card'>👤 {game_state['current_student']}</div>", unsafe_allow_html=True)
    
    # 타이머 연출
    if not game_state["is_exploded"]:
        progress_bar = st.progress(100)
        start_time = time.time()
        time_limit = 5.0
        
        while True:
            elapsed = time.time() - start_time
            remaining = max(0.0, time_limit - elapsed)
            ratio = remaining / time_limit
            
            progress_bar.progress(int(ratio * 100))
            
            if remaining <= 0:
                game_state["is_exploded"] = True
                game_state["last_update"] = time.time()
                st.rerun()
                break
            time.sleep(0.05)
            
    if game_state["is_exploded"]:
        name_placeholder.markdown(f"<div class='exploded-card'>💥 {game_state['current_student']} 당첨! 💥</div>", unsafe_allow_html=True)

# ----------------------------------------------------
# [4] 대기 상태일 때 자동 감지 리프레시 (2초 폴링)
# ----------------------------------------------------
if not game_state["is_active"]:
    time.sleep(2)
    st.rerun()