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
        "last_update": time.time(),
        "used_keywords": [] # 주제 중복 방지 리스트
    }

game_state = get_shared_game_state()

# ----------------------------------------------------
# [150개+ 대규모 키워드/문제 데이터베이스]
# ----------------------------------------------------
KEYWORDS_DB = [
    # 1. 넌센스 & 재치 센스 퀴즈 (50개)
    "왕이 넘어지면? (Answer: 바비큐)",
    "세상에서 가장 가난한 왕은? (Answer: 최저임금)",
    "오리가 도망치면? (Answer: 덕아웃)",
    "신발이 화나면? (Answer: 신발끈)",
    "아몬드가 죽으면? (Answer: 다이아몬드)",
    "초콜릿이 외로우면? (Answer: 외로움타)",
    "아이스크림이 차 사고 나면? (Answer: 차갑다)",
    "피자가 웃으면? (Answer: 피자웃)",
    "새가 날아가다 떨어지면? (Answer: 추락)",
    "사과가 웃으면? (Answer: 풋사과)",
    "바나나가 웃으면? (Answer: 바나나웃)",
    "수박 한 통에 1,000원, 두 통엔? (Answer: 두통)",
    "숫자 5가 제일 싫어하는 집은? (Answer: 오페라하우스)",
    "김밥이 경찰서에 간 이유는? (Answer: 옆구리가 터져서)",
    "세상에서 가장 지루한 중학교는? (Answer: 로딩중)",
    "세상에서 가장 빠른 약은? (Answer: 알약)",
    "사람을 다 살리는 산은? (Answer: 살릴산)",
    "다리가 4개인데 못 걷는 것은? (Answer: 책상/의자)",
    "모두를 일어서게 만드는 숫자? (Answer: 다섯)",
    "싸움을 제일 잘하는 오리는? (Answer: 을지문덕)",
    "소가 노래를 부르면? (Answer: 소송)",
    "세상에서 가장 긴 빈 빈 병은? (Answer: 긴병)",
    "자동차가 울면? (Answer: 잉카)",
    "새 중에 제일 아픈 새는? (Answer: 병새)",
    "불이 4곳에 나면? (Answer: 사파이어)",
    "칼이 울면? (Answer: 칼칼)",
    "우유가 아프면? (Answer: 앙팡)",
    "개구리가 노래를 못하는 이유? (Answer: 개굴개굴해서)",
    "할머니가 가장 좋아하는 악기? (Answer: 할미카)",
    "세상에서 가장 야한 채소는? (Answer: 버섯)",
    "물고기의 반대말은? (Answer: 불고기)",
    "양초 농장에 불이 나면? (Answer: 캔들파티)",
    "세상에서 제일 행복한 흥부는? (Answer: 흥부자)",
    "별 중에 가장 슬픈 별은? (Answer: 이별)",
    "콩 한 개를 영어로 하면? (Answer: 원두)",
    "바람이 귀엽게 불면? (Answer: 분다분다)",
    "비빔밥이 비벼지기 전에 하는 말? (Answer: 비비디바비디부)",
    "세상에서 제일 단 공은? (Answer: 알사탕)",
    "침대를 밀고 달리면? (Answer: 침대배송)",
    "소나무가 화나면? (Answer: 폼나네)",
    "약은 약인데 먹을 수 없는 약? (Answer: 치약)",
    "항상 미안해하는 연예인은? (Answer: 지성)",
    "세상에서 가장 똑똑한 새는? (Answer: 하버드)",
    "신사가 자기소개할 때 하는 말? (Answer: 신사임당)",
    "펭귄이 다니는 고등학교는? (Answer: 냉장고)",
    "토끼가 제일 잘하는 운동은? (Answer: 점프)",
    "세상에서 가장 뜨거운 과일은? (Answer: 천도복숭아)",
    "식빵이 길을 가다 넘어지면? (Answer: 프렌치토스트)",
    "소문난 잔치에 먹을 것 없다를 줄이면? (Answer: 꽝)",
    "창문이 깨질 때 나는 소리? (Answer: 와창)",

    # 2. 루키톤 & 창업/기술/아이디어 (35개)
    "전 세계를 바꾼 3대 사과 브랜드는?",
    "상상 속 기술을 실제로 만든다면 어떤 기술?",
    "일상에서 제일 불편해서 바꿔버리고 싶은 물건",
    "우리 학교 매점에 꼭 도입하고 싶은 스타트업 아이템",
    "돈을 무제한 지원받는다면 창업하고 싶은 분야",
    "스티브 잡스처럼 멋지게 발표할 때 필요한 필수 요소",
    "전 세계에서 인공지능(AI)이 대신할 수 없는 직업 1가지",
    "내가 미래에 대표(CEO)가 된다면 회사에 만들 사내 복지",
    "문경의 특산물(사과, 오미자 등)로 만들 수 있는 창업 아이템",
    "요즘 MZ세대가 돈을 아끼지 않고 쓰는 곳",
    "스마트폰 다음 세대를 이끌 미래 신기술 제품",
    "전 세계 인류를 구할 수 있는 미래 에너지 기술",
    "내가 만든 앱이 구글에서 1,000억에 팔린다면 제일 먼저 할 일",
    "실패해도 다시 일어서는 '기업가정신'을 한 단어로 표현하면?",
    "우리 팀 멘토님에게 배워보고 싶은 핵심 노하우",
    "학교 수업에 꼭 도입해야 할 유용한 AI 툴",
    "우리 동네(지역)를 핫플레이스로 만드는 로컬 아이디어",
    "쓰레기를 줄이거나 재활용하는 친환경 창업 아이디어",
    "요즘 10대들 사이에서 가장 유행하는 플랫폼/앱",
    "팀 프로젝트 할 때 제일 짜증 나는 빌런 유형",
    "팀 프로젝트 할 때 최고의 팀원 유형",
    "아이디어가 안 떠오를 때 내가 하는 일",
    "1년 안에 10억 버는 기발한 서비스 아이디어",
    "세상에 없던 새로운 배달 서비스 아이디어",
    "10대만을 위한 맞춤형 핀테크(금융) 앱 기능",
    "요즘 가장 인기 있는 생성형 AI 툴 이름",
    "창업 아이템 피칭(발표)할 때 절대 하면 안 되는 행동",
    "소비자의 주머니를 열게 만드는 3초 마케팅 기법",
    "내가 창업하면 채용하고 싶은 최고의 인재상",
    "고등학생만의 패기와 기술력이 결합된 최고의 시너지",
    "창업 동아리를 만든다면 붙이고 싶은 멋진 이름",
    "성공적인 사업계획서(BMC) 작성 시 가장 중요한 요소",
    "우리 팀 아이디어를 한 줄로 요약하는 슬로건",
    "특성화고 전공 기술을 살린 제조 스타트업 아이디어",
    "대학생 서포터즈 형/누나들과 같이 해보고 싶은 액티비티",

    # 3. 학교/대학/일상 & 공감 100% (35개)
    "학교 시험 1분 전에 내가 하는 행동",
    "시험 끝난 당일 제일 먼저 하고 싶은 것",
    "수업 시간에 안 졸기 위해 해본 신박한 방법",
    "급식표에서 이 메뉴 나오면 무조건 줄 1등으로 서는 음식",
    "학원/학교 땡땡이치고 가고 싶은 완벽한 장소",
    "선생님 몰래 교실 뒷자리에서 먹기 좋은 간식",
    "고등학교 생활 중 가장 잊지 못할 레전드 사건",
    "대학생이 되면 제일 먼저 해보고 싶은 로망",
    "용돈 받자마자 바로 플렉스(FLEX)하는 항목",
    "내가 아는 제일 쓸데없는 TMI 정보",
    "내 인생 최고의 영화 또는 인생 드라마",
    "내가 노래방 가며 무조건 부르는 18번 곡",
    "시험 기간에 꼭 찾아오는 마법 같은 법칙",
    "야자(야간자율학습) 시간에 시간 제일 잘 가는 방법",
    "시험 답 찍을 때 나만의 필승 법칙",
    "친구 단톡방에서 제일 많이 쓰는 이모티콘 종류",
    "내가 하루 중 가장 행복하다고 느끼는 순간",
    "주말 아침 11시에 내가 하고 있는 일",
    "스마트폰 배터리 1% 남았을 때 나의 대처법",
    "내 인생 최고의 맛집 한 곳 추천",
    "내가 제일 좋아하는 배달 음식 조합",
    "스트레스 폭발했을 때 먹는 매운 음식",
    "다시 태어난다면 해보고 싶은 직업",
    "100만 유튜버가 된다면 내 채널 주제",
    "내가 만약 하루 동안 투명인간이 된다면?",
    "내가 만약 복권 1등(30억)에 당첨된다면?",
    "가장 좋아하는 무인도 필수 소지품 3가지",
    "나만의 무기이자 숨겨진 특기/장기",
    "아침 등교 시간에 안 늦는 나만의 꿀팁",
    "내 책상 위에 항상 놓여있는 필수 아이템",
    "요즘 제일 빠져있는 유튜브 채널 또는 쇼츠 분야",
    "친구랑 싸웠을 때 자연스럽게 화해하는 꿀팁",
    "내가 세상에서 제일 싫어하는 음식/상황",
    "월요일 아침마다 드는 솔직한 생각",
    "나의 MBTI와 그 MBTI의 가장 큰 특징",

    # 4. 벨런스 게임 & 매운맛 취향 타투 (35개)
    "평생 라면 안 먹기 VS 평생 탄산음료 안 먹기",
    "재입대하기 VS 고3 시험기간으로 돌아가기",
    "평생 스마트폰 없이 살기 VS 평생 친구 없이 살기",
    "하루 동안 과거로 가기 VS 하루 동안 미래로 가기",
    "모든 사람에게 비밀 들키기 VS 평생 혼자 외롭게 살기",
    "여름에 에어컨 없이 살기 VS 겨울에 히터 없이 살기",
    "양념치킨 VS 후라이드치킨",
    "민트초코 호 VS 민트초코 불호",
    "파인애플 피자 호 VS 파인애플 피자 불호",
    "부먹 VS 찍먹",
    "평생 겨울만 계속되기 VS 평생 여름만 계속되기",
    "10억 받고 5년 동안 아무도 안 만나기 VS 그냥 살기",
    "내 비밀이 전교에 소문나기 VS 내가 친구 비밀 실수로 말하기",
    "평생 고기 안 먹기 VS 평생 밀가루 안 먹기",
    "자고 일어났더니 얼굴이 차은우/장원영 VS 통장에 100억",
    "하루 동안 새처럼 날기 VS 하루 동안 물고기처럼 수영하기",
    "친한 친구와 같은 사람 좋아하기 VS 원수와 같은 팀 되기",
    "노래 절대 못 부르기 VS 춤 절대 못 추기",
    "매일 아침 6시 일어나는 삶 VS 매일 밤 3시 자는 삶",
    "평생 소금 없이 먹기 VS 평생 설탕 없이 먹기",
    "스마트폰 액정 깨진 채 살기 VS 배터리 최대 50%로 살기",
    "말이 너무 많은 사람과 여행 VS 한마디도 안 하는 사람과 여행",
    "하루 동안 개가 되기 VS 하루 동안 고양이가 되기",
    "평생 와이파이 안 터지기 VS 평생 데이터 3G로 살기",
    "내 모든 인터넷 검색기록 공개 VS 내 단톡방 대화내역 공개",
    "매일 삼시세끼 탕수육 먹기 VS 매일 삼시세끼 국밥 먹기",
    "평생 신발 없이 다니기 VS 평생 양말 없이 다니기",
    "무인도에 혼자 갇히기 VS 제일 싫어하는 사람과 갇히기",
    "과거로 돌아가서 로또 번호 찍기 VS 미래로 가서 내 배우자 보고 오기",
    "평생 칫솔 없이 살기 VS 평생 수건 없이 살기",
    "모든 사람이 내 생각을 읽을 수 있음 VS 내가 모든 사람 생각을 읽음",
    "평생 이어폰 없이 음악 듣기 VS 평생 자막 없이 영화 보기",
    "키 190cm에 초거대 대머리 VS 키 150cm에 미남/미녀",
    "내가 좋아하는 사람이 나 싫어함 VS 내가 싫어하는 사람이 나 좋아함",
    "지금 당장 루키톤 우승하기 VS 10년 뒤 100억 자산가 되기"
]

# CSS 스타일링
st.markdown("""
    <style>
    /* 전체 배경 */
    .stApp { background-color: #121212; color: white; }
    .main-title { text-align: center; font-size: 2.2rem; font-weight: bold; color: #FFD166; margin-bottom: 20px; }
    
    /* Expander(접이식 창) 가독성 */
    div[data-testid="stExpander"] { background-color: #1e1e1e !important; border: 2px solid #333 !important; border-radius: 18px !important; }
    div[data-testid="stExpander"] summary { background-color: #2b2b36 !important; color: #FFD166 !important; font-weight: bold !important; font-size: 1.15rem !important; border-radius: 14px !important; }
    
    /* [기본 버튼] */
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
    
    /* [보조 버튼] - 전체 명단 초기화 */
    div.stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #FF70A6, #FF5964) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 10px rgba(255, 89, 100, 0.3) !important;
    }
    
    /* [게임 시작 버튼] */
    .start-btn button {
        background: linear-gradient(135deg, #FFD166, #FF9F1C) !important;
        color: #121212 !important;
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        padding: 18px !important;
        border-radius: 50px !important;
        border: none !important;
        box-shadow: 0 6px 18px rgba(255, 209, 102, 0.4) !important;
    }
    
    /* [패스 버튼] */
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
    .keyword-card { background-color: #1e1e1e; border-radius: 18px; padding: 22px; text-align: center; font-size: 1.7rem; font-weight: bold; color: #FFD166; border: 2px solid #333; margin-bottom: 20px; line-height: 1.4; }
    .name-card { background-color: #2b2b36; border-radius: 24px; padding: 30px; text-align: center; font-size: 3.5rem; font-weight: bold; color: #FFD166; margin: 20px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    .exploded-card { background-color: #381a1d; border-radius: 24px; padding: 30px; text-align: center; font-size: 3.5rem; font-weight: bold; color: #FF5964; border: 3px solid #FF5964; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🚀 2026 YUnicorn 루키톤<br>스피드 키워드 서바이벌 (150+ DB)</div>", unsafe_allow_html=True)

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
            game_state["used_keywords"] = []
            game_state["last_update"] = time.time()
            st.rerun()
    else:
        st.info("학생들은 이름을 입력하고 '✨ 등록' 버튼을 눌러주세요!")

st.divider()

# 중복 없는 무작위 주제 추출 함수
def get_random_keyword():
    available = [k for k in KEYWORDS_DB if k not in game_state["used_keywords"]]
    if not available: # 150개 전부 소진되면 리셋
        game_state["used_keywords"] = []
        available = KEYWORDS_DB
    
    selected = random.choice(available)
    game_state["used_keywords"].append(selected)
    return selected

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
            game_state["current_keyword"] = get_random_keyword()
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
            game_state["current_keyword"] = get_random_keyword()
            game_state["start_time"] = time.time() # 5초 타이머 리셋
            game_state["last_update"] = time.time()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

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
        name_placeholder.markdown(f"<div class='exploded-card'>💥 {game_state['current_student']} 당첨! 💥</div>", unsafe_allow_html=True)

# 대기 상태 시 2초 자동 폴링
if not game_state["is_active"]:
    time.sleep(2)
    st.rerun()