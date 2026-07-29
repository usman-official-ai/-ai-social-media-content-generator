from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List, Optional
from services.groq_service import groq_service

router = APIRouter(prefix="/calendar", tags=["calendar"])

class CalendarRequest(BaseModel):
    days: int

PLATFORM_TIMES = {
    "Instagram": "7 PM – 9 PM (Best engagement)",
    "LinkedIn": "9 AM – 11 AM (Professional hours)",
    "Facebook": "9 AM – 11 AM, 1 PM – 3 PM (Peak activity)",
    "Twitter": "12 PM – 1 PM, 5 PM – 6 PM (Lunch & commute)"
}

@router.post("/generate")
async def generate_calendar(request: CalendarRequest):
    try:
        days = min(max(request.days, 7), 30)
        
        themes = [
            "Industry News & Trends",
            "Customer Success Stories",
            "Product/Service Features",
            "Behind the Scenes",
            "Tips & How-To Guides",
            "Company Culture",
            "Community Engagement",
            "Educational Content",
            "Announcements",
            "Interactive Posts"
        ]
        
        platforms = ["Instagram", "Facebook", "LinkedIn", "Twitter"]
        content_types = ["Post", "Story", "Video", "Carousel", "Infographic"]
        
        plan = []
        start_date = datetime.now().date()
        
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            day_plan = {
                "day": i + 1,
                "date": current_date.strftime("%Y-%m-%d"),
                "day_name": current_date.strftime("%A"),
                "content_topic": themes[i % len(themes)],
                "content_type": content_types[i % len(content_types)],
                "platform": platforms[i % len(platforms)],
                "suggested_time": PLATFORM_TIMES.get(platforms[i % len(platforms)], "9 AM - 11 AM"),
                "status": "Draft",
                "notes": f"Focus on {themes[i % len(themes)]}"
            }
            plan.append(day_plan)
        
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
        raise HTTPException(status_code=500, detail=str(e))