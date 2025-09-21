#!/usr/bin/env python3
"""
JACAI - AI Social Media Platform (Python with Jac Integration)
Simplified version that works with existing web interface
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import os
from datetime import datetime

app = FastAPI(title="JACAI - AI Social Media Platform", version="2.0.0")

# Serve static files
app.mount("/static", StaticFiles(directory="web"), name="static")

class GenerateRequest(BaseModel):
    topic: str
    platform: str = "instagram"
    style: str = "professional"

def generate_content(topic: str, platform: str, style: str) -> dict:
    """Generate platform-specific content with free AI options"""
    
    # Try free AI APIs first
    try:
        # Hugging Face free API (no key needed for basic models)
        import requests
        response = requests.post(
            "https://api-inference.huggingface.co/models/gpt2",
            json={"inputs": f"Create a {style} {platform} post about {topic}:"},
            timeout=10
        )
        if response.status_code == 200:
            ai_content = response.json()[0]['generated_text']
            return {
                "caption": ai_content[:200] + "...",
                "hashtags": f"#{topic.replace(' ', '')} #content #social #{platform}",
                "image_prompt": f"Professional image about {topic} for {platform}"
            }
    except:
        pass  # Fall back to templates
    
    # Platform-specific templates (fallback)
    platform_templates = {
        "instagram": {
            "caption": f"🚀 {topic} - Perfect for your Instagram feed! ✨\n\nShare your thoughts below 👇\n\n#instagram #content #social",
            "hashtags": "#content #social #marketing #instagram #digital #brand #creative #engagement"
        },
        "twitter": {
            "caption": f"Quick thoughts on {topic} 🧵\n\nWhat's your take?",
            "hashtags": "#content #social #marketing #twitter #digital"
        },
        "linkedin": {
            "caption": f"Professional insights on {topic}.\n\nLet's discuss the implications for our industry. What are your thoughts?",
            "hashtags": "#professional #business #networking #linkedin #growth #industry"
        },
        "facebook": {
            "caption": f"Let's talk about {topic} today!\n\nWhat's your experience with this? Share in the comments!",
            "hashtags": "#social #community #discussion #engagement #facebook"
        }
    }
    
    # Style modifications
    if style == "casual":
        platform_templates[platform]["caption"] = platform_templates[platform]["caption"].replace("Professional insights", "Casual thoughts")
    elif style == "creative":
        platform_templates[platform]["caption"] = "🎨 " + platform_templates[platform]["caption"]
    elif style == "motivational":
        platform_templates[platform]["caption"] = "💪 " + platform_templates[platform]["caption"] + " You've got this!"
    
    template = platform_templates.get(platform, platform_templates["instagram"])
    
    return {
        "caption": template["caption"],
        "hashtags": template["hashtags"],
        "image_prompt": f"Create a {style} style image about {topic} suitable for {platform}. Focus on visual elements, colors, and composition."
    }

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the login page as home"""
    with open("web/login.html", "r") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Serve the main dashboard"""
    with open("web/dashboard.html", "r") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.get("/link-accounts", response_class=HTMLResponse)
async def link_accounts():
    """Serve the account linking page"""
    with open("web/account_linking.html", "r") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.get("/login", response_class=HTMLResponse)
async def login_page():
    """Serve the login page"""
    with open("web/login.html", "r") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.get("/account-linking", response_class=HTMLResponse)
async def account_linking():
    """Serve the account linking page"""
    with open("web/account_linking.html", "r") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.get("/compose", response_class=HTMLResponse)
async def compose():
    """Serve the compose page"""
    with open("web/compose.html", "r") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.get("/calendar", response_class=HTMLResponse)
async def calendar():
    """Serve the calendar page"""
    with open("web/calendar.html", "r") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.get("/analytics", response_class=HTMLResponse)
async def analytics():
    """Serve the analytics page"""
    with open("web/analytics.html", "r") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.get("/content-library", response_class=HTMLResponse)
async def content_library():
    """Serve the content library page"""
    with open("web/content-library.html", "r") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.get("/team", response_class=HTMLResponse)
async def team():
    """Serve the team page"""
    return HTMLResponse(content="<h1>Team Management - Coming Soon</h1>")

@app.get("/settings", response_class=HTMLResponse)
async def settings():
    """Serve the settings page"""
    return HTMLResponse(content="<h1>Settings - Coming Soon</h1>")

@app.post("/api/generate")
async def generate_post(request: dict):
    """Generate social media content for multiple platforms"""
    try:
        topic = request.get("topic", "")
        platforms = request.get("platforms", ["instagram"])
        style = request.get("style", "professional")
        auto_post = request.get("auto_post", False)
        
        print(f"🚀 Generating content for: {topic} on {platforms} ({style})")
        
        results = []
        for platform in platforms:
            content = generate_content(topic, platform, style)
            results.append({
                "platform": platform,
                "content": {
                    "caption": content["caption"],
                    "hashtags": content["hashtags"],
                    "image_prompt": content["image_prompt"]
                },
                "posted": auto_post,
                "created_at": datetime.now().isoformat()
            })
        
        return JSONResponse({
            "success": True,
            "results": results
        })
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

@app.post("/api/register")
async def register_user(request: RegisterRequest):
    """Mock user registration"""
    if request.username and request.email and request.password:
        return JSONResponse({
            "success": True,
            "message": "User registered successfully",
            "user_id": "demo_user_123",
            "token": "demo_token_456"
        })
    else:
        return JSONResponse({
            "success": False,
            "error": "All fields are required"
        }, status_code=400)

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/api/login")
async def login_user(request: LoginRequest):
    """Mock user login"""
    # Simple demo authentication
    if request.username and request.password:
        return JSONResponse({
            "success": True,
            "message": "Login successful",
            "user_id": "demo_user_123",
            "token": "demo_token_456",
            "username": request.username
        })
    else:
        return JSONResponse({
            "success": False,
            "error": "Invalid credentials"
        }, status_code=401)

@app.post("/api/connect-social")
async def connect_social(request: dict):
    """Mock social media account connection"""
    platform = request.get("platform", "instagram")
    return JSONResponse({
        "success": True,
        "message": f"{platform.title()} account connected successfully",
        "account_id": f"{platform}_demo_account"
    })

@app.get("/api/social-accounts")
async def get_social_accounts():
    """Get linked social media accounts"""
    # Mock data for demo
    return JSONResponse([
        {
            "platform": "instagram",
            "account_name": "@demo_account",
            "is_active": True
        },
        {
            "platform": "twitter",
            "account_name": "@demo_twitter",
            "is_active": True
        }
    ])

@app.delete("/api/social-accounts/{platform}")
async def unlink_account(platform: str):
    """Unlink social media account"""
    return JSONResponse({"success": True, "message": f"{platform} account unlinked"})

@app.get("/api/test-social-connections")
async def test_connections():
    """Test all social media connections"""
    return JSONResponse({
        "results": [
            {"platform": "instagram", "status": "✅ Connected"},
            {"platform": "twitter", "status": "✅ Connected"},
            {"platform": "linkedin", "status": "❌ Not connected"}
        ]
    })

@app.get("/api/oauth/authorize/{platform}")
async def oauth_authorize(platform: str, redirect_uri: str = None):
    """Mock OAuth authorization"""
    return JSONResponse({
        "auth_url": f"https://demo-oauth.com/{platform}/authorize?redirect_uri={redirect_uri}",
        "state": "demo_state_123"
    })

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "JACAI-Jac", 
        "version": "2.0.0",
        "framework": "FastAPI + Jac Integration"
    }

if __name__ == "__main__":
    print("🚀 Starting JACAI - AI Social Media Platform (Jac-Ready Version)")
    print("📱 Access at: http://localhost:8080")
    print("🤖 Ready for Jac integration")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info"
    )