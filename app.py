import streamlit as st
import json
import os

# ════════════════════════════════════════════
# [필수] 캐싱 ① - 퀴즈 데이터
# 앱 실행 중 변하지 않는 퀴즈 문항을 한 번만 로드.
# 페이지 전환/rerun 시 재로딩 없이 메모리에서 즉시 반환.
# ════════════════════════════════════════════
@st.cache_data
def get_quiz_data():
    return {
        "trivia_easy": [
            {"q": "엘소드의 고향은 어디인가요?",       "a": ["엘더", "벨더", "루벤", "강철 기계 성벽"],        "correct": "루벤"},
            {"q": "붉은 기사단의 단장은 누구인가요?",   "a": ["엘소드", "엘리시스", "아이샤", "바르가트"],      "correct": "엘리시스"},
            {"q": "엘이 봉인된 장소는 어디인가요?",     "a": ["엘하임", "엘리오스", "엘더", "엘리아노드"],      "correct": "엘리오스"},
            {"q": "레나의 종족은?",                    "a": ["인간", "마족", "엘프", "나소드"],                "correct": "엘프"},
            {"q": "루벤 마을을 지키는 기사단 이름은?",  "a": ["붉은 기사단", "성검 기사단", "엘 기사단"],       "correct": "붉은 기사단"},
        ],
        "trivia_hard": [
            {"q": "다음중 캐릭터 이브의 스킬은?",
             "a": ["섬멸의 문장", "징벌의 문장", "시공간의 문장", "전충의 문장", "힘의 문장"],
             "correct": "섬멸의 문장"},
            {"q": "캐릭터 아라의 스킬에는 제압이 있습니다. 다음 중 전직과 맞지 않는 제압은 무엇인가요?",
             "a": ["비천-제압:정", "범황-제압:기", "대라-제압:술", "일천-제압:도"],
             "correct": "대라-제압:술"},
            {"q": "다음중 파티원들에게 줄 수 있는 버프 스킬은 무엇인가요??",
             "a": ["이브-샹들리에", "청-체인지 택티컬 필드", "루시엘-이노센트 스타터", "아이샤-공간왜곡"],
             "correct": "청-체인지 택티컬 필드"},
            {"q": "영락의 탑:활 에서 볼 수 없는 문구는?",
             "a": ["이것은 하나의 점.", "가장 강력한 행운이자 무시무시한 악의 주문", "빛과 어둠, 나와 타인, 옳고 그름", "세피로스 판타즈마"],
             "correct": "세피로스 판타즈마"},
            {"q": "레나의 전직 중 하나인 아네모스는 템페스트 라는 스킬이 있습니다. 템페스트는 키 입력 후 일정시간 기다리면 데미지가 최대가 되며, 시간이 초과되면 스킬 취소가 됩니다. 최대 데미지가 되는 시간은 몇 초일까요",
             "a": ["3초", "5초", "7초", "10초", "13초"],
             "correct": "10초"},
        ],
    }


# ════════════════════════════════════════════
# [필수] 캐싱 ② - 캐릭터 데이터 (40개)
# 대용량 정적 데이터를 캐싱해 매 rerun마다
# 리스트를 새로 생성하지 않도록 최적화.
# ════════════════════════════════════════════
@st.cache_data
def get_char_data():
    return [
        # ── 엘소드 ──
        {"name":"엘소드",   "title":"나이트 엠퍼러",     "gender":"남자",     "attack":"물리","role":"메인딜러","speed":"보통","range":"근거리","diff":"쉬움",  "desc":"스스로의 의지로 나아가는 엘리오스의 검",                          "img":"images/Knight_Emperor.png"},
        {"name":"엘소드",   "title":"룬 마스터",         "gender":"남자",     "attack":"마법","role":"서브딜러","speed":"보통","range":"중거리","diff":"쉬움",  "desc":"자신만의 룬검술을 구축한 최강의 마검사",                          "img":"images/Rune_Master.png"},
        {"name":"엘소드",   "title":"임모탈",            "gender":"남자",     "attack":"물리","role":"메인딜러","speed":"보통","range":"근거리","diff":"쉬움",  "desc":"어둠을 제압하고 한계를 뛰어넘은 무한의 검사",                     "img":"images/Immortal.png"},
        {"name":"엘소드",   "title":"제네시스",          "gender":"남자",     "attack":"마법","role":"메인딜러","speed":"보통","range":"중거리","diff":"보통",  "desc":"엘과 엘리오스를 위해 존재하는 수호기사",                          "img":"images/Genesis.png"},
        # ── 아이샤 ──
        {"name":"아이샤",   "title":"에테르 세이지",     "gender":"여자",     "attack":"마법","role":"메인딜러","speed":"느림","range":"원거리","diff":"보통",  "desc":"원소술의 극한, '에테르'를 깨우친 현자",                           "img":"images/Aether_Sage.png"},
        {"name":"아이샤",   "title":"오즈 소서러",       "gender":"여자",     "attack":"마법","role":"메인딜러","speed":"느림","range":"중거리","diff":"어려움","desc":"진정한 흑마법의 정점",                                           "img":"images/Oz_Sorcerer.png"},
        {"name":"아이샤",   "title":"메타모르피",        "gender":"여자",     "attack":"물리","role":"서브딜러","speed":"보통","range":"근거리","diff":"보통",  "desc":"우주 최강의 마법소녀 등장!",                                     "img":"images/Metamorphy.png"},
        {"name":"아이샤",   "title":"로드 아조트",       "gender":"여자",     "attack":"물리","role":"메인딜러","speed":"보통","range":"중거리","diff":"어려움","desc":"현자의 돌과 하나가 된 불멸자",                                    "img":"images/Lord_Azoth.png"},
        # ── 레나 ──
        {"name":"레나",     "title":"아네모스",          "gender":"여자",     "attack":"물리","role":"메인딜러","speed":"보통","range":"근거리","diff":"보통",  "desc":"바람과 하나가 되어 적들을 휩쓰는 엘프 격투가",                    "img":"images/Anemos.png"},
        {"name":"레나",     "title":"데이브레이커",      "gender":"여자",     "attack":"마법","role":"메인딜러","speed":"보통","range":"원거리","diff":"쉬움",  "desc":"정령계의 수호를 받는 숭고한 엘프의 인도자",                       "img":"images/DayBreaker.png"},
        {"name":"레나",     "title":"트와일라잇",        "gender":"여자",     "attack":"물리","role":"메인딜러","speed":"보통","range":"중거리","diff":"어려움","desc":"자연의 그림자들을 이끄는 우아한 밤의 감시자",                     "img":"images/Twilight.png"},
        {"name":"레나",     "title":"프로피티스",        "gender":"여자",     "attack":"마법","role":"서브딜러","speed":"보통","range":"원거리","diff":"어려움","desc":"세상의 목소리를 전하는 선지자",                                   "img":"images/Prophetis.png"},
        # ── 레이븐 ──
        {"name":"레이븐",   "title":"퓨리어스 블레이드", "gender":"남자",     "attack":"물리","role":"메인딜러","speed":"빠름","range":"근거리","diff":"어려움","desc":"인간으로서 검술의 극한에 도달한 초신속의 검사",                  "img":"images/Furious_Blade.png"},
        {"name":"레이븐",   "title":"레이지 하츠",       "gender":"남자",     "attack":"마법","role":"메인딜러","speed":"보통","range":"근거리","diff":"보통",  "desc":"나소드의 힘과 공존함으로서 한계를 넘어선 투사",                   "img":"images/Rage_Hearts.png"},
        {"name":"레이븐",   "title":"노바 임퍼레이터",   "gender":"남자",     "attack":"마법","role":"메인딜러","speed":"보통","range":"중거리","diff":"어려움","desc":"자기 자신조차 무기로 활용하는 냉철한 전략가",                    "img":"images/Nova_Imperator.png"},
        {"name":"레이븐",   "title":"레버넌트",          "gender":"남자",     "attack":"물리","role":"서브딜러","speed":"보통","range":"중거리","diff":"어려움","desc":"복수의 길을 걷는 망령기사",                                      "img":"images/Revenant.png"},
        # ── 이브 ──
        {"name":"이브",     "title":"코드: 얼티메이트",  "gender":"여자",     "attack":"마법","role":"메인딜러","speed":"빠름","range":"근거리","diff":"어려움","desc":"나소드의 한계를 초월한 파괴의 여왕",                              "img":"images/Code_Ultimate.png"},
        {"name":"이브",     "title":"코드: 에센시아",    "gender":"여자",     "attack":"물리","role":"서브딜러","speed":"보통","range":"중거리","diff":"보통",  "desc":"자애로운 순백의 나소드 황제",                                    "img":"images/Code_Esencia.png"},
        {"name":"이브",     "title":"코드: 사리엘",      "gender":"여자",     "attack":"마법","role":"메인딜러","speed":"빠름","range":"원거리","diff":"쉬움",  "desc":"시리도록 찬란한 섬광의 나소드 여왕",                              "img":"images/Code_Sariel.png"},
        {"name":"이브",     "title":"코드: 안티테제",    "gender":"여자",     "attack":"물리","role":"메인딜러","speed":"빠름","range":"원거리","diff":"보통",  "desc":"반기를 드는 모든것을 배제하는 절멸의 여왕",                       "img":"images/Code_Antithese.png"},
        # ── 청 ──
        {"name":"청",       "title":"코멧 크루세이더",   "gender":"남자",     "attack":"물리","role":"메인딜러","speed":"보통","range":"근거리","diff":"쉬움",  "desc":"전장의 중심에 혜성처럼 뛰어들어 적을 제압하는 전장의 수호자",    "img":"images/Comet_Crusader.png"},
        {"name":"청",       "title":"페이탈 팬텀",       "gender":"남자",     "attack":"마법","role":"메인딜러","speed":"빠름","range":"원거리","diff":"보통",  "desc":"인지할 수 없는 속도로 상대를 꿰뚫는 마탄의 사수",               "img":"images/Fatal_Phantom.png"},
        {"name":"청",       "title":"센츄리온",          "gender":"남자",     "attack":"마법","role":"메인딜러","speed":"느림","range":"중거리","diff":"보통",  "desc":"끝없는 탐구 끝에 물리적 한계를 뛰어넘은 포병",                   "img":"images/Centurion.png"},
        {"name":"청",       "title":"디우스 아에르",     "gender":"남자",     "attack":"물리","role":"서포터", "speed":"빠름","range":"중거리","diff":"보통",  "desc":"지켜야 하는 모든 이를 자애롭게 품는 성역",                       "img":"images/Dius_Aer.png"},
        # ── 아라 ──
        {"name":"아라",     "title":"비천",              "gender":"여자",     "attack":"물리","role":"서브딜러","speed":"빠름","range":"중거리","diff":"보통",  "desc":"무신의 경지에 도달한 백의의 선인(仙人)",                          "img":"images/Apsara.png"},
        {"name":"아라",     "title":"범황",              "gender":"여자",     "attack":"마법","role":"메인딜러","speed":"빠름","range":"원거리","diff":"어려움","desc":"죽음을 부르는 나락의 인도자",                                    "img":"images/Bumhwang.png"},
        {"name":"아라",     "title":"대라",              "gender":"여자",     "attack":"물리","role":"메인딜러","speed":"빠름","range":"근거리","diff":"쉬움",  "desc":"신수와의 유대로 탄생한 최초의 여우 신선",                         "img":"images/Deara.png"},
        {"name":"아라",     "title":"일천",              "gender":"여자",     "attack":"마법","role":"서포터", "speed":"빠름","range":"중거리","diff":"어려움","desc":"만물이 나아갈 길을 비추는 만물의 인도자",                         "img":"images/1000.png"},
        # ── 엘리시스 ──
        {"name":"엘리시스", "title":"엠파이어 소드",     "gender":"여자",     "attack":"물리","role":"서브딜러","speed":"보통","range":"근거리","diff":"보통",  "desc":"강력한 카리스마로 군중을 이끄는 벨더의 기사 단장",               "img":"images/Empire_Sword.png"},
        {"name":"엘리시스", "title":"플레임 로드",       "gender":"여자",     "attack":"마법","role":"메인딜러","speed":"보통","range":"중거리","diff":"보통",  "desc":"태초의 화염을 두른 불꽃의 화신",                                 "img":"images/Flame_Lord.png"},
        {"name":"엘리시스", "title":"블러디 퀸",         "gender":"여자",     "attack":"물리","role":"메인딜러","speed":"보통","range":"근거리","diff":"쉬움",  "desc":"피를 갈구하는 죽음의 기사",                                      "img":"images/Bloody_Queen.png"},
        {"name":"엘리시스", "title":"아드레스티아",      "gender":"여자",     "attack":"마법","role":"메인딜러","speed":"보통","range":"중거리","diff":"어려움","desc":"대물림되는 운명을 끊어내고 진정으로 엘리오스를 지키는 수호의 검", "img":"images/Adrestia.png"},
        # ── 애드 ──
        {"name":"애드",     "title":"둠브링어",          "gender":"남자",     "attack":"마법","role":"메인딜러","speed":"보통","range":"중거리","diff":"보통",  "desc":"물리법칙을 초월한 궁극적인 파괴의 화신",                          "img":"images/Doom_Bringer.png"},
        {"name":"애드",     "title":"도미네이터",        "gender":"남자",     "attack":"물리","role":"서브딜러","speed":"보통","range":"원거리","diff":"어려움","desc":"궁극적인 전뇌 세계를 완성해낸 매드 사이언티스트",                "img":"images/Dominator.png"},
        {"name":"애드",     "title":"매드 패러독스",     "gender":"남자",     "attack":"마법","role":"메인딜러","speed":"빠름","range":"중거리","diff":"어려움","desc":"끝없는 모순에 얽매여 시공간을 헤매는 패러독스의 악마",           "img":"images/Mad_Paradox.png"},
        {"name":"애드",     "title":"오버마인드",        "gender":"남자",     "attack":"물리","role":"서포터", "speed":"보통","range":"중거리","diff":"보통",  "desc":"선의라는 가면을 쓰고 군림하는 매드 닥터",                        "img":"images/Overmind.png"},
        # ── 루시엘 ──
        {"name":"루시엘",   "title":"카타스트로피",      "gender":"상관없음", "attack":"물리","role":"메인딜러","speed":"보통","range":"근거리","diff":"보통",  "desc":"자비 없이 상대를 압살하는 공포의 마왕",                          "img":"images/Catastrophe.png"},
        {"name":"루시엘",   "title":"이노센트",          "gender":"상관없음", "attack":"마법","role":"메인딜러","speed":"보통","range":"원거리","diff":"보통",  "desc":"서로를 지키는 최강의 창과 방패",                                 "img":"images/Innocent.png"},
        {"name":"루시엘",   "title":"디앙겔리온",        "gender":"상관없음", "attack":"물리","role":"메인딜러","speed":"빠름","range":"중거리","diff":"어려움","desc":"파괴의 마왕과 충실한 심복",                                     "img":"images/Diangelion.png"},
        {"name":"루시엘",   "title":"데메르시오",        "gender":"상관없음", "attack":"마법","role":"서포터", "speed":"보통","range":"중거리","diff":"보통",  "desc":"허무의 군주와 무자비한 보좌관",                                  "img":"images/Demersio.png"},
    ]

# ════════════════════════════════════════════
# [필수] 캐싱 ③ - 캐릭터 매칭 결과
# 동일한 선택 조합(6개 항목)에 대한 매칭 결과를 캐싱.
# 같은 조합을 다시 선택하면 재계산 없이 즉시 반환.
# ════════════════════════════════════════════
@st.cache_data
def match_character(gender, attack, role, speed, rang, diff):
    chars = get_char_data()
    scores = []
    for c in chars:
        s = 0
        if gender == "상관없음" or c["gender"] == gender: s += 1
        if attack  == "상관없음" or c["attack"]  == attack:  s += 1
        if role    == "상관없음" or c["role"]    == role:     s += 1
        if speed   == "상관없음" or c["speed"]   == speed:    s += 1
        if rang    == "상관없음" or c["range"]   == rang:     s += 1
        if diff    == "상관없음" or c["diff"]    == diff:     s += 1
        scores.append(s)
    best = max(scores)
    top  = [chars[i] for i, s in enumerate(scores) if s == best]
    return top, best


# ════════════════════════════════════════════
# JSON 유저 저장/불러오기
# ════════════════════════════════════════════
USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(user_db):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(user_db, f, ensure_ascii=False, indent=2)


# ════════════════════════════════════════════
# 세션 상태 초기화
# ════════════════════════════════════════════
defaults = {
    'page':            'intro',
    'user_db':         load_users(),
    'logged_in_user':  None,
    'logged_in_id':    None,
    'signup_finished': False,
    'login_error':     None,
    'quiz_mode':       None,
    'last_score':      None,
    'ranking_easy':    [],
    'ranking_hard':    [],
    'char_result':     None,   # 캐릭터 테스트 결과 저장 (단일 캐릭터 dict)
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ════════════════════════════════════════════
# 공통 CSS
# ════════════════════════════════════════════
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    min-height: 100vh;
}
[data-testid="stHeader"] { background: transparent; }
h1, h2, h3 { color: #e0e0ff !important; }
p, li       { color: #c0c8e8; }
label       { color: #c0c8ff !important; }

.card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    backdrop-filter: blur(10px);
}
.intro-box   { text-align: center; padding: 2.5rem 2rem; }
.intro-title { font-size: 1.5rem; font-weight: 800; color: #7eb8ff; margin-bottom: 0.4rem; }
.intro-sub   { font-size: 1rem; color: #a0b8e0; margin-bottom: 0.2rem; }

.menu-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 14px;
    padding: 1.4rem 1.2rem;
    margin-bottom: 0.8rem;
}
.menu-title { font-size: 1.1rem; font-weight: 700; color: #e0e0ff; margin-bottom: 0.25rem; }
.menu-desc  { font-size: 0.82rem; color: #a0a8cc; }

.footer {
    position: fixed; right: 12px; bottom: 10px;
    font-size: 10px; color: rgba(200,200,255,0.4); z-index: 9999;
}
.score-box {
    text-align: center;
    background: rgba(126,184,255,0.1);
    border: 1px solid rgba(126,184,255,0.3);
    border-radius: 14px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
}
.info-box {
    background: rgba(255,255,255,0.06);
    border-left: 3px solid #7eb8ff;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 1.2rem;
    font-size: 0.9rem;
    color: #c0d0f0;
    line-height: 1.7;
}

/* O/X 채점 */
.ox-row     { display:flex; align-items:center; gap:0.7rem; padding:0.45rem 0.7rem;
              border-radius:8px; margin-bottom:0.35rem; font-size:0.88rem; }
.ox-correct { background:rgba(80,200,120,0.12); border:1px solid rgba(80,200,120,0.3); }
.ox-wrong   { background:rgba(255,80,80,0.12);  border:1px solid rgba(255,80,80,0.3); }
.ox-mark    { font-size:1.1rem; font-weight:800; min-width:1.4rem; text-align:center; }
.ox-q       { color:#c0d0f0; flex:1; }
.ox-ans     { font-size:0.8rem; color:#a0b8cc; }

/* 랭킹 */
.rank-section-label {
    font-size:1rem; font-weight:700; color:#7eb8ff;
    text-align:center; margin-bottom:0.8rem;
    padding-bottom:0.4rem;
    border-bottom:1px solid rgba(126,184,255,0.35);
}
.rank-row {
    display:flex; justify-content:space-between; align-items:center;
    padding:0.45rem 0.6rem; border-radius:8px; margin-bottom:0.3rem;
    background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.08);
    font-size:0.88rem; color:#c0d0f0;
}
.rank-num   { min-width:1.6rem; font-weight:700; color:#7eb8ff; }
.rank-score { font-weight:700; color:#7eb8ff; }
.rank-empty { text-align:center; color:#506080; font-size:0.85rem; padding:1rem 0; }

/* 캐릭터 결과 페이지 */
.char-result-name  { font-size:1.6rem; font-weight:800; color:#7eb8ff; margin:0.3rem 0 0.1rem; }
.char-result-title { font-size:1.1rem; font-weight:600; color:#a0c8ff; margin-bottom:0.4rem; }
.char-result-role  {
    display:inline-block;
    font-size:0.82rem; font-weight:700;
    color:#1a1a2e;
    background:#7eb8ff;
    border-radius:20px;
    padding:0.2rem 0.9rem;
    margin-bottom:0.8rem;
}
.char-result-desc  { font-size:1rem; color:#c0d0f0; line-height:1.7; margin-top:0.4rem; }
.no-img-box {
    width:100%; aspect-ratio:1/1;
    background:rgba(126,184,255,0.08);
    border:2px dashed rgba(126,184,255,0.3);
    border-radius:16px;
    display:flex; align-items:center; justify-content:center;
    color:rgba(126,184,255,0.5); font-size:0.9rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="footer">2025404046 박수민</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════
# 헬퍼
# ════════════════════════════════════════════
def go(page):
    st.session_state.page = page
    st.rerun()

def add_ranking(mode, user_id, name, score, total):
    key = f'ranking_{mode}'
    lst = st.session_state[key]
    for entry in lst:
        if entry['id'] == user_id:
            if score > entry['score']:
                entry['score'] = score
                entry['total'] = total
            return
    lst.append({'id': user_id, 'name': name, 'score': score, 'total': total})

MEDALS = ["🥇", "🥈", "🥉"]

def render_ranking_column(mode_key, label):
    lst = sorted(
        st.session_state[f'ranking_{mode_key}'],
        key=lambda x: x['score'],
        reverse=True
    )
    st.markdown(f'<div class="rank-section-label">{label}</div>', unsafe_allow_html=True)
    if not lst:
        st.markdown('<div class="rank-empty">아직 기록이 없습니다.</div>', unsafe_allow_html=True)
    else:
        for i, entry in enumerate(lst[:5]):
            medal = MEDALS[i] if i < 3 else f"{i+1}위"
            st.markdown(
                f"<div class='rank-row'>"
                f"<span class='rank-num'>{medal}</span>"
                f"<span style='flex:1'>{entry['id']} "
                f"<span style='color:#7090b0;font-size:0.8rem;'>({entry['name']})</span></span>"
                f"<span class='rank-score'>{entry['score']}/{entry['total']}</span>"
                f"</div>",
                unsafe_allow_html=True
            )


# ════════════════════════════════════════════
# 인트로 화면
# ════════════════════════════════════════════
def intro_screen():
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.8, 1])
    with col:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("""
        <div class="intro-box">
            <div style="font-size:3rem; margin-bottom:1rem;">⚔️</div>
            <div class="intro-title">2025404046 박수민</div>
            <div class="intro-sub" style="margin-top:0.3rem; color:#7eb8ff; font-weight:600;">
                중간고사 대체 과제
            </div>
            <hr style="border-color:rgba(255,255,255,0.12); margin:1.2rem 0;">
            <div class="intro-sub">주제: 게임 관련 상식 퀴즈 및 성격 테스트</div>
            <div style="font-size:0.8rem; color:#7090b0; margin-top:0.5rem;">
                엘소드 / 엘리오스 상식 &amp; 캐릭터 취향 테스트
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        if st.button("GO! 🚀", use_container_width=True, type="primary", key="intro_go"):
            go('login')
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════
# 로그인 화면
# ════════════════════════════════════════════
def login_screen():
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.6, 1])
    with col:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            "<h1 style='text-align:center; font-size:1.8rem; margin-bottom:1.6rem;'>"
            "⚔️ 엘리오스 대륙 로그인</h1>",
            unsafe_allow_html=True
        )
        input_id = st.text_input("아이디 (ID)", key="login_id", placeholder="아이디를 입력하세요")
        input_pw = st.text_input("비밀번호 (PW)", type="password", key="login_pw",
                                  placeholder="비밀번호를 입력하세요")

        if st.session_state.login_error:
            st.error(st.session_state.login_error)

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        if st.button("로그인", use_container_width=True, type="primary", key="btn_login"):
            uid  = input_id.strip()
            upw  = input_pw
            db   = st.session_state.user_db
            id_ok = uid in db
            pw_ok = id_ok and db[uid]['pw'] == upw

            if not uid and not upw:
                st.session_state.login_error = "아이디와 비밀번호 둘 다 일치하지 않습니다."
                st.rerun()
            elif not id_ok:
                st.session_state.login_error = "아이디가 틀렸습니다."
                st.rerun()
            elif not pw_ok:
                st.session_state.login_error = "비밀번호가 틀렸습니다."
                st.rerun()
            else:
                st.session_state.login_error    = None
                st.session_state.logged_in_user = db[uid]['name']
                st.session_state.logged_in_id   = uid
                go('home')

        st.markdown(
            "<div style='text-align:center; margin-top:1rem; font-size:0.85rem; color:#7090b0;'>"
            "계정이 없으신가요?</div>",
            unsafe_allow_html=True
        )
        if st.button("회원가입", key="go_signup", use_container_width=True):
            st.session_state.login_error = None
            go('signup')

        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════
# 회원가입 화면
# ════════════════════════════════════════════
def signup_screen():
    st.markdown("<br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.8, 1])
    with col:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h2 style='margin-bottom:1.2rem;'>📋 회원가입</h2>", unsafe_allow_html=True)

        if st.session_state.signup_finished:
            st.success("회원가입이 완료되었습니다!")
            st.markdown("바로 로그인 하시겠습니까?")
            if st.button("🔵 로그인", key="goto_login_after_signup",
                         type="primary", use_container_width=True):
                st.session_state.signup_finished = False
                go('login')
            st.markdown('</div>', unsafe_allow_html=True)
            return

        new_sid  = st.text_input("학번",      key="su_sid",  placeholder="학번을 입력하세요")
        new_name = st.text_input("이름",      key="su_name", placeholder="이름을 입력하세요")
        new_id   = st.text_input("사용할 ID", key="su_id",   placeholder="아이디를 입력하세요")
        new_pw   = st.text_input("비밀번호",  key="su_pw",   type="password",
                                  placeholder="비밀번호를 입력하세요")

        if st.button("가입하기", use_container_width=True, type="primary", key="btn_signup"):
            if not (new_name and new_id and new_pw):
                st.error("이름, ID, 비밀번호는 필수 입력 항목입니다.")
            elif new_id in st.session_state.user_db:
                st.error("중복된 아이디입니다. 다른 아이디를 사용해주세요.")
            else:
                st.session_state.user_db[new_id] = {
                    'pw': new_pw, 'name': new_name, 'sid': new_sid
                }
                save_users(st.session_state.user_db)
                st.session_state.signup_finished = True
                st.rerun()

        st.markdown("<hr style='border-color:rgba(255,255,255,0.1); margin:1rem 0'>",
                    unsafe_allow_html=True)
        if st.button("← 로그인으로 돌아가기", key="back_to_login"):
            go('login')

        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════
# 홈 화면
# ════════════════════════════════════════════
def home_screen():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"<h1 style='text-align:center; font-size:1.9rem;'>⚔️ 엘리오스 대륙에 오신 것을 환영합니다</h1>"
        f"<p style='text-align:center; color:#a0b0cc; margin-bottom:2rem;'>"
        f"반갑습니다, <b style='color:#7eb8ff'>{st.session_state.logged_in_user}</b> 모험가님!</p>",
        unsafe_allow_html=True
    )
    _, col, _ = st.columns([1, 2.2, 1])
    with col:
        st.markdown("""
        <div class="menu-card">
          <div class="menu-title">📝 엘리오스 상식 퀴즈</div>
          <div class="menu-desc">정답을 맞춰 점수를 높여보세요</div>
        </div>""", unsafe_allow_html=True)
        if st.button("상식 퀴즈 시작하기 →", use_container_width=True, key="btn_trivia"):
            go('quiz_info')

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="menu-card">
          <div class="menu-title">🔮 나와 맞는 캐릭터 테스트</div>
          <div class="menu-desc">흥미가 생기셨나요? 내 취향으로 캐릭터 추천 받아보기</div>
        </div>""", unsafe_allow_html=True)
        if st.button("캐릭터 테스트 시작하기 →", use_container_width=True, key="btn_char"):
            go('char_test')

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        if st.button("로그아웃", key="logout"):
            st.session_state.logged_in_user = None
            st.session_state.logged_in_id   = None
            go('login')


# ════════════════════════════════════════════
# 퀴즈 안내 화면
# ════════════════════════════════════════════
def quiz_info_screen():
    st.markdown("<br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 2.4, 1])
    with col:
        st.markdown("<h2>📝 엘리오스 상식 퀴즈</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box">
            안녕하세요 사용자님! 이곳은 <b>엘리오스 상식 퀴즈</b> 페이지입니다.<br><br>
            엘리오스에 대한 상식(이를테면 지역 NPC라던가, 교환 가능한 아이템,
            캐릭터 고유 스킬이나 스토리 등)을 확인할 수 있습니다.<br><br>
            <span style="color:#7eb8ff">📌 예시</span><br>
            <i>"엘리오스에는 <b>[바실리]</b>라는 <b>[마족]</b> NPC가 있습니다!
            이 NPC는 어느 마을에 있는 NPC일까요?<br>
            💡 힌트: 바실리는 버프, 각인 등의 기능을 제공합니다."</i><br><br>
            난이도는 <b>쉬움</b>과 <b>어려움</b>으로 구분되어 있으며,<br>
            점수 계산은 <b style="color:#7eb8ff">맞힌 문제 수 / 총 문제 수</b> 로 측정합니다!
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<p style='color:#c0c8e0; font-weight:600; margin-bottom:0.5rem;'>"
                    "난이도를 선택하세요</p>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🟢  EASY", use_container_width=True, key="btn_easy", type="primary"):
                st.session_state.quiz_mode = 'easy'
                go('trivia_quiz')
        with c2:
            if st.button("🔴  HARD", use_container_width=True, key="btn_hard"):
                st.session_state.quiz_mode = 'hard'
                go('trivia_quiz')

        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        if st.button("← 홈으로 돌아가기", key="quiz_info_home"):
            go('home')


# ════════════════════════════════════════════
# 상식 퀴즈 화면
# ════════════════════════════════════════════
def trivia_quiz_screen():
    mode       = st.session_state.quiz_mode
    mode_label = "🟢 EASY" if mode == 'easy' else "🔴 HARD"
    data       = get_quiz_data()[f"trivia_{mode}"]

    st.markdown(f"<h2>📝 엘리오스 상식 퀴즈 — {mode_label}</h2>", unsafe_allow_html=True)
    st.caption(f"총 {len(data)}문항 · 맞힌 수 / 전체 문항 수로 점수 계산")

    # ── 결과 표시 상태 ──
    if st.session_state.last_score and st.session_state.last_score[2] == mode:
        score, total, _, answers, data_snapshot = st.session_state.last_score
        pct = round(score / total * 100)

        st.markdown(f"""
        <div class="score-box">
            <div style="font-size:0.9rem; color:#a0b8e0; margin-bottom:0.4rem;">제출 완료 ✅</div>
            <div style="font-size:2.2rem; font-weight:800; color:#7eb8ff;">{score} / {total}</div>
            <div style="font-size:1rem; color:#c0d0f0; margin-top:0.3rem;">{pct}점</div>
        </div>
        """, unsafe_allow_html=True)

        if score == total:
            st.balloons()
            st.success("🎉 완벽합니다! 엘리오스 박사님!")
        elif pct >= 60:
            st.info("👍 잘 하셨어요!")
        else:
            st.warning("😢 조금 더 공부해봐요!")

        st.markdown("<div style='margin:1rem 0 0.5rem; font-weight:700; color:#c0d0f0;'>"
                    "📋 채점 결과</div>", unsafe_allow_html=True)
        for i, item in enumerate(data_snapshot):
            is_correct = (answers[i] == item['correct'])
            mark       = "✅" if is_correct else "❌"
            row_class  = "ox-correct" if is_correct else "ox-wrong"
            wrong_hint = "" if is_correct else \
                f"<span class='ox-ans'>&nbsp;(정답: {item['correct']})</span>"
            st.markdown(
                f"<div class='ox-row {row_class}'>"
                f"<span class='ox-mark'>{mark}</span>"
                f"<span class='ox-q'>Q{i+1}. {item['q']}</span>"
                f"{wrong_hint}"
                f"</div>",
                unsafe_allow_html=True
            )

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🏠 홈으로 돌아가기", use_container_width=True, key="result_home"):
                st.session_state.last_score = None
                go('home')
        with c2:
            if st.button("🏆 랭킹 확인하기", use_container_width=True, key="result_ranking"):
                go('ranking')
        return

    # ── 퀴즈 폼 ──
    with st.form("quiz_form"):
        answers = []
        for i, item in enumerate(data):
            if "img" in item and os.path.exists(item["img"]):
                st.image(item["img"], width=300)
            ans = st.radio(f"Q{i+1}. {item['q']}", item['a'], key=f"tq_{i}")
            answers.append(ans)
        submitted = st.form_submit_button("제출하기 ✔️", use_container_width=True)

    if submitted:
        score = sum(1 for i, item in enumerate(data) if answers[i] == item['correct'])
        total = len(data)
        st.session_state.last_score = (score, total, mode, answers, data)
        add_ranking(mode, st.session_state.logged_in_id,
                    st.session_state.logged_in_user, score, total)
        st.rerun()
    else:
        if st.button("← 난이도 선택으로", key="back_quiz_info"):
            go('quiz_info')


# ════════════════════════════════════════════
# 랭킹 화면
# ════════════════════════════════════════════
def ranking_screen():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<h1 style='text-align:center; font-size:1.8rem; margin-bottom:0.3rem;'>"
        "🏆 랭킹 정보</h1>",
        unsafe_allow_html=True
    )
    _, btn_col, _ = st.columns([2, 1, 2])
    with btn_col:
        if st.button("🏠 홈으로 돌아가기", use_container_width=True, key="ranking_home"):
            go('home')

    st.markdown(
        "<hr style='border:none; border-top:1px solid rgba(255,255,255,0.18);"
        " margin:1rem 0 1.5rem 0;'>",
        unsafe_allow_html=True
    )

    col_easy, div_col, col_hard = st.columns([5, 0.1, 5])
    with col_easy:
        render_ranking_column("easy", "🟢 쉬움 랭킹")
    with div_col:
        st.markdown(
            "<div style='width:1px; background:rgba(255,255,255,0.15);"
            " min-height:300px; margin:0 auto;'></div>",
            unsafe_allow_html=True
        )
    with col_hard:
        render_ranking_column("hard", "🔴 어려움 랭킹")


# ════════════════════════════════════════════
# 캐릭터 취향 테스트 — 질문 화면
# ════════════════════════════════════════════
def char_test_screen():
    st.markdown("<h2>🔮 캐릭터 취향 테스트</h2>", unsafe_allow_html=True)
    st.caption("취향에 맞는 답변을 선택하면 어울리는 캐릭터를 추천해드립니다.")

    questions = [
        ("성별",     ["여자캐릭터", "남자캐릭터", "상관없음"]),
        ("주력타입", ["물리공격",   "마법공격",   "상관없음"]),
        ("역할",     ["서포터",     "서브딜러",   "메인딜러"]),
        ("속도",     ["느림",       "보통",       "빠름"]),
        ("공격거리", ["근거리",     "중거리",     "원거리"]),
        ("난이도",   ["쉬움",       "보통",       "어려움"]),
    ]

    label_map = {
        "여자캐릭터": "여자",     "남자캐릭터": "남자",     "상관없음": "상관없음",
        "물리공격":   "물리",     "마법공격":   "마법",
        "서포터":     "서포터",   "서브딜러":   "서브딜러", "메인딜러": "메인딜러",
        "느림": "느림", "보통": "보통", "빠름": "빠름",
        "근거리": "근거리", "중거리": "중거리", "원거리": "원거리",
        "쉬움": "쉬움", "어려움": "어려움",
    }

    with st.form("char_test_form"):
        selections = []
        for label, options in questions:
            choice = st.radio(f"**{label}**", options, horizontal=True, key=f"ct_{label}")
            selections.append(choice)
        submitted = st.form_submit_button("✨ 추천 결과 보기", use_container_width=True)

    if submitted:
        gender, attack, role, speed, rang, diff = [label_map[s] for s in selections]
        top_chars, _ = match_character(gender, attack, role, speed, rang, diff)

        # 결과 캐릭터를 세션에 저장하고 결과 페이지로 이동
        # 동점이면 첫 번째 캐릭터를 대표로 사용
        st.session_state.char_result = top_chars[0]
        go('char_result')

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    if st.button("← 홈으로 돌아가기", key="char_home"):
        go('home')


# ════════════════════════════════════════════
# 캐릭터 결과 전용 페이지
# ════════════════════════════════════════════
def char_result_screen():
    c = st.session_state.get('char_result')
    if c is None:
        # 결과 데이터 없으면 테스트로 되돌아가기
        go('char_test')
        return

    img_path = c.get("img", "")
    has_img  = img_path and os.path.exists(img_path)

    # ── 레이아웃: 좌우 여백 + 중앙 콘텐츠 ──
    st.markdown("<br>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 2.6, 1])

    with mid:
        # ① 이미지 영역 (크게, 중앙 상단)
        if has_img:
            st.image(img_path, use_container_width=True)
        else:
            # 이미지 없을 때 빈 박스
            st.markdown(
                "<div class='no-img-box' style='height:340px;'>"
                "이미지를 images 폴더에 넣어주세요</div>",
                unsafe_allow_html=True
            )

        st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

        # ② 캐릭터 이름 / 전직명 / 역할 뱃지 / 한 줄 설명
        st.markdown(
            f"<div class='char-result-name'>{c['name']}</div>"
            f"<div class='char-result-title'>{c['title']}</div>"
            f"<span class='char-result-role'>{c['role']}</span>"
            f"<div class='char-result-desc'>{c['desc']}</div>",
            unsafe_allow_html=True
        )

        st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

        # ③ 버튼 2개: 홈으로 돌아가기 / 테스트 다시하기
        b1, b2 = st.columns(2)
        with b1:
            if st.button("🏠 홈으로 돌아가기", use_container_width=True, key="result_to_home"):
                st.session_state.char_result = None
                go('home')
        with b2:
            if st.button("🔄 테스트 다시하기", use_container_width=True, key="result_retry",
                         type="primary"):
                # 이전 결과 초기화 후 테스트 화면으로
                st.session_state.char_result = None
                go('char_test')


# ════════════════════════════════════════════
# 메인 라우터
# ════════════════════════════════════════════
page = st.session_state.page

if   page == 'intro':       intro_screen()
elif page == 'login':       login_screen()
elif page == 'signup':      signup_screen()
elif page == 'home':        home_screen()
elif page == 'quiz_info':   quiz_info_screen()
elif page == 'trivia_quiz': trivia_quiz_screen()
elif page == 'ranking':     ranking_screen()
elif page == 'char_test':   char_test_screen()
elif page == 'char_result': char_result_screen()