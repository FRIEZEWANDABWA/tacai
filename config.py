# JACAI Configuration
import os

# API Keys (set these as environment variables)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Social Media API Keys
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", "")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "")

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///jacai.db")

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

# Rate Limiting
RATE_LIMIT_PER_MINUTE = 10
RATE_LIMIT_PER_HOUR = 100

# Content Generation
MAX_CONTENT_LENGTH = 2000
SUPPORTED_PLATFORMS = ["instagram", "twitter", "linkedin", "facebook", "tiktok"]
SUPPORTED_STYLES = ["professional", "casual", "creative", "motivational", "humorous"]

# Image Generation
IMAGE_GENERATION_ENABLED = True
MAX_IMAGE_SIZE = "1024x1024"

# Scheduling
TIMEZONE = "UTC"
MAX_SCHEDULED_POSTS = 50