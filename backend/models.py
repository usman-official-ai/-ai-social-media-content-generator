from typing import Literal
from pydantic import BaseModel, Field

Platform = Literal["Facebook", "Instagram", "LinkedIn", "Twitter (X)"]
Goal = Literal["Sales", "Awareness", "Engagement"]
Tone = Literal[
    "Professional", "Friendly", "Funny", "Luxury", "Promotional", "Educational"
]
Language = Literal["English", "Urdu"]


class BusinessInfo(BaseModel):
    business_name: str = Field(..., min_length=1, examples=["Bright Smile Dental"])
    industry: str = Field(..., min_length=1, examples=["Healthcare / Dental Clinic"])
    target_audience: str = Field(..., min_length=1, examples=["Families in Lahore, ages 25-45"])
    product_service: str = Field(..., min_length=1, examples=["Teeth whitening & general dentistry"])
    goal: Goal = "Awareness"
    platform: Platform = "Instagram"
    tone: Tone = "Friendly"
    language: Language = "English"
    include_emojis: bool = True


class CalendarRequest(BusinessInfo):
    days: Literal[7, 30] = 7


class ContentResponse(BaseModel):
    short_caption: str
    medium_caption: str
    long_caption: str
    hashtags: list[str]
    cta: str
    image_prompt: str
    variations: dict


class HashtagsResponse(BaseModel):
    hashtags: list[str]
    trending_hashtags: list[str]


class CalendarResponse(BaseModel):
    calendar: list[dict]


class KeywordsResponse(BaseModel):
    keywords: list[str]


class PostingTimeResponse(BaseModel):
    platform: str
    best_time: str
    note: str
