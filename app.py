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
# [실시간 공유 데이터베이스] 모든 접속자가 상태를 공유함
# ----------------------------------------------------
@st.cache_resource
def get_shared_game_state():
    return {
        "students": [],
        "current_student": "",
        "current_keyword": "",
        "is_active": False,
        "is_exploded": False,
        "time_limit": 5,
        "game_version": 0 # 화면 새로고침용 카운터
    }

game_state = get_shared_game_state()

# 기본 키워드 목록
KEYWORDS = [
    "문경 최고의 맛집", "내가 제일 잘하는 기술", "학교 매점 최애 메뉴",
    "요즘 가장 즐겨하는 게임", "나만의 스트레스 해소법", "가지고 싶은 신기술 제품",
    "이번 루키톤에서 내 역할", "멘토님께 궁금한 점", "주말에 주로 하는 것"
]

# Style
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    .main-title { text-align: center; font-size: 2.2rem; font-weight: bold; color: #FFD166; margin-bottom: 20px; }
    
    /* Expander */
    div[data-testid="stExpander"] { background-color: #1e1e1e !important; border: 2px solid #333 !important; border-radius: 15px !important; }
    div[data-testid="stExpander"] summary { background-color: #2b2b36 !important; color: #FFD166 !important; font-weight: bold !important; font-size: 1.15rem !important; }
    
    /* Buttons */
    div.stButton > button { background-color: #06D6A0 !important; color: #121212 !important; font-weight: bold !important; border-radius: 12px !important; border: none !important; padding: 12px 20px !important; }
    div.stButton > button[kind="secondary"] { background-color: #FF5964 !important; color: #ffffff !important; }
    
    /* Cards */
    .keyword-card { background-color: #1e1e1e; border-radius: 15px; padding: 20px; text-align: center; font-size: 1.8rem; font-weight: bold; color: #06D6A0; border: 2px solid #333; margin-bottom: 20px; }
    .name-card { background-color: #2b2b36; border-radius: 20px; padding: 30px; text-align: center; font-size: 3.5rem; font-weight: bold; color: #FFD166; margin: 20px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    .exploded-card { background-color: #381a1d; border-radius: 20px; padding: 30px; text-align: center; font-size: 3.5rem; font-weight: bold; color: #FF5964; border: 3px solid #FF5964; }
    .host-badge { background-color: #FFD166; color: #121212; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 0.9rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🚀 2026 YUnicorn 루키톤<br>스피드 키워드 서바이벌</div>", unsafe_allow_html=True)

# ----------------------------------------------------
# [1] 방장 설정 & 이름 입력 영역
# ----------------------------------------------------
col_host, col_refresh = st.columns([3, 1])
with col_host:
    is_host = st.checkbox("👑 내가 방장(게임 진행자)입니다", value=False)
with col_refresh:
    if st.button("🔄 화면 갱신"):
        st.rerun()

with st.expander("🙋‍♂️ 참가자 이름 입력 / 명단 확인", expanded=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        new_name = st.text_input("이름 입력", placeholder="본인 이름을 입력하세요", label_visibility="collapsed")
    with col2:
        if st.button("✨ 등록", use_container_width=True):
            if new_name and new_name not in game_state["students"]:
                game_state["students"].append(new_name)
                st.success(f"'{new_name}' 등록 완료!")
                st.rerun()
    
    # 실시간 명단 표시
    if game_state["students"]:
        st.write(f"**현재 접속 참가자 ({len(game_state['students'])}명):**")
        tags = " ".join([f"`👤 {name}`" for name in game_state["students"]])
        st.markdown(tags)
        
        if is_host and st.button("🧹 전체 명단 초기화", type="secondary"):
            game_state["students"] = []
            game_state["is_active"] = False
            st.rerun()
    else:
        st.info("학생들은 이곳에 이름을 입력하고 등록 버튼을 눌러주세요!")

st.divider()

# ----------------------------------------------------
# [2] 게임 메인 제어 및 화면 표시
# ----------------------------------------------------

# 방장 전용 진행 컨트롤
if is_host:
    st.markdown("<span class='host-badge'>👑 방장 전용 컨트롤러</span>", unsafe_allow_html=True)
    if not game_state["students"]:
        st.warning("학생들이 먼저 이름을 등록해야 게임을 시작할 수 있습니다.")
    else:
        if st.button("🔥 폭탄 돌리기 / 다음 사람 지목 (START)", use_container_width=True):
            game_state["current_student"] = random.choice(game_state["students"])
            game_state["current_keyword"] = random.choice(KEYWORDS)
            game_state["is_active"] = True
            game_state["is_exploded"] = False
            game_state["game_version"] += 1
            st.rerun()

# 전체 화면 (학생 및 방장 공통 표시)
if game_state["is_active"]:
    st.markdown(f"<div class='keyword-card'>📌 주제: {game_state['current_keyword']}</div>", unsafe_allow_html=True)
    
    name_placeholder = st.empty()
    name_placeholder.markdown(f"<div class='name-card'>👤 {game_state['current_student']}</div>", unsafe_allow_html=True)
    
    # 타이머 연출 (방장 화면 기준 타이머 실행)
    if is_host and not game_state["is_exploded"]:
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
                st.rerun()
                break
            time.sleep(0.05)
            
    if game_state["is_exploded"]:
        name_placeholder.markdown(f"<div class='exploded-card'>💥 {game_state['current_student']} 당첨! 💥</div>", unsafe_allow_html=True)
else:
    st.info("방장(선생님)이 게임 시작 버튼을 누르면 화면에 주제와 당첨자가 나타납니다!")