import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

# Groq API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# Helper
def get_fallback_content(data):
    emoji = "✨" if data.get("include_emojis") else ""
    return {
        "short_caption": f"Transform your business with {data.get('business_name')} today! {emoji}",
        "medium_caption": f"At {data.get('business_name')}, we're revolutionizing the {data.get('industry')} industry.",
        "long_caption": f"Ready to take your business to the next level? {data.get('business_name')} specializes in {data.get('product_service')}.",
        "hashtags": [f"#{data.get('business_name', '').replace(' ', '')}", "#Business", "#Growth"],
        "call_to_action": f"Contact {data.get('business_name')} today!",
        "image_prompt": f"Professional {data.get('industry')} business setting"
    }

@app.route('/')
def home():
    return jsonify({"status": "ok", "message": "Flask + Groq API running on Vercel!"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "ai_provider": "Groq", "api_key_set": bool(GROQ_API_KEY)})

@app.route('/api/content/generate', methods=['POST'])
def generate_content():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        if not groq_client:
            return jsonify({"success": True, "data": get_fallback_content(data), "fallback": True})

        prompt = f"""You are an expert social media marketing specialist.
Generate social media content for:
Business Name: {data.get('business_name')}
Industry: {data.get('industry')}
Target Audience: {data.get('target_audience')}
Product/Service: {data.get('product_service')}
Platform: {data.get('platform')}
Goal: {data.get('goal')}
Tone: {data.get('tone')}
Language: {data.get('language')}
Include Emojis: {data.get('include_emojis')}

Generate:
1. Short Caption (1-2 sentences)
2. Medium Caption (3-4 sentences)
3. Long Caption (5-6 sentences)
4. 20 Relevant Hashtags
5. Call To Action
6. AI Image Prompt

Return ONLY valid JSON:
{{"short_caption": "...", "medium_caption": "...", "long_caption": "...", "hashtags": ["#tag1", "#tag2"], "call_to_action": "...", "image_prompt": "..."}}"""

        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Return ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ],
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=2048,
        )

        response_text = response.choices[0].message.content
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        if start != -1 and end > start:
            data = json.loads(response_text[start:end])
            return jsonify({"success": True, "data": data})
        else:
            return jsonify({"success": True, "data": get_fallback_content(data), "fallback": True})

    except Exception as e:
        return jsonify({"success": True, "data": get_fallback_content(data), "fallback": True})

if __name__ == "__main__":
    app.run(debug=True)