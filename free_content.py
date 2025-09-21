#!/usr/bin/env python3
"""
Free Content Generation Methods for JACAI
"""

import requests
import random
from datetime import datetime

def get_free_ai_content(topic: str, platform: str) -> str:
    """Get free AI-generated content using various free APIs"""
    
    # Method 1: Hugging Face Inference API (Free)
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
            headers={"Authorization": "Bearer hf_demo"},  # Demo token
            json={"inputs": f"Write a {platform} post about {topic}"},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()[0]['generated_text']
    except:
        pass
    
    # Method 2: OpenAI-compatible free endpoints
    free_endpoints = [
        "https://api.openai-proxy.com/v1/chat/completions",
        "https://free-api.openai.com/v1/chat/completions"
    ]
    
    for endpoint in free_endpoints:
        try:
            response = requests.post(endpoint, 
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": f"Create a {platform} post about {topic}"}],
                    "max_tokens": 150
                },
                timeout=10
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
        except:
            continue
    
    # Method 3: Template-based generation (Always works)
    templates = {
        "instagram": [
            f"🚀 {topic} is changing the game! ✨\n\nWhat's your experience with this? Drop a comment below! 👇\n\n#trending #content #social",
            f"💡 Quick thoughts on {topic}:\n\n• It's revolutionary\n• Game-changing potential\n• Worth exploring\n\nWhat do you think? 🤔",
            f"🎯 {topic} insights:\n\nThis is something everyone should know about. The impact is incredible!\n\nSave this post for later 📌"
        ],
        "twitter": [
            f"🧵 Thread on {topic}:\n\n1/ This is bigger than most people realize\n2/ The implications are huge\n3/ Here's why you should care...",
            f"Hot take: {topic} is the future 🔥\n\nWho else is excited about this? #tech #innovation",
            f"Just discovered something amazing about {topic} 🤯\n\nThis changes everything. Thread below 👇"
        ],
        "linkedin": [
            f"Professional insight on {topic}:\n\nAfter analyzing the trends, I believe this will significantly impact our industry. Here's my take on what professionals should know.\n\nWhat's your perspective?",
            f"Industry update: {topic}\n\nKey takeaways for professionals:\n• Strategic importance\n• Market implications\n• Future opportunities\n\nLet's discuss in the comments.",
            f"Thought leadership: {topic}\n\nAs someone working in this space, I've observed some interesting patterns. The potential for growth and innovation is substantial."
        ]
    }
    
    platform_templates = templates.get(platform, templates["instagram"])
    return random.choice(platform_templates)

def get_trending_hashtags(topic: str, platform: str) -> str:
    """Generate trending hashtags for free"""
    
    # Base hashtags by platform
    platform_tags = {
        "instagram": ["#content", "#social", "#trending", "#viral", "#explore", "#instagood"],
        "twitter": ["#trending", "#tech", "#innovation", "#discussion", "#thread"],
        "linkedin": ["#professional", "#business", "#industry", "#networking", "#growth", "#leadership"]
    }
    
    # Topic-based hashtags
    topic_words = topic.lower().split()
    topic_tags = [f"#{word}" for word in topic_words if len(word) > 3]
    
    # Combine and return
    base_tags = platform_tags.get(platform, platform_tags["instagram"])
    all_tags = topic_tags + base_tags[:5]
    
    return " ".join(all_tags[:8])

def generate_free_content_batch(topics: list, platforms: list) -> dict:
    """Generate free content for multiple topics and platforms"""
    
    results = []
    
    for topic in topics:
        for platform in platforms:
            content = {
                "topic": topic,
                "platform": platform,
                "caption": get_free_ai_content(topic, platform),
                "hashtags": get_trending_hashtags(topic, platform),
                "image_prompt": f"Create a professional, engaging image about {topic} suitable for {platform}. Modern, clean design with vibrant colors.",
                "generated_at": datetime.now().isoformat(),
                "method": "free_ai"
            }
            results.append(content)
    
    return {"success": True, "results": results, "cost": "$0.00"}

if __name__ == "__main__":
    # Test free content generation
    topics = ["AI productivity", "social media marketing", "remote work"]
    platforms = ["instagram", "twitter", "linkedin"]
    
    print("🆓 Testing Free Content Generation...")
    results = generate_free_content_batch(topics, platforms)
    
    print(f"✅ Generated {len(results['results'])} pieces of content for FREE!")
    
    for content in results['results'][:3]:  # Show first 3
        print(f"\n📱 {content['platform'].upper()} - {content['topic']}")
        print(f"Caption: {content['caption'][:100]}...")
        print(f"Hashtags: {content['hashtags']}")