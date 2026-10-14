# 🇮🇹 Daily-Italy — L'Italiano Quotidiano

An artisanal, interactive Italian vocabulary mastery application built upon the acclaimed book ***"Le prime 3000 parole"*** (Alma Edizioni).

Designed with a luminous Mediterranean visual identity, multi-page routing, open course exploration (no mandatory login wall), 15-word milestone units, interactive 3D flashcards with native speech synthesis, contextual exercise quizzes, **Busuu-style Spaced Repetition (SRS) Smart Review**, friend leaderboards, and an **RBAC Admin Panel**.

---

## 🌟 Key Architectural Features

* **Structured 60-Chapter Curriculum Across CEFR Levels:**
  - **Level A1:** 10 Chapters (Beginner foundational communication)
  - **Level A2:** 10 Chapters (Daily life, social interactions & travel)
  - **Level B1:** 20 Chapters (Complex grammar, idioms & word families)
  - **Level B2:** 20 Chapters (Nuanced expression & literary mastery)
* **Four Dedicated Multimodal Labs in Every Chapter:**
  1. **Vocabulary Lab:** 15 high-frequency thematic words with pronunciation and audio.
  2. **Grammar Studio:** Clear English grammatical explanations, syntax rules, and reference conjugation tables tailored for English speakers learning Italian.
  3. **Authentic Reading & Cultural Dialogues:** Immersion passages with audio, toggleable English translations, and comprehension questions with instant red/green feedback.
  4. **Writing Lab:** Scenario prompts with starter word chips, sentence composition, anti-skip length validation, and model Italian solution comparison.
* **Placement Testing (Jump to Next Level):** 10-question placement tests for A2, B1, and B2. Scoring $\ge 70\%$ immediately unlocks all chapters of that level.
* **Strict Chapter Progression:** Chapters unlock sequentially; readers must verify comprehension check questions and submit writing before advancing.
* **Navigation Carousel:** Smooth navigation bar carousel arrows allowing instant one-click direct switching to any tab.
* **Mediterranean Light Visual Design:** Warm linen canvas (`#fbf9f5`), Tuscan terracotta (`#d94a38`), olive sage (`#2d6a4f`), and Amalfi azure (`#0284c7`), with elegant Lora & Plus Jakarta Sans typography.
* **Role-Based Access Control (RBAC):** Distinct `user` and `admin` roles. Admins have access to the `/admin` oversight dashboard to monitor users, chapters, and community activity.
* **SuperMemo-2 (SM-2) Spaced Repetition:** Flashcard ratings dynamically optimize review intervals in SQLite/PostgreSQL.
* **Interactive Exercises:** Multiple choice and cloze with instant audio feedback and shake animations.
* **Automated CI/CD Pipeline:** Complete GitHub Actions pipeline running `pytest`, building multi-stage Docker images, and triggering automated cloud deployment.

---

## 🏗️ Technical Stack

* **Backend:** Python 3.10+, FastAPI (Asynchronous REST API, OpenAPI docs at `/docs`), SQLAlchemy, Pydantic, Bcrypt, PyMuPDF, RapidOCR.
* **Database:** SQLite (`backend/data/italian_vocab.db`) with automatic migrations & seeding.
* **Testing Area:** `pytest` test suite with 100% pass rate across auth, RBAC, curriculum, exercises, and SRS.
* **Frontend:** Modern Single Page Application (SPA) with URL hash routing (`#/home`, `#/courses`, `#/study/:id`, `#/quiz/:id`, `#/review`, `#/leaderboard`, `#/admin`), Web Speech Synthesis, Web Audio API, and PWA capabilities.
* **DevOps:** GitHub Actions CI/CD (`.github/workflows/ci-cd.yml`), Multi-stage Dockerfile, Docker Compose, Kubernetes manifests (`k8s/`), and `render.yaml`.

---

## 🧪 Testing Area & Test Execution

Run the complete automated test suite locally:
```bash
# Run all tests with verbose output
python -m pytest backend/tests/ -v
```

Tests verify:
1. `test_auth.py`: User registration, duplicate handling, JWT login, profile retrieval.
2. `test_rbac.py`: Role separation (401 for anonymous, 403 for standard users, 200 for admins).
3. `test_curriculum.py`: Open public access to courses, units, words, and grammar tips.
4. `test_exercises.py`: Instant answer verification endpoint (`check-answer`) and full quiz submission.
5. `test_srs.py`: SuperMemo-2 spaced repetition interval calculation.

---

## 🚀 Quickstart: Running Locally

### 1. Direct Python Execution
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Seed curriculum database (if not already seeded)
python -m backend.scripts.seed_curriculum

# 3. Start development server
python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```
Open **`http://localhost:8000`** in your browser. Interactive API documentation is at **`http://localhost:8000/docs`**.

### 2. Docker Compose
```bash
docker compose up --build
```

### 3. Kubernetes (k3s / Minikube / Kind)
```bash
kubectl apply -f k8s/deployment.yaml
```

---

## 🌐 100% Free Web Deployment (Render.com)

1. Push this repository to GitHub:
   ```bash
   git add .
   git commit -m "feat: complete Daily-Italy application with light theme and RBAC"
   git push -u origin main
   ```
2. Log into [Render.com](https://render.com) (free account).
3. Click **New +** $\rightarrow$ **Blueprint** and select your GitHub repository.
4. Render detects `render.yaml` automatically, builds the application, runs tests, and provides you with a free live URL:
   `https://daily-italy-app.onrender.com`

