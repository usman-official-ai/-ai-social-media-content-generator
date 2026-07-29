import os
import json
import logging
from typing import Dict, Any, List, Optional
from groq import Groq
from utils.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GroqService:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=self.api_key)
        self.model = settings.GROQ_MODEL
        self.max_tokens = settings.GROQ_MAX_TOKENS
        self.temperature = settings.GROQ_TEMPERATURE
        
        logger.info(f"✅ Groq API initialized with model: {self.model}")

    def generate_content(self, prompt: str, max_tokens: int = None, temperature: float = None) -> Dict[str, Any]:
        """Generate content using Groq API"""
        try:
            logger.info("📤 Sending request to Groq API...")
            
            if max_tokens is None:
                max_tokens = self.max_tokens
            if temperature is None:
                temperature = self.temperature
            
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert social media marketing specialist with 10+ years of experience. Always return ONLY valid JSON responses."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=1,
                stop=None,
            )
            
            response_text = chat_completion.choices[0].message.content
            logger.info(f"📥 Response received, length: {len(response_text)}")
            
            return {
                "success": True,
                "response": response_text,
                "model": self.model,
                "usage": {
                    "tokens": chat_completion.usage.total_tokens if hasattr(chat_completion, 'usage') else 0
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error calling Groq API: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def generate_json_response(self, prompt: str, expected_fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """Generate content and ensure valid JSON response"""
        try:
            # Enhanced prompt to force JSON output
            json_prompt = f"""{prompt}

IMPORTANT: Return ONLY valid JSON. No markdown, no explanations, no extra text. Just the JSON object."""
            
            result = self.generate_content(json_prompt)
            
            if not result["success"]:
                return {"success": False, "error": result["error"]}
            
            response_text = result["response"]
            
            # Try to extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                try:
                    data = json.loads(json_str)
                    
                    # Check if all expected fields are present
                    if expected_fields:
                        for field in expected_fields:
                            if field not in data:
                                data[field] = f"Default {field.replace('_', ' ')}"
                    
                    return {
                        "success": True,
                        "data": data,
                        "raw_response": response_text
                    }
                except json.JSONDecodeError as e:
                    logger.error(f"JSON parsing error: {e}")
                    return {
                        "success": False,
                        "error": "Failed to parse JSON response",
                        "raw_response": response_text
                    }
            else:
                return {
                    "success": False,
                    "error": "No JSON found in response",
                    "raw_response": response_text
                }
                
        except Exception as e:
            logger.error(f"Error in generate_json_response: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

# Create singleton instance
groq_service = GroqService()