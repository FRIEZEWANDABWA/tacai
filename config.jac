import:py os;

// JACAI Configuration - Jaseci/Jac Version
// Environment and settings management

node Config {
    has gemini_api_key: str;
    has openai_api_key: str;
    has claude_api_key: str;
    has jwt_secret: str;
    has database_url: str;
    has redis_url: str;
    has environment: str;
    
    can load_config with `root entry {
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "");
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "");
        self.claude_api_key = os.getenv("CLAUDE_API_KEY", "");
        self.jwt_secret = os.getenv("JWT_SECRET", "jacai-secret-key");
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///jacai.db");
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379");
        self.environment = os.getenv("ENVIRONMENT", "development");
        
        return self;
    }
    
    can get_social_config(platform: str) -> dict {
        social_configs = {
            "instagram": {
                "client_id": os.getenv("INSTAGRAM_CLIENT_ID", ""),
                "client_secret": os.getenv("INSTAGRAM_CLIENT_SECRET", ""),
                "redirect_uri": os.getenv("INSTAGRAM_REDIRECT_URI", "http://localhost:8080/auth/instagram/callback")
            },
            "twitter": {
                "client_id": os.getenv("TWITTER_CLIENT_ID", ""),
                "client_secret": os.getenv("TWITTER_CLIENT_SECRET", ""),
                "redirect_uri": os.getenv("TWITTER_REDIRECT_URI", "http://localhost:8080/auth/twitter/callback")
            },
            "linkedin": {
                "client_id": os.getenv("LINKEDIN_CLIENT_ID", ""),
                "client_secret": os.getenv("LINKEDIN_CLIENT_SECRET", ""),
                "redirect_uri": os.getenv("LINKEDIN_REDIRECT_URI", "http://localhost:8080/auth/linkedin/callback")
            },
            "facebook": {
                "client_id": os.getenv("FACEBOOK_CLIENT_ID", ""),
                "client_secret": os.getenv("FACEBOOK_CLIENT_SECRET", ""),
                "redirect_uri": os.getenv("FACEBOOK_REDIRECT_URI", "http://localhost:8080/auth/facebook/callback")
            }
        };
        
        return social_configs.get(platform, {});
    }
}

// Global configuration instance
glob config = spawn here --> Config();

with entry {
    config.load_config();
    print("⚙️ Configuration loaded successfully");
}