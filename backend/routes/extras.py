from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import io
import json
from datetime import datetime
from services.groq_service import groq_service

router = APIRouter(prefix="/extras", tags=["extras"])

class SEOKeywordsRequest(BaseModel):
    business_name: str
    industry: str
    product_service: str

class DownloadRequest(BaseModel):
    content: Dict[str, Any]
    business_name: str
    format: str

class PostingTimeRequest(BaseModel):
    platform: str

PLATFORM_TIMES = {
    "Instagram": "7 PM – 9 PM (Best engagement)",
    "LinkedIn": "9 AM – 11 AM (Professional hours)",
    "Facebook": "9 AM – 11 AM, 1 PM – 3 PM (Peak activity)",
    "Twitter": "12 PM – 1 PM, 5 PM – 6 PM (Lunch & commute)"
}

@router.post("/seo-keywords")
async def generate_seo_keywords(request: SEOKeywordsRequest):
    try:
        prompt = f"""Generate 15 SEO keywords for:
Business: {request.business_name}
Industry: {request.industry}
Product/Service: {request.product_service}

Return ONLY valid JSON:
{{
    "seo_keywords": ["keyword1", "keyword2", ...]
}}"""

        result = groq_service.generate_json_response(
            prompt,
            expected_fields=['seo_keywords']
        )
        
        if result["success"]:
            return {"success": True, "data": result["data"]}
        else:
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
                },
                "fallback": True
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/posting-time")
async def get_posting_time(request: PostingTimeRequest):
    try:
        platform = request.platform
        
        if platform in PLATFORM_TIMES:
            return {
                "success": True,
                "data": {
                    "platform": platform,
                    "best_time": PLATFORM_TIMES[platform],
                    "timezone": "Local Time",
                    "tips": [
                        "Post 30 minutes before peak time",
                        "Engage with comments immediately",
                        "Share to stories at peak time",
                        "Use analytics to track engagement"
                    ]
                }
            }
        else:
            return {
                "success": True,
                "data": {
                    "platform": platform,
                    "best_time": "9 AM – 11 AM and 1 PM – 3 PM",
                    "timezone": "Local Time",
                    "tips": [
                        "Test different times",
                        "Monitor engagement metrics",
                        "Adjust based on audience analytics"
                    ]
                }
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/download")
async def download_content(request: DownloadRequest):
    try:
        content = request.content
        business_name = request.business_name
        file_format = request.format.lower()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{business_name}_{timestamp}"
        
        if file_format == 'txt':
            txt_content = f"""
╔══════════════════════════════════════════════════════════════╗
║  AI-GENERATED SOCIAL MEDIA CONTENT                          ║
║  Generated for: {business_name}                            ║
║  Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}     ║
╚══════════════════════════════════════════════════════════════╝

📝 SHORT CAPTION
{'-' * 50}
{content.get('short_caption', 'N/A')}

📝 MEDIUM CAPTION
{'-' * 50}
{content.get('medium_caption', 'N/A')}

📝 LONG CAPTION
{'-' * 50}
{content.get('long_caption', 'N/A')}

#️⃣ HASHTAGS
{'-' * 50}
{', '.join(content.get('hashtags', []))}

📢 CALL TO ACTION
{'-' * 50}
{content.get('call_to_action', 'N/A')}

🖼️ IMAGE PROMPT
{'-' * 50}
{content.get('image_prompt', 'N/A')}

{'-' * 50}
Generated by AI Social Media Content Generator
Powered by Groq AI
"""
            
            return StreamingResponse(
                io.BytesIO(txt_content.encode('utf-8')),
                media_type="text/plain",
                headers={"Content-Disposition": f"attachment; filename={filename}.txt"}
            )
        
        elif file_format == 'pdf':
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.enums import TA_CENTER
            
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            
            title_style = ParagraphStyle(
                'TitleStyle',
                parent=styles['Heading1'],
                fontSize=24,
                alignment=TA_CENTER,
                spaceAfter=30
            )
            
            heading_style = ParagraphStyle(
                'HeadingStyle',
                parent=styles['Heading2'],
                fontSize=16,
                spaceAfter=10
            )
            
            content_style = ParagraphStyle(
                'ContentStyle',
                parent=styles['Normal'],
                fontSize=12,
                spaceAfter=15
            )
            
            story = []
            story.append(Paragraph("AI-GENERATED SOCIAL MEDIA CONTENT", title_style))
            story.append(Paragraph(f"Generated for: {business_name}", styles['Normal']))
            story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            story.append(Spacer(1, 20))
            
            sections = [
                ("📝 SHORT CAPTION", content.get('short_caption', 'N/A')),
                ("📝 MEDIUM CAPTION", content.get('medium_caption', 'N/A')),
                ("📝 LONG CAPTION", content.get('long_caption', 'N/A')),
                ("#️⃣ HASHTAGS", ', '.join(content.get('hashtags', []))),
                ("📢 CALL TO ACTION", content.get('call_to_action', 'N/A')),
                ("🖼️ IMAGE PROMPT", content.get('image_prompt', 'N/A'))
            ]
            
            for heading, text in sections:
                story.append(Paragraph(heading, heading_style))
                story.append(Paragraph(text, content_style))
                story.append(Spacer(1, 10))
            
            story.append(Spacer(1, 30))
            story.append(Paragraph("Powered by Groq AI", styles['Normal']))
            
            doc.build(story)
            buffer.seek(0)
            
            return StreamingResponse(
                buffer,
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename={filename}.pdf"}
            )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))