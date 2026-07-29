from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import content, hashtags, calendar, extras
from utils.config import settings

app = FastAPI(
    title="AI Social Media Content Generator API",
    description="Generates captions, hashtags, CTAs, image prompts, content "
    "calendars and SEO keywords for businesses using Groq API.",
    version="1.0.0",
)

# CORS configuration - FIXED
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(content.router, prefix="/api")
app.include_router(hashtags.router, prefix="/api")
app.include_router(calendar.router, prefix="/api")
app.include_router(extras.router, prefix="/api")


@app.get("/")
async def root():
    return {"status": "ok", "message": "AI Social Media Content Generator API is running with Groq."}


@app.get("/health")
async def health():
    return {"status": "healthy", "ai_provider": "Groq"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)