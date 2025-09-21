#!/usr/bin/env python3
"""
JACAI - AI-Powered Social Media Generator
Simple Python version that works instantly
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
import requests
from datetime import datetime
import os

# AI Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-gemini-api-key-here")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

app = FastAPI(title="JACAI - AI Social Media Generator", version="1.0.0")

# Serve static files
app.mount("/static", StaticFiles(directory="web"), name="static")
templates = Jinja2Templates(directory="web")

class GenerateRequest(BaseModel):
    topic: str
    platform: str = "instagram"
    style: str = "professional"

def call_gemini(prompt: str) -> str:
    """Mock AI responses for demo (no API key needed)"""
    import random
    import time
    
    # Simulate API delay
    time.sleep(1)
    
    # Mock responses based on prompt type
    if "hashtag" in prompt.lower():
        hashtags = [
            "#motivation #success #mindset #goals #inspiration #hustle #entrepreneur #growth",
            "#socialmedia #content #marketing #digital #brand #creative #strategy #engagement",
            "#tech #innovation #ai #future #startup #coding #development #technology",
            "#lifestyle #wellness #health #fitness #selfcare #mindfulness #balance #positivity"
        ]
        return random.choice(hashtags)
    
    elif "image" in prompt.lower():
        image_prompts = [
            "Professional corporate setting with clean lines, modern office space, natural lighting, minimalist design, high-quality photography style",
            "Vibrant and colorful creative workspace, artistic elements, inspiring quotes, energetic atmosphere, contemporary design",
            "Motivational scene with upward arrows, success symbols, bright colors, dynamic composition, inspiring visual metaphors",
            "Social media themed illustration with icons, connections, networks, modern flat design, engaging visual elements"
        ]
        return random.choice(image_prompts)
    
    else:  # Caption generation
        captions = [
            "🚀 Ready to take your goals to the next level? Success isn't just about the destination—it's about the journey and the mindset you bring along the way. Every small step counts, every effort matters, and every challenge is an opportunity to grow stronger. What's one goal you're working toward this week? Share it below and let's support each other! 💪✨ #MotivationMonday",
            
            "💡 Innovation happens when we dare to think differently. In today's fast-paced world, the companies and individuals who thrive are those who embrace change, learn continuously, and aren't afraid to challenge the status quo. What's one innovative idea you've been thinking about lately? Let's discuss how we can turn ideas into reality! 🌟",
            
            "🎯 Content creation is more than just posting—it's about building genuine connections with your audience. Every piece of content should tell a story, provide value, or spark meaningful conversations. Remember: authenticity beats perfection every time. What story are you telling through your content today? 📱✨",
            
            "🌱 Personal growth is a continuous journey, not a destination. Each day presents new opportunities to learn something new, overcome a challenge, or help someone else along their path. The key is consistency and patience with yourself. What's one thing you've learned about yourself recently? 💭🌟"
        ]
        return random.choice(captions)

def generate_caption(topic: str, platform: str, style: str) -> str:
    """Generate platform-specific caption"""
    platform_specs = {
        "instagram": "Instagram post with emojis, engaging and visual, 150-200 words",
        "twitter": "Twitter post, concise, under 280 characters, engaging",
        "linkedin": "LinkedIn post, professional tone, business-focused, 200-300 words",
        "facebook": "Facebook post, conversational and engaging, 100-150 words"
    }
    
    style_guides = {
        "professional": "Use professional language, focus on expertise and value",
        "casual": "Use friendly, conversational tone with personality",
        "creative": "Be creative, use metaphors and storytelling",
        "motivational": "Be inspiring and encouraging, focus on growth"
    }
    
    prompt = f"Create a {style} {platform_specs.get(platform, 'social media post')} about '{topic}'. {style_guides.get(style, '')} Make it engaging and shareable."
    
    return call_gemini(prompt)

def generate_hashtags(topic: str, platform: str) -> str:
    """Generate relevant hashtags"""
    prompt = f"Generate 8-10 relevant, trending hashtags for a {platform} post about '{topic}'. Include a mix of popular and niche hashtags. Return only hashtags separated by spaces, starting with #."
    
    return call_gemini(prompt)

def generate_image_prompt(topic: str, platform: str, style: str) -> str:
    """Generate image generation prompt"""
    prompt = f"Create a detailed image generation prompt for a {style} style image about '{topic}' suitable for {platform}. Focus on visual elements, colors, and composition. Keep it under 100 words."
    
    return call_gemini(prompt)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/generate")
async def generate_post(request: GenerateRequest):
    try:
        print(f"🚀 Generating content for: {request.topic} ({request.platform}, {request.style})")
        
        # Generate all content
        caption = generate_caption(request.topic, request.platform, request.style)
        hashtags = generate_hashtags(request.topic, request.platform)
        image_prompt = generate_image_prompt(request.topic, request.platform, request.style)
        
        return JSONResponse({
            "success": True,
            "post": {
                "topic": request.topic,
                "platform": request.platform,
                "style": request.style,
                "caption": caption,
                "hashtags": hashtags,
                "image_prompt": image_prompt,
                "created_at": datetime.now().isoformat()
            }
        })
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "JACAI"}

@app.get("/api/test-gemini")
async def test_gemini():
    """Test AI generation (demo mode)"""
    test_result = call_gemini("Say hello in one word")
    return {"result": test_result, "mode": "demo"}

if __name__ == "__main__":
    print("🚀 Starting JACAI - AI Social Media Generator")
    print("📱 Access at: http://localhost:8080")
    print("🤖 Powered by Gemini AI")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info"
    )