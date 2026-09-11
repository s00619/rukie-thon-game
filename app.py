import random
import time
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="2026 YUnicorn 루키톤 - 스피드 키워드 서바이벌",
    page_icon="💥",
    layout="centered"
)

# 커스텀 CSS (Expander 및 버튼 가독성 완전 개선)
st.markdown("""
    <style>
    /* 전체 배경 */
    .stApp {
        background-color: #121212;
        color: white;
    }
    
    /* 메인 타이틀 */
    .main-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: bold;
        color: #FFD166;
        margin-bottom: 25px;
    }
    
    /* Expander(접이식 창) 가독성 개선 */
    div[data-testid="stExpander"] {
        background-color: #1e1e1e !important;
        border: 2px solid #333 !important;
        border-radius: 15px !important;
    }
    
    div[data-testid="stExpander"] summary {
        background-color: #2b2b36 !important;
        color: #FFD166 !important; /* 선명한 노란색 글자 */
        font-weight: bold !important;
        font-size: 1.15rem !important;
        border-radius: 12px !important;
        padding: 12px 18px !important;
    }
    
    div[data-testid="stExpander"] summary:hover {
        background-color: #383848 !important;
        color: #FFFFFF !important;
    }

    /* 버튼 가독성 고정 (글자색 & 배경색 강제 지정) */
    div.stButton > button {
        background-color: #06D6A0 !important; /* 선명한 그린 배경 */
        color: #121212 !important; /* 검은색 글씨로 가독성 확보 */
        font-weight: bold !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease !important;
    }
    
    div.stButton > button:hover {
        background-color: #05b88a !important;
        color: #ffffff !important; /* 마우스 올렸을 때 흰글씨 */
        box-shadow: 0 4px 12px rgba(6, 214, 160, 0.4) !important;
    }

    /* 삭제 및 보조 버튼 전용 스타일 */
    div.stButton > button[kind="secondary"] {
        background-color: #FF5964 !important; /* 핑크/레드 배경 */
        color: #ffffff !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #d9414c !important;
        box-shadow: 0 4px 12px rgba(255, 89, 100, 0.4) !important;
    }

    /* 입력창(Text Input) 스타일 */
    div[data-baseweb="input"] {
        background-color: #2a2a2a !important;
        border-radius: 10px !important;
        border: 1px solid #444 !important;
    }
    div[data-baseweb="input"] input {
        color: #ffffff !important;
    }
    
    /* 카드 스타일 */
    .keyword-card {
        background-color: #1e1e1e;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        font-size: 1.8rem;
        font-weight: bold;
        color: #06D6A0;
        border: 2px solid #333;
        margin-bottom: 20px;
    }
    .name-card {
        background-color: #2b2b36;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        font-size: 3.5rem;
        font-weight: bold;
        color: #FFD166;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .exploded-card {
        background-color: #381a1d;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        font-size: 3.5rem;
        font-weight: bold;
        color: #FF5964;
        border: 3px solid #FF5964;
    }
    </style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if "students" not in st.session_state:
    st.session_state.students = []

if "keywords" not in st.session_state:
    st.session_state.keywords = [
        "문경 최고의 맛집", "내가 제일 잘하는 기술", "학교 매점 최애 메뉴",
        "요즘 가장 즐겨하는 게임", "나만의 스트레스 해소법", "가지고 싶은 신기술 제품",
        "이번 루키톤에서 내 역할", "멘토님께 궁금한 점", "주말에 주로 하는 것"
    ]

st.markdown("<div class='main-title'>🚀 2026 YUnicorn 루키톤<br>스피드 키워드 서바이벌</div>", unsafe_allow_html=True)

# --- [1] 학생 이름 입력 및 관리 영역 ---
with st.expander("🙋‍♂️ 참가자 이름 입력 / 관리하기 (클릭하여 열기/접기)", expanded=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        new_name = st.text_input("이름을 입력하세요", placeholder="예: 홍길동", label_visibility="collapsed")
    with col2:
        if st.button("✨ 추가", use_container_width=True):
            if new_name and new_name not in st.session_state.students:
                st.session_state.students.append(new_name)
                st.rerun()
    
    # 등록된 명단 표시
    if st.session_state.students:
        st.write("**현재 참가자 목록:**")
        tags = " ".join([f"`👤 {name}`" for name in st.session_state.students])
        st.markdown(tags)
        
        if st.button("🧹 전체 명단 삭제", type="secondary"):
            st.session_state.students = []
            st.rerun()
    else:
        st.info("이름을 입력하고 추가 버튼을 눌러주세요!")

st.divider()

# --- [2] 게임 진행 영역 ---
if not st.session_state.students:
    st.warning("참가자가 최소 1명 이상 등록되어야 게임을 시작할 수 있습니다.")
else:
    if st.button("🔥 폭탄 돌리기 (START / NEXT)", use_container_width=True):
        selected_student = random.choice(st.session_state.students)
        selected_keyword = random.choice(st.session_state.keywords)
        
        # 주제 및 지목된 학생 출력
        st.markdown(f"<div class='keyword-card'>📌 주제: {selected_keyword}</div>", unsafe_allow_html=True)
        name_placeholder = st.empty()
        name_placeholder.markdown(f"<div class='name-card'>👤 {selected_student}</div>", unsafe_allow_html=True)
        
        # 타이머 애니메이션 (5초 카운트다운)
        progress_bar = st.progress(100)
        time_limit = 5.0
        start_time = time.time()
        
        while True:
            elapsed = time.time() - start_time
            remaining = max(0.0, time_limit - elapsed)
            ratio = remaining / time_limit
            
            progress_bar.progress(int(ratio * 100))
            
            if remaining <= 0:
                break
            time.sleep(0.05)
            
        # 시간 초과 시 폭발 연출
        name_placeholder.markdown(f"<div class='exploded-card'>💥 {selected_student} 당첨! 💥</div>", unsafe_allow_html=True)