import os
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from groq import Groq

app = FastAPI(
    title="AI Social Media Content Generator API",
    description="Generates social media content using Groq API",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ContentRequest(BaseModel):
    business_name: str
    industry: str
    target_audience: str
    product_service: str
    goal: str
    platform: str
    tone: str
    language: str
    include_emojis: bool

class HashtagRequest(BaseModel):
    industry: str
    business_name: str
    target_audience: str

class CalendarRequest(BaseModel):
    days: int

class PostingTimeRequest(BaseModel):
    platform: str

class SEOKeywordsRequest(BaseModel):
    business_name: str
    industry: str
    product_service: str

# Constants
PLATFORM_TIMES = {
    "Instagram": "7 PM – 9 PM",
    "LinkedIn": "9 AM – 11 AM",
    "Facebook": "9 AM – 11 AM, 1 PM – 3 PM",
    "Twitter": "12 PM – 1 PM, 5 PM – 6 PM"
}

# Initialize Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

def get_fallback_content(request):
    emoji = "✨" if request.include_emojis else ""
    return {
        "short_caption": f"Transform your business with {request.business_name} today! {emoji}",
        "medium_caption": f"At {request.business_name}, we're revolutionizing the {request.industry} industry.",
        "long_caption": f"Ready to take your business to the next level? {request.business_name} specializes in {request.product_service}.",
        "hashtags": [f"#{request.business_name.replace(' ', '')}", f"#{request.industry}", "#Business", "#Growth"],
        "call_to_action": f"Contact {request.business_name} today!",
        "image_prompt": f"Professional {request.industry} business setting"
    }

@app.get("/")
async def root():
    return {"status": "ok", "message": "AI Social Media Generator API running on Vercel!"}

@app.get("/health")
async def health():
    return {"status": "healthy", "ai_provider": "Groq", "api_key_set": bool(GROQ_API_KEY)}

@app.post("/api/content/generate")
async def generate_content(request: ContentRequest):
    try:
        if not groq_client:
            return {"success": True, "data": get_fallback_content(request), "fallback": True}
        
        prompt = f"""You are an expert social media marketing specialist.

Generate social media content for:
Business Name: {request.business_name}
Industry: {request.industry}
Target Audience: {request.target_audience}
Product/Service: {request.product_service}
Platform: {request.platform}
Goal: {request.goal}
Tone: {request.tone}
Language: {request.language}
Include Emojis: {request.include_emojis}

Generate:
1. Short Caption (1-2 sentences)
2. Medium Caption (3-4 sentences)
3. Long Caption (5-6 sentences)
4. 20 Relevant Hashtags
5. Call To Action
6. AI Image Prompt

Return ONLY valid JSON with this exact structure:
{{
    "short_caption": "your short caption here",
    "medium_caption": "your medium caption here",
    "long_caption": "your long caption here",
    "hashtags": ["#tag1", "#tag2"],
    "call_to_action": "your CTA here",
    "image_prompt": "your image prompt here"
}}"""

        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert social media marketing specialist. Always return ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ],
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=2048,
        )
        
        response_text = response.choices[0].message.content
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        if start_idx != -1 and end_idx > start_idx:
            data = json.loads(response_text[start_idx:end_idx])
            return {"success": True, "data": data}
        else:
            return {"success": True, "data": get_fallback_content(request), "fallback": True}
        
    except Exception as e:
        return {"success": True, "data": get_fallback_content(request), "fallback": True}

@app.post("/api/hashtags/generate")
async def generate_hashtags(request: HashtagRequest):
    try:
        if not groq_client:
            return {"success": True, "data": {"trending_hashtags": [f"#{request.industry}2026", "#BusinessGrowth"]}, "fallback": True}
        
        prompt = f"""Generate 20 trending hashtags for 2026 for:
Industry: {request.industry}
Business: {request.business_name}

Return ONLY valid JSON:
{{
    "trending_hashtags": ["#tag1", "#tag2"]
}}"""
        
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Return ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ],
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=1024,
        )
        
        response_text = response.choices[0].message.content
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        if start_idx != -1 and end_idx > start_idx:
            data = json.loads(response_text[start_idx:end_idx])
            return {"success": True, "data": data}
        else:
            return {"success": True, "data": {"trending_hashtags": [f"#{request.industry}2026", "#BusinessGrowth"]}, "fallback": True}
        
    except Exception as e:
        return {"success": True, "data": {"trending_hashtags": [f"#{request.industry}2026", "#BusinessGrowth"]}, "fallback": True}

@app.post("/api/calendar/generate")
async def generate_calendar(request: CalendarRequest):
    try:
        days = min(max(request.days, 7), 30)
        themes = ["Industry News", "Success Stories", "Product Features", "Behind the Scenes", "Tips & Guides"]
        platforms = ["Instagram", "Facebook", "LinkedIn", "Twitter"]
        content_types = ["Post", "Story", "Video", "Carousel"]
        
        plan = []
        from datetime import datetime, timedelta
        start_date = datetime.now().date()
        
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            plan.append({
                "day": i + 1,
                "date": current_date.strftime("%Y-%m-%d"),
                "day_name": current_date.strftime("%A"),
                "content_topic": themes[i % len(themes)],
                "content_type": content_types[i % len(content_types)],
                "platform": platforms[i % len(platforms)],
                "suggested_time": PLATFORM_TIMES.get(platforms[i % len(platforms)], "9 AM - 11 AM"),
                "status": "Draft",
                "notes": f"Focus on {themes[i % len(themes)]}"
            })
        
        return {
            "success": True,
            "data": {
                "daily_content_plan": plan,
                "total_days": days,
                "start_date": start_date.isoformat(),
                "summary": {
                    "total_posts": days,
                    "platforms_used": list(set([p["platform"] for p in plan])),
                    "content_types": list(set([p["content_type"] for p in plan]))
                }
            }
        }
    except Exception as e:
        return {"success": True, "data": {"daily_content_plan": [], "total_days": days, "error": str(e)}}

@app.post("/api/extras/seo-keywords")
async def generate_seo_keywords(request: SEOKeywordsRequest):
    return {
        "success": True,
        "data": {
            "seo_keywords": [
                f"{request.industry} solutions",
                f"{request.product_service} services",
                f"best {request.industry}",
                f"professional {request.industry}",
                f"{request.business_name} reviews",
                f"affordable {request.industry}",
                f"{request.industry} near me",
                f"top {request.industry} companies",
                f"{request.industry} experts",
                f"quality {request.product_service}",
                f"{request.industry} consultants",
                f"{request.industry} specialists",
                f"trusted {request.industry}",
                f"reliable {request.industry}",
                f"experienced {request.industry}"
            ]
        }
    }

@app.post("/api/extras/posting-time")
async def get_posting_time(request: PostingTimeRequest):
    platform = request.platform
    if platform in PLATFORM_TIMES:
        return {
            "success": True,
            "data": {
                "platform": platform,
                "best_time": PLATFORM_TIMES[platform],
                "timezone": "Local Time",
                "tips": ["Post 30 minutes before peak time", "Engage with comments immediately"]
            }
        }
    else:
        return {
            "success": True,
            "data": {
                "platform": platform,
                "best_time": "9 AM – 11 AM",
                "timezone": "Local Time",
                "tips": ["Test different times", "Monitor engagement metrics"]
            }
        }