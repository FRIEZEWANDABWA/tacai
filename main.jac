"""
JACAI - AI-Powered Social Media Generator
Built with Jac Language for instant deployment
"""

import:py from fastapi, FastAPI, Request;
import:py from fastapi.responses, HTMLResponse, JSONResponse;
import:py from fastapi.staticfiles, StaticFiles;
import:py from fastapi.templating, Jinja2Templates;
import:py from pydantic, BaseModel;
import:py uvicorn;
import:py os;
import:py json;
import:py requests;
import:py from datetime, datetime;

# AI Models Configuration
glob AI_MODELS = {
    "gemini_key": "AIzaSyDw6iEZWeDrHCv88JBlGkEW4OyFf1a3fCc",
    "gemini_url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
};

# Social Media Post Model
obj SocialPost {
    has topic: str;
    has platform: str;
    has style: str;
    has caption: str = "";
    has hashtags: str = "";
    has image_prompt: str = "";
    has created_at: str = "";
    
    can generate_content {
        self.created_at = str(datetime.now());
        self.generate_caption();
        self.generate_hashtags();
        self.generate_image_prompt();
    }
    
    can generate_caption {
        platform_specs = {
            "instagram": "Instagram post with emojis, engaging and visual, 150-200 words",
            "twitter": "Twitter post, concise, under 280 characters, engaging",
            "linkedin": "LinkedIn post, professional tone, business-focused, 200-300 words",
            "facebook": "Facebook post, conversational and engaging, 100-150 words"
        };
        
        style_guides = {
            "professional": "Use professional language, focus on expertise and value",
            "casual": "Use friendly, conversational tone with personality",
            "creative": "Be creative, use metaphors and storytelling",
            "motivational": "Be inspiring and encouraging, focus on growth"
        };
        
        prompt = f"Create a {self.style} {platform_specs.get(self.platform, 'social media post')} about '{self.topic}'. {style_guides.get(self.style, '')} Make it engaging and shareable.";
        
        self.caption = self.call_gemini(prompt);
    }
    
    can generate_hashtags {
        prompt = f"Generate 8-10 relevant, trending hashtags for a {self.platform} post about '{self.topic}'. Include a mix of popular and niche hashtags. Return only hashtags separated by spaces, starting with #.";
        
        self.hashtags = self.call_gemini(prompt);
    }
    
    can generate_image_prompt {
        prompt = f"Create a detailed image generation prompt for a {self.style} style image about '{self.topic}' suitable for {self.platform}. Focus on visual elements, colors, and composition. Keep it under 100 words.";
        
        self.image_prompt = self.call_gemini(prompt);
    }
    
    can call_gemini(prompt: str) -> str {
        try {
            headers = {"Content-Type": "application/json"};
            data = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }]
            };
            
            response = requests.post(
                f"{AI_MODELS['gemini_url']}?key={AI_MODELS['gemini_key']}",
                headers=headers,
                json=data
            );
            
            if response.status_code == 200 {
                result = response.json();
                return result["candidates"][0]["content"]["parts"][0]["text"];
            } else {
                return f"Error: Unable to generate content. Status: {response.status_code}";
            }
        } except Exception as e {
            return f"Error: {str(e)}";
        }
    }
}

# Request Models
obj GenerateRequest {
    has topic: str;
    has platform: str = "instagram";
    has style: str = "professional";
}

# FastAPI App
glob app = FastAPI(title="JACAI - AI Social Media Generator", version="1.0.0");

# Serve static files
app.mount("/static", StaticFiles(directory="web"), name="static");
templates = Jinja2Templates(directory="web");

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request) {
    return templates.TemplateResponse("index.html", {"request": request});
}

@app.post("/api/generate")
async def generate_post(request: GenerateRequest) {
    try {
        # Create and generate post
        post = SocialPost(
            topic=request.topic,
            platform=request.platform,
            style=request.style
        );
        
        post.generate_content();
        
        return JSONResponse({
            "success": True,
            "post": {
                "topic": post.topic,
                "platform": post.platform,
                "style": post.style,
                "caption": post.caption,
                "hashtags": post.hashtags,
                "image_prompt": post.image_prompt,
                "created_at": post.created_at
            }
        });
    } except Exception as e {
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500);
    }
}

@app.get("/api/health")
async def health_check() {
    return {"status": "healthy", "service": "JACAI"};
}

# Main entry point
walker main {
    can run {
        print("🚀 Starting JACAI - AI Social Media Generator");
        print("📱 Access at: http://localhost:8000");
        print("🤖 Powered by Gemini AI");
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info"
        );
    }
}