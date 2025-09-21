"""
AI Service for JACAI - Real AI Integration
"""
import requests
import openai
from config import GEMINI_API_KEY, OPENAI_API_KEY
import json
import time
from typing import Dict, List

class AIService:
    def __init__(self):
        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
        
    def generate_content(self, topic: str, platform: str, style: str, use_openai: bool = False) -> Dict:
        """Generate content using AI"""
        if use_openai and self.openai_client:
            return self._generate_with_openai(topic, platform, style)
        else:
            return self._generate_with_gemini(topic, platform, style)
    
    def _generate_with_gemini(self, topic: str, platform: str, style: str) -> Dict:
        """Generate content using Gemini"""
        try:
            # Generate caption
            caption_prompt = self._build_caption_prompt(topic, platform, style)
            caption = self._call_gemini(caption_prompt)
            
            # Generate hashtags
            hashtag_prompt = f"Generate 8-10 trending hashtags for {platform} about '{topic}'. Return only hashtags with # symbol, separated by spaces."
            hashtags = self._call_gemini(hashtag_prompt)
            
            # Generate image prompt
            image_prompt = f"Create a detailed image prompt for {style} style visual about '{topic}' for {platform}. Include colors, composition, mood. Max 100 words."
            image_description = self._call_gemini(image_prompt)
            
            return {
                "caption": caption,
                "hashtags": hashtags,
                "image_prompt": image_description,
                "ai_provider": "gemini"
            }
        except Exception as e:
            return self._fallback_content(topic, platform, style, str(e))
    
    def _generate_with_openai(self, topic: str, platform: str, style: str) -> Dict:
        """Generate content using OpenAI"""
        try:
            # Generate caption
            caption_prompt = self._build_caption_prompt(topic, platform, style)
            caption_response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": caption_prompt}],
                max_tokens=300,
                temperature=0.7
            )
            caption = caption_response.choices[0].message.content
            
            # Generate hashtags
            hashtag_response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Generate 8-10 hashtags for {platform} about '{topic}'"}],
                max_tokens=100,
                temperature=0.5
            )
            hashtags = hashtag_response.choices[0].message.content
            
            # Generate image prompt
            image_response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Create image prompt for {style} {topic} visual"}],
                max_tokens=150,
                temperature=0.6
            )
            image_prompt = image_response.choices[0].message.content
            
            return {
                "caption": caption,
                "hashtags": hashtags,
                "image_prompt": image_prompt,
                "ai_provider": "openai"
            }
        except Exception as e:
            return self._fallback_content(topic, platform, style, str(e))
    
    def _call_gemini(self, prompt: str) -> str:
        """Call Gemini API"""
        try:
            headers = {"Content-Type": "application/json"}
            data = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            
            response = requests.post(
                f"{self.gemini_url}?key={GEMINI_API_KEY}",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["candidates"][0]["content"]["parts"][0]["text"]
            else:
                raise Exception(f"Gemini API error: {response.status_code}")
                
        except Exception as e:
            raise Exception(f"Gemini API call failed: {str(e)}")
    
    def _build_caption_prompt(self, topic: str, platform: str, style: str) -> str:
        """Build platform-specific caption prompt"""
        platform_specs = {
            "instagram": "Instagram post with emojis, engaging and visual, 150-200 words, include call-to-action",
            "twitter": "Twitter post, concise, under 280 characters, engaging, trending",
            "linkedin": "LinkedIn post, professional tone, business-focused, 200-300 words, thought leadership",
            "facebook": "Facebook post, conversational and engaging, 100-150 words, community-focused",
            "tiktok": "TikTok description, trendy, fun, with popular hashtags, under 150 characters"
        }
        
        style_guides = {
            "professional": "Use professional language, focus on expertise and value, authoritative tone",
            "casual": "Use friendly, conversational tone with personality, relatable",
            "creative": "Be creative, use metaphors and storytelling, artistic approach",
            "motivational": "Be inspiring and encouraging, focus on growth and success",
            "humorous": "Use appropriate humor, witty, entertaining but respectful"
        }
        
        return f"""Create a {style} {platform_specs.get(platform, 'social media post')} about "{topic}".

Style guide: {style_guides.get(style, '')}

Requirements:
- Make it engaging and shareable
- Include relevant emojis where appropriate
- End with a question or call-to-action to encourage engagement
- Ensure it matches the {platform} audience and format
- Topic focus: {topic}

Generate only the caption text, no additional formatting or labels."""
    
    def _fallback_content(self, topic: str, platform: str, style: str, error: str) -> Dict:
        """Fallback content when AI fails"""
        print(f"AI generation failed: {error}. Using fallback content.")
        
        fallback_captions = {
            "professional": f"Exploring {topic} and its impact on our industry. What are your thoughts on this important subject? Share your insights below. #professional #insights",
            "casual": f"Just thinking about {topic} and how it affects us all! 🤔 What's your take on this? Let's chat in the comments! ✨",
            "creative": f"🎨 {topic} is like a canvas waiting for our creativity. Every perspective adds a new color to the masterpiece. What's your brushstroke? 🖌️",
            "motivational": f"💪 {topic} reminds us that every challenge is an opportunity to grow stronger. What's one lesson you've learned recently? Share your wisdom! 🌟"
        }
        
        return {
            "caption": fallback_captions.get(style, f"Sharing thoughts on {topic}. What do you think?"),
            "hashtags": f"#{topic.replace(' ', '')} #content #socialmedia #engagement #community",
            "image_prompt": f"Professional image about {topic}, clean design, modern style",
            "ai_provider": "fallback",
            "error": error
        }

# Global AI service instance
ai_service = AIService()