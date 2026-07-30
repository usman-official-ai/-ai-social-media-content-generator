# The Content Wire — AI Social Media Content Generator  

   <img width="1536" height="1024" alt="ChatGPT Image Jul 29, 2026, 09_50_50 PM" src="https://github.com/user-attachments/assets/7c96cf98-6c92-4f9c-9e7a-8e4fdbfbc1ce" />    
   

An AI-powered web app that turns a few business details into ready-to-post
social media content: captions (short/medium/long), hashtags, a call-to-action,
an AI image prompt, A/B/C variations, a content calendar, SEO keywords, and a
best-time-to-post suggestion — for Facebook, Instagram, LinkedIn, or Twitter/X,
in English or Urdu.

Built as a full-stack project: **Flask** backend calling the **Groq 
API**, and a **React + Tailwind CSS** frontend.  

**Frontend (Live):**  
[https://ai-social-media-content-generator-phi.vercel.app](https://ai-social-media-content-generator-phi.vercel.app)

---

## ✨ Features  

| Feature | Description |
|---|---|
| Business intake form | Business name, industry, audience, product/service, goal, platform, tone, language, emoji toggle |
| Caption generator | Short, medium, and long captions in one call |
| Hashtag generator | 15–20 hashtags, with trending ones flagged separately |
| CTA generator | One strong, goal-matched call-to-action |
| AI image prompt | A ready-to-use prompt for image-generation tools |
| Content variations | Version A / B / C of the caption, different angles |
| Content calendar | 7-day or 30-day post-idea calendar |
| SEO keywords | 10–15 discovery keywords for captions/bios/alt text |
| Best posting time | Platform-specific posting-time guidance |
| Copy & export | One-click copy, and download as `.txt` or `.pdf` |

---

## 🧱 Tech Stack

- **Frontend:** React 19, Tailwind CSS 3, Axios, jsPDF, Vite
- **Backend:** Python, FastAPI, Uvicorn, Pydantic
- **AI:** Google Gemini API (`google-generativeai`, free tier)
- **Deployment:** Vercel (frontend) + Render (backend)

---

## 📁 Project Structure

```
AI-Social-Media-Generator/
│
├── frontend/                  React + Tailwind app
│   ├── src/
│   │   ├── components/        BusinessForm, ResultCard, HashtagList, etc.
│   │   ├── pages/Home.jsx      Main page — wires form + tabs + API calls
│   │   └── services/           api.js (backend calls), download.js (TXT/PDF)
│   ├── .env.example
│   └── package.json
│
├── backend/                   FastAPI app
│   ├── app.py                 App entrypoint, CORS, router registration
│   ├── routes/                content.py, hashtags.py, calendar.py, extras.py
│   ├── prompts/                templates.py — all Gemini prompt strings
│   ├── services/                gemini_service.py — Gemini API wrapper
│   ├── utils/                  config.py, json_parser.py
│   ├── models.py               Pydantic request/response schemas
│   ├── requirements.txt
│   └── .env.example
│
└── README.md
```

---

## 🚀 Local Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- A free Gemini API key from [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # then paste your GEMINI_API_KEY into .env

python app.py                   # or: uvicorn app:app --reload
```

The API is now running at `http://localhost:8000`. Interactive docs (Swagger)
are available at `http://localhost:8000/docs`.

### 2. Frontend

```bash
cd frontend
npm install

cp .env.example .env            # VITE_API_URL should point at the backend above

npm run dev
```

The app is now running at `http://localhost:5173`.

---

## 🔌 API Reference

Base URL: `http://localhost:8000/api`

| Method | Endpoint | Body | Description |
|---|---|---|---|
| `POST` | `/generate-content` | `BusinessInfo` | Captions, hashtags, CTA, image prompt, variations |
| `POST` | `/generate-hashtags` | `BusinessInfo` | 15–20 hashtags + trending subset |
| `POST` | `/generate-calendar` | `BusinessInfo & { days: 7 \| 30 }` | Day-by-day content calendar |
| `POST` | `/generate-keywords` | `BusinessInfo` | 10–15 SEO keywords |
| `GET`  | `/best-posting-time?platform=Instagram` | — | Platform posting-time guidance |

`BusinessInfo` shape:

```json
{
  "business_name": "Bright Smile Dental",
  "industry": "Healthcare / Dental Clinic",
  "target_audience": "Families in Lahore, ages 25-45",
  "product_service": "Teeth whitening & general dentistry",
  "goal": "Awareness",
  "platform": "Instagram",
  "tone": "Friendly",
  "language": "English",
  "include_emojis": true
}
```

Full request/response schemas are auto-documented at `/docs` (Swagger UI)
and `/redoc` once the backend is running.

---

## ☁️ Deployment

### Backend → Render

1. Push this repo to GitHub.
2. On [Render](https://render.com), create a **New Web Service** and connect the repo.
3. Set:
   - **Root directory:** `backend`
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
4. Add environment variables from `backend/.env.example` (`GEMINI_API_KEY`,
   `GEMINI_MODEL`, and `CORS_ORIGINS` — set this to your Vercel frontend URL
   once you have it).
5. Deploy. Note the resulting URL, e.g. `https://your-app.onrender.com`.

### Frontend → Vercel

1. On [Vercel](https://vercel.com), import the same repo.
2. Set:
   - **Root directory:** `frontend`
   - **Framework preset:** Vite
3. Add environment variable `VITE_API_URL` = your Render backend URL from above.
4. Deploy. Note the resulting URL, e.g. `https://your-app.vercel.app`.
5. Go back to Render and update `CORS_ORIGINS` to include that Vercel URL,
   then redeploy the backend so it accepts requests from the live frontend.

---

## 🧠 How content generation works

Every generation endpoint builds a prompt (see `backend/prompts/templates.py`),
sends it to Gemini with `response_mime_type: application/json`, and parses the
result with a small helper (`backend/utils/json_parser.py`) that strips
markdown code fences before parsing — so a stray ```` ```json ```` wrapper from
the model never breaks the API response.

---

## 🛠️ Troubleshooting

- **"GEMINI_API_KEY is not set"** — copy `backend/.env.example` to `backend/.env`
  and add your key.
- **CORS errors in the browser** — make sure `CORS_ORIGINS` in `backend/.env`
  includes the exact frontend origin you're using (`http://localhost:5173` for
  local dev).
- **Frontend can't reach the API** — check `VITE_API_URL` in `frontend/.env`
  matches where the backend is actually running.

---

## 📄 License

Built for educational/portfolio use.
