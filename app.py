import random
import time
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="2026 YUnicorn 루키톤 - 스피드 서바이벌",
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
        "time_limit": 7.0, # 7초 제한시간
        "last_update": time.time(),
        "used_keywords": []
    }

game_state = get_shared_game_state()

# ----------------------------------------------------
# [150개+ TMI & 자기소개 중심 데이터베이스]
# ----------------------------------------------------
KEYWORDS_DB = [
    # 1. 개인 프로필 & 기본 TMI
    "나의 MBTI와 그 유형의 가장 큰 특징은?",
    "나의 혈액형과 평소 내 성격의 공통점은?",
    "내가 태어난 띠(생년)와 별자리는?",
    "형제관계(외동/첫째/둘째/막내)와 장단점 한 가지!",
    "가장 좋아하는 음식 3가지를 초스피드로 말하기!",
    "절대 못 먹거나 가장 싫어하는 음식은?",
    "나의 현재 솔직한 신장(키) 또는 발 사이즈는?",
    "좌우명이나 평소 가슴에 품고 사는 한마디는?",
    "내 외모에서 가장 마음에 드는 부분은?",
    "내 별명(별칭)과 그 별명이 생긴 이유는?",
    "가장 좋아하는 색깔과 그 이유!",
    "내가 가장 잘 만드는(요리할 수 있는) 음식은?",
    "내 인생에서 가장 소중한 보물 1호는?",
    "나의 태몽이나 이름에 담긴 뜻은?",
    "내 생일(월/일)과 생일에 받고 싶은 선물은?",
    "내가 좋아하는 계절과 싫어하는 계절은?",
    "자신 있는 본인의 시력(양안) 상태는?",
    "본인이 가장 좋아하는 동물은?",
    "가장 최근에 산 소지품이나 물건은?",
    "평소 주량(음료수/탄산 포함)이나 최애 음료는?",
    "나의 시그니처 포즈나 표정 하나 선보이기!",
    "자신 있는 본인만의 숨겨진 신체 비밀/특징은?",
    "핸드폰 배경화면에 설정되어 있는 사진은?",
    "평소 잠드는 시간과 평균 수면 시간은?",
    "자주 쓰는 인스타그램/SNS 아이디의 의미는?",
    "가장 최근에 검색해 본 검색어는?",
    "나의 지갑 속에 항상 들어있는 물건은?",
    "본인이 생각하는 나의 가장 큰 장점 한 가지!",
    "내가 고치고 싶은 나의 소소한 단점 한 가지!",
    "가장 자주 사용하는 이모티콘이나 짤은?",
    "오늘 아침에 가장 먼저 한 행동은?",
    "가장 최근에 나를 웃게 만들었던 일은?",
    "가장 좋아하는 브랜드(의류, 신발, 전자기기 등)는?",
    "내 인생 영화나 최고의 드라마 한 편은?",
    "지금 당장 떠나고 싶은 여행지는?",
    "평소에 가장 즐겨 입는 패션 스타일은?",
    "스마트폰 앱 중 하루에 가장 오래 쓰는 앱은?",
    "본인의 가장 오래된 절친/친구 이름은?",
    "자신 있는 노래방 18번 곡 제목은?",
    "본인이 가장 좋아하는 스트리머/유튜버는?",

    # 2. 취향 & 습관 & 일상 TMI
    "스트레스받을 때 풀어버리는 나만의 방법은?",
    "시험 끝난 날 가장 먼저 하는 일은?",
    "주말 아침에 눈떴을 때 주로 하는 행동은?",
    "학교/집에서 가장 좋아하는 나만의 비밀 공간은?",
    "학원이나 학교 땡땡이치고 가고 싶은 장소는?",
    "가장 즐겨 먹는 배달 음식 조합은?",
    "교실/독서실 책상 위에 꼭 놓여있는 필수템은?",
    "가장 최근에 먹은 맛있는 음식 메뉴는?",
    "용돈 받으면 가장 먼저 지출하는 항목은?",
    "세상에서 제일 싫어하는 상황 한 가지는?",
    "가장 좋아하는 라면 종류와 맛있게 끓이는 팁!",
    "가장 좋아하는 떡볶이 브랜드와 맵기 단계는?",
    "아침 등교/출근 시간에 절대 안 늦는 꿀팁은?",
    "가장 최근에 감동받아 울거나 뭉클했던 적은?",
    "내가 제일 좋아하는 무인도 필수 소지품 3가지!",
    "본인이 제일 싫어하는 벌레나 동물은?",
    "자기 전 마지막으로 들려오는 소리나 음악은?",
    "가장 좋아하는 과자/간식 브랜드는?",
    "수업 시간에 졸릴 때 깨는 나만의 신박한 방법은?",
    "가장 좋아하는 커피 메뉴(또는 디저트)는?",
    "본인이 생각하는 나만의 특기/장기는?",
    "100만 유튜버가 된다면 운영할 채널 주제는?",
    "하루 중 내가 가장 행복하다고 느끼는 순간은?",
    "가장 최근에 한 소비 중 돈이 아깝지 않았던 것은?",
    "가장 좋아하는 아이돌/연예인 이름은?",
    "버킷리스트 1번에 적혀있는 꿈은?",
    "가장 최근에 읽은 책이나 감명 깊었던 글귀는?",
    "내가 알고 있는 제일 쓸데없는 TMI 정보 한 가지!",
    "학창 시절 가장 기억에 남는 최고의 레전드 사건은?",
    "가장 좋아하는 운동 경기나 스포츠 종목은?",
    "내 카카오톡 프로필 뮤직(배경음악)은?",
    "스마트폰 배터리 1% 남았을 때 나의 행동은?",
    "가장 좋아하는 패스트푸드(버거 등) 브랜드는?",
    "다시 태어난다면 해보고 싶은 꿈의 직업은?",
    "내가 만약 하루 동안 투명인간이 된다면 하고 싶은 일?",
    "복권 1등(30억) 당첨 시 제일 먼저 살 물건은?",
    "친구와 싸웠을 때 먼저 화해하는 나만의 노하우는?",
    "월요일 아침마다 머릿속에 드는 솔직한 생각은?",
    "내가 살아오면서 가장 화났던 순간은?",
    "가장 좋아하는 아이스크림 맛은?",

    # 3. 루키톤 & 창업 & 특성화고/대학생 TMI
    "이번 루키톤에 참여하게 된 솔직한 계기는?",
    "루키톤 팀원들에게 내세울 수 있는 나만의 필살기 역량!",
    "내가 밤새워 몰입할 수 있는 관심 분야는?",
    "우리 학교(또는 내 전공)의 가장 큰 자랑거리 한 가지!",
    "내가 제일 잘 다루는 프로그램/기술/도구는?",
    "돈을 무제한 지원받는다면 창업하고 싶은 아이템은?",
    "스티브 잡스처럼 멋지게 발표할 때 나에게 필요한 것은?",
    "일상에서 가장 불편해서 꼭 새로 만들고 싶은 제품은?",
    "우리 학교 매점에 꼭 도입하고 싶은 창업 아이템은?",
    "내가 미래에 대표(CEO)가 된다면 만들고 싶은 사내 복지는?",
    "이번 루키톤 우승 상금을 받는다면 어디에 쓸 것인가?",
    "팀 프로젝트 할 때 제일 선호하는 나의 역할(리더/아이디어/발표 등)?",
    "팀 프로젝트 할 때 가장 피하고 싶은 팀원 유형은?",
    "팀 프로젝트 할 때 최고라고 생각하는 팀원 유형은?",
    "아이디어가 안 떠올라 막힐 때 내가 하는 행동은?",
    "창업 아이템 피칭(발표)할 때 가장 중요한 요소는?",
    "우리 팀 아이디어를 한 줄로 나타내는 슬로건은?",
    "대학생 서포터즈 형/누나들에게 가장 궁금한 점 한 가지!",
    "멘토님에게 꼭 배워가고 싶은 노하우 한 가지!",
    "1년 안에 10억을 벌 수 있는 신박한 서비스 아이디어는?",
    "세상에 없던 새로운 배달/스마트 서비스 아이디어는?",
    "10대만을 위한 맞춤형 금융/생활 앱 기능 아이디어는?",
    "소비자의 마음을 3초 만에 사로잡는 마케팅 문구는?",
    "내가 만들고 싶은 창업 동아리 이름은?",
    "내가 만약 인공지능(AI)을 만든다면 어떤 AI를 만들까?",
    "특성화고 전공 기술을 살린 멋진 제조 아이디어는?",
    "문경의 특산물(사과, 오미자)을 활용한 기발한 상품은?",
    "실패해도 다시 일어서는 기업가정신을 한 단어로 표현하면?",
    "내가 제일 자랑스러워하는 나의 소소한 성과 한 가지!",
    "10대/20대 사이에서 가장 대박 날 것 같은 사업 분야는?",
    "우리 팀 분위기를 한 단어로 표현한다면?",
    "해보고 싶은 최고의 로컬/지역 재생 프로젝트 아이디어는?",
    "나만의 창의력을 끌어올리는 비밀 시간/장소는?",
    "이번 루키톤을 통해 얻어가고 싶은 최종 목표는?",
    "미래의 나에게 전달하고 싶은 한마디 응원은?",

    # 4. 취향 선택 밸런스 게임 문항
    "부먹 VS 찍먹, 나의 선택과 이유는?",
    "민트초코 호 VS 불호, 나의 입장은?",
    "파인애플 피자 호 VS 불호, 나의 입장은?",
    "평생 라면 안 먹기 VS 평생 탄산음료 안 먹기?",
    "평생 스마트폰 없이 살기 VS 평생 친구 없이 살기?",
    "하루 동안 과거로 가기 VS 하루 동안 미래로 가기?",
    "여름에 에어컨 없이 살기 VS 겨울에 히터 없이 살기?",
    "양념치킨 VS 후라이드치킨?",
    "평생 겨울만 계속되기 VS 평생 여름만 계속되기?",
    "평생 고기 안 먹기 VS 평생 밀가루 안 먹기?",
    "얼굴이 완벽한 미남/미녀 되기 VS 통장에 100억 있기?",
    "친한 친구와 같은 사람 좋아하기 VS 원수와 같은 팀 되기?",
    "노래 절대 못 부르기 VS 춤 절대 못 추기?",
    "매일 아침 6시 일어나는 삶 VS 매일 밤 3시 자는 삶?",
    "평생 소금 없이 먹기 VS 평생 설탕 없이 먹기?",
    "스마트폰 액정 깨진 채 살기 VS 배터리 최대 50%로 살기?",
    "말이 너무 많은 사람과 여행 VS 한마디도 안 하는 사람과 여행?",
    "평생 와이파이 안 터지기 VS 평생 데이터 3G로 살기?",
    "내 모든 인터넷 검색기록 공개 VS 내 단톡방 대화내역 공개?",
    "매일 삼시세끼 탕수육 먹기 VS 매일 삼시세끼 국밥 먹기?",
    "무인도에 혼자 갇히기 VS 제일 싫어하는 사람과 갇히기?",
    "평생 칫솔 없이 살기 VS 평생 수건 없이 살기?",
    "내가 좋아하는 사람이 나 싫어함 VS 내가 싫어하는 사람이 나 좋아함?",
    "지금 당장 루키톤 우승하기 VS 10년 뒤 100억 자산가 되기?",
    "평생 짜장면만 먹기 VS 평생 짬뽕만 먹기?",
    "평생 이어폰 없이 음악 듣기 VS 평생 자막 없이 영화 보기?",
    "아침에 일찍 일어나기 VS 밤늦게까지 안 자고 버티기?",
    "산으로 여행 가기 VS 바다로 여행 가기?",
    "콜라 VS 사이다?",
    "김치찌개 VS 된장찌개?",
    "매운 음식 잘 먹기 VS 달콤한 디저트 잘 먹기?",
    "노트북으로 작업하기 VS 태블릿/스마트폰으로 작업하기?",
    "집순이/집돌이 VS 무조건 나가 놀기?",
    "계획대로 움직이기(J) VS 즉흥적으로 움직이기(P)?",
    "현실적인 생각 위주(S) VS 상상력 풍부한 생각 위주(N)?"
]

# CSS 스타일링
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    .main-title { text-align: center; font-size: 2.2rem; font-weight: bold; color: #FFD166; margin-bottom: 20px; }
    
    div[data-testid="stExpander"] { background-color: #1e1e1e !important; border: 2px solid #333 !important; border-radius: 18px !important; }
    div[data-testid="stExpander"] summary { background-color: #2b2b36 !important; color: #FFD166 !important; font-weight: bold !important; font-size: 1.15rem !important; border-radius: 14px !important; }
    
    div.stButton > button {
        background: linear-gradient(135deg, #06D6A0, #118AB2) !important;
        color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        border-radius: 50px !important;
        border: none !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 10px rgba(6, 214, 160, 0.3) !important;
    }
    div.stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #FF70A6, #FF5964) !important;
        color: #ffffff !important;
    }
    
    .start-btn button {
        background: linear-gradient(135deg, #FFD166, #FF9F1C) !important;
        color: #121212 !important;
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        padding: 18px !important;
        border-radius: 50px !important;
    }
    
    .pass-btn button {
        background: linear-gradient(135deg, #06D6A0, #04A777) !important;
        color: #ffffff !important;
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        padding: 18px !important;
        border-radius: 50px !important;
        box-shadow: 0 6px 18px rgba(6, 214, 160, 0.5) !important;
    }
    
    .wait-box {
        background-color: #1e1e1e;
        border: 2px dashed #FFD166;
        border-radius: 18px;
        padding: 15px;
        text-align: center;
        font-size: 1.2rem;
        color: #FFD166;
        font-weight: bold;
    }

    .keyword-card { background-color: #1e1e1e; border-radius: 18px; padding: 22px; text-align: center; font-size: 1.7rem; font-weight: bold; color: #FFD166; border: 2px solid #333; margin-bottom: 20px; line-height: 1.4; }
    .name-card { background-color: #2b2b36; border-radius: 24px; padding: 30px; text-align: center; font-size: 3.5rem; font-weight: bold; color: #FFD166; margin: 20px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    .exploded-card { background-color: #381a1d; border-radius: 24px; padding: 30px; text-align: center; font-size: 3.5rem; font-weight: bold; color: #FF5964; border: 3px solid #FF5964; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🚀 2026 YUnicorn 루키톤<br>스피드 TMI 서바이벌</div>", unsafe_allow_html=True)

# ----------------------------------------------------
# [1] 기기 세션 로그인 & 명단 관리 (방장 제외 로직)
# ----------------------------------------------------
if "my_name" not in st.session_state:
    st.session_state["my_name"] = ""

with st.expander("🙋‍♂️ 내 이름 등록 / 접속자 확인", expanded=True):
    col_host_check, _ = st.columns([3, 1])
    is_host = col_host_check.checkbox("👑 방장(진행자)으로 접속하기 (지목 제외)", value=(st.session_state["my_name"] == "방장"))
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if is_host:
            st.session_state["my_name"] = "방장"
            st.info("👑 현재 '방장(진행자)' 권한입니다. 폭탄 지목 대상에서 제외됩니다.")
        else:
            input_name = st.text_input("이름 입력", value=("" if st.session_state["my_name"] == "방장" else st.session_state["my_name"]), placeholder="본인 이름을 입력하세요", label_visibility="collapsed")
    
    with col2:
        if not is_host and st.button("✨ 등록", use_container_width=True):
            if input_name and input_name != "방장":
                st.session_state["my_name"] = input_name
                if input_name not in game_state["students"]:
                    game_state["students"].append(input_name)
                    game_state["last_update"] = time.time()
                st.rerun()

    if st.session_state["my_name"] and st.session_state["my_name"] != "방장":
        st.success(f"📱 이 기기는 **[{st.session_state['my_name']}]** 님의 화면입니다.")
        
    if game_state["students"]:
        st.write(f"**현재 생존 학생 참가자 ({len(game_state['students'])}명):**")
        tags = " ".join([f"`👤 {name}`" for name in game_state["students"]])
        st.markdown(tags)
        
        if (is_host or st.session_state["my_name"] == "방장") and st.button("🧹 전체 명단 초기화", type="secondary"):
            game_state["students"] = []
            game_state["is_active"] = False
            game_state["used_keywords"] = []
            game_state["last_update"] = time.time()
            st.rerun()
    else:
        st.info("학생들은 본인 이름을 등록해주세요!")

st.divider()

# 무작위 주제 추출
def get_random_keyword():
    available = [k for k in KEYWORDS_DB if k not in game_state["used_keywords"]]
    if not available:
        game_state["used_keywords"] = []
        available = KEYWORDS_DB
    
    selected = random.choice(available)
    game_state["used_keywords"].append(selected)
    return selected

# ----------------------------------------------------
# [2] 게임 진행 및 자동 당사자/방장 버튼 컨트롤
# ----------------------------------------------------
if not game_state["students"]:
    st.warning("⚠️ 학생 참가자를 1명 이상 등록해 주세요.")
else:
    # 1) 게임 시작 전/종료 상태
    if not game_state["is_active"] or game_state["is_exploded"]:
        st.markdown("<div class='start-btn'>", unsafe_allow_html=True)
        if st.button("🚀 게임 시작 (폭탄 돌리기 시작!)", use_container_width=True):
            game_state["current_student"] = random.choice(game_state["students"])
            game_state["current_keyword"] = get_random_keyword()
            game_state["is_active"] = True
            game_state["is_exploded"] = False
            game_state["start_time"] = time.time()
            game_state["last_update"] = time.time()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # 2) 게임 진행 중 상태 (학생 당사자 or 방장만 제어 가능)
    else:
        current_target = game_state["current_student"]
        my_name = st.session_state["my_name"]

        # [당사자 또는 방장 화면]: 패스 버튼 노출
        if my_name == current_target or my_name == "방장" or is_host:
            st.markdown("<div class='pass-btn'>", unsafe_allow_html=True)
            btn_label = "▶️ 외쳤다! 다음 사람에게 패스" if my_name == current_target else f"👑 [방장 권한] {current_target} 님 답변 완료 -> 패스"
            if st.button(btn_label, use_container_width=True):
                candidates = [s for s in game_state["students"] if s != current_target]
                if not candidates:
                    candidates = game_state["students"]
                    
                game_state["current_student"] = random.choice(candidates)
                game_state["current_keyword"] = get_random_keyword()
                game_state["start_time"] = time.time() # 7초 리셋
                game_state["last_update"] = time.time()
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
        # [타인 화면]: 대기 안내문 표시
        else:
            st.markdown(f"<div class='wait-box'>⏳ 현재 [{current_target}] 님이 답변 중입니다. (대기 중...)</div>", unsafe_allow_html=True)

# ----------------------------------------------------
# [3] 화면 연출 및 타이머 처리
# ----------------------------------------------------
if game_state["is_active"]:
    st.markdown(f"<div class='keyword-card'>📌 {game_state['current_keyword']}</div>", unsafe_allow_html=True)
    
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
        name_placeholder.markdown(f"<div class='exploded-card'>💥 {game_state['current_student']} 님 탈락! 💥</div>", unsafe_allow_html=True)

# 대기 상태 시 2초 자동 폴링
if not game_state["is_active"]:
    time.sleep(2)
    st.rerun()