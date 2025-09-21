#!/usr/bin/env python3
"""
JACAI - Jaseci Integration Server
Bridges Jaseci graph execution with FastAPI web interface
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import subprocess
import json
import os

app = FastAPI(title="JACAI - Jaseci Powered", version="3.0.0")

# Serve static files
app.mount("/static", StaticFiles(directory="web"), name="static")

class JaseciExecutor:
    """Execute Jaseci walkers and manage graph state"""
    
    def __init__(self):
        self.graph_initialized = False
    
    def execute_walker(self, walker_name: str, data: dict = None) -> dict:
        """Execute a Jaseci walker with data"""
        try:
            if not self.graph_initialized:
                self.initialize_graph()
            
            # Prepare Jaseci command
            cmd = [
                "jac", "run", "jacai_proper.jac",
                "-w", walker_name
            ]
            
            if data:
                cmd.extend(["-ctx", json.dumps(data)])
            
            # Execute walker
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                cwd="/home/frieze/projects/jacai-jac"
            )
            
            if result.returncode == 0:
                # Parse walker output
                try:
                    return json.loads(result.stdout.strip().split('\n')[-1])
                except:
                    return {"success": True, "output": result.stdout}
            else:
                return {"success": False, "error": result.stderr}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def initialize_graph(self):
        """Initialize the Jaseci graph"""
        try:
            result = subprocess.run(
                ["jac", "run", "jacai_proper.jac"],
                capture_output=True,
                text=True,
                cwd="/home/frieze/projects/jacai-jac"
            )
            self.graph_initialized = True
            return result.returncode == 0
        except:
            return False

# Global Jaseci executor
jaseci = JaseciExecutor()

# Request models
class GenerateRequest(BaseModel):
    topic: str
    platforms: list
    style: str = "professional"
    user_id: str = "1"

class AuthRequest(BaseModel):
    username: str
    password: str
    email: str = ""

class SocialRequest(BaseModel):
    platform: str
    user_id: str
    account_name: str = ""

# Routes
@app.get("/", response_class=HTMLResponse)
async def home():
    with open("web/login.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    with open("web/dashboard.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.post("/api/register")
async def register(request: AuthRequest):
    """Register user via Jaseci walker"""
    result = jaseci.execute_walker("api_orchestrator", {
        "action": "register",
        "data": {
            "username": request.username,
            "email": request.email,
            "password": request.password
        }
    })
    return JSONResponse(result)

@app.post("/api/login")
async def login(request: AuthRequest):
    """Login user via Jaseci walker"""
    result = jaseci.execute_walker("api_orchestrator", {
        "action": "login",
        "data": {
            "username": request.username,
            "password": request.password
        }
    })
    return JSONResponse(result)

@app.post("/api/generate")
async def generate_content(request: dict):
    """Generate content via Jaseci walker"""
    result = jaseci.execute_walker("api_orchestrator", {
        "action": "generate_content",
        "data": {
            "topic": request.get("topic", ""),
            "platforms": request.get("platforms", ["instagram"]),
            "style": request.get("style", "professional"),
            "user_id": request.get("user_id", "1")
        }
    })
    return JSONResponse(result)

@app.post("/api/connect-social")
async def connect_social(request: dict):
    """Connect social account via Jaseci walker"""
    result = jaseci.execute_walker("api_orchestrator", {
        "action": "connect_social",
        "data": {
            "platform": request.get("platform", ""),
            "user_id": request.get("user_id", ""),
            "account_name": request.get("account_name", "")
        }
    })
    return JSONResponse(result)

@app.get("/api/social-accounts")
async def get_social_accounts(user_id: str = "1"):
    """Get social accounts via Jaseci walker"""
    result = jaseci.execute_walker("api_orchestrator", {
        "action": "get_social_accounts",
        "data": {"user_id": user_id}
    })
    return JSONResponse(result if isinstance(result, list) else [])

@app.get("/api/analytics")
async def get_analytics(user_id: str = "1"):
    """Get user analytics via Jaseci walker"""
    result = jaseci.execute_walker("api_orchestrator", {
        "action": "get_analytics",
        "data": {"user_id": user_id}
    })
    return JSONResponse(result)

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "JACAI-Jaseci",
        "version": "3.0.0",
        "architecture": "Graph-based with Jaseci",
        "graph_initialized": jaseci.graph_initialized
    }

@app.get("/api/graph-status")
async def graph_status():
    """Get Jaseci graph status"""
    return {
        "initialized": jaseci.graph_initialized,
        "nodes": ["user_registry", "content_hub", "social_platforms"],
        "walkers": ["auth_manager", "content_generator", "social_manager", "analytics_engine"]
    }

if __name__ == "__main__":
    print("🚀 Starting JACAI - Jaseci Powered Version")
    print("📊 Graph-based architecture with AI-native processing")
    print("🤖 Advanced social media automation platform")
    print("📱 Access at: http://localhost:8082")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8082,
        log_level="info"
    )