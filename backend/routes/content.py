from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from services.groq_service import groq_service

router = APIRouter(prefix="/content", tags=["content"])

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

@router.post("/generate")
async def generate_content(request: ContentRequest):
    try:
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
1. Short Caption (1-2 sentences) - Catchy and attention-grabbing
2. Medium Caption (3-4 sentences) - Engaging and informative
3. Long Caption (5-6 sentences) - Detailed and compelling
4. 20 Relevant Hashtags - Mix of trending and niche hashtags
5. Call To Action - Clear and actionable
6. AI Image Prompt - Detailed visual description for image generation

Return ONLY valid JSON with this exact structure:
{{
    "short_caption": "your short caption here",
    "medium_caption": "your medium caption here",
    "long_caption": "your long caption here",
    "hashtags": ["#tag1", "#tag2", ...],
    "call_to_action": "your CTA here",
    "image_prompt": "your image prompt here"
}}"""

        result = groq_service.generate_json_response(
            prompt,
            expected_fields=['short_caption', 'medium_caption', 'long_caption', 'hashtags', 'call_to_action', 'image_prompt']
        )
        
        if result["success"]:
            return {"success": True, "data": result["data"]}
        else:
            # Fallback content
            fallback = {
                "short_caption": f"Transform your business with {request.business_name} today! ✨",
                "medium_caption": f"At {request.business_name}, we're revolutionizing the {request.industry} industry.",
                "long_caption": f"Ready to take your business to the next level? {request.business_name} specializes in {request.product_service}.",
                "hashtags": [f"#{request.business_name.replace(' ', '')}", f"#{request.industry}", "#Business", "#Growth"],
                "call_to_action": f"Contact {request.business_name} today!",
                "image_prompt": f"Professional {request.industry} business setting"
            }
            return {"success": True, "data": fallback, "fallback": True}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))