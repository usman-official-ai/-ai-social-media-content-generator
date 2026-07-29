from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from services.groq_service import groq_service

router = APIRouter(prefix="/hashtags", tags=["hashtags"])

class HashtagRequest(BaseModel):
    industry: str
    business_name: str
    target_audience: str

@router.post("/generate")
async def generate_hashtags(request: HashtagRequest):
    try:
        prompt = f"""Generate 20 trending hashtags for 2026 for:
Industry: {request.industry}
Business: {request.business_name}
Target Audience: {request.target_audience}

Include mix of:
- Industry-specific hashtags for 2026 trends
- Trending hashtags in 2026
- Viral marketing hashtags
- Branded hashtags

Return ONLY valid JSON:
{{
    "trending_hashtags": ["#tag1", "#tag2", ...]
}}"""

        result = groq_service.generate_json_response(
            prompt,
            expected_fields=['trending_hashtags']
        )
        
        if result["success"]:
            return {"success": True, "data": result["data"]}
        else:
            # Fallback hashtags
            return {
                "success": True,
                "data": {
                    "trending_hashtags": [
                        f"#{request.industry.replace(' ', '')}2026",
                        f"#{request.business_name.replace(' ', '')}",
                        "#BusinessGrowth2026",
                        "#MarketingTips2026",
                        "#DigitalStrategy2026",
                        "#SuccessMindset",
                        "#InnovationHub",
                        "#QualityMatters",
                        "#ClientFirst",
                        "#ResultsNow",
                        "#TrendingNow",
                        "#IndustryExpert",
                        "#BestPractices",
                        "#BusinessSolutions",
                        "#MarketLeader",
                        "#GrowthHacker",
                        "#ProfessionalService",
                        "#ValueAddition",
                        "#FutureForward",
                        "#CommunityBuilding"
                    ]
                },
                "fallback": True
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))