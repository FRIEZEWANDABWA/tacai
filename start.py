#!/usr/bin/env python3
"""
JACAI Startup Script
"""

import uvicorn
from app import app

if __name__ == "__main__":
    print("🚀 Starting JACAI - AI Social Media Platform (Jac-Ready Version)")
    print("📱 Access at: http://localhost:8081")
    print("🤖 Ready for Jac integration")
    print("🔗 Features: Content Generation, Social Media Integration, User Management")
    print()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8081,
        log_level="info",
        reload=False
    )