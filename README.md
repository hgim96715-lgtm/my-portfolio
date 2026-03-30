# 🌐 Data Engineer Portfolio


> **Streamlit 기반 인터랙티브 포트폴리오** — 프로젝트, 일일 챌린지, 옵시디언 학습 노트를 한눈에

🔗 **Live Demo:** [gongstudyde-ixkmtnttnimw8wszmtxgzg.streamlit.app](https://gongstudyde-ixkmtnttnimw8wszmtxgzg.streamlit.app/)

---

## ✨ 주요 기능

### 🏠 Home
- 자기소개 및 커리어 스토리
- 기술 스택 뱃지
- 프로젝트 카드 미리보기
- GitHub 커밋 히스토리 시각화

### 👩‍💻 About
- 응급구조사 → 디지털 교과서 퍼블리셔 → 데이터 엔지니어 전환 스토리
- 보유 기술 및 자격증

### 📚 Obsidian Wiki
- **GitHub API 연동**으로 옵시디언 노트를 실시간 렌더링
- 카테고리별 학습 노트 탐색 (Python, SQL, Kafka, Spark, Airflow 등)
- Mermaid 다이어그램 지원

### 💪 Daily Challenge
- SQL / Python / Linux 일일 챌린지 기록
- 캘린더 뷰 + 연속 일수 통계
- 난이도별 필터링

### 🚆 Seoul Train Project
- 서울역 실시간 열차 데이터 파이프라인 상세 문서
- 단계별 구현 과정 (Docker → API → Kafka → Spark → Superset)

### 🚑 Hospital Project
- 응급실 실시간 병상 현황 파이프라인 상세 문서
- 도메인 지식 기반 트러블슈팅 과정

---

## 🛠 기술 스택

| 역할 | 기술 |
|------|------|
| Frontend | Streamlit |
| Data Source | GitHub API (옵시디언 노트 연동) |
| Visualization | Mermaid, GitHub Chart |
| Deployment | Streamlit Cloud |

---

## 📂 폴더 구조

```
my-portfolio/
├── Home.py                 # 메인 페이지
├── pages/
│   ├── 1_About.py          # 자기소개
│   ├── 2_Obsidian.py       # 옵시디언 Wiki
│   ├── 3_Challenge.py      # 일일 챌린지
│   ├── 4_Seoul_train.py    # 열차 프로젝트
│   └── 5_Hospital.py       # 병원 프로젝트
├── requirements.txt
└── README.md
```

---

## 🚀 로컬 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 실행
streamlit run Home.py
```

---

## 💡 특징

- **노션 대신 옵시디언** — GitHub API로 마크다운 노트를 실시간 렌더링
- **일일 챌린지 시각화** — 꾸준함을 캘린더와 통계로 증명
- **프로젝트 상세 문서화** — 단순 결과물이 아닌 과정을 보여줌

---

## 📫 Contact

- 📧 Email: hgim96715@email.com
- 🐙 GitHub: [github.com/hgim96715-lgtm](https://github.com/hgim96715-lgtm)

---

© 2026 Kim Han Gyeong