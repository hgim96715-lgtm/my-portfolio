import streamlit as st
import requests
import base64
import re

st.set_page_config(
    page_title="Seoul Train | Data Engineer",
    page_icon="🚆",
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
GITHUB_REPO  = "gong_home"
BRANCH       = "main"
PROJECT_PATH = "10_Projects/16_Project_Seoul_Train"   # 서울역 노트 경로

STEPS = [
    {"file": "00_Seoul_Station_Real-Time_Train_Project",      "label": "Overview",       "color": "#00C2FF"},
    {"file": "01_Docker_Setup_Postgresql_Setup",       "label": " Docker",         "color": "#A78BFA"},
    {"file": "02_API_Producer",       "label": " API",            "color": "#34D399"},
    {"file": "03_Kafka_Producer",     "label": " Kafka Producer", "color": "#F59E0B"},
    {"file": "04_Spark_Streaming",    "label": " Spark",          "color": "#F87171"},
    {"file": "05_Superset_Dashboard", "label": "Superset",       "color": "#60A5FA"},
    {"file": "06_Airflow_Pipeline",   "label": " Airflow",        "color": "#FB923C"},
    {"file": "07_Integration_Test",   "label": " 통합 테스트",     "color": "#4ADE80"},
]

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
    border-top: 3px solid #00C2FF; border-radius: 10px;
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
.gh-btn:hover { border-color: #00C2FF; color: #00C2FF !important; }
.stMarkdown table  { width: 100%; font-family: monospace; }
.stMarkdown thead tr th { color: #00C2FF; background: #161b22; text-align: center; }
.stMarkdown code { font-family: monospace; }
</style>
""")

# ──────────────────────────────────────────────
# 
# ──────────────────────────────────────────────
@st.cache_data(ttl=600)
def get_md(file_name: str) -> str:
    url = (
        #  url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/10_Projects/{folder}?ref={BRANCH}"
        f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}"
        f"/contents/{PROJECT_PATH}/{file_name}.md?ref={BRANCH}"
    )
    headers = {}
    if "GITHUB_TOKEN" in st.secrets:
        headers["Authorization"] = f"token {st.secrets['GITHUB_TOKEN']}"
    r = requests.get(url, headers=headers, timeout=10)
    if r.status_code != 200:
        st.error(f"GitHub API 에러 발생 :{r.status_code}")
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
        url = (
            f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}"
            f"/{BRANCH}/99_Assets(이미지&첨부파일저장소)/{encoded}"
        )
        return f"![{filename}]({url})"
    text = re.sub(r'!\[\[([^\]]+)\]\]', replace_image, text)
    # Obsidian 내부 링크 [[XXX]] → 텍스트만 남김
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
    st.markdown("**🚄 서울역 열차 파이프라인**")

    selected_step = st.radio(
        label="Step",
        options=[s["file"] for s in STEPS],
        format_func=lambda f: next(s["label"] for s in STEPS if s["file"] == f),
        label_visibility="collapsed",
    )
    st.html("<hr class='divider'/>")
    st.caption("© 2026 Kim Han Gyeong")

# ──────────────────────────────────────────────
# 메인 헤더
# ──────────────────────────────────────────────
st.html("""
    <h1 class='page-title'>
        <i class="fa-solid fa-train" style="color: #00C2FF;"></i> Seoul Station Train Dashboard
    </h1>
    <div class='page-sub'>Kafka · Spark · Airflow · Superset · Docker 기반 실시간 열차 파이프라인</div>
""")

stack_badges = " ".join([
    f"<span class='stack-badge' style='color:{c};border-color:{c}44;background:{c}11;'>{n}</span>"
    for n, c in TECH_STACK
])

st.html(f"""
    <div class='project-header'>
        <div class='project-title'>🚄 Real-time Train Pipeline</div>
        <div style='color:#8b949e; font-size:0.9rem; margin-bottom:0.8rem;'>
            공공데이터 API 로 서울역 열차 운행 데이터를 수집하여
            실시간 운행 현황 추적과 전날 지연 분석을 보여주는 데이터 파이프라인.<br/>
            당일 실시간 API 차단 시 계획 데이터 기반 상태 추정 로직을 직접 설계하였으며,
            <b>실제 코레일 어플과 직접 대조하며 데이터의 정합성을 철저히 검증</b>했습니다.<br/>
            모든 인프라는 Docker Compose 로 로컬에서 재현 가능하게 구성했습니다.
        </div>
        {stack_badges}
        <br/><br/>
        <a class='gh-btn'
           href='https://github.com/{GITHUB_USER}/{GITHUB_REPO}/tree/{BRANCH}/{PROJECT_PATH}'
           target='_blank'>
            <i class='fa-brands fa-github'></i> GitHub 코드 보기
        </a>
    </div>
""")

st.html("<hr class='divider'/>")

# ──────────────────────────────────────────────
# 
# ──────────────────────────────────────────────
current = next(s for s in STEPS if s["file"] == selected_step)
st.html(f"<strong class='page-label'>{current['label']}</strong>")

with st.spinner("노트 불러오는 중.. 🚗"):
    raw = get_md(selected_step)

if raw:
    render_md_with_mermaid(raw)
else:
    st.warning("🥹 GitHub에서 파일을 불러올 수 없습니다. 경로를 확인하세요.")
    st.code(f"{PROJECT_PATH}/{selected_step}.md", language="text")