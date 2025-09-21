#!/usr/bin/env python3
"""
JACAI Pro - Multi-User AI Social Media Generator
With authentication, multi-platform posting, and n8n integration
"""

from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import jwt
import bcrypt
import sqlite3
import requests
from datetime import datetime, timedelta
from typing import Optional, List
import os

# Configuration
SECRET_KEY = "your-secret-key-change-this"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(title="JACAI Pro - Multi-User AI Social Media Generator", version="2.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Serve static files
app.mount("/static", StaticFiles(directory="web"), name="static")
templates = Jinja2Templates(directory="web")

# Database setup
def init_db():
    conn = sqlite3.connect('jacai.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        )
    ''')
    
    # Social accounts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS social_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            platform TEXT NOT NULL,
            account_name TEXT,
            access_token TEXT,
            refresh_token TEXT,
            expires_at TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Generated posts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generated_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            topic TEXT NOT NULL,
            platform TEXT NOT NULL,
            style TEXT NOT NULL,
            caption TEXT,
            hashtags TEXT,
            image_prompt TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            posted_at TIMESTAMP,
            post_status TEXT DEFAULT 'draft',
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class GenerateRequest(BaseModel):
    topic: str
    platforms: List[str] = ["instagram"]
    style: str = "professional"
    auto_post: bool = False

class SocialAccountLink(BaseModel):
    platform: str
    access_token: str
    account_name: str

# Authentication functions
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(username: str = Depends(verify_token)):
    conn = sqlite3.connect('jacai.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND is_active = TRUE", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return {
        "id": user[0],
        "username": user[1],
        "email": user[2],
        "role": user[4]
    }

# AI Generation (Mock for demo)
def generate_content(topic: str, platform: str, style: str) -> dict:
    import random
    import time
    
    time.sleep(1)  # Simulate API delay
    
    platform_content = {
        "instagram": {
            "caption": f"🌟 {topic} is the key to success! Every journey starts with a single step, and today is your day to shine. Remember, consistency beats perfection every time. What's your next move? 💪✨ #inspiration #motivation #success",
            "hashtags": "#inspiration #motivation #success #mindset #goals #hustle #entrepreneur #growth #lifestyle #positivity",
            "image_prompt": f"Professional Instagram post about {topic}, vibrant colors, modern design, inspirational quote overlay"
        },
        "twitter": {
            "caption": f"🚀 {topic} reminder: Small steps lead to big changes. What's one thing you're working on today? #motivation #success",
            "hashtags": "#motivation #success #mindset #goals #hustle #entrepreneur",
            "image_prompt": f"Twitter header image about {topic}, clean design, bold typography"
        },
        "linkedin": {
            "caption": f"Professional insight on {topic}: In today's competitive landscape, the key to success lies in continuous learning and adaptation. Here are three strategies that have proven effective... What's your experience with {topic}? Share your thoughts below.",
            "hashtags": "#professional #business #leadership #growth #strategy #networking",
            "image_prompt": f"Professional LinkedIn post about {topic}, corporate style, clean layout"
        }
    }
    
    return platform_content.get(platform, platform_content["instagram"])

# Social Media Posting (Mock implementations)
def post_to_instagram(content: dict, access_token: str) -> bool:
    # Mock Instagram posting
    print(f"📸 Posted to Instagram: {content['caption'][:50]}...")
    return True

def post_to_twitter(content: dict, access_token: str) -> bool:
    # Mock Twitter posting
    print(f"🐦 Posted to Twitter: {content['caption'][:50]}...")
    return True

def post_to_linkedin(content: dict, access_token: str) -> bool:
    # Mock LinkedIn posting
    print(f"💼 Posted to LinkedIn: {content['caption'][:50]}...")
    return True

# Routes
@app.on_event("startup")
async def startup_event():
    init_db()
    print("🚀 JACAI Pro initialized with database")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.post("/api/register")
async def register(user: UserCreate):
    conn = sqlite3.connect('jacai.db')
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (user.username, user.email))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Hash password
    password_hash = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    
    # Insert user
    cursor.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        (user.username, user.email, password_hash)
    )
    conn.commit()
    conn.close()
    
    return {"message": "User created successfully"}

@app.post("/api/login")
async def login(user: UserLogin):
    conn = sqlite3.connect('jacai.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password_hash FROM users WHERE username = ? AND is_active = TRUE", (user.username,))
    db_user = cursor.fetchone()
    conn.close()
    
    if not db_user or not bcrypt.checkpw(user.password.encode('utf-8'), db_user[2]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/link-social-account")
async def link_social_account(account: SocialAccountLink, current_user: dict = Depends(get_current_user)):
    conn = sqlite3.connect('jacai.db')
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT OR REPLACE INTO social_accounts (user_id, platform, account_name, access_token) VALUES (?, ?, ?, ?)",
        (current_user["id"], account.platform, account.account_name, account.access_token)
    )
    conn.commit()
    conn.close()
    
    return {"message": f"{account.platform} account linked successfully"}

@app.get("/api/social-accounts")
async def get_social_accounts(current_user: dict = Depends(get_current_user)):
    conn = sqlite3.connect('jacai.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT platform, account_name, is_active FROM social_accounts WHERE user_id = ? AND is_active = TRUE",
        (current_user["id"],)
    )
    accounts = cursor.fetchall()
    conn.close()
    
    return [{"platform": acc[0], "account_name": acc[1], "is_active": acc[2]} for acc in accounts]

@app.post("/api/generate")
async def generate_post(request: GenerateRequest, current_user: dict = Depends(get_current_user)):
    try:
        results = []
        
        for platform in request.platforms:
            # Generate content
            content = generate_content(request.topic, platform, request.style)
            
            # Save to database
            conn = sqlite3.connect('jacai.db')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO generated_posts (user_id, topic, platform, style, caption, hashtags, image_prompt) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (current_user["id"], request.topic, platform, request.style, content["caption"], content["hashtags"], content["image_prompt"])
            )
            post_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Auto-post if requested
            if request.auto_post:
                # Get user's social account for this platform
                conn = sqlite3.connect('jacai.db')
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT access_token FROM social_accounts WHERE user_id = ? AND platform = ? AND is_active = TRUE",
                    (current_user["id"], platform)
                )
                account = cursor.fetchone()
                conn.close()
                
                if account:
                    # Post to social media
                    posted = False
                    if platform == "instagram":
                        posted = post_to_instagram(content, account[0])
                    elif platform == "twitter":
                        posted = post_to_twitter(content, account[0])
                    elif platform == "linkedin":
                        posted = post_to_linkedin(content, account[0])
                    
                    if posted:
                        # Update post status
                        conn = sqlite3.connect('jacai.db')
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE generated_posts SET post_status = 'posted', posted_at = CURRENT_TIMESTAMP WHERE id = ?",
                            (post_id,)
                        )
                        conn.commit()
                        conn.close()
            
            results.append({
                "platform": platform,
                "content": content,
                "post_id": post_id,
                "posted": request.auto_post
            })
        
        return {"success": True, "results": results}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/posts")
async def get_posts(current_user: dict = Depends(get_current_user)):
    conn = sqlite3.connect('jacai.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT topic, platform, style, caption, hashtags, created_at, post_status FROM generated_posts WHERE user_id = ? ORDER BY created_at DESC LIMIT 50",
        (current_user["id"],)
    )
    posts = cursor.fetchall()
    conn.close()
    
    return [
        {
            "topic": post[0],
            "platform": post[1],
            "style": post[2],
            "caption": post[3],
            "hashtags": post[4],
            "created_at": post[5],
            "status": post[6]
        }
        for post in posts
    ]

# n8n Integration Endpoints
@app.post("/api/n8n/generate")
async def n8n_generate(request: dict):
    """Endpoint for n8n to generate content"""
    # This endpoint can be called by n8n workflows
    # No authentication required for automation
    
    topic = request.get("topic", "motivation")
    platforms = request.get("platforms", ["instagram"])
    style = request.get("style", "professional")
    
    results = []
    for platform in platforms:
        content = generate_content(topic, platform, style)
        results.append({
            "platform": platform,
            "content": content
        })
    
    return {"success": True, "results": results}

@app.get("/link-accounts", response_class=HTMLResponse)
async def link_accounts_page(request: Request):
    return templates.TemplateResponse("account_linking.html", {"request": request})

@app.get("/api/oauth/authorize/{platform}")
async def oauth_authorize(platform: str, redirect_uri: str, current_user: dict = Depends(get_current_user)):
    """Start OAuth flow for platform"""
    try:
        from oauth_service import oauth_service
        auth_url = oauth_service.get_auth_url(platform, current_user["id"], redirect_uri)
        return {"auth_url": auth_url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/oauth/callback")
async def oauth_callback(code: str, state: str, platform: str = None):
    """Handle OAuth callback"""
    try:
        from oauth_service import oauth_service
        
        # Verify state
        state_data = oauth_service.verify_state(state)
        user_id = state_data["user_id"]
        platform = state_data["platform"]
        
        # Exchange code for token
        redirect_uri = f"{request.base_url}oauth/callback"
        token_data = oauth_service.exchange_code_for_token(platform, code, redirect_uri)
        
        # Get user info
        user_info = oauth_service.get_user_info(platform, token_data["access_token"])
        
        # Save to database
        conn = sqlite3.connect('jacai.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO social_accounts (user_id, platform, account_name, access_token, refresh_token) VALUES (?, ?, ?, ?, ?)",
            (user_id, platform, user_info.get("username", "Unknown"), token_data["access_token"], token_data.get("refresh_token"))
        )
        conn.commit()
        conn.close()
        
        return HTMLResponse("<script>window.close(); window.opener.location.reload();</script>")
        
    except Exception as e:
        return HTMLResponse(f"<h1>Error: {str(e)}</h1>")

@app.post("/api/link-social-account")
async def link_social_account_manual(account: SocialAccountLink, current_user: dict = Depends(get_current_user)):
    """Manually link social account with token"""
    conn = sqlite3.connect('jacai.db')
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT OR REPLACE INTO social_accounts (user_id, platform, account_name, access_token) VALUES (?, ?, ?, ?)",
        (current_user["id"], account.platform, account.account_name, account.access_token)
    )
    conn.commit()
    conn.close()
    
    return {"message": f"{account.platform} account linked successfully"}

@app.get("/api/test-social-connections")
async def test_social_connections(current_user: dict = Depends(get_current_user)):
    """Test all linked social media connections"""
    from social_media_service import social_service
    
    conn = sqlite3.connect('jacai.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT platform, account_name, access_token FROM social_accounts WHERE user_id = ? AND is_active = TRUE",
        (current_user["id"],)
    )
    accounts = cursor.fetchall()
    conn.close()
    
    results = []
    for account in accounts:
        platform, account_name, access_token = account
        test_result = social_service.validate_account(platform, access_token)
        results.append({
            "platform": platform,
            "account_name": account_name,
            "status": "connected" if test_result["valid"] else "failed",
            "details": test_result
        })
    
    return {"results": results}

@app.delete("/api/social-accounts/{platform}")
async def unlink_social_account(platform: str, current_user: dict = Depends(get_current_user)):
    """Unlink social media account"""
    conn = sqlite3.connect('jacai.db')
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE social_accounts SET is_active = FALSE WHERE user_id = ? AND platform = ?",
        (current_user["id"], platform)
    )
    conn.commit()
    conn.close()
    
    return {"message": f"{platform} account unlinked successfully"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "JACAI Pro", "version": "2.0.0"}

if __name__ == "__main__":
    print("🚀 Starting JACAI Pro - Multi-User AI Social Media Generator")
    print("📱 Access at: http://localhost:8080")
    print("🔐 Features: Authentication, Multi-platform, n8n Integration")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info"
    )