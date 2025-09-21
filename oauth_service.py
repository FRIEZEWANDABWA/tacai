"""
OAuth Service for Social Media Account Linking
"""
import requests
import json
from urllib.parse import urlencode, parse_qs
from config import *
import secrets
import sqlite3
from datetime import datetime, timedelta

class OAuthService:
    def __init__(self):
        self.oauth_configs = {
            "instagram": {
                "auth_url": "https://api.instagram.com/oauth/authorize",
                "token_url": "https://api.instagram.com/oauth/access_token",
                "scope": "user_profile,user_media",
                "client_id": "your-instagram-client-id"
            },
            "twitter": {
                "auth_url": "https://twitter.com/i/oauth2/authorize",
                "token_url": "https://api.twitter.com/2/oauth2/token",
                "scope": "tweet.read tweet.write users.read",
                "client_id": "your-twitter-client-id"
            },
            "linkedin": {
                "auth_url": "https://www.linkedin.com/oauth/v2/authorization",
                "token_url": "https://www.linkedin.com/oauth/v2/accessToken",
                "scope": "w_member_social r_liteprofile",
                "client_id": "your-linkedin-client-id"
            }
        }
    
    def get_auth_url(self, platform: str, user_id: int, redirect_uri: str) -> str:
        """Generate OAuth authorization URL"""
        if platform not in self.oauth_configs:
            raise ValueError(f"Platform {platform} not supported")
        
        config = self.oauth_configs[platform]
        state = self.generate_state(user_id, platform)
        
        params = {
            "client_id": config["client_id"],
            "redirect_uri": redirect_uri,
            "scope": config["scope"],
            "response_type": "code",
            "state": state
        }
        
        return f"{config['auth_url']}?{urlencode(params)}"
    
    def generate_state(self, user_id: int, platform: str) -> str:
        """Generate secure state parameter"""
        state_data = {
            "user_id": user_id,
            "platform": platform,
            "timestamp": datetime.now().timestamp(),
            "nonce": secrets.token_urlsafe(16)
        }
        
        # Store state in database for verification
        conn = sqlite3.connect('jacai.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS oauth_states (
                state TEXT PRIMARY KEY,
                user_id INTEGER,
                platform TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP
            )
        ''')
        
        state = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(minutes=10)
        
        cursor.execute('''
            INSERT INTO oauth_states (state, user_id, platform, expires_at)
            VALUES (?, ?, ?, ?)
        ''', (state, user_id, platform, expires_at))
        
        conn.commit()
        conn.close()
        
        return state
    
    def verify_state(self, state: str) -> dict:
        """Verify OAuth state parameter"""
        conn = sqlite3.connect('jacai.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, platform, expires_at
            FROM oauth_states
            WHERE state = ?
        ''', (state,))
        
        result = cursor.fetchone()
        
        if result:
            # Clean up used state
            cursor.execute('DELETE FROM oauth_states WHERE state = ?', (state,))
            conn.commit()
        
        conn.close()
        
        if not result:
            raise ValueError("Invalid state parameter")
        
        if datetime.fromisoformat(result[2]) < datetime.now():
            raise ValueError("State parameter expired")
        
        return {
            "user_id": result[0],
            "platform": result[1]
        }
    
    def exchange_code_for_token(self, platform: str, code: str, redirect_uri: str) -> dict:
        """Exchange authorization code for access token"""
        if platform not in self.oauth_configs:
            raise ValueError(f"Platform {platform} not supported")
        
        config = self.oauth_configs[platform]
        
        data = {
            "client_id": config["client_id"],
            "client_secret": f"your-{platform}-client-secret",
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri
        }
        
        response = requests.post(config["token_url"], data=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Token exchange failed: {response.text}")
    
    def get_user_info(self, platform: str, access_token: str) -> dict:
        """Get user information from platform"""
        endpoints = {
            "instagram": "https://graph.instagram.com/me?fields=id,username,account_type",
            "twitter": "https://api.twitter.com/2/users/me",
            "linkedin": "https://api.linkedin.com/v2/people/~"
        }
        
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = requests.get(endpoints[platform], headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get user info: {response.text}")

oauth_service = OAuthService()