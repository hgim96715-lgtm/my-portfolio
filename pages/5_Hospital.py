import streamlit as st
import requests
import base64
import re

st.set_page_config(
    page_title="Hospital | Data Engineer",
    page_icon="🚑",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<link rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# 설정
# ──────────────────────────────────────────────
GITHUB_USER  = "hgim96715-lgtm"
GITHUB_REPO  = "hospital-realtime-pipeline"
BRANCH       = "main"

TECH_STACK = [
    ("Apache Kafka",   "#F59E0B"),
    ("Apache Spark",   "#F87171"),
    ("Apache Airflow", "#60A5FA"),
    ("PostgreSQL",     "#34D399"),
    ("Apache Superset","#60A5FA"),
    ("Python",         "#A78BFA"),
    ("Docker",         "#00C2FF"),
    ("Streamlit",      "#FF4B4B"),
]

# ──────────────────────────────────────────────
# 스타일
# ──────────────────────────────────────────────
st.html("""
<style>
section[data-testid="stSidebar"] { padding-top: 2rem; }
a { text-decoration: none; }
section[data-testid="stSidebar"] .sub-title { color: #8b949e; font-family: monospace; }
.divider { border: none; border-top: 1px solid #30363d; margin: 1.2rem 0; }
.page-title { font-size: 2rem; font-weight: 700; font-family: monospace; color: #e6edf3; }
.page-sub   { font-family: monospace; color: #8b949e; font-size: 0.9rem; margin-bottom: 1rem; }
.page-label { font-family: monospace; color: #00C2FF; }
.project-header {
    background: #161b22; border: 1px solid #30363d;
    border-top: 3px solid #FF4B4B; border-radius: 10px;
    padding: 1.5rem 2rem; margin-bottom: 1rem; font-family: monospace;
}
.project-title { font-size: 1.3rem; font-weight: 700; color: #e6edf3; margin-bottom: 0.4rem; }
.stack-badge {
    display: inline-block; border-radius: 6px; padding: 4px 12px;
    margin: 3px; font-size: 0.8rem; font-weight: 600;
    border: 1px solid; opacity: 0.85; cursor: default;
}
.gh-btn {
    display: inline-block; background: #21262d; color: #e6edf3 !important;
    border: 1px solid #30363d; border-radius: 8px; padding: 8px 18px; font-size: 0.88rem;
}
.gh-btn:hover { border-color: #FF4B4B; color: #FF4B4B !important; }
.insight-box {
    background: #161b22; border: 1px solid #30363d;
    border-left: 3px solid #FF4B4B; border-radius: 8px;
    padding: 1rem 1.5rem; margin: 0.8rem 0;
    font-family: monospace; font-size: 0.88rem; color: #c9d1d9; line-height: 1.8;
}
.stMarkdown table  { width: 100%; font-family: monospace; }
.stMarkdown thead tr th { color: #00C2FF; background: #161b22; text-align: center; }
.stMarkdown code { font-family: monospace; }
</style>
""")

# ──────────────────────────────────────────────
# GitHub API 함수
# ──────────────────────────────────────────────
@st.cache_data(ttl=600)
def get_readme() -> str:
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/docs/README.md?ref={BRANCH}"
    
    headers = {}
    if "GITHUB_TOKEN" in st.secrets:
        headers["Authorization"] = f"token {st.secrets['GITHUB_TOKEN']}"
    r = requests.get(url, headers=headers, timeout=10)
    if r.status_code != 200:
        st.error(f"GitHub API 에러: {r.status_code}")
        return ""
    return base64.b64decode(r.json()["content"]).decode("utf-8")


def extract_mermaid(text: str):
    diagrams = re.findall(r'```mermaid\n([\s\S]*?)```', text)
    cleaned  = re.sub(r'```mermaid\n[\s\S]*?```', '<!-- mermaid -->', text)
    return diagrams, cleaned


def clean_md(text: str) -> str:
    text = re.sub(r'^---[\s\S]*?---\n', '', text)
    text = re.sub(r'```dataview[\s\S]*?```', '> 📊 *Dataview 블록은 Obsidian에서 확인하세요*', text)
    text = re.sub(r'>\s*\[!(\w+)\]\s*', r'> **[\1]** ', text)
    def replace_image(m):
        filename = re.sub(r'\|.*$', '', m.group(1).strip())
        encoded  = requests.utils.quote(filename)
        url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{BRANCH}/docs/{encoded}"
        return f"![{filename}]({url})"
    text = re.sub(r'!\[\[([^\]]+)\]\]', replace_image, text)
    text = re.sub(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]',
                  lambda m: m.group(2) or m.group(1), text)
    return text.strip()


def render_md_with_mermaid(raw: str):
    diagrams, text = extract_mermaid(raw)
    cleaned = clean_md(text)
    parts = cleaned.split('<!-- mermaid -->')
    for i, part in enumerate(parts):
        if part.strip():
            st.markdown(part)
        if i < len(diagrams):
            try:
                from streamlit_mermaid import st_mermaid
                st_mermaid(diagrams[i], height=400)
            except ImportError:
                st.code(diagrams[i], language="text")
                st.caption("`pip install streamlit-mermaid` 설치 시 다이어그램으로 표시됩니다.")

# ──────────────────────────────────────────────
# 사이드바
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 👩‍💻 Kim Han Gyeong")
    st.html("<p class='sub-title'>Data Engineer</p>")
    st.html("<hr class='divider'/>")
    st.markdown("**🚑 응급실 파이프라인**")
    st.html("<hr class='divider'/>")
    st.caption("© 2026 Kim Han Gyeong")

# ──────────────────────────────────────────────
# 메인 헤더
# ──────────────────────────────────────────────
st.html("""
    <h1 class='page-title'>
        <i class="fa-solid fa-truck-medical" style="color: #FF4B4B;"></i> 응급실 실시간 병상 현황
    </h1>
    <div class='page-sub'>Kafka · Spark · Airflow · Superset · Docker 기반 실시간 응급실 데이터 파이프라인</div>
""")

stack_badges = " ".join([
    f"<span class='stack-badge' style='color:{c};border-color:{c}44;background:{c}11;'>{n}</span>"
    for n, c in TECH_STACK
])

st.html(f"""
    <div class='project-header'>
        <div class='project-title'>🚑 Real-time Emergency Room Pipeline</div>
        <div style='color:#8b949e; font-size:0.9rem; margin-bottom:0.8rem;'>
            응급구조사로 근무하며 직접 경험한 응급실 포화 문제에서 출발한 프로젝트입니다.<br/>
            소방(119) 실습 시절 목격했던 119 지령센터-병원 간 실시간 병상 공유 시스템을
            <b>데이터 엔지니어의 시각으로 직접 역설계(Reverse Engineering)</b>하여 구현했습니다.<br/>
            공공데이터 API로 전국 응급실 병상 현황을 수집해 Kafka로 버퍼링하고,
            Spark Streaming으로 처리 · PostgreSQL에 적재 · Superset으로 시각화하는
            End-to-End 파이프라인입니다.
        </div>
        {stack_badges}
        <br/><br/>
        <a class='gh-btn'
           href='https://github.com/{GITHUB_USER}/{GITHUB_REPO}'
           target='_blank'>
            <i class='fa-brands fa-github'></i> GitHub 코드 보기
        </a>
    </div>
""")

# 핵심 인사이트 카드
st.html("""
    <div class='insight-box'>
        💡 <b>도메인 지식을 반영한 hvec 분류 기준</b><br/>
        🟢 hvec &gt; 10 &nbsp;&nbsp; 응급실 여유 있음<br/>
        🟡 0 &lt; hvec ≤ 10 &nbsp; 응급실 포화 직전 &nbsp;← 병상 10 이하부터 중증 환자 1명에 즉시 포화<br/>
        🔴 hvec ≤ 0 &nbsp;&nbsp;&nbsp; 응급실 포화 상태<br/><br/>
        📊 <b>주요 인사이트</b> &nbsp;|&nbsp;
        가장 위험한 시간대: <b>18시</b> &nbsp;|&nbsp;
        서울 포화율: <b>23.48%</b> &nbsp;|&nbsp;
        삼성서울병원 hvec = <b>-26</b>
    </div>
""")

st.html("<hr class='divider'/>")

# ──────────────────────────────────────────────
# README 렌더링
# ──────────────────────────────────────────────
with st.spinner("노트 불러오는 중.. 🚑"):
    raw = get_readme()

if raw:
    render_md_with_mermaid(raw)
else:
    st.warning("🥹 GitHub에서 파일을 불러올 수 없습니다. 경로를 확인하세요.")