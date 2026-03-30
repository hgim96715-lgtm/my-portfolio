import streamlit as st
import requests
import base64
import re

st.set_page_config(
    page_title="Wiki | Obsidian",
    page_icon="https://obsidian.md/favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">""",unsafe_allow_html=True)


st.html("""
<style>
section[data-testid="stSidebar"] { padding-top: 2rem; }
section[data-testid="stSidebar"] .sub-title{color:#8b949e;font-family:monospace;}
.divider{border:none;border-top:1px solid #30363d;margin:1.2rem 0;}
.page-title{font-size:2rem;font-family:monospace;color:#e6edf3;}
.page-sub{font-family:monospace;color:#8b949e;font-size:0.9rem;margin-bottom:1rem;}

div[data-testid="stButton"] {width: 100% !important;}
div[data-testid="stButton"] > button {background: #0d1117 !important;border: 1px solid #21262d !important;border-radius: 10px !important;color: #e6edf3 !important;padding: 1rem 1.1rem !important;box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;width: 100% !important;height: 80px !important;min-height: 80px !important;max-height: 80px !important;display: flex !important;align-items: center !important; justify-content: flex-start !important;}

div[data-testid="stButton"] > button:hover,
div[data-testid="stButton"] > button[kind="primary"]{border-color: #00C2FF !important;border-top-color: #00C2FF !important;background: #161b22 !important;color: #00C2FF !important;box-shadow: 0 4px 16px rgba(0,194,255,0.15) !important;}

div[data-testid="stButton"] > button p {font-family: monospace !important;font-size: 0.88rem !important;font-weight: 600 !important;margin: 0 !important;text-align: left !important;line-height: 1.5 !important;display: -webkit-box !important;-webkit-line-clamp: 2 !important;-webkit-box-orient: vertical !important;overflow: hidden !important;
    text-overflow: ellipsis !important;white-space: normal !important;word-break: break-word !important;}

.md-body {background: #161b22;border: 1px solid #30363d;border-radius: 8px;padding: 1.5rem 2rem;color: #c9d1d9;
    line-height: 1.8;}

.empty-msg {color: #8b949e;font-family: monospace;font-size: 0.9rem;padding: 1rem;text-align: center;}
</style>
""")


GITHUB_USER='hgim96715-lgtm'
GITHUB_REPO = 'gong_home'
BRANCH ='main'

CATEGORIES = {
    "20_Wiki/21_Languages":      {"label": "Languages",       "subs": ["Python", "SQL"]},
    "20_Wiki/22_Data_Processing":{"label": "Data Processing", "subs": ["Flink", "Kafka", "Pandas", "Spark"]},
    "20_Wiki/23_Orchestration":  {"label": "Orchestration",   "subs": ["Airflow"]},
    "20_Wiki/24_Infrastructure": {"label": "Infrastructure",  "subs": ["Docker", "Linux"]},
    "20_Wiki/25_CS_Basics":      {"label": "CS Basics",       "subs": []},
    "20_Wiki/26_Visualization":  {"label": "Visualization",   "subs": ["Streamlit", "Superset"]},
}

def get_headers():
    """GitHub API 헤더 반환 (토큰이 있으면 사용, 없으면 빈 헤더)"""
    headers = {}
    try:
        token = st.secrets.get("GITHUB_TOKEN", "")
        if token:
            headers["Authorization"] = f"token {token}"
    except Exception:
        pass
    return headers

@st.cache_data(ttl=300)
def get_tree(path: str) -> list:
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{path}?ref={BRANCH}"
    headers = get_headers()
    try:
        r = requests.get(url, timeout=10, headers=headers)
        if r.status_code == 200:
            data = r.json()
            # API가 리스트를 반환하는지 확인
            if isinstance(data, list):
                return data
        return []
    except Exception:
        return []

@st.cache_data(ttl=300)
def get_md_content(path: str) -> str:
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{path}?ref={BRANCH}"
    headers = get_headers()
    try:
        r = requests.get(url, timeout=10, headers=headers)
        if r.status_code == 200:
            data = r.json()
            content = base64.b64decode(data['content']).decode("utf-8")
            return content
        return ""
    except Exception:
        return ""

def clean_obsidian_md(text: str) -> str:
    text = re.sub(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', 
                  lambda m: m.group(2) or m.group(1), text)
    text = re.sub(r'```dataview[\s\S]*?```', 
                  '> 📊 *Dataview 블록은 Obsidian에서 확인하세요*', text)
    text = re.sub(r'>\s*\[!(\w+)\]\s*', r'> **[\1]** ', text)
    return text

@st.cache_data(ttl=300)
def collect_md_files(path: str) -> list:
    files = []
    items = get_tree(path)
    for item in items:
        if isinstance(item, dict):
            if item.get('type') == 'file' and item.get('name', '').endswith('.md'):
                files.append({
                    "name": item['name'].replace('.md', '').replace('_', ' '),
                    "path": item['path']
                })
            elif item.get('type') == 'dir':
                files.extend(collect_md_files(item['path']))
    return files

def on_category_change():
    if "selected_md" in st.session_state:
        del st.session_state["selected_md"]
    if "selected_name" in st.session_state:
        del st.session_state["selected_name"]

# 사이드바
with st.sidebar:
    st.markdown("### 👩‍💻 Kim Han Gyeong")
    st.html("<p class='sub-title'>Data Engineer</p>")
    st.html("<hr class='divider'/>")
    
    st.html('<strong><i class="fa-solid fa-folder"></i> Wiki 카테고리</strong>')
    selected_wiki_key = st.radio(
        label="카테고리",
        options=list(CATEGORIES.keys()),
        format_func=lambda k: CATEGORIES[k]['label'],
        label_visibility='collapsed',
        on_change=on_category_change
    )
    st.html("<hr class='divider'/>")
    st.caption("© 2026 Kim Han Gyeong")
    
    
# 메인 화면
wiki_info = CATEGORIES[selected_wiki_key]

st.html(f"""
    <h1 class='page-title'>
        <img src="https://upload.wikimedia.org/wikipedia/commons/1/10/2023_Obsidian_logo.svg" 
             style="width: 1em; height: 1em; vertical-align: middle; margin-bottom: 4px;"> 
        Obsidian Wiki
    </h1>
    <div class='page-sub'>{wiki_info['label']} 카테고리의 학습 노트입니다.</div>
""")
st.html("<hr class='divider'/>")

subs = wiki_info["subs"]

if subs:
    tabs = st.tabs(subs)
    tab_map = dict(zip(subs, tabs))
else:
    tab_map = {"전체": st.container()}

@st.fragment
def render_file_list(folder_path):
    files = collect_md_files(folder_path)
    if not files:
        st.html("<p class='empty-msg'>아직 노트가 없습니다. Obsidian에서 열심히 공부해주세요😅</p>")
        return
    
    search = st.text_input("🔍 노트 검색:", placeholder='파일명 검색하고 싶으면 여기에 적어주세요', key=folder_path)
    if search:
        files = [f for f in files if search.lower() in f['name'].lower()]
        
    st.caption(f"총 {len(files)}개의 노트가 검색되었습니다.")
    
    cols = st.columns(3)
    for i, f in enumerate(files):
        with cols[i % 3]:
            is_active = st.session_state.get("selected_md") == f["path"]
            
            if st.button(
                f"📄  {f['name']}",
                key=f["path"],
                type="primary" if is_active else "secondary",
                use_container_width=True
            ):
                st.session_state["selected_md"] = f["path"]
                st.session_state["selected_name"] = f["name"]
                st.rerun() 
    
    if 'selected_md' in st.session_state and st.session_state.get("selected_md", "").startswith(folder_path):
        render_markdown_content()
        
def render_markdown_content():
    st.html("<hr class='divider'/>")
    st.subheader(st.session_state['selected_name']) 
    
    with st.spinner("노트 불러오는 중.."):
        raw = get_md_content(st.session_state['selected_md'])
        if raw:
            cleaned = clean_obsidian_md(raw)
            st.markdown(cleaned)
        else:
            st.warning("노트를 불러올 수 없습니다.")


if subs:
    for sub_name, tab in tab_map.items():
        folder = f"{selected_wiki_key}/{sub_name}"
        with tab:
            render_file_list(folder)
else:
    with tab_map["전체"]:
        render_file_list(selected_wiki_key)