"""
All prompt strings live here, separate from route/service logic, so they can
be tuned or A/B tested without touching application code.
"""


def _emoji_line(include_emojis: bool) -> str:
    return (
        "Include tasteful, relevant emojis throughout the captions."
        if include_emojis
        else "Do not use any emojis. Keep the text emoji-free."
    )


def content_prompt(info: dict) -> str:
    return f"""You are an expert social media marketing specialist and copywriter.

Generate social media content for the business below, written specifically for
{info['platform']}, in a {info['tone']} tone, in {info['language']}.
{_emoji_line(info['include_emojis'])}

Business Name: {info['business_name']}
Industry: {info['industry']}
Target Audience: {info['target_audience']}
Product/Service: {info['product_service']}
Goal: {info['goal']}
Platform: {info['platform']}
Tone: {info['tone']}
Language: {info['language']}

Return ONLY a valid JSON object (no markdown fences, no commentary) with this
exact shape:

{{
  "short_caption": "1-2 line caption",
  "medium_caption": "3-5 line caption",
  "long_caption": "a longer storytelling-style caption, 6-10 lines",
  "hashtags": ["#tag1", "#tag2", "... 20 relevant hashtags total"],
  "cta": "one strong call-to-action sentence",
  "image_prompt": "a detailed AI image-generation prompt matching the brand and post",
  "variations": {{
    "version_a": "an alternate short/medium caption, different angle",
    "version_b": "another alternate caption, different angle",
    "version_c": "a third alternate caption, different angle"
  }}
}}

Only output the JSON object, nothing else."""


def hashtags_prompt(info: dict) -> str:
    return f"""You are a social media hashtag strategist.

Generate 15-20 hashtags for this business, mixing niche, industry, and
currently trending/viral hashtags. Also separately flag which ones are
"trending" style hashtags.

Business Name: {info['business_name']}
Industry: {info['industry']}
Target Audience: {info['target_audience']}
Platform: {info['platform']}

Return ONLY valid JSON (no markdown fences) in this exact shape:

{{
  "hashtags": ["#tag1", "#tag2", "... 15-20 total"],
  "trending_hashtags": ["#trend1", "#trend2", "... 5-8 of the above or related trending tags"]
}}

Only output the JSON object, nothing else."""


def calendar_prompt(info: dict, days: int) -> str:
    return f"""You are a social media content strategist.

Create a {days}-day content calendar for this business, one idea per day,
varying the content type (educational, promotional, behind-the-scenes,
testimonial, engagement/question, product highlight, etc.).

Business Name: {info['business_name']}
Industry: {info['industry']}
Target Audience: {info['target_audience']}
Platform: {info['platform']}
Goal: {info['goal']}
Tone: {info['tone']}

Return ONLY valid JSON (no markdown fences) in this exact shape:

{{
  "calendar": [
    {{
      "day": 1,
      "content_type": "e.g. Educational",
      "topic": "short topic/headline for the post",
      "caption_idea": "1-2 sentence caption idea"
    }}
  ]
}}

The "calendar" array must contain exactly {days} entries, day 1 through day {days}.
Only output the JSON object, nothing else."""


def keywords_prompt(info: dict) -> str:
    return f"""You are an SEO strategist for social media and content marketing.

Generate 10-15 SEO/discovery keywords and short keyword phrases relevant to
this business that would help its content get found (for captions, alt text,
and bios).

Business Name: {info['business_name']}
Industry: {info['industry']}
Target Audience: {info['target_audience']}
Product/Service: {info['product_service']}

Return ONLY valid JSON (no markdown fences) in this exact shape:

{{
  "keywords": ["keyword one", "keyword two", "... 10-15 total"]
}}

Only output the JSON object, nothing else."""
